"""
Задания:
• составьте классы, согласно своего варианта индивидуального задания, с
необходимыми атрибутами для хранения значений;
• добавьте методы в классы для получения данных из атрибутов и устанавливающих
значения в них;
• используя конструкцию if __name__ == '__main__': проверьте корректность работы с
составленными классами.
"""


class Vehicle:
    def __init__(self, name, usage_hours, mileage, repairs_count, characteristics):
        self.name = name
        self.usage_hours = usage_hours
        self.mileage = mileage
        self.repairs_count = repairs_count
        self.characteristics = characteristics

    def get_info(self):
        return {
            "Name": self.name,
            "Usage Hours": self.usage_hours,
            "Mileage": self.mileage,
            "Repairs Count": self.repairs_count,
            "Characteristics": self.characteristics,
        }

    def update_info(self, name, usage_hours, mileage, repairs_count, characteristics):
        self.name = name
        self.usage_hours = usage_hours
        self.mileage = mileage
        self.repairs_count = repairs_count
        self.characteristics = characteristics


class Route:
    def __init__(self, name, vehicle, driver, schedule):
        self.name = name
        self.vehicle = vehicle
        self.driver = driver
        self.schedule = schedule

    def get_info(self):
        return {
            "Route Name": self.name,
            "Vehicle": self.vehicle,
            "Driver": self.driver,
            "Schedule": self.schedule,
        }

    def update_info(self, name, vehicle, driver, schedule):
        self.name = name
        self.vehicle = vehicle
        self.driver = driver
        self.schedule = schedule


class Driver:
    def __init__(self, last_name, first_name, middle_name, birth_year, start_year, experience, position, gender, address, city, phone):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.birth_year = birth_year
        self.start_year = start_year
        self.experience = experience
        self.position = position
        self.gender = gender
        self.address = address
        self.city = city
        self.phone = phone

    def get_info(self):
        return {
            "Name": f"{self.last_name} {self.first_name} {self.middle_name}",
            "Birth Year": self.birth_year,
            "Start Year": self.start_year,
            "Experience": self.experience,
            "Position": self.position,
            "Gender": self.gender,
            "Address": self.address,
            "City": self.city,
            "Phone": self.phone,
        }

    def update_info(self, last_name, first_name, middle_name, birth_year, start_year, experience, position, gender, address, city, phone):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.birth_year = birth_year
        self.start_year = start_year
        self.experience = experience
        self.position = position
        self.gender = gender
        self.address = address
        self.city = city
        self.phone = phone


class MaintenanceStaff:
    def __init__(self, position, last_name, first_name, middle_name, birth_year, start_year, experience, gender, address, city, phone):
        self.position = position
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.birth_year = birth_year
        self.start_year = start_year
        self.experience = experience
        self.gender = gender
        self.address = address
        self.city = city
        self.phone = phone

    def get_info(self):
        return {
            "Position": self.position,
            "Name": f"{self.last_name} {self.first_name} {self.middle_name}",
            "Birth Year": self.birth_year,
            "Start Year": self.start_year,
            "Experience": self.experience,
            "Gender": self.gender,
            "Address": self.address,
            "City": self.city,
            "Phone": self.phone,
        }

    def update_info(self, position, last_name, first_name, middle_name, birth_year,
                    start_year, experience, gender, address, city, phone):
        self.position = position
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.birth_year = birth_year
        self.start_year = start_year
        self.experience = experience
        self.gender = gender
        self.address = address
        self.city = city
        self.phone = phone


class Garage:
    def __init__(self, name, vehicle, repair_type, date_received, date_released, repair_result, personnel):
        self.name = name
        self.vehicle = vehicle
        self.repair_type = repair_type
        self.date_received = date_received
        self.date_released = date_released
        self.repair_result = repair_result
        self.personnel = personnel

    def get_info(self):
        return {
            "Garage Name": self.name,
            "Vehicle": self.vehicle,
            "Repair Type": self.repair_type,
            "Date Received": self.date_received,
            "Date Released": self.date_released,
            "Repair Result": self.repair_result,
            "Personnel": self.personnel,
        }

    def update_info(self, name, vehicle, repair_type, date_received, date_released, repair_result, personnel):
        self.name = name
        self.vehicle = vehicle
        self.repair_type = repair_type
        self.date_received = date_received
        self.date_released = date_released
        self.repair_result = repair_result
        self.personnel = personnel


if __name__ == '__main__':
    vehicle = Vehicle("Bus", 1200, 50000, 3, "Diesel engine, 50 seats")
    driver = Driver("Ivanov", "Ivan", "Ivanovich", 1980, 2005, 20,
                    "Bus driver", "Male", "Street 123", "Moscow", "+123456789")

    route = Route("Route 42", vehicle.get_info(), driver.get_info(), "8:00 - 20:00")

    staff1 = MaintenanceStaff("Technician", "Petrov", "Petr", "Petrovich", 1985, 2010, 15,
                              "Male", "Street 456", "Saint-Petersburg", "+987654321")

    garage = Garage("Main Garage", vehicle.get_info(), "Engine repair",
                    "2025-01-10", "2025-01-15", "Successful", [staff1])

    print("Vehicle Info:", vehicle.get_info())
    print("Driver Info:", driver.get_info())
    print("Route Info:", route.get_info())
    print("Garage Info:", garage.get_info())

    driver.update_info("Ivanov", "Ivan", "Ivanovich", 1980, 2005, 25,
                       "Bus driver", "Male", "Street 123", "Moscow", "+88005553535")
    print("New Driver Info:", driver.get_info())
