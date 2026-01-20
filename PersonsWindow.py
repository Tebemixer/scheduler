import sqlite3
import customtkinter as ctk
from others import show_error_popup


class PersonsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.attributes("-topmost", True)

        self.title("Личности")
        self.geometry("520x420")

        # Форма
        self.last_name_entry = ctk.CTkEntry(self, placeholder_text="Фамилия")
        self.last_name_entry.pack(pady=(10, 5), fill="x", padx=20)

        self.first_name_entry = ctk.CTkEntry(self, placeholder_text="Имя")
        self.first_name_entry.pack(pady=5, fill="x", padx=20)

        self.job_entry = ctk.CTkEntry(self, placeholder_text="Должность")
        self.job_entry.pack(pady=5, fill="x", padx=20)

        # Список
        self.listbox = ctk.CTkTextbox(self, height=160)
        self.listbox.pack(pady=10, fill="both", expand=True, padx=20)
        self.listbox.configure(state="disabled")

        # Кнопки
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.add_btn = ctk.CTkButton(btn_frame, text="Добавить", command=self.add_person)
        self.add_btn.grid(row=0, column=0, padx=8)

        # self.update_btn = ctk.CTkButton(btn_frame, text="Обновить список", command=self.load_persons)
        # self.update_btn.grid(row=0, column=1, padx=8)

        self.delete_btn = ctk.CTkButton(btn_frame, text="Удалить по id", fg_color="red", command=self.delete_person)
        self.delete_btn.grid(row=0, column=2, padx=8)

        # Поле для удаления
        self.delete_id_entry = ctk.CTkEntry(self, placeholder_text="id для удаления")
        self.delete_id_entry.pack(pady=(0, 10), fill="x", padx=20)

        self.load_persons()

    def load_persons(self):
        conn = sqlite3.connect(self.parent.tasks_db)
        cursor = conn.cursor()
        cursor.execute("SELECT id, last_name, first_name, job FROM persons ORDER BY last_name, first_name")
        rows = cursor.fetchall()
        conn.close()

        self.listbox.configure(state="normal")
        self.listbox.delete("1.0", "end")

        if not rows:
            self.listbox.insert("end", "Пока нет записей.\n")
        else:
            for pid, last_name, first_name, job in rows:
                job_part = f" — {job}" if job else ""
                self.listbox.insert("end", f"id={pid}: {last_name} {first_name}{job_part}\n")

        self.listbox.configure(state="disabled")

    def add_person(self):
        last_name = self.last_name_entry.get().strip()
        first_name = self.first_name_entry.get().strip()
        job = self.job_entry.get().strip()

        if not last_name or not first_name:
            show_error_popup("Фамилия и имя обязательны")
            return

        conn = sqlite3.connect(self.parent.tasks_db)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            "INSERT INTO persons(last_name, first_name, job) VALUES (?, ?, ?)",
            (last_name, first_name, job if job else None)
        )
        conn.commit()
        conn.close()

        self.last_name_entry.delete(0, "end")
        self.first_name_entry.delete(0, "end")
        self.job_entry.delete(0, "end")
        self.load_persons()

    def delete_person(self):
        raw = self.delete_id_entry.get().strip()
        if not raw.isdigit():
            show_error_popup("Для удаления нужен числовой id")
            return
        pid = int(raw)

        conn = sqlite3.connect(self.parent.tasks_db)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("DELETE FROM persons WHERE id = ?", (pid,))
        conn.commit()
        conn.close()

        self.delete_id_entry.delete(0, "end")
        self.load_persons()
