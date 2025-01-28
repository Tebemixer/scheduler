import unittest
import os
from unittest.mock import patch
from lab.eighth import AutoCity, Vehicle, Route, Driver
import lab.eighth


class TestAutoCity(unittest.TestCase):
    def setUp(self):
        self.autocity = AutoCity()
        self.cleanup()

    def tearDown(self):
        lab.eighth._next_vehicle = 0
        lab.eighth._next_driver = 0
        lab.eighth._next_route = 0
        lab.eighth._next_garage = 0
        lab.eighth._next_maintenancestaff = 0

    def cleanup(self):
        """Удаляет созданные тестовые файлы баз данных."""
        databases = [
            'Vehicle.pkl', 'Route.pkl', 'Driver.pkl', 'MaintenanceStaff.pkl', 'Garage.pkl'
        ]
        for db in databases:
            if os.path.exists(db):
                os.remove(db)

    @patch('builtins.input', side_effect=['Test Route', '1', '1', 'Test schedule'])
    def test_add_route(self, mock_input):
        """Тестирует добавления объекта Route в базу данных."""
        self.autocity.route_database.add_object()
        self.assertEqual(len(self.autocity.route_database.database), 1)
        test = self.autocity.route_database.get_object_by_id(1)
        self.assertEqual(test.name, "Test Route")
        self.assertEqual(test.vehicle, [1])
        self.assertEqual(test.driver, [1])
        self.assertEqual(test.schedule, 'Test schedule')

    def test_delete_route(self):
        """Тестирует удаления объекта Route из базы данных."""
        route = Route('Test Route', [1], [1], 'Test schedule')
        self.autocity.route_database.database[route.id] = route
        self.autocity.route_database.save_database()

        self.assertEqual(len(self.autocity.route_database.database), 1)

        self.autocity.route_database.delete_object(route.id)
        self.assertEqual(len(self.autocity.route_database.database), 0)

    @patch("builtins.open")
    @patch('builtins.input', side_effect=['Updated Route', '20', '200', '1', 'Updated schedule'])
    def test_update_route(self, mock_input, mock_file):
        """Тестирует обновления объекта Route в базе данных."""
        route = Route('Test Route', [1], [1], 'Test schedule')
        self.autocity.route_database.database[route.id] = route
        self.autocity.route_database.save_database()

        self.autocity.route_database.change_object(route.id)
        updated_route = self.autocity.route_database.database[route.id]
        self.assertEqual(route, updated_route)

    @patch('builtins.input', side_effect=['Test Vehicle', '10', '100', '2', 'Test characteristics'])
    def test_add_vehicle(self, mock_input):
        """Тестирует добавления объекта Vehicle в базу данных."""
        self.autocity.vehicle_database.add_object()
        self.assertEqual(len(self.autocity.vehicle_database.database), 1)

        test = self.autocity.vehicle_database.get_object_by_id(1)
        self.assertEqual(test.name, "Test Vehicle")
        self.assertEqual(test.usage_hours, 10)
        self.assertEqual(test.mileage, 100)
        self.assertEqual(test.repairs_count, 2)
        self.assertEqual(test.characteristics, "Test characteristics")

    def test_delete_vehicle(self):
        """Тестирует удаления объекта Vehicle из базы данных."""
        vehicle = Vehicle('Test Vehicle', 10, 100, 2, 'Test characteristics')
        self.autocity.vehicle_database.database[vehicle.id] = vehicle
        self.autocity.vehicle_database.save_database()

        self.assertEqual(len(self.autocity.vehicle_database.database), 1)

        self.autocity.vehicle_database.delete_object(vehicle.id)
        self.assertEqual(len(self.autocity.vehicle_database.database), 0)

    @patch("builtins.open")
    @patch('builtins.input', side_effect=['Updated Vehicle', '20', '200', '1', 'Updated characteristics'])
    def test_update_vehicle(self, mock_input, mock_open):
        """Тестирует обновления объекта Vehicle в базе данных."""
        vehicle = Vehicle('Test Vehicle', 10, 100, 2, 'Test characteristics')
        self.autocity.vehicle_database.database[vehicle.id] = vehicle
        self.autocity.vehicle_database.save_database()

        self.autocity.vehicle_database.change_object(vehicle.id)
        updated_vehicle = self.autocity.vehicle_database.database[vehicle.id]
        self.assertEqual(vehicle, updated_vehicle)

    def test_choose_database(self):
        """Тестирует выбора базы данных."""
        self.autocity.choose_database(1)
        self.assertEqual(self.autocity.cur_database.cls, Vehicle)

        self.autocity.choose_database(3)
        self.assertEqual(self.autocity.cur_database.cls, Driver)


if __name__ == '__main__':
    unittest.main()
