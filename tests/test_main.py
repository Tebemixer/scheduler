import unittest
from unittest.mock import patch, MagicMock, call
from main import OrganizerApp, create_table, TASKS_DB, CONFIG_FILE
from unittest.mock import patch, mock_open

class TestOrganizerApp(unittest.TestCase):
    def setUp(self):
        """Инициализируем тестовое приложение."""
        self.app = OrganizerApp()
        self.app.withdraw()  # Скрываем главное окно для ускорения тестов

    def tearDown(self):
        """Закрываем приложение после теста."""
        self.app.destroy()


    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='{"notifications_enabled": true}')
    @patch("os.path.exists", return_value=True)
    def test_load_config(self, mock_path_exists, mock_open):
        """Тестируем загрузку конфигурации."""
        self.app.load_config()
        mock_path_exists.assert_called_once_with(CONFIG_FILE)
        mock_open.assert_called_once_with(CONFIG_FILE, "r")
        self.assertTrue(self.app.notifications_enabled.get())

    @patch("sqlite3.connect")
    def test_create_table(self, mock_connect):
        """Тестируем создание таблицы в базе данных."""
        create_table()
        mock_connect.assert_called_once_with(TASKS_DB)
        mock_connect().cursor().execute.assert_called_once()
        mock_connect().commit.assert_called_once()
        mock_connect().close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
