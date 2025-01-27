"""
преобразуйте атрибуты и методы своих классов, согласно варианта индивидуального
работы, в приватные для предотвращения переопределения;
• используйте в разработанных классах свойства для предоставления доступа к
атрибутам;
• создайте не менее двух собственных классов исключений с атрибутами и примените
их в своих классах, согласно варианта индивидуальной работы, генерируя
исключения;
• используйте unittest для проверки, что в коде происходит генерация исключений
(assertRaises).

ВВЕДЕНЫ КЛАССЫ InvalidPhoneError InvalidExperienceError
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
        self.__name = name
        self.__usage_hours = usage_hours
        self.__mileage = mileage
        self.__repairs_count = repairs_count
        self.__characteristics = characteristics
        self.__id = _next_vehicle_number()
        self.__change_history = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def usage_hours(self):
        return self.__usage_hours

    @usage_hours.setter
    def usage_hours(self, value):
        self.__usage_hours = value

    @property
    def mileage(self):
        return self.__mileage

    @mileage.setter
    def mileage(self, value):
        self.__mileage = value

    @property
    def repairs_count(self):
        return self.__repairs_count

    @repairs_count.setter
    def repairs_count(self, value):
        self.__repairs_count = value

    @property
    def characteristics(self):
        return self.__characteristics

    @characteristics.setter
    def characteristics(self, value):
        self.__characteristics = value

    @property
    def id(self):
        return self.__id

    @property
    def change_history(self):
        return self.__change_history

    def __get_info(self):
        return {
            "Name": self.name,
            "Usage Hours": self.usage_hours,
            "Mileage": self.mileage,
            "Repairs Count": self.repairs_count,
            "Characteristics": self.characteristics,
            'id': self.id
        }

    def __str__(self):
        return str(self.__get_info())[1:-1]  # Воспользуемся тем, что у dict есть свой str

    def __update_info(self, name, usage_hours, mileage, repairs_count, characteristics):
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
        self.__name = name
        self.__vehicle = vehicle
        self.__driver = driver
        self.__schedule = schedule
        self.__id = _next_route_number()
        self.__change_history = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def vehicle(self):
        return self.__vehicle

    @vehicle.setter
    def vehicle(self, value):
        self.__vehicle = value

    @property
    def driver(self):
        return self.__driver

    @driver.setter
    def driver(self, value):
        self.__driver = value

    @property
    def schedule(self):
        return self.__schedule

    @schedule.setter
    def schedule(self, value):
        self.__schedule = value

    @property
    def id(self):
        return self.__id

    @property
    def change_history(self):
        return self.__change_history

    def __get_info(self):
        return {
            "Route Name": self.name,
            "Vehicle": self.vehicle,
            "Driver": self.driver,
            "Schedule": self.schedule,
            'id': self.id
        }

    def __str__(self):
        return str(self.__get_info())[1:-1]

    def __update_info(self, name, vehicle, driver, schedule):
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
        self.__last_name = last_name
        self.__first_name = first_name
        self.__middle_name = middle_name
        self.__birth_year = birth_year
        self.__gender = gender
        self.__address = address
        self.__city = city
        self.__phone = phone
        self.__change_history = []

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        self.__first_name = value

    @property
    def middle_name(self):
        return self.__middle_name

    @middle_name.setter
    def middle_name(self, value):
        self.__middle_name = value

    @property
    def birth_year(self):
        return self.__birth_year

    @birth_year.setter
    def birth_year(self, value):
        self.__birth_year = value

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, value):
        self.__gender = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, value):
        self.__city = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        flag = 0
        for x in value:
            if x not in '+()- 0123456789':
                flag = 1
                raise InvalidPhoneError(value)
        if flag == 0:
            self.__phone = value

    @property
    def change_history(self):
        return self.__change_history

    # ИНАЧЕ НЕ УНАСЛЕДУЮЕТСЯ
    def get_info(self):
        return {
            "Name": f"{self.last_name} {self.first_name} {self.middle_name}",
            "Birth Year": self.birth_year,
            "Gender": self.gender,
            "Address": self.address,
            "City": self.city,
            "Phone": self.phone,
        }

    # ИНАЧЕ НЕ УНАСЛЕДУЮЕТСЯ
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
        self.__start_year = start_year
        self.__experience = experience
        self.__position = position
        self.__id = _next_driver_number()

    @property
    def start_year(self):
        return self.__start_year

    @start_year.setter
    def start_year(self, value):
        self.__start_year = value

    @property
    def experience(self):
        return self.__experience

    @experience.setter
    def experience(self, value):
        if not isinstance(value, int) or value < 0:
            raise InvalidExperienceError(value)
        else:
            self.__experience = value

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    @property
    def id(self):
        return self.__id

    def __get_info(self):
        info = super(Driver, self).get_info()
        info["Start Year"] = self.start_year
        info["Experience"] = self.experience
        info["Position"] = self.position
        info["id"] = self.id
        return info

    def __str__(self):
        return str(self.get_info())[1:-1]

    def __update_info(self, last_name, first_name, middle_name, birth_year, gender, address, city, phone, start_year,
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
        self.__start_year = start_year
        self.__experience = experience
        self.__position = position
        self.__id = _next_maintenancestaff_number()

    @property
    def start_year(self):
        return self.__start_year

    @start_year.setter
    def start_year(self, value):
        self.__start_year = value

    @property
    def experience(self):
        return self.__experience

    @experience.setter
    def experience(self, value):
        if not isinstance(value, int) or value < 0:
            raise InvalidExperienceError(value)
        else:
            self.__experience = value

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    @property
    def id(self):
        return self.__id

    def __get_info(self):
        info = super(MaintenanceStaff, self).get_info()
        info["Start Year"] = self.start_year
        info["Experience"] = self.experience
        info["Position"] = self.position
        info["id"] = self.id
        return info

    def __str__(self):
        return str(self.get_info())[1:-1]

    def __update_info(self, last_name, first_name, middle_name, birth_year, gender, address, city, phone, start_year,
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
        self.__name = name
        self.__vehicle = vehicle
        self.__repair_type = repair_type
        self.__date_received = date_received
        self.__date_released = date_released
        self.__repair_result = repair_result
        self.__personnel = personnel
        self.__id = _next_garage_number()
        self.__change_history = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def vehicle(self):
        return self.__vehicle

    @vehicle.setter
    def vehicle(self, value):
        self.__vehicle = value

    @property
    def repair_type(self):
        return self.__repair_type

    @repair_type.setter
    def repair_type(self, value):
        self.__repair_type = value

    @property
    def date_received(self):
        return self.__date_received

    @date_received.setter
    def date_received(self, value):
        self.__date_received = value

    @property
    def date_released(self):
        return self.__date_released

    @date_released.setter
    def date_released(self, value):
        self.__date_released = value

    @property
    def repair_result(self):
        return self.__repair_result

    @repair_result.setter
    def repair_result(self, value):
        self.__repair_result = value

    @property
    def personnel(self):
        return self.__personnel

    @personnel.setter
    def personnel(self, value):
        self.__personnel = value

    @property
    def id(self):
        return self.__id

    @property
    def change_history(self):
        return self.__change_history

    def __get_info(self):
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
        return str(self.__get_info())[1:-1]

    def __update_info(self, name, vehicle, repair_type, date_received, date_released, repair_result, personnel):
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


class InvalidPhoneError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Invalid phone {0}, only digits are allowed'.format(self.value)


class InvalidExperienceError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if isinstance(self.value, int) and self.value <0:
            return 'Invalid experience value {0}<0'.format(self.value)
        else:
            return 'Invalid experience value {0}, must be int'.format(self.value)


driver = Driver("Ivanov", "Ivan", "Ivanovich", 1980, 2005, 20,
                "Bus driver", "Male", "Street 123", "Moscow", "+123456789")
driver.experience = 5
