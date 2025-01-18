"""
Задания:
• используйте при описании конструкторов значения по умолчанию;
• добавьте в описание класса метод __str__() для строкового представления значений
атрибутов экземпляра класса;
• используйте генерацию идентификаторов для классов, согласно индивидуального
задания;
• разработайте тесты для проведения модульного тестирования созданных методов в
этой работе: конструкторов по умолчанию, строкового представления значений и
генерации идентификаторов.
"""
_next_vehicle = 0
_next_route = 0
_next_driver = 0
_next_maintenancestaff = 0
_next_garage = 0


def _next_vehicle_number():
    global _next_vehicle
    _next_vehicle += 1
    return _next_vehicle


def _next_route_number():
    global _next_route
    _next_route += 1
    return _next_route


def _next_driver_number():
    global _next_driver
    _next_driver += 1
    return _next_driver


def _next_maintenancestaff_number():
    global _next_maintenancestaff
    _next_maintenancestaff += 1
    return _next_maintenancestaff


def _next_garage_number():
    global _next_garage
    _next_garage += 1
    return _next_garage


class Vehicle:
    def __init__(self, name, usage_hours=0, mileage=0, repairs_count=0, characteristics=''):
        self.name = name
        self.usage_hours = usage_hours
        self.mileage = mileage
        self.repairs_count = repairs_count
        self.characteristics = characteristics
        self.id = _next_vehicle_number()

    def get_info(self):
        return {
            "Name": self.name,
            "Usage Hours": self.usage_hours,
            "Mileage": self.mileage,
            "Repairs Count": self.repairs_count,
            "Characteristics": self.characteristics,
            'id': self.id
        }

    def __str__(self):
        return str(self.get_info())[1:-1]  # Воспользуемся тем, что у dict есть свой str

    def update_info(self, name, usage_hours, mileage, repairs_count, characteristics):
        self.name = name
        self.usage_hours = usage_hours
        self.mileage = mileage
        self.repairs_count = repairs_count
        self.characteristics = characteristics


class Route:
    def __init__(self, name, vehicle, driver, schedule=''):
        self.name = name
        self.vehicle = vehicle
        self.driver = driver
        self.schedule = schedule
        self.id = _next_route_number()
    def get_info(self):
        return {
            "Route Name": self.name,
            "Vehicle": self.vehicle,
            "Driver": self.driver,
            "Schedule": self.schedule,
            'id': self.id
        }

    def __str__(self):
        return str(self.get_info())[1:-1]

    def update_info(self, name, vehicle, driver, schedule):
        self.name = name
        self.vehicle = vehicle
        self.driver = driver
        self.schedule = schedule


class Driver:
    def __init__(self, last_name, first_name, middle_name, birth_year, start_year, experience, position, gender,
                 address='', city='', phone=''):
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
        self.id = _next_driver_number()

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
            'id': self.id
        }

    def __str__(self):
        return str(self.get_info())[1:-1]

    def update_info(self, last_name, first_name, middle_name, birth_year, start_year, experience, position, gender,
                    address, city, phone):
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
    def __init__(self, position, last_name, first_name, middle_name, birth_year, start_year, experience, gender,
                 address='', city='', phone=''):
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
        self.id = _next_maintenancestaff_number()

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
            'id': self.id
        }

    def __str__(self):
        return str(self.get_info())[1:-1]

    def update_info(self, position, last_name, first_name, middle_name, birth_year, start_year, experience, gender,
                    address, city, phone):
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
    def __init__(self, name, vehicle, repair_type, date_received, date_released, repair_result='', personnel=[]):
        self.name = name
        self.vehicle = vehicle
        self.repair_type = repair_type
        self.date_received = date_received
        self.date_released = date_released
        self.repair_result = repair_result
        self.personnel = personnel
        self.id = _next_garage_number()

    def get_info(self):
        return {
            "Garage Name": self.name,
            "Vehicle": self.vehicle,
            "Repair Type": self.repair_type,
            "Date Received": self.date_received,
            "Date Released": self.date_released,
            "Repair Result": self.repair_result,
            "Personnel": self.personnel,
            'id': self.id
        }

    def __str__(self):
        return str(self.get_info())[1:-1]

    def update_info(self, name, vehicle, repair_type, date_received, date_released, repair_result, personnel):
        self.name = name
        self.vehicle = vehicle
        self.repair_type = repair_type
        self.date_received = date_received
        self.date_released = date_released
        self.repair_result = repair_result
        self.personnel = personnel

