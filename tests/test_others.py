import unittest
from unittest.mock import patch, MagicMock
from others import show_error_popup, get_tasks_by_date
from Task import Task


class TestUtilityFunctions(unittest.TestCase):
    @patch("customtkinter.CTkButton")
    @patch("customtkinter.CTkLabel")
    @patch("customtkinter.CTkToplevel")
    def test_show_error_popup(self, mock_toplevel, mock_label, mock_button):
        """Тестирует, что окно ошибки создается корректно."""
        mock_window = MagicMock()
        mock_toplevel.return_value = mock_window

        show_error_popup("Test error message")

        mock_toplevel.assert_called_once()
        mock_window.title.assert_called_once_with("Ошибка")
        mock_window.geometry.assert_called_once_with("320x150")
        mock_window.grab_set.assert_called_once()

    @patch("main.sqlite3.connect")
    def test_get_tasks_by_date(self, mock_connect):
        """Тестирует функцию get_tasks_by_date."""
        test_date = "25-12-25"
        test_rows = [
            ("Task1", "Description1", "09:00", "10:00", "25-12-25", "tag1", 0, 0, "25-12-25 08:50", 1),
            ("Task2", "Description2", "11:00", "12:00", "25-12-25", "tag2", 1, 1, "25-12-25 10:50", 2)
        ]
        expected_tasks = [Task(*row) for row in test_rows]

        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = test_rows
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = get_tasks_by_date(test_date, "fake_tasks.db")
        executed_query, executed_params = mock_cursor.execute.call_args[0]
        expected_query = """
                SELECT name, description, start_time, end_time, date, tags , done, notified, date_notif, id
                FROM tasks
                WHERE date = ?
            """
        self.assertEqual(" ".join(executed_query.split()), " ".join(expected_query.split()))
        self.assertEqual(executed_params, (test_date,))

        mock_connect.return_value.close.assert_called_once()
        self.assertEqual(result, expected_tasks)


if __name__ == "__main__":
    unittest.main()
