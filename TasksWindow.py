import sqlite3
from others import show_error_popup
import customtkinter as ctk
from Task import Task
from datetime import datetime, timedelta
import re
import tkinter as tk
from typing import List, Tuple

class BaseTaskWindow(ctk.CTkToplevel):
    """Общий предок для окон добавления/редактирования задач."""
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.attributes("-topmost", True)
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

        self.tags_entry = ctk.CTkEntry(self, placeholder_text="Заметки (через запятую)")
        self.tags_entry.pack(pady=5, fill="x", padx=20)

        # --- Личности (постепенное добавление строками) ---
        self.person_options: List[Tuple[int, str]] = self.load_person_options()  # (id, label)
        self.person_rows = []  # list[dict(frame, combo)]

        self.persons_label = ctk.CTkLabel(self, text="Личности")
        self.persons_label.pack(pady=(10, 0))

        self.persons_frame = ctk.CTkFrame(self)
        self.persons_frame.pack(pady=5, fill="x", padx=20)

        self.add_person_button = ctk.CTkButton(
            self,
            text="+ Добавить личность",
            command=self.add_person_row
        )
        self.add_person_button.pack(pady=(5, 0))
        self.add_person_row()

    def get_data(self) -> Task:
        """Возвращает задачу по данным из полей ввода."""
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

    def load_person_options(self) -> List[Tuple[int, str]]:
        conn = sqlite3.connect(self.parent.tasks_db)
        cursor = conn.cursor()
        cursor.execute("SELECT id, last_name, first_name, job FROM persons ORDER BY last_name, first_name")
        rows = cursor.fetchall()
        conn.close()

        options = []
        for pid, last_name, first_name, job in rows:
            label = f"{last_name} {first_name}"
            if job:
                label += f" — {job}"
            options.append((pid, label))
        return options

    def add_person_row(self, preset_person_id: int | None = None) -> None:
        labels = [lbl for _, lbl in self.person_options]
        if not labels:
            labels = ["(Сначала добавьте личности в меню)"]

        row_frame = ctk.CTkFrame(self.persons_frame)
        row_frame.pack(fill="x", pady=4)

        combo = ctk.CTkComboBox(row_frame, values=labels, width=300)
        combo.pack(side="left", padx=(8, 8), pady=6)

        # preset (для edit)
        if preset_person_id is not None:
            id_to_label = {pid: lbl for pid, lbl in self.person_options}
            if preset_person_id in id_to_label:
                combo.set(id_to_label[preset_person_id])

        del_btn = ctk.CTkButton(
            row_frame, text="×", width=34, fg_color="red",
            command=lambda: self.remove_person_row(row_frame)
        )
        del_btn.pack(side="left", padx=(0, 8), pady=6)

        self.person_rows.append({"frame": row_frame, "combo": combo})

    def remove_person_row(self, row_frame) -> None:
        self.person_rows = [r for r in self.person_rows if r["frame"] != row_frame]
        row_frame.destroy()
        if not self.person_rows:
            self.add_person_row()

    def get_selected_person_ids(self) -> List[int]:
        """Вернуть выбранные person_id; дубли не допускаются (будет ValueError)."""
        label_to_id = {lbl: pid for pid, lbl in self.person_options}

        selected = []
        for r in self.person_rows:
            lbl = r["combo"].get().strip()
            if lbl in label_to_id:        # игнорируем пустые/подсказку
                selected.append(label_to_id[lbl])

        # запрет дублей
        if len(selected) != len(set(selected)):
            raise ValueError("Одна и та же личность выбрана несколько раз")

        return selected


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
        try:
            selected_person_ids = self.get_selected_person_ids()
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
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            INSERT INTO tasks (name, description, start_time, end_time, date, tags, done, notified, date_notif)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (task.name, task.description, task.start_time, task.end_time, task.date,
              task.tags, task.done, task.notified, task.date_notif))

        task_id = cursor.lastrowid
        if selected_person_ids:
            cursor.executemany(
                "INSERT INTO task_person(task_id, person_id) VALUES (?, ?)",
                [(task_id, pid) for pid in selected_person_ids]
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
        self.date = self.task.date
        self.preselect_persons()

        # Поля для редактирования данных
        self.name_entry.insert(0, self.task.name)

        if self.task.description:
            self.description_entry.insert(0, self.task.description)

        if self.task.start_time:
            self.start_time_entry.insert(0, self.task.start_time)

        if self.task.end_time:
            self.end_time_entry.insert(0, self.task.end_time)

        if self.task.notified == 0:
            self.date_notif_entry.insert(0, self.get_what_insert_in_date_notif(self.task))

        if self.task.tags:
            self.tags_entry.insert(0, self.task.tags)

        self.done_status = ctk.IntVar(value=self.task.done)
        self.checkbox = ctk.CTkCheckBox(
            self,
            text="Выполнено",
            variable=self.done_status,
            onvalue=1,
            offvalue=0
        )
        self.checkbox.pack(pady=20)
        self.prefill_person_rows()


        # Кнопки для сохранения или удаления задачи
        self.save_button = ctk.CTkButton(self, text="Сохранить изменения", command=self.update_task)
        self.save_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(self, text="Удалить задачу", fg_color="red", command=self.delete_task)
        self.delete_button.pack(pady=10)

    def update_task(self) -> None:
        """Обновляет задачу в БД."""
        try:
            task = super().get_data()
            selected_person_ids = self.get_selected_person_ids()
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
        cursor.execute("DELETE FROM task_person WHERE task_id = ?", (self.task.id,))
        if selected_person_ids:
            cursor.executemany(
                "INSERT INTO task_person(task_id, person_id) VALUES (?, ?)",
                [(self.task.id, pid) for pid in selected_person_ids]
            )


        cursor.execute("DELETE FROM task_person WHERE task_id = ?", (self.task.id,))

        selected_person_ids = self.get_selected_person_ids()
        if selected_person_ids:
            cursor.executemany(
                "INSERT INTO task_person(task_id, person_id) VALUES (?, ?)",
                [(self.task.id, pid) for pid in selected_person_ids]
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
            dt1 = datetime.strptime(task.date + ' 00:00', self.parent.date_format)
        dt2 = datetime.strptime(task.date_notif, self.parent.date_format)
        delta = dt1 - dt2
        total_seconds = delta.total_seconds()
        days = int(total_seconds // 86400)
        hours = int((total_seconds % 86400) // 3600)
        minutes = int((total_seconds % 3600) // 60)
        result = f"{days:02}:{hours:02}:{minutes:02}"
        return result

    def prefill_person_rows(self) -> None:
        for r in list(self.person_rows):
            r["frame"].destroy()
        self.person_rows.clear()

        conn = sqlite3.connect(self.parent.tasks_db)
        cursor = conn.cursor()
        cursor.execute("SELECT person_id FROM task_person WHERE task_id = ?", (self.task.id,))
        person_ids = [row[0] for row in cursor.fetchall()]
        conn.close()

        if not person_ids:
            self.add_person_row()
            return

        for pid in person_ids:
            self.add_person_row(preset_person_id=pid)



