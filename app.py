import customtkinter as ctk
from tkcalendar import Calendar
import json
import os

# Настройка глобальных параметров CustomTkinter
ctk.set_appearance_mode("System")  # Темный/светлый режим
ctk.set_default_color_theme("blue")  # Цветовая тема

# Путь для сохранения задач
TASKS_FILE = "tasks.json"


# Функция для загрузки задач из файла
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Ошибка: Некорректный формат файла задач. Файл будет перезаписан.")
                return {}
    return {}


# Функция для сохранения задач в файл
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


# Класс задачи
class Task:
    def __init__(self, name, description, start_time, end_time, tags):
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.tags = tags

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "tags": self.tags,
        }

    @staticmethod
    def from_dict(data):
        try:
            return Task(
                data["name"],
                data.get("description", ""),
                data["start_time"],
                data["end_time"],
                data.get("tags", []),
            )
        except KeyError as e:
            print(f"Ошибка: отсутствует ключ {e} в задаче. Задача будет пропущена.")
            return None


# Главное окно приложения
class OrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройки главного окна
        self.title("Органайзер")
        self.geometry("900x600")

        # Загруженные задачи
        self.tasks = {
            date: [task for task in (Task.from_dict(task) for task in task_list) if task]
            for date, task_list in load_tasks().items()
        }

        # Элементы интерфейса
        self.create_interface()

    def create_interface(self):
        # Календарь
        self.calendar = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.pack(side="right", fill="y", padx=20, pady=20)
        self.calendar.bind("<<CalendarSelected>>", self.update_task_list)

        # Список задач
        self.task_listbox = ctk.CTkTextbox(self, width=400)
        self.task_listbox.configure(state="normal")  # Отключим прямое редактирование
        self.task_listbox.bind("<Double-1>", self.open_task_editor)  # Обработчик двойного клика
        self.task_listbox.pack(side="left", fill="both", padx=20, pady=20)

        # Кнопка для добавления задачи
        self.add_task_button = ctk.CTkButton(self, text="Добавить задачу", command=self.open_add_task_window)
        self.add_task_button.pack(side="bottom", pady=10)

        # Инициализация задач для текущей даты
        self.update_task_list()

    def update_task_list(self, event=None):
        selected_date = self.calendar.get_date()
        self.task_listbox.configure(state="normal")
        self.task_listbox.delete("1.0", "end")

        if selected_date in self.tasks:
            for i, task in enumerate(self.tasks[selected_date]):
                self.task_listbox.insert("end", f"{i + 1}. {task.start_time}-{task.end_time}: {task.name}\n")

        self.task_listbox.configure(state="disabled")

    def open_task_editor(self, event):
        try:
            selected_date = self.calendar.get_date()
            index = int(self.task_listbox.index("@%d,%d" % (event.x, event.y)).split(".")[0]) - 1
            if selected_date in self.tasks and 0 <= index < len(self.tasks[selected_date]):
                task = self.tasks[selected_date][index]
                EditTaskWindow(self, selected_date, task)
        except Exception as e:
            print("Ошибка при открытии задачи:", e)

    def open_add_task_window(self):
        AddTaskWindow(self)

    def save_all_tasks(self):
        serialized_tasks = {date: [task.to_dict() for task in task_list] for date, task_list in self.tasks.items()}
        save_tasks(serialized_tasks)


# Окно добавления задачи
class AddTaskWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.title("Добавить задачу")
        self.geometry("400x400")

        # Поля для ввода данных
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Название задачи")
        self.name_entry.pack(pady=5, fill="x", padx=20)

        self.description_entry = ctk.CTkEntry(self, placeholder_text="Описание задачи")
        self.description_entry.pack(pady=5, fill="x", padx=20)

        self.start_time_entry = ctk.CTkEntry(self, placeholder_text="Время начала (HH:MM)")
        self.start_time_entry.pack(pady=5, fill="x", padx=20)

        self.end_time_entry = ctk.CTkEntry(self, placeholder_text="Время окончания (HH:MM)")
        self.end_time_entry.pack(pady=5, fill="x", padx=20)

        self.tags_entry = ctk.CTkEntry(self, placeholder_text="Теги (через запятую)")
        self.tags_entry.pack(pady=5, fill="x", padx=20)

        # Кнопка для сохранения задачи
        self.save_button = ctk.CTkButton(self, text="Сохранить задачу", command=self.save_task)
        self.save_button.pack(pady=20)

    def save_task(self):
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()
        start_time = self.start_time_entry.get().strip()
        end_time = self.end_time_entry.get().strip()
        tags = [tag.strip() for tag in self.tags_entry.get().strip().split(",")]

        if not name or not start_time or not end_time:
            print("Ошибка: Пожалуйста, заполните обязательные поля.")
            return

        selected_date = self.parent.calendar.get_date()
        new_task = Task(name, description, start_time, end_time, tags)

        if selected_date not in self.parent.tasks:
            self.parent.tasks[selected_date] = []

        self.parent.tasks[selected_date].append(new_task)
        self.parent.save_all_tasks()
        self.parent.update_task_list()
        self.destroy()


# Окно редактирования задачи
class EditTaskWindow(ctk.CTkToplevel):
    def __init__(self, parent, date, task):
        super().__init__(parent)

        self.parent = parent
        self.date = date
        self.task = task
        self.title("Редактировать задачу")
        self.geometry("400x400")

        # Поля для редактирования данных
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Название задачи")
        self.name_entry.insert(0, task.name)
        self.name_entry.pack(pady=5, fill="x", padx=20)

        self.description_entry = ctk.CTkEntry(self, placeholder_text="Описание задачи")
        self.description_entry.insert(0, task.description)
        self.description_entry.pack(pady=5, fill="x", padx=20)

        self.start_time_entry = ctk.CTkEntry(self, placeholder_text="Время начала (HH:MM)")
        self.start_time_entry.insert(0, task.start_time)
        self.start_time_entry.pack(pady=5, fill="x", padx=20)

        self.end_time_entry = ctk.CTkEntry(self, placeholder_text="Время окончания (HH:MM)")
        self.end_time_entry.insert(0, task.end_time)
        self.end_time_entry.pack(pady=5, fill="x", padx=20)

        self.tags_entry = ctk.CTkEntry(self, placeholder_text="Теги (через запятую)")
        self.tags_entry.insert(0, ",".join(task.tags))
        self.tags_entry.pack(pady=5, fill="x", padx=20)

        # Кнопки для сохранения или удаления задачи
        self.save_button = ctk.CTkButton(self, text="Сохранить изменения", command=self.save_task)
        self.save_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(self, text="Удалить задачу", fg_color="red", command=self.delete_task)
        self.delete_button.pack(pady=10)

    def save_task(self):
        self.task.name = self.name_entry.get().strip()
        self.task.description = self.description_entry.get().strip()
        self.task.start_time = self.start_time_entry.get().strip()
        self.task.end_time = self.end_time_entry.get().strip()
        self.task.tags = [tag.strip() for tag in self.tags_entry.get().strip().split(",")]

        self.parent.save_all_tasks()
        self.parent.update_task_list()
        self.destroy()

    def delete_task(self):
        self.parent.tasks[self.date].remove(self.task)
        if not self.parent.tasks[self.date]:
            del self.parent.tasks[self.date]

        self.parent.save_all_tasks()
        self.parent.update_task_list()
        self.destroy()


# Запуск приложения
if __name__ == "__main__":
    app = OrganizerApp()
    app.mainloop()
