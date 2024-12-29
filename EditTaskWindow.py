import customtkinter as ctk
import sqlite3
from others import show_error_popup
from datetime import datetime, timedelta

class EditTaskWindow(ctk.CTkToplevel):
    def __init__(self, parent, task):
        super().__init__(parent)

        self.parent = parent
        self.task = task
        self.title("Редактировать задачу")
        self.geometry("400x400")

        # Поля для редактирования данных
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Название задачи")
        if task.name:
            self.name_entry.insert(0, task.name)
        self.name_entry.pack(pady=5, fill="x", padx=20)

        self.description_entry = ctk.CTkEntry(self, placeholder_text="Описание задачи")
        if task.description:
            self.description_entry.insert(0, task.description)
        self.description_entry.pack(pady=5, fill="x", padx=20)

        self.start_time_entry = ctk.CTkEntry(self, placeholder_text="Время начала (ЧЧ:MM)")
        if task.start_time:
            self.start_time_entry.insert(0, task.start_time)
        self.start_time_entry.pack(pady=5, fill="x", padx=20)

        self.end_time_entry = ctk.CTkEntry(self, placeholder_text="Время окончания (ЧЧ:MM)")
        if task.end_time:
            self.end_time_entry.insert(0, task.end_time)
        self.end_time_entry.pack(pady=5, fill="x", padx=20)

        self.date_notif_entry = ctk.CTkEntry(self, placeholder_text="Напомнить за (ДД:ЧЧ:MM)")
        if task.notified:
            self.date_notif_entry.insert(0, self.get_what_insert_in_date_notif(task))
        self.date_notif_entry.pack(pady=5, fill="x", padx=20)

        self.tags_entry = ctk.CTkEntry(self, placeholder_text="Теги (через запятую)")
        if task.tags:
            self.tags_entry.insert(0, task.tags)
        self.tags_entry.pack(pady=5, fill="x", padx=20)

        # Чекбокс для включения/выключения уведомлений

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



    def update_task(self):
        self.task.name = self.name_entry.get().strip()
        self.task.description = self.description_entry.get().strip()
        self.task.start_time = self.start_time_entry.get().strip()
        self.task.end_time = self.end_time_entry.get().strip()
        self.task.tags = self.tags_entry.get().strip()
        self.task.done = self.done_status.get()
        self.task.date_notif = self.get_date_notif(self.task)
        if self.task.date_notif == self.task.start_time+' 00:00':
            self.task.notified = 1
        else:
            self.task.notified = 0
        if not self.task.name:
            show_error_popup("Для создания задачи необходимо дать ей имя")
            return

        connection = sqlite3.connect(self.parent.tasks_db)
        cursor = connection.cursor()

        cursor.execute('UPDATE tasks SET name = ?, description = ?, start_time = ?, end_time =?, tags=?, done=?, '
                       'notified=?, date_notif=?  WHERE id = ?',
                       (self.task.name, self.task.description, self.task.start_time, self.task.end_time, self.task.tags, self.task.done, self.task.notified, self.task.date_notif, self.task.id)
                       )

        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()
        self.parent.update_task_list()
        self.destroy()

    def delete_task(self):
        connection = sqlite3.connect(self.parent.tasks_db)
        cursor = connection.cursor()

        cursor.execute('DELETE FROM tasks WHERE id = ?', (self.task.id,))
        print(f"Удалена задача с id {self.task.id}")
        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()

        self.parent.update_task_list()
        self.destroy()

    def get_what_insert_in_date_notif(self, task):
        if task.start_time:
            dt1 = datetime.strptime(task.date + ' ' + task.start_time, self.parent.date_format)
        else:
            dt1 = datetime.strptime(task.date + '00:00', self.parent.date_format)
        dt2 = datetime.strptime(task.date_notif, self.parent.date_format)
        delta = dt1 - dt2

        # Получение дней, часов и минут из разницы
        total_seconds = delta.total_seconds()
        days = int(total_seconds // 86400)  # Секунды в сутках
        hours = int((total_seconds % 86400) // 3600)  # Оставшиеся секунды переводим в часы
        minutes = int((total_seconds % 3600) // 60)  # Оставшиеся секунды переводим в минуты

        # Результат в формате DD:HH:MM
        result = f"{days:02}:{hours:02}:{minutes:02}"

        return result

    def get_date_notif(self, task):
        # Преобразование строки даты в объект datetime
        if len(task.start_time):
            initial_date = self.task.date + ' ' + task.start_time
        else:
            initial_date = self.task.date + ' 00:00'

        # Преобразование строки даты в объект datetime
        base_date = datetime.strptime(initial_date, self.parent.date_format)
        if len(self.date_notif_entry.get().strip()):
            # Разделение интервала на дни, часы и минуты
            days, hours, minutes = map(int, self.date_notif_entry.get().strip().split(":"))

            # Создание объекта timedelta
            time_delta = timedelta(days=days, hours=hours, minutes=minutes)

            date_notif = base_date - time_delta

            return date_notif.strftime(self.parent.date_format)
        else:
            return initial_date


