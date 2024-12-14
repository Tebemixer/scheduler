import customtkinter as ctk
from tkcalendar import Calendar

# Настройка глобальных параметров CustomTkinter
ctk.set_appearance_mode("System")  # Темный/светлый режим
ctk.set_default_color_theme("blue")  # Цветовая тема

# Создаем главное окно приложения
class OrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройки главного окна
        self.title("Органайзер")
        self.geometry("800x600")

        # Основные элементы интерфейса
        self.create_main_menu()

    def create_main_menu(self):
        # Заголовок приложения
        self.label = ctk.CTkLabel(self, text="Добро пожаловать в Органайзер", font=("Arial", 20))
        self.label.pack(pady=20)

        # Кнопка для открытия окна расписания
        self.schedule_button = ctk.CTkButton(self, text="Расписание", command=self.open_schedule_window)
        self.schedule_button.pack(pady=10)

        # Кнопка для открытия окна заметок
        self.notes_button = ctk.CTkButton(self, text="Заметки", command=self.open_notes_window)
        self.notes_button.pack(pady=10)

        # Кнопка для открытия окна напоминаний
        self.reminders_button = ctk.CTkButton(self, text="Напоминания", command=self.open_reminders_window)
        self.reminders_button.pack(pady=10)

        # Кнопка для выхода
        self.exit_button = ctk.CTkButton(self, text="Выход", command=self.quit)
        self.exit_button.pack(pady=10)

    def open_schedule_window(self):
        ScheduleWindow(self)

    def open_notes_window(self):
        NotesWindow(self)

    def open_reminders_window(self):
        RemindersWindow(self)

# Окно "Расписание"
class ScheduleWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Расписание")
        self.geometry("600x400")

        # Календарь
        self.calendar = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.pack(pady=20)

        # Поле для ввода задачи
        self.task_entry = ctk.CTkEntry(self, placeholder_text="Введите задачу")
        self.task_entry.pack(pady=10, fill="x", padx=20)

        # Кнопка для добавления задачи
        self.add_task_button = ctk.CTkButton(self, text="Добавить задачу", command=self.add_task)
        self.add_task_button.pack(pady=10)

        # Список задач
        self.task_listbox = ctk.CTkTextbox(self, height=10)
        self.task_listbox.pack(pady=10, fill="both", padx=20, expand=True)

        self.tasks = {}

    def add_task(self):
        date = self.calendar.get_date()
        task = self.task_entry.get()

        if not task.strip():
            return

        if date not in self.tasks:
            self.tasks[date] = []
        self.tasks[date].append(task)

        self.task_entry.delete(0, "end")
        self.update_task_list(date)

    def update_task_list(self, date):
        self.task_listbox.delete("1.0", "end")
        if date in self.tasks:
            for task in self.tasks[date]:
                self.task_listbox.insert("end", f"- {task}\n")

# Окно "Заметки"
class NotesWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Заметки")
        self.geometry("400x300")

        label = ctk.CTkLabel(self, text="Окно заметок", font=("Arial", 16))
        label.pack(pady=20)

# Окно "Напоминания"
class RemindersWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Напоминания")
        self.geometry("400x300")

        label = ctk.CTkLabel(self, text="Окно напоминаний", font=("Arial", 16))
        label.pack(pady=20)

# Запуск приложения
if __name__ == "__main__":
    app = OrganizerApp()
    app.mainloop()
