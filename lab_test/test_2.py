import unittest
from lab.second import Vehicle, Driver, Route, Garage, MaintenanceStaff
import lab.second


class TestSecond(unittest.TestCase):
    # def setUp(self):
    #     self.staff = MaintenanceStaff("Technician", "Petrov", "Petr", "Petrovich", 1985, 2010, 15,
    #                                   "Male", "Street 456", "Saint-Petersburg", "+987654321")
    #     self.garage = Garage(name="Main Garage", vehicle=self.vehicle.id, repair_type="Engine Repair",
    #                          date_received="2025-01-10", date_released="2025-01-12", repair_result="Success",
    #                          personnel=[self.staff])

    def tearDown(self):
        lab.second._next_vehicle = 0
        lab.second._next_driver = 0
        lab.second._next_route = 0
        lab.second._next_garage = 0
        lab.second._next_maintenancestaff = 0

    def test_vehicle_creation_default(self):
        # Отсутствуют ключи repairs count и characteristics
        self.vehicle = Vehicle(name="Bus", usage_hours=10, mileage=500)
        self.assertEqual(self.vehicle.name, "Bus")
        self.assertEqual(self.vehicle.usage_hours, 10)
        self.assertEqual(self.vehicle.mileage, 500)
        self.assertEqual(self.vehicle.repairs_count, 0)
        self.assertEqual(self.vehicle.characteristics, "")
        self.assertEqual(self.vehicle.id, 1)

    def test_vehicle_str(self):
        self.vehicle = Vehicle(name="Bus", usage_hours=10, mileage=500, repairs_count=2, characteristics="Large")
        self.assertIn("Bus", str(self.vehicle))
        self.assertIn("10", str(self.vehicle))
        self.assertIn("500", str(self.vehicle))
        self.assertIn("2", str(self.vehicle))
        self.assertIn("Large", str(self.vehicle))
        self.assertIn("'id': 1", str(self.vehicle))

    def test_vehicle_id_generator(self):
        self.vehicle1 = Vehicle(name="Bus")
        self.vehicle2 = Vehicle(name="Bike")
        self.assertEqual(self.vehicle1.id, 1)
        self.assertEqual(self.vehicle2.id, 2)

    def test_driver_creation_default(self):
        # Отсутствуют ключи city, address, phone
        self.driver = Driver(last_name="Doe", first_name="John", middle_name="M", birth_year=1985, start_year=2010,
                             experience=10, position="Driver", gender="Male")
        self.assertEqual(self.driver.last_name, "Doe")
        self.assertEqual(self.driver.first_name, "John")
        self.assertEqual(self.driver.middle_name, "M")
        self.assertEqual(self.driver.birth_year, 1985)
        self.assertEqual(self.driver.start_year, 2010)
        self.assertEqual(self.driver.experience, 10)
        self.assertEqual(self.driver.position, "Driver")
        self.assertEqual(self.driver.gender, "Male")
        self.assertEqual(self.driver.address, "")
        self.assertEqual(self.driver.city, "")
        self.assertEqual(self.driver.phone, "")
        self.assertEqual(self.driver.id, 1)

    def test_driver_str(self):
        self.driver = Driver(last_name="Doe", first_name="John", middle_name="M", birth_year=1985, start_year=2010,
                             experience=10, position="Driver", gender="Male")
        self.assertIn("Doe John M", str(self.driver))
        self.assertIn("1985", str(self.driver))
        self.assertIn("10", str(self.driver))
        self.assertIn("Driver", str(self.driver))
        self.assertIn("Male", str(self.driver))
        self.assertIn("'id': 1", str(self.driver))

    def test_driver_id_generator(self):
        self.driver1 = Driver(last_name="Doe", first_name="John", middle_name="M", birth_year=1985, start_year=2010,
                              experience=10, position="Driver", gender="Male")
        self.driver2 = Driver(last_name="Joe", first_name="Ivan", middle_name="O", birth_year=1925, start_year=1980,
                              experience=100, position="High Driver", gender="Male")
        self.assertEqual(self.driver1.id, 1)
        self.assertEqual(self.driver2.id, 2)

    def test_route_creation(self):
        # Отсутствует ключ schedule
        self.vehicle = Vehicle(name="Bus", usage_hours=10, mileage=500, repairs_count=2, characteristics="Large")
        self.driver = Driver(last_name="Doe", first_name="John", middle_name="M", birth_year=1985, start_year=2010,
                             experience=10, position="Driver", gender="Male")
        self.route = Route(name="Route 1", vehicle=self.vehicle.id, driver=self.driver.id)
        self.assertEqual(self.route.name, "Route 1")
        self.assertEqual(self.route.vehicle, 1)
        self.assertEqual(self.route.driver, 1)
        self.assertEqual(self.route.schedule, "")
        self.assertEqual(self.route.id, 1)

    def test_route_str(self):
        self.vehicle = Vehicle(name="Bus", usage_hours=10, mileage=500, repairs_count=2, characteristics="Large")
        self.driver = Driver(last_name="Doe", first_name="John", middle_name="M", birth_year=1985, start_year=2010,
                             experience=10, position="Driver", gender="Male")
        self.route = Route(name="Route 1", vehicle=self.vehicle.id, driver=self.driver.id, schedule="8:00 AM - 5:00 PM")
        self.assertIn("Route 1", str(self.route))
        self.assertIn("8:00 AM - 5:00 PM", str(self.route))
        self.assertIn("1", str(self.route))

    def test_route_id_generator(self):
        self.vehicle = Vehicle(name="Bus", usage_hours=10, mileage=500, repairs_count=2, characteristics="Large")
        self.driver = Driver(last_name="Doe", first_name="John", middle_name="M", birth_year=1985, start_year=2010,
                             experience=10, position="Driver", gender="Male")
        self.route1 = Route(name="Route 1", vehicle=self.vehicle.id, driver=self.driver.id)
        self.route2 = Route(name="Route 1", vehicle=self.vehicle.id, driver=self.driver.id)
        self.assertEqual(self.route1.id, 1)
        self.assertEqual(self.route2.id, 2)

    def test_garage_creation_default(self):
        # Отсутствует ключ repair_result и personnel
        self.vehicle = Vehicle(name="Bus", usage_hours=10, mileage=500, repairs_count=2, characteristics="Large")
        self.garage = Garage(name="Main Garage", vehicle=self.vehicle.id, repair_type="Engine Repair",
                             date_received="2025-01-10", date_released="2025-01-12")
        self.assertEqual(self.garage.name, "Main Garage")
        self.assertEqual(self.garage.vehicle, 1)
        self.assertEqual(self.garage.repair_type, "Engine Repair")
        self.assertEqual(self.garage.date_received, "2025-01-10")
        self.assertEqual(self.garage.date_released, "2025-01-12")
        self.assertEqual(self.garage.repair_result, "")
        self.assertEqual(self.garage.personnel, [])
        self.assertEqual(self.garage.id, 1)

    def test_garage_str(self):
        self.vehicle = Vehicle(name="Bus", usage_hours=10, mileage=500, repairs_count=2, characteristics="Large")
        self.garage = Garage(name="Main Garage", vehicle=self.vehicle.id, repair_type="Engine Repair",
                             date_received="2025-01-10", date_released="2025-01-12", repair_result="Success")
        self.assertIn("Main Garage", str(self.garage))
        self.assertIn("Engine Repair", str(self.garage))
        self.assertIn("2025-01-10", str(self.garage))
        self.assertIn("2025-01-12", str(self.garage))
        self.assertIn("Success", str(self.garage))
        self.assertIn("1", str(self.garage))

    def test_garage_id_generator(self):
        self.vehicle = Vehicle(name="Bus", usage_hours=10, mileage=500, repairs_count=2, characteristics="Large")
        self.garage1 = Garage(name="Main Garage", vehicle=self.vehicle.id, repair_type="Engine Repair",
                              date_received="2025-01-10", date_released="2025-01-12", repair_result="Success")
        self.garage2 = Garage(name="Second Garage", vehicle=self.vehicle.id, repair_type="Engine Repair",
                              date_received="2025-01-10", date_released="2025-01-12", repair_result="Success")
        self.assertEqual(self.garage1.id, 1)
        self.assertEqual(self.garage2.id, 2)

    def test_maintenance_staff_creation_default(self):
        # Отсутствуют ключи city, address, phone
        self.staff = MaintenanceStaff(position="Mechanic", last_name="Smith", first_name="Alice", middle_name="K",
                                 birth_year=1990, start_year=2015, experience=8, gender="Female")
        self.assertEqual(self.staff.position, "Mechanic")
        self.assertEqual(self.staff.last_name, "Smith")
        self.assertEqual(self.staff.first_name, "Alice")
        self.assertEqual(self.staff.middle_name, "K")
        self.assertEqual(self.staff.birth_year, 1990)
        self.assertEqual(self.staff.start_year, 2015)
        self.assertEqual(self.staff.experience, 8)
        self.assertEqual(self.staff.gender, "Female")
        self.assertEqual(self.staff.address, "")
        self.assertEqual(self.staff.city, "")
        self.assertEqual(self.staff.phone, "")
        self.assertEqual(self.staff.id, 1)

    def test_maintenance_staff_str(self):
        self.staff = MaintenanceStaff(position="Mechanic", last_name="Smith", first_name="Alice", middle_name="K",
                                 birth_year=1990, start_year=2015, experience=8, gender="Female",
                                 address="123 Main St", city="Springfield", phone="555-1234")
        self.assertIn("Mechanic", str(self.staff))
        self.assertIn("Smith Alice K", str(self.staff))
        self.assertIn("1990", str(self.staff))
        self.assertIn("2015", str(self.staff))
        self.assertIn("8", str(self.staff))
        self.assertIn("Female", str(self.staff))
        self.assertIn("123 Main St", str(self.staff))
        self.assertIn("Springfield", str(self.staff))
        self.assertIn("555-1234", str(self.staff))
        self.assertIn("'id': 1", str(self.staff))

    def test_maintenance_staff_id_generator(self):
        self.staff1 = MaintenanceStaff(position="Mechanic", last_name="Smith", first_name="Alice", middle_name="K",
                                      birth_year=1990, start_year=2015, experience=8, gender="Female",
                                      address="123 Main St", city="Springfield", phone="555-1234")
        self.staff2 = MaintenanceStaff(position="High Mechanic", last_name="Biden", first_name="Joe", middle_name="Y",
                                       birth_year=1995, start_year=2025, experience=0, gender="Male",
                                       address="126 Main St", city="Springfield", phone="555-145")
        self.assertEqual(self.staff1.id, 1)
        self.assertEqual(self.staff2.id, 2)


if __name__ == "__main__":
    unittest.main()
