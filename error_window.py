import customtkinter as ctk

# Функция для создания всплывающего окна ошибки
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