import sqlite3
from error_window import show_error_popup
import customtkinter as ctk
import json
from Task import Task
class TaskWindow(ctk.CTkToplevel):

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
        self.save_button = ctk.CTkButton(self, text="Сохранить задачу", command=self.add_task)
        self.save_button.pack(pady=20)

    def add_task(self):
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()
        start_time = self.start_time_entry.get().strip()
        end_time = self.end_time_entry.get().strip()
        date = self.parent.calendar.get_date()
        tags = [tag.strip() for tag in self.tags_entry.get().strip().split(",")]
        if not name:
            show_error_popup("Для создания задачи необходимо имя")
            return

        selected_date = self.parent.calendar.get_date()
        task = Task(name, description, start_time, end_time, date, tags)



        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (name, description, start_time, end_time, date, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (task.name, task.description, task.start_time, task.end_time, task.date, ",".join(task.tags)))
        conn.commit()
        conn.close()

        self.parent.update_task_list()
        self.destroy()



