import customtkinter as ctk
from tkcalendar import Calendar

from Task import Task
from TaskWindow import TaskWindow
from EditTaskWindow import EditTaskWindow
import sqlite3
from datetime import datetime
# Настройка глобальных параметров CustomTkinter
ctk.set_appearance_mode("System")  # Темный/светлый режим
ctk.set_default_color_theme("blue")  # Цветовая тема


TASKS_DB = "tasks.db"

def create_table():
    conn = sqlite3.connect(TASKS_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT, 
            start_time TEXT,
            end_time TEXT,
            date TEXT NOT NULL,
            tags TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_tasks_by_date(date):
    """
    Извлекает задачи из базы данных, относящиеся к определённой дате.

    :param date: Дата в формате "YYYY-MM-DD".
    :return: Список объектов Task, относящихся к указанной дате.
    """
    conn = sqlite3.connect(TASKS_DB)
    cursor = conn.cursor()
    query = """
        SELECT name, description, start_time, end_time, date, tags , id
        FROM tasks
        WHERE date = ?
    """
    cursor.execute(query, (date,))
    rows = cursor.fetchall()
    conn.close()

    tasks = []
    for row in rows:
        task = Task(*row)
        tasks.append(task)
    return tasks

# Главное окно приложения
class OrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.tasks_db = TASKS_DB
        self.cur_tasks = []
        # Настройки главного окна
        self.title("Органайзер")
        self.geometry("900x600")
        create_table()
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
        for i, task in enumerate(get_tasks_by_date(selected_date)):
            self.task_listbox.insert("end", f"{i + 1}. {task.start_time}-{task.end_time}: {task.name}\n")
            self.cur_tasks.append(task)
        self.task_listbox.configure(state="disabled")



    def open_task_editor(self, event):
        try:
            selected_date = self.calendar.get_date()
            index = int(self.task_listbox.index("@%d,%d" % (event.x, event.y)).split(".")[0]) - 1
            task = self.cur_tasks[index]
            EditTaskWindow(self, task)
        except Exception as e:
            print("Ошибка при открытии задачи:", e)

    def open_add_task_window(self):
        TaskWindow(self)




# Запуск приложения
if __name__ == "__main__":
    app = OrganizerApp()
    app.mainloop()
