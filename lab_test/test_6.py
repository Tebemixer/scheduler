import unittest
from lab.sixth import Vehicle, MaintenanceStaff, Garage
import lab.sixth


class TestVehicleOperations(unittest.TestCase):
    def setUp(self):
        """Создание объекта Vehicle перед каждым тестом."""
        self.vehicle = Vehicle(name="Test Vehicle", mileage=100)

    def tearDown(self):
        lab.sixth._next_vehicle = 0
        lab.sixth._next_maintenancestaff = 0
        
    def test_add_mileage(self):
        """Тестирует метода __add__ (увеличение пробега)."""
        self.vehicle + 50
        self.assertEqual(self.vehicle.mileage, 150, "__add__ должен увеличивать пробег.")

    def test_sub_mileage(self):
        """Тестирует метода __sub__ (уменьшение пробега)."""
        self.vehicle - 30
        self.assertEqual(self.vehicle.mileage, 70, "__sub__ должен уменьшать пробег.")

    def test_mul_mileage(self):
        """Тестирует метода __mul__ (умножение пробега)."""
        self.vehicle * 2
        self.assertEqual(self.vehicle.mileage, 200, "__mul__ должен умножать пробег.")

    def test_truediv_mileage(self):
        """Тестирует метода __truediv__ (деление пробега)."""
        self.vehicle / 2
        self.assertEqual(self.vehicle.mileage, 50, "__truediv__ должен делить пробег.")

    def test_truediv_mileage_zero(self):
        """Тестирует деления на ноль для метода __truediv__ (ожидаемое исключение)."""
        with self.assertRaises(ZeroDivisionError):
            self.vehicle / 0


class TestGarageOperations(unittest.TestCase):
    def setUp(self):
        """Создание объектов Garage и MaintenanceStaff перед каждым тестом."""
        self.staff1 = MaintenanceStaff("Smith", "John", "A.", 1985, 2010, 10, "Mechanic", "Male")
        self.staff2 = MaintenanceStaff("Doe", "Jane", "B.", 1990, 2015, 5, "Technician", "Female")
        self.garage = Garage(name="Main Garage", vehicle=None, repair_type="General", date_received="2025-01-01", date_released="2025-01-10")

    def test_add_personnel(self):
        """Тестирует метода __add__ (добавление персонала)."""
        self.garage + self.staff1
        self.assertIn(self.staff1, self.garage.personnel, "__add__ должен добавлять персонал в гараж.")

    def test_sub_personnel(self):
        """Тестирует метода __sub__ (удаление персонала)."""
        self.garage + self.staff1
        self.garage - self.staff1
        self.assertNotIn(self.staff1, self.garage.personnel, "__sub__ должен удалять персонал из гаража.")


if __name__ == "__main__":
    unittest.main()
