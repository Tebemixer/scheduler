import sqlite3
import customtkinter as ctk
from Task import Task


def show_error_popup(message: str) -> None:
    """Создает окно ошибки с текстовым сообщением внутри, подстраивая размер под текст."""
    error_window = ctk.CTkToplevel()
    error_window.title("Ошибка")
    error_window.grab_set()
    error_window.attributes("-topmost", True)
    # Создаем виджеты
    label = ctk.CTkLabel(error_window, text=message, font=("Arial", 14), wraplength=300)
    label.pack(padx=20, pady=20)  # Добавляем отступы для красоты
    close_button = ctk.CTkButton(error_window, text="Закрыть", command=error_window.destroy)
    close_button.pack(pady=(0, 20))

    # Обновляем размеры окна на основе содержимого
    error_window.update_idletasks()
    width = error_window.winfo_reqwidth()
    height = error_window.winfo_reqheight()
    error_window.geometry(f"{width}x{height}")



def get_tasks_by_date(date: str, task_db: str) -> list:
    """Возвращает список tasks соответствующих переданной дате."""
    conn = sqlite3.connect(task_db)
    cursor = conn.cursor()
    query = """
        SELECT name, description, start_time, end_time, date, tags , done, notified, date_notif, id
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
