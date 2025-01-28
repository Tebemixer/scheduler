import unittest
import os
from unittest.mock import patch, MagicMock
from lab.eighth import AutoCity, Vehicle, Route, Driver, MaintenanceStaff, Garage
import lab.eighth


class TestAutoCity(unittest.TestCase):
    def setUp(self):
        """Создание тестового окружения перед каждым тестом."""
        # Создаем экземпляр AutoCity
        self.autocity = AutoCity()

        # Удаляем тестовые базы данных, если они существуют
        self.cleanup()

    def tearDown(self):
        """Очистка после выполнения теста."""
        lab.eighth._next_vehicle = 0
        lab.eighth._next_driver = 0
        lab.eighth._next_route = 0
        lab.eighth._next_garage = 0
        lab.eighth._next_maintenancestaff = 0
        self.cleanup()

    def cleanup(self):
        """Удаляем созданные тестовые файлы баз данных."""
        databases = [
            'Vehicle.pkl', 'Route.pkl', 'Driver.pkl', 'MaintenanceStaff.pkl', 'Garage.pkl'
        ]
        for db in databases:
            if os.path.exists(db):
                os.remove(db)

    @patch('builtins.input', side_effect=['Test Vehicle', '10', '100', '2', 'Test characteristics'])
    @patch('lab.eighth.Vehicle', autospec=True)
    def test_add_vehicle(self, mock_vehicle, mock_input):
        """Тест добавления объекта Vehicle в базу данных с мокированием."""
        mock_vehicle.return_value = MagicMock()
        mock_vehicle.return_value.get_public_info.return_value = 'Mocked Vehicle Info'

        self.autocity.vehicle_database.add_object()

        self.assertEqual(len(self.autocity.vehicle_database.database), 1)
        vehicle = list(self.autocity.vehicle_database.database.values())[0]
        self.assertEqual(vehicle.get_public_info(), 'Mocked Vehicle Info')

    @patch('builtins.input', side_effect=['Test Route', '1', '1', 'Test schedule'])
    @patch('lab.eighth.Route', autospec=True)
    def test_add_route(self, mock_route, mock_input):
        """Тест добавления объекта Route в базу данных с мокированием."""
        mock_route.return_value = MagicMock()
        mock_route.return_value.get_public_info.return_value = 'Mocked Route Info'

        self.autocity.route_database.add_object()

        self.assertEqual(len(self.autocity.route_database.database), 1)
        route = list(self.autocity.route_database.database.values())[0]
        self.assertEqual(route.get_public_info(), 'Mocked Route Info')

    @patch('lab.eighth.Vehicle', autospec=True)
    def test_delete_vehicle(self, mock_vehicle):
        """Тест удаления объекта Vehicle из базы данных с мокированием."""
        mock_vehicle.return_value = MagicMock()
        vehicle = mock_vehicle.return_value
        vehicle.id = 1

        self.autocity.vehicle_database.database[vehicle.id] = vehicle
        self.autocity.vehicle_database.save_database()

        self.assertEqual(len(self.autocity.vehicle_database.database), 1)

        self.autocity.vehicle_database.delete_object(vehicle.id)
        self.assertEqual(len(self.autocity.vehicle_database.database), 0)

    @patch('builtins.input', side_effect=['Updated Vehicle', '20', '200', '1', 'Updated characteristics'])
    @patch('lab.eighth.Vehicle', autospec=True)
    def test_update_vehicle(self, mock_vehicle, mock_input):
        """Тест обновления объекта Vehicle в базе данных с мокированием."""
        mock_vehicle.return_value = MagicMock()
        vehicle = mock_vehicle.return_value
        vehicle.id = 1
        vehicle.get_public_info.return_value = 'Updated Mocked Vehicle Info'

        self.autocity.vehicle_database.database[vehicle.id] = vehicle
        self.autocity.vehicle_database.save_database()

        self.autocity.vehicle_database.change_object(vehicle.id)
        updated_vehicle = self.autocity.vehicle_database.database[vehicle.id]
        self.assertEqual(updated_vehicle.get_public_info(), 'Updated Mocked Vehicle Info')

    @patch('lab.eighth.AutoCity.printDB', autospec=True)
    def test_choose_database(self, mock_printDB):
        """Тест выбора базы данных с мокированием метода printDB."""
        self.autocity.choose_database(1)
        self.assertEqual(self.autocity.cur_database.cls, Vehicle)
        mock_printDB.assert_called_with(self.autocity, self.autocity.vehicle_database)

        self.autocity.choose_database(3)
        self.assertEqual(self.autocity.cur_database.cls, Driver)
        mock_printDB.assert_called_with(self.autocity, self.autocity.driver_database)


if __name__ == '__main__':
    unittest.main()