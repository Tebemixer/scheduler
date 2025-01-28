"""
Задания:
• свяжите разработанные классы исходя из логики и организации работы, согласно
варианта индивидуального задания;
• создайте декораторы и используйте их для методов своих классов:
◦ вывод времени выполнения метода;
◦ счётчик вызовов метода.

Route не может быть с кем-то связан по причине того, что маршрут обслуживает несколько водителей и несколько машин.
Класс Garage связан c Vehicle
"""
from datetime import datetime
import pickle
import time
from functools import wraps


def time_execution(func):
    """Декоратор для измерения времени выполнения метода."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Время выполнения {func.__name__}: {end_time - start_time:.6f} секунд")
        return result
    return wrapper


def count_calls(func):
    """Декоратор для подсчета вызовов метода."""
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        print(f"Метод {func.__name__} вызван {wrapper.calls} раз(а)")
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


_next_vehicle = 0
_next_route = 0
_next_driver = 0
_next_maintenancestaff = 0
_next_garage = 0


def _next_vehicle_number():
    """Генерирует следующий ID для Vehicle"""
    global _next_vehicle
    _next_vehicle += 1
    return _next_vehicle


def _next_route_number():
    """Генерирует следующий ID для Route"""
    global _next_route
    _next_route += 1
    return _next_route


def _next_driver_number():
    """Генерирует следующий ID для Driver"""
    global _next_driver
    _next_driver += 1
    return _next_driver


def _next_maintenancestaff_number():
    """Генерирует следующий ID для MaintenanceStaff"""
    global _next_maintenancestaff
    _next_maintenancestaff += 1
    return _next_maintenancestaff


def _next_garage_number():
    """Генерирует следующий ID для Garage"""
    global _next_garage
    _next_garage += 1
    return _next_garage


class Vehicle:
    """Класс Vehicle отражает характеристики автотранспорта"""
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

    @time_execution
    @count_calls
    def __get_info(self):
        """Возвращает словарь с ключами-атрибутами"""
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

    @time_execution
    @count_calls
    def __update_info(self, name, usage_hours, mileage, repairs_count, characteristics):
        """Производит переопределение всех атрибутов, а также записывает изменения в файл txt"""
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

    def __add__(self, value):
        """Увеличивает пробег"""
        self.mileage += value

    def __sub__(self, value):
        """Уменьшает пробег"""
        self.mileage -= value

    def __mul__(self, value):
        """Умножает пробег"""
        self.mileage *= value

    def __truediv__(self, value):
        """Делит пробег"""
        self.mileage /= value


class Route:
    """Класс Route отражает описание маршрута"""
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
        """Возвращает словарь с ключами-атрибутами"""
        return {
            "Route Name": self.name,
            "Vehicle": self.vehicle,
            "Driver": self.driver,
            "Schedule": self.schedule,
            'id': self.id
        }

    def __str__(self):
        return str(self.__get_info())[1:-1]

    @time_execution
    @count_calls
    def __update_info(self, name, vehicle, driver, schedule):
        """Производит переопределение всех атрибутов, а также записывает изменения в файл txt"""
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

    def __add__(self, value):
        """Добавляет к маршруту водителя"""
        if isinstance(value, Driver):
            self.driver.append(value)

    def __sub__(self, value):
        """Убирает водителя с маршрута"""
        if isinstance(value, Driver):
            self.driver.remove(value)


class Person:
    """Класс Person является предком Driver и MaintenanceStaff. Создан для сокращения кода ввиду одинаковых полей у
    этих двух классов. НЕ ПРЕДНАЗНАЧЕН ДЛЯ ИСПОЛЬЗОВАНИЯ"""
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

    @time_execution
    @count_calls
    # ИНАЧЕ НЕ УНАСЛЕДУЮЕТСЯ
    def get_info(self):
        """Возвращает словарь с ключами-атрибутами"""
        return {
            "Name": f"{self.last_name} {self.first_name} {self.middle_name}",
            "Birth Year": self.birth_year,
            "Gender": self.gender,
            "Address": self.address,
            "City": self.city,
            "Phone": self.phone,
        }

    @time_execution
    @count_calls
    # ИНАЧЕ НЕ УНАСЛЕДУЮЕТСЯ
    def update_info(self, last_name, first_name, middle_name, birth_year, gender,
                    address, city, phone):
        """Производит переопределение всех атрибутов"""
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

    def __add__(self, value):
        """Увеличивает год рождения"""
        self.birth_year += value

    def __sub__(self, value):
        """Уменьшает год рождения"""
        self.birth_year -= value

    def __mul__(self, value):
        """Умножает год рождения"""
        self.birth_year *= value

    def __truediv__(self, value):
        """Делит год рождения"""
        self.birth_year /= value


class Driver(Person):
    """Класс Driver отражает характеристики водителя"""
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

    @time_execution
    @count_calls
    def __get_info(self):
        """Возвращает словарь с ключами-атрибутами"""
        info = super(Driver, self).get_info()
        info["Start Year"] = self.start_year
        info["Experience"] = self.experience
        info["Position"] = self.position
        info["id"] = self.id
        return info

    def __str__(self):
        return str(self.get_info())[1:-1]

    @time_execution
    @count_calls
    def __update_info(self, last_name, first_name, middle_name, birth_year, gender, address, city, phone, start_year,
                      experience, position):
        """Производит переопределение всех атрибутов, а также записывает изменения в файл txt"""
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

    def __add__(self, value):
        """Увеличивает опыт работы"""
        self.experience += value

    def __sub__(self, value):
        """Уменьшает опыт работы"""
        self.experience -= value

    def __mul__(self, value):
        """Умножает опыт работы"""
        self.experience *= value

    def __truediv__(self, value):
        """Делит опыт работы"""
        self.experience /= value


class MaintenanceStaff(Person):
    """Класс MaintenanceStaff отражает описание обслуживающего персонала"""
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

    @time_execution
    @count_calls
    def __get_info(self):
        """Возвращает словарь с ключами-атрибутами"""
        info = super(MaintenanceStaff, self).get_info()
        info["Start Year"] = self.start_year
        info["Experience"] = self.experience
        info["Position"] = self.position
        info["id"] = self.id
        return info

    def __str__(self):
        return str(self.get_info())[1:-1]

    @time_execution
    @count_calls
    def __update_info(self, last_name, first_name, middle_name, birth_year, gender, address, city, phone, start_year,
                      experience, position):
        """Производит переопределение всех атрибутов, а также записывает изменения в файл txt"""
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

    def __add__(self, value):
        """Увеличивает опыт работы"""
        self.experience += value

    def __sub__(self, value):
        """Уменьшает опыт работы"""
        self.experience -= value

    def __mul__(self, value):
        """Умножает опыт работы"""
        self.experience *= value

    def __truediv__(self, value):
        """Делит опыт работы"""
        self.experience /= value


@time_execution
@count_calls
class Garage:
    """Класс Garage отражает описание гаражного хозяйства"""
    def __init__(self, name, vehicle, repair_type, date_received, date_released, repair_result='', personnel=[]):
        self.__name = name
        self.__repair_type = repair_type
        self.__date_received = date_received
        self.__date_released = date_released
        self.__repair_result = repair_result
        self.__personnel = personnel
        self.__id = _next_garage_number()
        self.__change_history = []
        if isinstance(vehicle, Vehicle):
            self.__vehicle = vehicle
        else:
            self.__vehicle = Vehicle(vehicle["Name"], vehicle["Usage Hours"], vehicle["Mileage"], vehicle["Repairs "
                                                                                                          "Count"],
                                     vehicle["Characteristics"])

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

    @time_execution
    @count_calls
    def __get_info(self):
        """Возвращает словарь с ключами-атрибутами"""
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

    @time_execution
    @count_calls
    def __update_info(self, name, vehicle, repair_type, date_received, date_released, repair_result, personnel):
        """Производит переопределение всех атрибутов, а также записывает изменения в файл txt"""
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

    def __add__(self, value):
        """Добавляет к гаражному хозяйству обслуживающий персонал"""
        if isinstance(value, MaintenanceStaff):
            self.personnel.append(value)

    def __sub__(self, value):
        """Удаляет с гаражного хозяйства обслуживающий персонал"""
        if isinstance(value, MaintenanceStaff):
            self.personnel.remove(value)


class PersistenceClass:
    @staticmethod
    def serialize(something):
        """Сериализиует объект, называя файл (имя класса)_(id объекта).pkl"""
        with open('{0}_{1}.pkl'.format(type(something).__name__, something.id), 'wb') as f:
            pickle.dump(something, f)

    @staticmethod
    def deserialize(file_name):
        """Десериализирует объект по файлу вида (имя класса)_(id объекта).pkl"""
        with open(file_name, 'rb') as f:
            something = pickle.load(f)
            return something


class InvalidPhoneError(Exception):
    """Описывает ошибку некорректного номера телефона"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Invalid phone {0}, only digits are allowed'.format(self.value)


class InvalidExperienceError(Exception):
    """Описывает ошибку некорректного опыта работы"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if isinstance(self.value, int) and self.value < 0:
            return 'Invalid experience value {0}<0'.format(self.value)
        else:
            return 'Invalid experience value {0}, must be int'.format(self.value)


vehicle = Vehicle("Bus", 1200, 50000, 3, "Diesel engine, 50 seats")
vehicle._Vehicle__get_info()
vehicle1 = Vehicle("Truck", 600, 32, 1, "Mad Max loves it")
vehicle1._Vehicle__get_info()
