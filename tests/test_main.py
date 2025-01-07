import unittest
from unittest.mock import patch, MagicMock, call
from main import OrganizerApp, create_table, TASKS_DB
import sqlite3
import json
from datetime import datetime
from Task import Task


class TestOrganizerApp(unittest.TestCase):
    def setUp(self):
        """Инициализируем тестируемый объект."""
        self.app = OrganizerApp()
        #self.app.withdraw()  # Скрываем главное окно для тестов

    def tearDown(self):
        """Закрываем приложение после теста."""
        self.app.destroy()

    @patch("main.Calendar")
    @patch("main.ctk.CTkTextbox")
    @patch("main.get_tasks_by_date", return_value=[])
    def test_create_interface(self, mock_get_tasks_by_date, mock_textbox, mock_calendar):
        """Тестируем создание интерфейса."""
        self.app.create_interface()

        # Проверяем вызовы
        mock_calendar.assert_called_once_with(
            self.app,
            selectmode="day",
            date_pattern="yy-mm-dd",
            locale="ru"
        )
        mock_textbox.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='{"notifications_enabled": true}')
    def test_load_config(self, mock_open, mock_path_exists):
        """Тестируем загрузку конфигурации."""
        self.app.load_config()

        mock_path_exists.assert_called_once_with(self.app.config_file)
        mock_open.assert_called_once_with(self.app.config_file, "r")
        self.assertTrue(self.app.notifications_enabled.get())

    @patch("json.dump")
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_save_config(self, mock_open, mock_json_dump):
        """Тестируем сохранение конфигурации."""
        self.app.notifications_enabled.set(True)
        self.app.save_config()

        # Проверяем, что файл открылся
        mock_open.assert_called_once_with(self.app.config_file, "w")
        # Проверяем, что json.dump вызвался с правильными аргументами
        mock_json_dump.assert_called_once_with({"notifications_enabled": True}, mock_open())

    @patch("main.get_tasks_by_date", return_value=[
        Task("Task1", "Desc1", "09:00", "10:00", "23-12-25", "tag1", 0, 0, "23-12-25 08:55", 1)
    ])
    def test_update_task_list(self, mock_get_tasks_by_date):
        """Тестируем обновление списка задач."""
        self.app.update_task_list()
        mock_get_tasks_by_date.assert_called_once()

    @patch("main.EditTaskWindow")
    @patch("customtkinter.CTkTextbox.index", return_value="1.0")
    def test_open_task_editor(self, mock_index, mock_toplevel):
        """Тестируем открытие окна редактора задачи."""
        # Подготовка тестовых данных
        mock_task = Task("Task1", "Desc1", "09:00", "10:00", "23-12-25", "tag1", 0, 0, "23-12-25 08:55", 1)
        self.app.cur_tasks = [mock_task]

        # Создание mock-события
        mock_event = MagicMock()
        mock_event.x = 10
        mock_event.y = 10

        # Вызов тестируемого метода
        self.app.open_task_editor(mock_event)

        # Проверяем, что EditTaskWindow был вызван
        mock_toplevel.assert_called_once_with(self.app, mock_task)

    @patch("main.AddTaskWindow")
    def test_open_add_task_window(self, mock_toplevel):
        """Тестируем открытие окна добавления задачи."""
        self.app.open_add_task_window()
        mock_toplevel.assert_called_once()

    @patch("others.get_tasks_by_date", return_value=[
        Task("Task1", "Desc1", "09:00", "10:00", "23-12-25", "tag1", 0, 0, "23-12-25 08:55", 1)
    ])
    @patch("sqlite3.connect")
    @patch("customtkinter.CTkToplevel")
    def test_check_time(self, mock_toplevel, mock_connect, mock_get_tasks_by_date):
        """Тестируем проверку времени уведомлений."""
        self.app.notifications_enabled.set(True)

        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime.strptime("23-12-25 08:56", "%y-%m-%d %H:%M")
            mock_datetime.today.return_value.strftime.return_value = "23-12-25"

            self.app.check_time()
            mock_get_tasks_by_date.assert_called()
            mock_toplevel.assert_called_once()
            mock_connect.assert_called_once_with(TASKS_DB)

    @patch("main.ctk.CTkButton")
    @patch("main.ctk.CTkLabel")
    @patch("main.ctk.CTkToplevel")
    def test_show_notification(self, mock_toplevel, mock_label, mock_button):
        """Тестируем создание окна уведомления."""
        mock_task = Task("Task1", "Desc1", "09:00", "10:00", "23-12-25", "tag1", 0, 0, "23-12-25 08:55", 1)
        self.app.show_notification(mock_task)
        mock_toplevel.assert_called_once()

    @patch("sqlite3.connect")
    def test_create_table(self, mock_connect):
        """Тестируем создание таблицы."""
        create_table()

        mock_connect.assert_called_once_with(TASKS_DB)
        mock_connect().cursor().execute.assert_called_once()
        mock_connect().commit.assert_called_once()
        mock_connect().close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
