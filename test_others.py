import sys
import os
os.chdir("..")
import unittest
import others
from unittest.mock import patch, MagicMock
from Task import Task


class TestFunctions(unittest.TestCase):

    @patch("others.ctk.CTkToplevel")  # Мокаем CTkToplevel для GUI
    def test_show_error_popup(self, MockCTkToplevel):
        # Создаем мок для окна
        mock_window = MagicMock()
        MockCTkToplevel.return_value = mock_window

        # Вызываем функцию
        others.show_error_popup("Test error message")

        # Проверяем, что окно было создано
        MockCTkToplevel.assert_called_once()
        mock_window.title.assert_called_once_with("Ошибка")
        mock_window.geometry.assert_called_once_with("320x150")
        mock_window.grab_set.assert_called_once()
        mock_window.destroy.assert_not_called()  # Окно не должно быть уничтожено сразу

    @patch("others.sqlite3.connect")  # Мокаем соединение с базой данных
    def test_get_tasks_by_date(self, mock_connect):
        # Настраиваем мок для базы данных
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Данные, которые будет возвращать запрос
        mock_cursor.fetchall.return_value = [
            ("Task 1", "Description 1", "10:00", "11:00", "2024-12-30", "tag1,tag2", 0, 0, None, 1),
            ("Task 2", "Description 2", "11:00", "12:00", "2024-12-30", "tag3", 1, 0, None, 2),
        ]

        # Вызываем функцию
        result = others.get_tasks_by_date("2024-12-30", "mock_db.db")

        # Проверяем, что соединение с базой данных было установлено
        mock_connect.assert_called_once_with("mock_db.db")
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("""
            SELECT name, description, start_time, end_time, date, tags , done, notified, date_notif, id
            FROM tasks
            WHERE date = ?
        """, ("2024-12-30",))

        # Проверяем, что соединение было закрыто
        mock_conn.close.assert_called_once()

        # Проверяем, что результат функции соответствует ожиданиям
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Task)
        self.assertEqual(result[0].name, "Task 1")
        self.assertEqual(result[1].name, "Task 2")


if __name__ == "__main__":
    unittest.main()

