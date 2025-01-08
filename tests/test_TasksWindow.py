import unittest
from unittest.mock import patch, MagicMock
import re
import tkinter as tk
from TasksWindow import AddTaskWindow, EditTaskWindow, Task


def normalize_sql(sql):
    """Нормализует SQL-запрос, убирая лишние пробелы и символы новой строки."""
    return re.sub(r"\s+", " ", sql.strip())


class TestAddTaskWindow(unittest.TestCase):
    def setUp(self):
        """Создаем родительское окно и пример данных."""
        self.parent = tk.Tk()
        self.parent.date_format = "%d-%m-%y %H:%M"
        self.parent.tasks_db = ":memory:"
        self.parent.withdraw()

        # Мокаем календарь
        self.parent.calendar = MagicMock()
        self.parent.calendar.get_date = MagicMock(return_value="25-12-25")

        # Мокаем метод update_task_list
        self.parent.update_task_list = MagicMock()

        self.task_example = Task(
            name="Test Task",
            description="Test Description",
            start_time="09:00",
            end_time="10:00",
            date="25-12-25",
            tags="tag1,tag2",
            done=0,
            notified=1,
            date_notif="25-12-25 08:50",
            id=1
        )

    def tearDown(self):
        """Закрываем родительское окно после теста."""
        self.parent.destroy()

    @patch("sqlite3.connect")
    def test_add_task_valid_data(self, mock_connect):
        """Тестируем добавление задачи с валидными данными."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        window = AddTaskWindow(self.parent)

        # Мокаем данные ввода
        window.name_entry.get = MagicMock(return_value="Test Task")
        window.description_entry.get = MagicMock(return_value="Test Description")
        window.start_time_entry.get = MagicMock(return_value="09:00")
        window.end_time_entry.get = MagicMock(return_value="10:00")
        window.date_notif_entry.get = MagicMock(return_value="00:01:00")
        window.tags_entry.get = MagicMock(return_value="tag1,tag2")

        # Вызываем метод добавления задачи
        window.add_task()

        # Получаем нормализованные SQL-запросы
        expected_sql = normalize_sql("""
            INSERT INTO tasks (name, description, start_time, end_time, date, tags, done, notified, date_notif)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """)

        actual_sql = normalize_sql(mock_cursor.execute.call_args[0][0])

        # Сравниваем нормализованные SQL-запросы
        self.assertEqual(expected_sql, actual_sql)

        # Проверяем параметры
        mock_cursor.execute.assert_any_call(
            mock_cursor.execute.call_args[0][0],
            ("Test Task", "Test Description", "09:00", "10:00", "25-12-25", "tag1,tag2", 0, 0, "25-12-25 08:00")
        )

        # Проверяем, что update_task_list был вызван
        self.parent.update_task_list.assert_called_once()


class TestEditTaskWindow(unittest.TestCase):
    def setUp(self):
        """Создаем родительское окно и пример данных."""
        self.parent = tk.Tk()
        self.parent.date_format = "%d-%m-%y %H:%M"
        self.parent.tasks_db = ":memory:"
        self.parent.withdraw()

        # Мокаем метод update_task_list
        self.parent.update_task_list = MagicMock()

        self.task_example = Task(
            name="Test Task",
            description="Test Description",
            start_time="09:00",
            end_time="10:00",
            date="25-12-25",
            tags="tag1,tag2",
            done=0,
            notified=1,
            date_notif="25-12-25 08:50",
            id=1
        )

    def tearDown(self):
        """Закрываем родительское окно после теста."""
        self.parent.destroy()

    @patch("sqlite3.connect")
    def test_update_task_valid_data(self, mock_connect):
        """Тестируем добавление задачи с валидными данными."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        window = EditTaskWindow(self.parent, self.task_example)

        # Мокаем данные ввода
        window.name_entry.get = MagicMock(return_value="Edited Task")
        window.description_entry.get = MagicMock(return_value="Edited Description")
        window.start_time_entry.get = MagicMock(return_value="08:00")
        window.end_time_entry.get = MagicMock(return_value="11:00")
        window.date_notif_entry.get = MagicMock(return_value="00:01:00")
        window.tags_entry.get = MagicMock(return_value="tag1,tag3")
        window.done_status.get = MagicMock(return_value=1)
        # Вызываем метод добавления задачи
        window.update_task()

        # Получаем нормализованные SQL-запросы
        expected_sql = normalize_sql(
            'UPDATE tasks SET name = ?, description = ?, start_time = ?, end_time =?, tags=?, done=?, notified=?, '
            'date_notif=?  WHERE id = ?'
        )

        actual_sql = normalize_sql(mock_cursor.execute.call_args[0][0])

        # Сравниваем нормализованные SQL-запросы
        self.assertEqual(expected_sql, actual_sql)
        # Проверяем параметры
        mock_cursor.execute.assert_any_call(
            mock_cursor.execute.call_args[0][0],
            ("Edited Task", "Edited Description", "08:00", "11:00", "tag1,tag3", 1, 0, "25-12-25 07:00", 1)
        )

        # Проверяем, что update_task_list был вызван
        self.parent.update_task_list.assert_called_once()

    @patch("sqlite3.connect")
    def test_delete_task(self, mock_connect):
        """Тестируем добавление задачи с валидными данными."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        window = EditTaskWindow(self.parent, self.task_example)
        window.delete_task()


        # Получаем нормализованные SQL-запросы
        expected_sql = normalize_sql('DELETE FROM tasks WHERE id = ?')
        actual_sql = normalize_sql(mock_cursor.execute.call_args[0][0])

        # Сравниваем нормализованные SQL-запросы
        self.assertEqual(expected_sql, actual_sql)
        # Проверяем параметры
        mock_cursor.execute.assert_any_call(
            mock_cursor.execute.call_args[0][0],
            (self.task_example.id,)
        )

        # Проверяем, что update_task_list был вызван
        self.parent.update_task_list.assert_called_once()

    def test_get_what_insert_in_date_notif(self):
        window = EditTaskWindow(self.parent, self.task_example)
        self.assertEqual(
            EditTaskWindow.get_what_insert_in_date_notif(window, self.task_example),
            '00:00:10'
            )


if __name__ == "__main__":
    unittest.main()
