import customtkinter as ctk
from tkcalendar import Calendar
import os
import json
from TaskWindow import TaskWindow
from EditTaskWindow import EditTaskWindow
import sqlite3
import threading
from others import get_tasks_by_date
import time
from datetime import datetime
# Настройка глобальных параметров CustomTkinter
ctk.set_appearance_mode("System")  # Темный/светлый режим
ctk.set_default_color_theme("blue")  # Цветовая тема


TASKS_DB = "tasks.db"
CONFIG_FILE = "config.json"


# Главное окно приложения
class OrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.tasks_db = TASKS_DB
        self.config_file = CONFIG_FILE
        self.cur_tasks = []
        # Настройки главного окна
        self.title("Органайзер")
        self.geometry("900x600")
        create_table()
        # Элементы интерфейса
        self.create_interface()
        self.today_task = []

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
        self.today_task = get_tasks_by_date(self.calendar.get_date(),self.tasks_db)

        # Чекбокс для включения/выключения уведомлений
        self.notifications_enabled = ctk.BooleanVar()
        self.load_config()
        self.checkbox = ctk.CTkCheckBox(
            self,
            text="Включить уведомления",
            variable=self.notifications_enabled,
            command=self.save_config,
            onvalue=True,
            offvalue=False
        )
        self.checkbox.pack(pady=20)

        self.check_thread = threading.Thread(target=self.check_time, daemon=True)
        self.check_thread.start()

    def update_task_list(self, event=None):
        selected_date = self.calendar.get_date()
        self.task_listbox.configure(state="normal")
        self.task_listbox.delete("1.0", "end")
        for i, task in enumerate(get_tasks_by_date(selected_date,self.tasks_db)):
            self.task_listbox.insert("end", f"{i + 1}. {task.start_time}-{task.end_time}: {task.name}\n")
            self.cur_tasks.append(task)
        self.task_listbox.configure(state="disabled")

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                config = json.load(f)
                self.notifications_enabled.set(config.get("notifications_enabled", True))

    def save_config(self):
        config = {
            "notifications_enabled": self.notifications_enabled.get()
        }
        with open(self.config_file, "w") as f:
            json.dump(config, f)
        if self.notifications_enabled.get():
            self.check_thread = threading.Thread(target=self.check_time, daemon=True)
            self.check_thread.start()


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

    def check_time(self):
        while self.notifications_enabled.get():
            self.today_task = get_tasks_by_date(datetime.today().strftime("%Y-%m-%d"),self.tasks_db)
            now = datetime.now().strftime("%H:%M")
            for task in self.today_task:
                if now == task.start_time and not (task.done):
                    if self.notifications_enabled.get():  # Уведомления включены
                        self.show_notification(task)

                        connection = sqlite3.connect(self.tasks_db)
                        cursor = connection.cursor()
                        cursor.execute(
                            'UPDATE tasks SET done = ? WHERE id = ?',
                            (
                                1,
                                task.id,
                            )
                        )
                        connection.commit()
                        connection.close()
            time.sleep(5)

    def show_notification(self, task):
        notification_window = ctk.CTkToplevel(self)
        notification_window.title("Напоминание")
        notification_window.geometry("300x150")
        text=f"{task.name}\n{task.description}\n{task.start_time}-{task.end_time}\n{task.tags}"
        label = ctk.CTkLabel(notification_window, text=text, font=("Arial", 14))
        label.pack(pady=20)

        close_button = ctk.CTkButton(notification_window, text="Закрыть", command=notification_window.destroy)
        close_button.pack(pady=10)


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
            tags TEXT,
            done INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    app = OrganizerApp()
    app.mainloop()
