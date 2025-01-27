import unittest
from lab.fifth import Driver, MaintenanceStaff, InvalidPhoneError, InvalidExperienceError
import lab.fifth


class TestCustomExceptions(unittest.TestCase):
    def setUp(self):
        self.driver = Driver(
                last_name="Doe",
                first_name="Jane",
                middle_name="Smith",
                birth_year=1985,
                start_year=2010,
                experience=12,
                position="Driver",
                gender="Female",
                phone='12345'
            )
        self.staff = MaintenanceStaff("Technician", "Petrov", "Petr", "Petrovich", 1985, 2010, 15,
                                      "Male", "Street 456", "Saint-Petersburg", "+987654321")

    def tearDown(self):
        lab.fifth._next_driver = 0
        lab.fifth._next_maintenancestaff = 0

    def test_invalid_phone_error_driver(self):
        """Тестирует, что InvalidPhoneError возникает при некорректном номере телефона у Driver."""
        with self.assertRaises(InvalidPhoneError) as context:
            self.driver.phone = 'Invalidphone123'
        self.assertIn("Invalid phone", str(context.exception))

    def test_invalid_phone_error_maintenancestaff(self):
        """Тестирует, что InvalidPhoneError возникает при некорректном номере телефона у MaintenanceStaff."""
        with self.assertRaises(InvalidPhoneError) as context:
            self.staff.phone = 'Invalidphone+123'
        self.assertIn("Invalid phone", str(context.exception))

    def test_invalid_experience_error_negative_driver(self):
        """Тестирует, что InvalidExperienceError возникает при отрицательном опыте у Driver."""
        with self.assertRaises(InvalidExperienceError) as context:
            self.driver.experience = -5
        self.assertIn("Invalid experience value", str(context.exception))
        self.assertIn("<0", str(context.exception))

    def test_invalid_experience_error_negative_maintenancestaff(self):
        """Тестирует, что InvalidExperienceError возникает при отрицательном опыте у MaintenanceStaff."""
        with self.assertRaises(InvalidExperienceError) as context:
            self.staff.experience = -5
        self.assertIn("Invalid experience value", str(context.exception))
        self.assertIn("<0", str(context.exception))

    def test_invalid_experience_error_non_int_driver(self):
        """Тестирует, что InvalidExperienceError возникает при некорректном типе опыта у Driver."""
        with self.assertRaises(InvalidExperienceError) as context:
            self.driver.experience = "FiveYears"
        self.assertIn("Invalid experience value", str(context.exception))
        self.assertIn("must be int", str(context.exception))

    def test_invalid_experience_error_non_int_maintenancestaff(self):
        """Тестирует, что InvalidExperienceError возникает при некорректном типе опыта у MaintenanceStaff."""
        with self.assertRaises(InvalidExperienceError) as context:
            self.staff.experience = "FiveYears"
        self.assertIn("Invalid experience value", str(context.exception))
        self.assertIn("must be int", str(context.exception))


if __name__ == "__main__":
    unittest.main()
