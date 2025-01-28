import unittest
from unittest.mock import patch
import os
import pickle

from lab.eighth import AutoCity, Vehicle, Driver
import lab.eighth

class TestAutoCity(unittest.TestCase):
    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.auto_city = AutoCity()

        # Удаляем тестовые файлы баз данных перед началом теста
        for filename in ['Vehicle.pkl', 'Route.pkl', 'Driver.pkl', 'MaintenanceStaff.pkl', 'Garage.pkl']:
            if os.path.exists(filename):
                os.remove(filename)

    def tearDown(self):
        """Очистка после каждого теста"""
        for filename in ['Vehicle.pkl', 'Route.pkl', 'Driver.pkl', 'MaintenanceStaff.pkl', 'Garage.pkl']:
            if os.path.exists(filename):
                os.remove(filename)
        lab.eighth._next_vehicle = 0
        lab.eighth._next_maintenancestaff = 0
        lab.eighth._next_route = 0
        lab.eighth._next_garage = 0
        lab.eighth._next_driver = 0
    def test_add_vehicle(self):
        """Тест добавления транспортного средства в базу данных"""
        self.auto_city.vehicle_database.add_object("Car1", 100, 2000, 0, "Electric")
        vehicle = self.auto_city.vehicle_database.get_object_by_id(1)
        self.assertIsNotNone(vehicle)
        self.assertEqual(vehicle.name, "Car1")
        self.assertEqual(vehicle.usage_hours, 100)
        self.assertEqual(vehicle.mileage, 2000)

    def test_change_vehicle(self):
        """Тест изменения данных транспортного средства"""
        self.auto_city.vehicle_database.add_object("Car1", 100, 2000, 0, "Electric")
        self.auto_city.vehicle_database.change_object(1, "Car2, 200, 3000, 1, Hybrid")
        vehicle = self.auto_city.vehicle_database.get_object_by_id(1)
        self.assertEqual(vehicle.name, "Car2")
        self.assertEqual(vehicle.mileage, 3000)

    def test_delete_vehicle(self):
        """Тест удаления транспортного средства"""
        self.auto_city.vehicle_database.add_object("Car1", 100, 2000, 0, "Electric")
        self.auto_city.vehicle_database.delete_object(1)
        vehicle = self.auto_city.vehicle_database.get_object_by_id(1)
        self.assertIsNone(vehicle)

    def test_iterate_database(self):
        """Тест итерации по базе данных"""
        self.auto_city.vehicle_database.add_object("Car1", 100, 2000, 0, "Electric")
        self.auto_city.vehicle_database.add_object("Car2", 150, 2500, 1, "Hybrid")
        vehicles = list(self.auto_city.vehicle_database)
        self.assertEqual(len(vehicles), 2)
        self.assertEqual(vehicles[0].name, "Car1")
        self.assertEqual(vehicles[1].name, "Car2")

    def test_choose_database(self):
        """Тест выбора базы данных"""
        self.auto_city.choose_database(1)
        self.assertEqual(self.auto_city.cur_database, self.auto_city.vehicle_database)
        self.auto_city.choose_database(3)
        self.assertEqual(self.auto_city.cur_database, self.auto_city.driver_database)

    def test_save_and_load_database(self):
        """Тест сохранения и загрузки базы данных"""
        self.auto_city.vehicle_database.add_object("Car1", 100, 2000, 0, "Electric")
        self.auto_city.vehicle_database.save_database()
        self.auto_city.vehicle_database.open_database()
        vehicle = self.auto_city.vehicle_database.get_object_by_id(1)
        self.assertIsNotNone(vehicle)
        self.assertEqual(vehicle.name, "Car1")


if __name__ == "__main__":
    unittest.main()
