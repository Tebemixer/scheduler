"""
Задания:
• используйте в описание классов, согласно варианта индивидуального задания,
наследование — для этого определите для одного из классов-сущностей не менее двух
потомков, которые расширяют атрибуты-данные и атрибуты-методы родительского
класса;
• для использования полиморфизма в классах-потомках измените реализацию
отдельных унаследованных методов, отвечающих за изменение и считывание
значений из атрибутов классов;
• протестируйте с помощью unittest создание экземпляров классов-потомков,
использование добавленных в них новых методов, изменённых унаследованных
методов.

ВВЕДЕН КЛАСС Person, его потомки Driver и MaintenanceStaff
"""
from datetime import datetime
import pickle

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
        self.change_history = []

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
        r = '{0};{1}:'.format(datetime.today(), self.id)
        if name != self.name:
            r += ' name:{0}->{1};'.format(self.name, name)
        self.name = name
        if usage_hours != self.usage_hours:
            r += ' usage_hours:{0}->{1};'.format(self.usage_hours, usage_hours)
        self.usage_hours = usage_hours
        if mileage != self.mileage:
            r += ' mileage:{0}->{1};'.format(self.mileage, mileage)
        self.mileage = mileage
        if repairs_count != self.repairs_count:
            r += ' repairs_count:{0}->{1};'.format(self.repairs_count, repairs_count)
        self.repairs_count = repairs_count
        if characteristics != self.characteristics:
            r += ' characteristics:{0}->{1};'.format(self.characteristics, characteristics)
        self.characteristics = characteristics
        if r[-1] != ':':
            self.change_history.append(r[:-1] + '\n')
            with open('history of change {0}.txt'.format(type(self).__name__), 'a') as f:
                f.write(r[:-1] + '\n')

    def __del__(self):
        self.change_history.clear()


class Route:
    def __init__(self, name, vehicle, driver, schedule=''):
        self.name = name
        self.vehicle = vehicle
        self.driver = driver
        self.schedule = schedule
        self.id = _next_route_number()
        self.change_history = []

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
        r = '{0};{1}:'.format(datetime.today(), self.id)
        if name != self.name:
            r += ' name:{0}->{1};'.format(self.name, name)
        self.name = name
        if vehicle != self.vehicle:
            r += ' vehicle:{0}->{1};'.format(self.vehicle, vehicle)
        self.vehicle = vehicle
        if driver != self.driver:
            r += ' driver:{0}->{1};'.format(self.driver, driver)
        self.driver = driver
        if schedule != self.schedule:
            r += ' schedule:{0}->{1};'.format(self.schedule, schedule)
        self.schedule = schedule
        if r[-1] != ':':
            self.change_history.append(r[:-1] + '\n')
            with open('history of change {0}.txt'.format(type(self).__name__), 'a') as f:
                f.write(r[:-1] + '\n')

    def __del__(self):
        self.change_history.clear()


class Person:
    def __init__(self, last_name, first_name, middle_name, birth_year, gender,
                 address='', city='', phone=''):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.birth_year = birth_year
        self.gender = gender
        self.address = address
        self.city = city
        self.phone = phone
        self.change_history = []

    def get_info(self):
        return {
            "Name": f"{self.last_name} {self.first_name} {self.middle_name}",
            "Birth Year": self.birth_year,
            "Gender": self.gender,
            "Address": self.address,
            "City": self.city,
            "Phone": self.phone,
        }

    def update_info(self, last_name, first_name, middle_name, birth_year, gender,
                    address, city, phone):
        r = '{0};{1}:'.format(datetime.today(), self.id)
        if last_name != self.last_name:
            r += ' last_name:{0}->{1};'.format(self.last_name, last_name)
        self.last_name = last_name
        if first_name != self.first_name:
            r += ' first_name:{0}->{1};'.format(self.first_name, first_name)
        self.first_name = first_name
        if middle_name != self.middle_name:
            r += ' middle_name:{0}->{1};'.format(self.middle_name, middle_name)
        self.middle_name = middle_name
        if birth_year != self.birth_year:
            r += ' birth_year:{0}->{1};'.format(self.birth_year, birth_year)
        self.birth_year = birth_year
        if gender != self.gender:
            r += ' gender:{0}->{1};'.format(self.gender, gender)
        self.gender = gender
        if address != self.address:
            r += ' address:{0}->{1};'.format(self.address, address)
        self.address = address
        if city != self.city:
            r += ' city:{0}->{1};'.format(self.city, city)
        self.city = city
        if phone != self.phone:
            r += ' phone:{0}->{1};'.format(self.phone, phone)
        self.phone = phone
        return r


