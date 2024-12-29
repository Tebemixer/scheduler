import sqlite3

import customtkinter as ctk

from Task import Task


def show_error_popup(message):
    # Создаем окно ошибки
    error_window = ctk.CTkToplevel()
    error_window.title("Ошибка")
    error_window.geometry("300x150")

    # Делаем окно модальным
    error_window.grab_set()

    # Текст ошибки
    label = ctk.CTkLabel(error_window, text=message, font=("Arial", 14))
    label.pack(pady=20)

    # Кнопка закрытия
    close_button = ctk.CTkButton(error_window, text="Закрыть", command=error_window.destroy)
    close_button.pack(pady=10)

def get_tasks_by_date(date,task_db):
    conn = sqlite3.connect(task_db)
    cursor = conn.cursor()
    query = """
        SELECT name, description, start_time, end_time, date, tags , done, id
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
