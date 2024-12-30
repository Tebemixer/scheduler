import unittest
from unittest.mock import patch, MagicMock
from others import show_error_popup, get_tasks_by_date
from Task import Task


class TestUtilityFunctions(unittest.TestCase):

    @patch("customtkinter.CTkToplevel")
    def test_show_error_popup(self, mock_toplevel):
        """Тестирует, что окно ошибки создается корректно."""
        mock_window = MagicMock()
        mock_toplevel.return_value = mock_window

        show_error_popup("Test error message")

        # Проверяем, что окно создается
        mock_toplevel.assert_called_once()
        mock_window.title.assert_called_once_with("Ошибка")
        mock_window.geometry.assert_called_once_with("320x150")
        mock_window.grab_set.assert_called_once()


if __name__ == "__main__":
    unittest.main()
