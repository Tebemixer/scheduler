import sqlite3
from others import show_error_popup
import customtkinter as ctk
from Task import Task
from datetime import datetime, timedelta
import re


class BaseTaskWindow(ctk.CTkToplevel):
    """Общий предок для окон добавления/редактирования задач."""
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.date = None
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

    def get_data(self) -> Task:

        name = self.name_entry.get().strip()
        if not name:
            raise ValueError("Для создания задачи необходимо дать ей имя")

        start_time = self.start_time_entry.get().strip()
        if not re.fullmatch(r"^\d{2}:\d{2}$", start_time) and start_time != '':
            raise ValueError("Задайте время начала в формате ЧЧ:ММ")

        end_time = self.end_time_entry.get().strip()
        if not re.fullmatch(r"^\d{2}:\d{2}$", end_time) and end_time != '':
            raise ValueError("Задайте время окончания в формате ЧЧ:ММ")

        date_notif = self.date_notif_entry.get().strip()
        if not re.fullmatch(r"^\d{2}:\d{2}:\d{2}$", date_notif) and date_notif != '':
            raise ValueError("Задайте время напоминания перед началом события в формате ДД:ЧЧ:ММ")
        date_notif = self.get_date_notif(start_time, date_notif)

        description = self.description_entry.get().strip()
        tags = self.tags_entry.get().strip()

        task = Task(name, description, start_time, end_time, self.date, tags, done=0, notified=1,
                    date_notif=date_notif)
        return task

    def get_date_notif(self, start_time: str, date_notif: str) -> str:
        """Вычисляет date_notif для task перед добавлением в БД."""
        if len(start_time):
            initial_date = self.date + ' ' + start_time
        else:
            initial_date = self.date + ' 00:00'
        base_date = datetime.strptime(initial_date, self.parent.date_format)
        if len(self.date_notif_entry.get().strip()):
            days, hours, minutes = map(int, date_notif.split(":"))
            time_delta = timedelta(days=days, hours=hours, minutes=minutes)
            date_notif = (base_date - time_delta).strftime(self.parent.date_format)
            return date_notif
        else:
            return initial_date


class AddTaskWindow(BaseTaskWindow):
    """Окно создание задачи."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Добавить задачу")
        self.geometry("400x400")

        self.date = self.parent.calendar.get_date()

        # Кнопка для сохранения задачи
        self.save_button = ctk.CTkButton(self, text="Сохранить задачу", command=self.add_task)
        self.save_button.pack(pady=20)

    def add_task(self) -> None:
        """Добавляет задачу в базу данных."""
        try:
            task = super().get_data()
        except ValueError as error:
            show_error_popup(f"{error}")
            return

        if not (len(self.date_notif_entry.get().strip())):
            notified = 1
        else:
            notified = 0

        task.notified = notified
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

class EditTaskWindow(BaseTaskWindow):
    """Окно редактирования задачи."""
    def __init__(self, parent, task):
        super().__init__(parent)
        self.task = task
        self.title("Редактировать задачу")
        self.geometry("400x400")
        self.date = task.date

        # Поля для редактирования данных
        self.name_entry.insert(0, task.name)

        if task.description:
            self.description_entry.insert(0, task.description)

        if task.start_time:
            self.start_time_entry.insert(0, task.start_time)

        if task.end_time:
            self.end_time_entry.insert(0, task.end_time)

        if not bool(task.notified):
            self.date_notif_entry.insert(0, self.get_what_insert_in_date_notif(task))

        if task.tags:
            self.tags_entry.insert(0, task.tags)

        self.done_status = ctk.IntVar(value=task.done)
        self.checkbox = ctk.CTkCheckBox(
            self,
            text="Выполнено",
            variable=self.done_status,
            onvalue=1,
            offvalue=0
        )
        self.checkbox.pack(pady=20)

        # Кнопки для сохранения или удаления задачи
        self.save_button = ctk.CTkButton(self, text="Сохранить изменения", command=self.update_task)
        self.save_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(self, text="Удалить задачу", fg_color="red", command=self.delete_task)
        self.delete_button.pack(pady=10)

    def update_task(self) -> None:
        """Обновляет задачу в БД."""
        try:
            task = super().get_data()
        except ValueError as error:
            show_error_popup(f"{error}")
            return
        task.done = self.done_status.get()
        if self.task.notified == 0 or len(self.date_notif_entry.get().strip()) != 0:
            task.notified = 0

        connection = sqlite3.connect(self.parent.tasks_db)
        cursor = connection.cursor()

        cursor.execute('UPDATE tasks SET name = ?, description = ?, start_time = ?, end_time =?, tags=?, done=?, '
                       'notified=?, date_notif=?  WHERE id = ?',
                       (task.name, task.description, task.start_time, task.end_time, task.tags,
                        task.done, task.notified, task.date_notif, self.task.id)
                       )
        connection.commit()
        connection.close()
        self.parent.update_task_list()
        self.destroy()

    def delete_task(self) -> None:
        """Удаляет задачу из БД."""
        connection = sqlite3.connect(self.parent.tasks_db)
        cursor = connection.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (self.task.id,))
        connection.commit()
        connection.close()
        self.parent.update_task_list()
        self.destroy()

    def get_what_insert_in_date_notif(self, task: Task) -> str:
        """Вычисляет вставку в поле времени для уведомления."""
        if task.start_time:
            dt1 = datetime.strptime(task.date + ' ' + task.start_time, self.parent.date_format)
        else:
            dt1 = datetime.strptime(task.date + '00:00', self.parent.date_format)
        dt2 = datetime.strptime(task.date_notif, self.parent.date_format)
        delta = dt1 - dt2
        total_seconds = delta.total_seconds()
        days = int(total_seconds // 86400)
        hours = int((total_seconds % 86400) // 3600)
        minutes = int((total_seconds % 3600) // 60)
        result = f"{days:02}:{hours:02}:{minutes:02}"
        return result







