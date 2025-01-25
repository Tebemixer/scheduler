import unittest
from lab.fourth import Driver, MaintenanceStaff
import lab.fourth
from unittest.mock import patch, mock_open


class TestPersonClasses(unittest.TestCase):
    def setUp(self):
        self.driver = Driver(
            last_name="Smith",
            first_name="John",
            middle_name="A.",
            birth_year=1985,
            start_year=2010,
            experience=13,
            position="Truck Driver",
            gender="Male",
            address="123 Main St",
            city="New York",
            phone="123-456-7890"
        )

        self.maintenance_staff = MaintenanceStaff(
            last_name="Doe",
            first_name="Jane",
            middle_name="B.",
            birth_year=1990,
            start_year=2015,
            experience=8,
            position="Technician",
            gender="Female",
            address="456 Elm St",
            city="San Francisco",
            phone="987-654-3210"
        )

    def tearDown(self):
        lab.fourth._next_driver = 0
        lab.fourth._next_maintenancestaff = 0

    def test_driver_creation(self):

        self.assertEqual(self.driver.last_name, "Smith")
        self.assertEqual(self.driver.first_name, "John")
        self.assertEqual(self.driver.position, "Truck Driver")
        self.assertEqual(self.driver.experience, 13)
        self.assertEqual(self.driver.gender, 'Male')
        self.assertEqual(self.driver.start_year, 2010)
        self.assertEqual(self.driver.id, 1)

    def test_maintenance_staff_creation(self):
        self.assertEqual(self.maintenance_staff.last_name, "Doe")
        self.assertEqual(self.maintenance_staff.first_name, "Jane")
        self.assertEqual(self.maintenance_staff.position, "Technician")
        self.assertEqual(self.maintenance_staff.experience, 8)
        self.assertEqual(self.maintenance_staff.gender, 'Female')
        self.assertEqual(self.maintenance_staff.start_year, 2015)
        self.assertEqual(self.maintenance_staff.id, 1)

    def test_driver_get_info(self):
        info = self.driver.get_info()
        self.assertEqual(info["Name"], "Smith John A.")
        self.assertEqual(info["Position"], "Truck Driver")

    def test_maintenance_staff_get_info(self):
        info = self.maintenance_staff.get_info()
        self.assertEqual(info["Name"], "Doe Jane B.")
        self.assertEqual(info["Position"], "Technician")

    @patch("builtins.open", new_callable=mock_open)
    def test_driver_update_info(self, mock_file):
        self.driver.update_info(
            last_name="Brown",
            first_name="John",
            middle_name="A.",
            birth_year=1985,
            gender="Male",
            address="123 Main St",
            city="New York",
            phone="123-456-7890",
            start_year=2011,
            experience=14,
            position="Senior Truck Driver"
        )
        self.assertEqual(self.driver.last_name, "Brown")
        self.assertEqual(self.driver.position, "Senior Truck Driver")
        self.assertEqual(self.driver.experience, 14)

        mock_file.assert_called_once_with('history of change Driver.txt', 'a')
        mock_file().write.assert_called()

    @patch("builtins.open", new_callable=mock_open)
    def test_maintenance_staff_update_info(self, mock_file):
        self.maintenance_staff.update_info(
            last_name="Smith",
            first_name="Jane",
            middle_name="B.",
            birth_year=1990,
            gender="Female",
            address="789 Pine St",
            city="Los Angeles",
            phone="555-555-5555",
            start_year=2016,
            experience=9,
            position="Senior Technician"
        )
        self.assertEqual(self.maintenance_staff.last_name, "Smith")
        self.assertEqual(self.maintenance_staff.position, "Senior Technician")
        self.assertEqual(self.maintenance_staff.experience, 9)

        mock_file.assert_called_once_with('history of change MaintenanceStaff.txt', 'a')
        mock_file().write.assert_called()


if __name__ == "__main__":
    unittest.main()