class Driver(Person):
    def __init__(self, last_name, first_name, middle_name, birth_year, start_year, experience, position, gender,
                 address='', city='', phone=''):
        super(Driver, self).__init__(last_name, first_name, middle_name, birth_year, gender,
                                     address, city, phone)
        self.start_year = start_year
        self.experience = experience
        self.position = position
        self.id = _next_driver_number()

    def get_info(self):
        info = super(Driver, self).get_info()
        info["Start Year"] = self.start_year
        info["Experience"] = self.experience
        info["Position"] = self.position
        info["id"] = self.id
        return info

    def __str__(self):
        return str(self.get_info())[1:-1]

    def update_info(self, last_name, first_name, middle_name, birth_year, gender, address, city, phone, start_year,
                    experience, position):
        r = super(Driver, self).update_info(last_name, first_name, middle_name, birth_year, gender,
                                            address, city, phone)
        if start_year != self.start_year:
            r += ' start_year:{0}->{1};'.format(self.start_year, start_year)
        self.start_year = start_year
        if experience != self.experience:
            r += ' experience:{0}->{1};'.format(self.experience, experience)
        self.experience = experience
        if position != self.position:
            r += ' position:{0}->{1};'.format(self.position, position)
        self.position = position
        if r[-1] != ':':
            self.change_history.append(r[:-1] + '\n')
            with open('history of change {0}.txt'.format(type(self).__name__), 'a') as f:
                f.write(r[:-1] + '\n')

    def __del__(self):
        self.change_history.clear()


class MaintenanceStaff(Person):
    def __init__(self, last_name, first_name, middle_name, birth_year, start_year, experience, position, gender,
                 address='', city='', phone=''):
        super(MaintenanceStaff, self).__init__(last_name, first_name, middle_name, birth_year, gender,
                                               address, city, phone)
        self.start_year = start_year
        self.experience = experience
        self.position = position
        self.id = _next_maintenancestaff_number()

    def get_info(self):
        info = super(MaintenanceStaff, self).get_info()
        info["Start Year"] = self.start_year
        info["Experience"] = self.experience
        info["Position"] = self.position
        info["id"] = self.id
        return info

    def __str__(self):
        return str(self.get_info())[1:-1]

    def update_info(self, last_name, first_name, middle_name, birth_year, gender, address, city, phone, start_year,
                    experience, position):
        r = super(MaintenanceStaff, self).update_info(last_name, first_name, middle_name, birth_year, gender,
                                                      address, city, phone)
        if start_year != self.start_year:
            r += ' start_year:{0}->{1};'.format(self.start_year, start_year)
        self.start_year = start_year
        if experience != self.experience:
            r += ' experience:{0}->{1};'.format(self.experience, experience)
        self.experience = experience
        if position != self.position:
            r += ' position:{0}->{1};'.format(self.position, position)
        self.position = position
        if r[-1] != ':':
            self.change_history.append(r[:-1] + '\n')
            with open('history of change {0}.txt'.format(type(self).__name__), 'a') as f:
                f.write(r[:-1] + '\n')

    def __del__(self):
        self.change_history.clear()


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
        self.change_history = []

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
        r = '{0};{1}:'.format(datetime.today(), self.id)
        if name != self.name:
            r += ' name:{0}->{1};'.format(self.name, name)
        self.name = name
        if vehicle != self.vehicle:
            r += ' vehicle:{0}->{1};'.format(self.vehicle, vehicle)
        self.vehicle = vehicle
        if repair_type != self.repair_type:
            r += ' repair_type:{0}->{1};'.format(self.repair_type, repair_type)
        self.repair_type = repair_type
        if date_received != self.date_received:
            r += ' date_received:{0}->{1};'.format(self.date_received, date_received)
        self.date_received = date_received
        if date_released != self.date_released:
            r += ' date_released:{0}->{1};'.format(self.date_released, date_released)
        self.date_released = date_released
        if repair_result != self.repair_result:
            r += ' repair_result:{0}->{1};'.format(self.repair_result, repair_result)
        self.repair_result = repair_result
        if personnel != self.personnel:
            r += ' personnel:{0}->{1};'.format(self.personnel, personnel)
        self.personnel = personnel
        if r[-1] != ':':
            with open('history of change {0}.txt'.format(type(self).__name__), 'a') as f:
                f.write(r[:-1] + '\n')

    def __del__(self):
        self.change_history.clear()


class PersistenceClass:
    @staticmethod
    def serialize(something):
        with open('{0}_{1}.pkl'.format(type(something).__name__, something.id), 'wb') as f:
            pickle.dump(something, f)

    @staticmethod
    def deserialize(file_name):
        with open(file_name, 'rb') as f:
            something = pickle.load(f)
            return something
