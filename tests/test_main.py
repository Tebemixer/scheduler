import threading
import time
import unittest
from unittest.mock import patch, MagicMock
from main import OrganizerApp, create_table, TASKS_DB
from datetime import datetime, timedelta
from Task import Task


class TestOrganizerApp(unittest.TestCase):
    def setUp(self):
        """Инициализирует тестируемый объект."""
        self.app = OrganizerApp()
        self.app.withdraw()  # Скрываем главное окно для тестов

    def tearDown(self):
        """Закрывает приложение после теста."""
        self.app.destroy()

    @patch("main.Calendar")
    @patch("main.ctk.CTkTextbox")
    @patch("main.get_tasks_by_date", return_value=[])
    def test_create_interface(self, mock_get_tasks_by_date, mock_textbox, mock_calendar):
        """Тестирует создание интерфейса."""
        self.app.create_interface()

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
        """Тестирует загрузку конфигурации."""
        self.app.load_config()

        mock_path_exists.assert_called_once_with(self.app.config_file)
        mock_open.assert_called_once_with(self.app.config_file, "r")
        self.assertTrue(self.app.notifications_enabled.get())

    @patch("json.dump")
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_save_config(self, mock_open, mock_json_dump):
        """Тестирует сохранение конфигурации."""
        self.app.notifications_enabled.set(True)
        self.app.save_config()

        mock_open.assert_called_once_with(self.app.config_file, "w")
        mock_json_dump.assert_called_once_with({"notifications_enabled": True}, mock_open())

    @patch("main.get_tasks_by_date", return_value=[
        Task("Task1", "Desc1", "09:00", "10:00", "23-12-25", "tag1", 0, 0, "23-12-25 08:55", 1)
    ])
    def test_update_task_list(self, mock_get_tasks_by_date):
        """Тестирует обновление списка задач."""
        self.app.update_task_list()
        mock_get_tasks_by_date.assert_called_once()

    @patch("main.EditTaskWindow")
    @patch("customtkinter.CTkTextbox.index", return_value="1.0")
    def test_open_task_editor(self, mock_index, mock_toplevel):
        """Тестирует открытие окна редактора задачи."""
        mock_task = Task("Task1", "Desc1", "09:00", "10:00", "23-12-25", "tag1", 0, 0, "23-12-25 08:55", 1)
        self.app.cur_tasks = [mock_task]

        mock_event = MagicMock()
        mock_event.x = 10
        mock_event.y = 10

        self.app.open_task_editor(mock_event)
        mock_toplevel.assert_called_once_with(self.app, mock_task)

    @patch("main.AddTaskWindow")
    def test_open_add_task_window(self, mock_toplevel):
        """Тестирует открытие окна добавления задачи."""
        self.app.open_add_task_window()
        mock_toplevel.assert_called_once()

    @patch("main.get_tasks_by_date")
    @patch("main.datetime")
    @patch("main.OrganizerApp.show_notification")
    @patch("main.sqlite3.connect")
    def test_check_time(self, mock_connect, mock_show_notification, mock_datetime, mock_get_tasks_by_date):
        """Тестирует метод check_time."""
        now = datetime(2025, 1, 7, 9, 0, 0)
        mock_datetime.now.return_value = now
        mock_datetime.strptime.side_effect = datetime.strptime
        mock_datetime.today.return_value = now

        task = Task(
            name="Test Task",
            description="Test Description",
            start_time="09:00",
            end_time="10:00",
            date="25-01-07",
            tags="tag1",
            done=0,
            notified=0,
            date_notif=(now - timedelta(minutes=1)).strftime("%y-%m-%d %H:%M"),
            id=1
        )
        mock_get_tasks_by_date.return_value = [task]

        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        self.app.notifications_enabled_flag = True  # Активируем уведомления
        self.app.stop_check_time.clear()

        thread = threading.Thread(target=self.app.check_time)
        thread.start()
        time.sleep(1)
        self.app.stop_check_time.set()
        thread.join()

        mock_show_notification.assert_called_once_with(task)
        mock_cursor.execute.assert_called_once_with(
            'UPDATE tasks SET notified = ? WHERE id = ?',
            (1, task.id)
        )
        mock_connect.return_value.commit.assert_called_once()

    @patch("main.ctk.CTkButton")
    @patch("main.ctk.CTkLabel")
    @patch("main.ctk.CTkToplevel")
    def test_show_notification(self, mock_toplevel, mock_label, mock_button):
        """Тестирует создание окна уведомления."""
        mock_task = Task("Task1", "Desc1", "09:00", "10:00", "23-12-25", "tag1", 0, 0, "23-12-25 08:55", 1)
        self.app.show_notification(mock_task)
        mock_toplevel.assert_called_once()

    @patch("sqlite3.connect")
    def test_create_table(self, mock_connect):
        """Тестирует создание таблицы."""
        create_table()

        mock_connect.assert_called_once_with(TASKS_DB)
        mock_connect().cursor().execute.assert_called_once()
        mock_connect().commit.assert_called_once()
        mock_connect().close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
