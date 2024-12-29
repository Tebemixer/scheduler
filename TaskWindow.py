import sqlite3
from others import show_error_popup
import customtkinter as ctk
from Task import Task
from datetime import datetime, timedelta


class TaskWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.title("Добавить задачу")
        self.geometry("400x400")

        self.date = self.parent.calendar.get_date()
        # Поля для ввода данных
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Название задачи")
        self.name_entry.pack(pady=5, fill="x", padx=20)

        self.description_entry = ctk.CTkEntry(self, placeholder_text="Описание задачи")
        self.description_entry.pack(pady=5, fill="x", padx=20)

        self.start_time_entry = ctk.CTkEntry(self, placeholder_text="Время начала (ЧЧ:MM)")
        self.start_time_entry.pack(pady=5, fill="x", padx=20)

        self.end_time_entry = ctk.CTkEntry(self, placeholder_text="Время окончания (ЧЧ:MM)")
        self.end_time_entry.pack(pady=5, fill="x", padx=20)

        self.date_notif_entry = ctk.CTkEntry(self, placeholder_text="Напомнить за (ДД:ЧЧ:MM)")
        self.date_notif_entry.pack(pady=5, fill="x", padx=20)

        self.tags_entry = ctk.CTkEntry(self, placeholder_text="Теги (через запятую)")
        self.tags_entry.pack(pady=5, fill="x", padx=20)

        # Кнопка для сохранения задачи
        self.save_button = ctk.CTkButton(self, text="Сохранить задачу", command=self.add_task)
        self.save_button.pack(pady=20)

    def add_task(self):
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()
        start_time = self.start_time_entry.get().strip()
        end_time = self.end_time_entry.get().strip()
        tags = self.tags_entry.get().strip()
        date_notif = self.get_date_notif(start_time)
        if not (len(self.date_notif_entry.get().strip())):
            notified = 1
        else:
            notified = 0
        if not name:
            show_error_popup("Для создания задачи необходимо дать ей имя")
            return
        task = Task(name, description, start_time, end_time, self.date, tags, done=0, notified=notified,
                    date_notif=date_notif)
        conn = sqlite3.connect(self.parent.tasks_db)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (name, description, start_time, end_time, date, tags, done, notified, date_notif)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
                       (task.name, task.description, task.start_time, task.end_time, task.date, task.tags, task.done,
                        task.notified, task.date_notif)
                       )
        conn.commit()
        conn.close()

        self.parent.update_task_list()
        self.destroy()

    def get_date_notif(self, start_time=None):
        # Преобразование строки даты в объект datetime
        if len(start_time):
            initial_date = self.date + ' ' + start_time
        else:
            initial_date = self.date + ' 00:00'

        # Преобразование строки даты в объект datetime
        base_date = datetime.strptime(initial_date, self.parent.date_format)
        if len(self.date_notif_entry.get().strip()):
            # Разделение интервала на дни, часы и минуты
            days, hours, minutes = map(int, self.date_notif_entry.get().strip().split(":"))

            # Создание объекта timedelta
            time_delta = timedelta(days=days, hours=hours, minutes=minutes)

            date_notif = (base_date - time_delta).strftime(self.parent.date_format)

            return date_notif
        else:
            return initial_date
