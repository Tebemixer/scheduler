import unittest
from Task import Task


class TestTask(unittest.TestCase):
    def setUp(self):
        """Тестирует объект Task для использования в тестах."""
        self.task = Task(
            name="Test Task",
            description="Test Description",
            start_time="10:00",
            end_time="11:00",
            date="2024-12-30",
            tags="test,example",
            done=1,
            notified=1,
            date_notif="2024-12-29 09:00",
            id=42
        )

    def test_task_initialization(self):
        """Тестирует правильность инициализации объекта Task."""
        self.assertEqual(self.task.name, "Test Task")
        self.assertEqual(self.task.description, "Test Description")
        self.assertEqual(self.task.start_time, "10:00")
        self.assertEqual(self.task.end_time, "11:00")
        self.assertEqual(self.task.date, "2024-12-30")
        self.assertEqual(self.task.tags, "test,example")
        self.assertEqual(self.task.done, 1)
        self.assertEqual(self.task.notified, 1)
        self.assertEqual(self.task.date_notif, "2024-12-29 09:00")
        self.assertEqual(self.task.id, 42)

    def test_to_dict(self):
        """Тестирует правильность преобразования задачи в словарь."""
        task_dict = self.task.to_dict()
        expected_dict = {
            "name": "Test Task",
            "description": "Test Description",
            "start_time": "10:00",
            "end_time": "11:00",
            "date": "2024-12-30",
            "tags": "test,example",
            "done": 1,
            "notified": 1,
            "date_notif": "2024-12-29 09:00",
            "id": 42
        }
        self.assertEqual(task_dict, expected_dict)

    def test_from_dict_success(self):
        """Тестирует создание задачи из корректного словаря."""
        task_data = {
            "name": "New Task",
            "description": "New Description",
            "start_time": "12:00",
            "end_time": "13:00",
            "date": "2024-12-31",
            "tags": "work,urgent",
            "done": 0,
            "notified": 0,
            "date_notif": "",
            "id": 43
        }
        new_task = Task.from_dict(task_data)
        self.assertIsNotNone(new_task)
        self.assertEqual(new_task.name, "New Task")
        self.assertEqual(new_task.description, "New Description")
        self.assertEqual(new_task.start_time, "12:00")
        self.assertEqual(new_task.end_time, "13:00")
        self.assertEqual(new_task.date, "2024-12-31")
        self.assertEqual(new_task.tags, "work,urgent")
        self.assertEqual(new_task.done, 0)
        self.assertEqual(new_task.notified, 0)
        self.assertEqual(new_task.date_notif, "")
        self.assertEqual(new_task.id, 43)

    def test_from_dict_missing_keys(self):
        """Тестирует обработку отсутствующих ключей в словаре."""
        incomplete_task_data = {
            "name": "Incomplete Task",
            "description": "Missing some keys",
            "start_time": "15:00",
            # Отсутствуют ключи: "end_time", "date", "tags", "done", "notified", "date_notif", "id"
        }
        new_task = Task.from_dict(incomplete_task_data)
        self.assertIsNone(new_task)

    def test_from_dict_key_error_message(self):
        """Тестирует вывод ошибки при отсутствии ключа."""
        incomplete_task_data = {
            "name": "Task",
            "description": "Some description",
            # Пропущен ключ "start_time"
        }
        with self.assertLogs(level="ERROR") as log:
            new_task = Task.from_dict(incomplete_task_data)
            self.assertIsNone(new_task)
            self.assertIn("Ошибка: отсутствует ключ 'start_time' в задаче", log.output[0])


class TestTaskEquality(unittest.TestCase):
    def setUp(self):
        """Инициализирует тестовые объекты Task."""
        self.task1 = Task("Task1", "Description1", "09:00", "10:00", "25-12-25", "tag1", 0, 0, "25-12-25 08:50", 1)
        self.task2 = Task("Task1", "Description1", "09:00", "10:00", "25-12-25", "tag1", 0, 0, "25-12-25 08:50", 1)
        self.task3 = Task("Task2", "Description2", "11:00", "12:00", "26-12-25", "tag2", 1, 1, "25-12-25 10:50", 2)

    def test_equal_tasks(self):
        """Тестирует, что два идентичных объекта считаются равными."""
        self.assertEqual(self.task1, self.task2, "Идентичные задачи должны быть равны")

    def test_not_equal_tasks(self):
        """Тестирует, что два разных объекта считаются неравными."""
        self.assertNotEqual(self.task1, self.task3, "Разные задачи не должны быть равны")

    def test_comparison_with_other_type(self):
        """Тестирует, что объект Task не равен объекту другого типа."""
        self.assertNotEqual(self.task1, "Not a Task", "Задача не должна быть равна строке")

    def test_self_equality(self):
        """Тестирует, что объект равен самому себе."""
        self.assertEqual(self.task1, self.task1, "Задача должна быть равна самой себе")


if __name__ == "__main__":
    unittest.main()

