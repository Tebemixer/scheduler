import unittest
import os
from lab.third import Vehicle, Driver, Route, MaintenanceStaff, Garage, PersistenceClass
from unittest.mock import MagicMock, patch, mock_open
import lab.third


class TestLab(unittest.TestCase):

    def setUp(self):
        """Создает тестовые объекты для каждого класса."""
        self.vehicle = Vehicle("Bus", 1200, 50000, 3, "Diesel engine, 50 seats")
        self.driver = Driver("Ivanov", "Ivan", "Ivanovich", 1980, 2005, 20, "Bus driver", "Male")
        self.route = Route("Route 42", self.vehicle, self.driver, "8:00 - 20:00")
        self.staff = MaintenanceStaff("Technician", "Petrov", "Petr", "Petrovich", 1985, 2010, 15, "Male")
        self.garage = Garage("Main Garage", self.vehicle, "Engine repair", "2025-01-10", "2025-01-15", "Successful", [self.staff])

    def tearDown(self):
        """Обнуляет генераторы id после тестов."""
        lab.third._next_vehicle = 0
        lab.third._next_driver = 0
        lab.third._next_route = 0
        lab.third._next_garage = 0
        lab.third._next_maintenancestaff = 0

    def test_vehicle_destruction(self):
        """Тестирует деструктор Vehicle."""
        self.vehicle.change_history = MagicMock()
        self.vehicle.__del__()
        self.vehicle.change_history.clear.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_vehicle_transaction(self, mocked_open):
        """Тестируем обновление информации о Vehicle."""
        self.vehicle.update_info("Truck", 1500, 60000, 4, "Electric engine, 30 seats")
        mocked_open.assert_called_once_with('history of change Vehicle.txt', 'a')

        file_handle = mocked_open()
        file_handle.write.assert_called_once()

        written_data = file_handle.write.call_args[0][0]
        self.assertIn("Bus->Truck", written_data)
        self.assertIn("usage_hours:1200->1500;", written_data)

    @patch("builtins.open", new_callable=mock_open)
    @patch("pickle.dump")
    @patch("pickle.load")
    def test_serialization_vehicle(self, mock_load, mock_dump, mocked_open):
        """Тестирует сериализацию и десериализацию объекта Vehicle."""
        mock_load.return_value = self.vehicle

        PersistenceClass.serialize(self.vehicle)
        mocked_open.assert_called_once_with(f"Vehicle_{self.vehicle.id}.pkl", "wb")
        mock_dump.assert_called_once_with(self.vehicle, mocked_open())

        loaded_vehicle = PersistenceClass.deserialize(f"Vehicle_{self.vehicle.id}.pkl")
        mocked_open.assert_called_with(f"Vehicle_{self.vehicle.id}.pkl", "rb")
        mock_load.assert_called_once_with(mocked_open())
        self.assertEqual(self.vehicle.get_info(), loaded_vehicle.get_info())


    def test_driver_destruction(self):
        """Тестирует деструктор Driver."""
        self.driver.change_history = MagicMock()
        self.driver.__del__()
        self.driver.change_history.clear.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_driver_transaction(self, mocked_open):
        """Тестируем обновление информации о Driver."""
        self.driver.update_info("Smirnov", "Ivan", "Ivanovich", 1980, 2005, 20, "Bus driver", "Male", '', '', '')
        mocked_open.assert_called_once_with('history of change Driver.txt', 'a')

        file_handle = mocked_open()
        file_handle.write.assert_called_once()

        written_data = file_handle.write.call_args[0][0]
        self.assertIn("Ivanov->Smirnov", written_data)

    @patch("builtins.open", new_callable=mock_open)
    @patch("pickle.dump")
    @patch("pickle.load")
    def test_serialization_driver(self, mock_load, mock_dump, mocked_open):
        """Тестирует сериализацию и десериализацию объекта Driver."""
        mock_load.return_value = self.driver

        PersistenceClass.serialize(self.driver)
        mocked_open.assert_called_once_with(f"Driver_{self.driver.id}.pkl", "wb")
        mock_dump.assert_called_once_with(self.driver, mocked_open())

        loaded_driver = PersistenceClass.deserialize(f"Driver_{self.driver.id}.pkl")
        mocked_open.assert_called_with(f"Driver_{self.driver.id}.pkl", "rb")
        mock_load.assert_called_once_with(mocked_open())
        self.assertEqual(self.driver.get_info(), loaded_driver.get_info())

    def test_route_destruction(self):
        """Тестирует деструктор Route."""
        self.route.change_history = MagicMock()
        self.route.__del__()
        self.route.change_history.clear.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_route_transaction(self, mocked_open):
        """Тестируем обновление информации о Route."""
        self.route.update_info("Route 42", self.vehicle, self.driver, "12:00 - 20:00")
        mocked_open.assert_called_once_with('history of change Route.txt', 'a')

        file_handle = mocked_open()
        file_handle.write.assert_called_once()

        written_data = file_handle.write.call_args[0][0]
        self.assertIn("8:00 - 20:00->12:00 - 20:00", written_data)

    def test_maintancestaff_destruction(self):
        """Тестирует деструктор MaintenanceStaff."""
        self.staff.change_history = MagicMock()
        self.staff.__del__()
        self.staff.change_history.clear.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_maintancestaff_transaction(self, mocked_open):
        """Тестируем обновление информации о MaintenanceStaff."""
        self.staff.update_info("High Technician", "Petrov", "Petr", "Petrovich", 1985, 2010, 15, "Male", '', '', '')
        mocked_open.assert_called_once_with('history of change MaintenanceStaff.txt', 'a')

        file_handle = mocked_open()
        file_handle.write.assert_called_once()

        written_data = file_handle.write.call_args[0][0]
        self.assertIn("Technician->High Technician", written_data)

    def test_garage_destruction(self):
        """Тестирует деструктор Garage."""
        self.garage.change_history = MagicMock()
        self.garage.__del__()
        self.garage.change_history.clear.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_garage_transaction(self, mocked_open):
        """Тестируем обновление информации о Garage."""
        self.garage.update_info("Main Garage", self.vehicle, "Engine repair", "2025-01-10", "???", "Fail", [self.staff])
        mocked_open.assert_called_once_with('history of change Garage.txt', 'a')

        file_handle = mocked_open()
        file_handle.write.assert_called_once()

        written_data = file_handle.write.call_args[0][0]
        self.assertIn("Fail", written_data)
        self.assertIn("???", written_data)


if __name__ == "__main__":
    unittest.main()
