"""
Задания:
• используйте агрегацию для манипулирования данными (добавление, изменение,
удаление и просмотр) основных классов сущностей, согласно варианта
индивидуального задания;
• разработайте консольное приложение, использующее интерактивный режим с
пользователем, по манипулированию данных основных классов сущностей;
• реализуйте функциональность, указанную в индивидуальном задании;
• протестируйте корректность выполнения действий по манипулированию данными и
выполнение требуемых функций с помощью unittest.


УБРАНЫ ДЕКОРАТОРЫ
ВВЕДЕН КЛАСС ClassBase
каждому классу дан публичный метод изменения атрибутов
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
        if isinstance(name, str) and ',' in name:
            # Разбиваем строку на части
            parts = name.split(',')
            if len(parts) < 4:  # Убедимся, что есть хотя бы 4 значения
                raise ValueError("Строка должна содержать не менее 4 полей, разделенных запятыми.")
            self.__name = parts[0].strip()
            self.__usage_hours = int(parts[1].strip())
            self.__mileage = int(parts[2].strip())
            self.__repairs_count = int(parts[3].strip())
            self.__characteristics = ','.join(parts[4:]).strip()
        else:
            # Стандартная инициализация, если переданы отдельные параметры
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
        """Возвращает словарь с ключами-атрибутами"""
        return {
            "Name": self.name,
            "Usage Hours": self.usage_hours,
            "Mileage": self.mileage,
            "Repairs Count": self.repairs_count,
            "Characteristics": self.characteristics,
            'id': self.id
        }

    def get_public_info(self):
        return self.__get_info()

    def update_public_info(self, row):
        row = row.split(',')
        self.__update_info(name=row[0], usage_hours=row[0], mileage=row[0], repairs_count=row[0],
                           characteristics=row[0])

    def __str__(self):
        return str(self.__get_info())[1:-1]  # Воспользуемся тем, что у dict есть свой str

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
        if isinstance(name, str) and ',' in name:
            parts = name.split(',')
            if len(parts) < 4:
                raise ValueError("Строка должна содержать не менее 4 полей: name, vehicle, driver, schedule.")

            self.__name = parts[0].strip()
            self.__vehicle = parts[1].strip()
            self.__driver = parts[2].strip()
            self.__schedule = parts[3].strip()
        else:
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

    def get_public_info(self):
        return self.__get_info()

    def __str__(self):
        return str(self.__get_info())[1:-1]

    def update_public_info(self, name, vehicle, driver, schedule):
        self.__update_info(name, vehicle, driver, schedule)

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
        if isinstance(last_name, str) and ',' in last_name:
            parts = last_name.split(',')
            if len(parts) < 5:
                raise ValueError(
                    "Строка должна содержать не менее 5 полей: last_name, first_name, middle_name, birth_year, gender.")

            self.__last_name = parts[0].strip()
            self.__first_name = parts[1].strip()
            self.__middle_name = parts[2].strip()
            self.__birth_year = int(parts[3].strip())
            self.__gender = parts[4].strip()
            self.__address = parts[5].strip() if len(parts) > 5 else ''
            self.__city = parts[6].strip() if len(parts) > 6 else ''
            self.__phone = parts[7].strip() if len(parts) > 7 else ''
        else:
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
        """Возвращает словарь с ключами-атрибутами"""
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

    def __init__(self, last_name, first_name=None, middle_name=None, birth_year=None, start_year=None,
                 experience=None, position=None, gender=None, address='', city='', phone=''):
        if isinstance(last_name, str) and ',' in last_name:
            parts = last_name.split(',')
            if len(parts) < 8:
                raise ValueError(
                    "Строка должна содержать не менее 8 полей: last_name, first_name, middle_name, birth_year, "
                    "start_year, experience, position, gender.")

            super().__init__(parts[0], parts[1], parts[2], int(parts[3]), parts[7],
                             address='', city='', phone='')
            self.__start_year = int(parts[4].strip())
            self.__experience = int(parts[5].strip())
            self.__position = parts[6].strip()
        else:
            super().__init__(last_name, first_name, middle_name, birth_year, gender,
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
        """Возвращает словарь с ключами-атрибутами"""
        info = super(Driver, self).get_info()
        info["Start Year"] = self.start_year
        info["Experience"] = self.experience
        info["Position"] = self.position
        info["id"] = self.id
        return info

    def get_public_info(self):
        return self.__get_info()

    def update_public_info(self, last_name, first_name, middle_name, birth_year, gender, address, city, phone,
                           start_year,
                           experience, position):
        self.__update_info(last_name, first_name, middle_name, birth_year, gender, address, city, phone, start_year,
                           experience, position)

    def __str__(self):
        return str(self.get_info())[1:-1]

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

    def __init__(self, last_name, first_name=None, middle_name=None, birth_year=None, start_year=None,
                 experience=None, position=None, gender=None, address='', city='', phone=''):
        if isinstance(last_name, str) and ',' in last_name:
            parts = last_name.split(',')
            if len(parts) < 8:
                raise ValueError(
                    "Строка должна содержать не менее 8 полей: last_name, first_name, middle_name, birth_year, "
                    "start_year, experience, position, gender.")

            super().__init__(parts[0], parts[1], parts[2], int(parts[3]), parts[7],
                             address='', city='', phone='')
            self.__start_year = int(parts[4].strip())
            self.__experience = int(parts[5].strip())
            self.__position = parts[6].strip()
        else:
            super().__init__(last_name, first_name, middle_name, birth_year, gender,
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
        """Возвращает словарь с ключами-атрибутами"""
        info = super(MaintenanceStaff, self).get_info()
        info["Start Year"] = self.start_year
        info["Experience"] = self.experience
        info["Position"] = self.position
        info["id"] = self.id
        return info

    def get_public_info(self):
        return self.__get_info()

    def update_public_info(self, last_name, first_name, middle_name, birth_year, gender, address, city, phone,
                           start_year,
                           experience, position):
        self.__update_info(last_name, first_name, middle_name, birth_year, gender, address, city, phone, start_year,
                           experience, position)

    def __str__(self):
        return str(self.get_info())[1:-1]

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
        if isinstance(name, str) and ',' in name:
            parts = name.split(',')
            if len(parts) < 5:
                raise ValueError(
                    "Строка должна содержать не менее 5 полей: name, vehicle, repair_type, date_received, "
                    "date_released.")

            self.__name = parts[0].strip()
            self.__vehicle = Vehicle(parts[1].strip()) if ',' in parts[1] else parts[1].strip()
            self.__repair_type = parts[2].strip()
            self.__date_received = parts[3].strip()
            self.__date_released = parts[4].strip()
            self.__repair_result = ','.join(parts[5:]).strip() if len(parts) > 5 else ''
            self.__personnel = personnel
        else:
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

    def get_public_info(self):
        return self.__get_info()

    def update_public_info(self, name, vehicle, repair_type, date_received, date_released, repair_result, personnel):
        self.__update_info(name, vehicle, repair_type, date_received, date_released, repair_result, personnel)

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


class ClassBase:
    def __init__(self, cls):
        self.filename = '{0}.pkl'.format(cls.__name__)
        self.cls = cls
        self.database = {}
        self.index = 0
        try:
            self.open_database()
        except:
            self.save_database()

    def __iter__(self):
        for item in self.database:
            yield self.database[item]

    def next(self):
        if self.index == len(self.database):
            raise StopIteration
        self.index = self.index + 1
        return self.database[self.index]

    def prev(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.database[self.index]

    def open_database(self):
        with open(self.filename, 'rb') as f:
            self.database = pickle.load(f)

    def save_database(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.database, f)

    def add_object(self, *args):
        object = self.cls(*args)
        self.database[object.id] = object
        self.save_database()

    def get_object_by_id(self, id):
        if id not in self.database:
            return None
        return self.database[id]

    def delete_object(self, id):
        del self.database[id]

        self.save_database()

    def change_object(self, id, *args):
        object = self.get_object_by_id(id)
        if not object:
            raise ValueError('value does not exist')
        object.update_public_info(*args)
        self.save_database()


class AutoCity:
    def __init__(self):
        self.vehicle_database = ClassBase(Vehicle)
        self.route_database = ClassBase(Route)
        self.driver_database = ClassBase(Driver)
        self.maintenancestaff_database = ClassBase(MaintenanceStaff)
        self.garage_database = ClassBase(Garage)
        self.cur_database = self.vehicle_database

    def printDB(self, database):
        for x in database:
            print('{0} id {1} Description {2}'.format(database.cls.__name__, x.id, x.get_public_info()))

    def choose_database(self, value):
        if value == 1:
            self.cur_database = self.vehicle_database
        elif value == 2:
            self.cur_database = self.route_database
        elif value == 3:
            self.cur_database = self.driver_database
        elif value == 4:
            self.cur_database = self.maintenancestaff_database
        elif value == 5:
            self.cur_database = self.garage_database
        if value in range(1, 7):
            self.printDB(self.cur_database)

    def run(self):
        choice = 0
        choices = {
            1: lambda: self.choose_database(int(input('enter number of option'))),
            2: lambda: self.cur_database.add_object(
                input('enter info about {0}'.format(self.cur_database.cls.__name__))),
            3: lambda: self.cur_database.delete_object(int(input('enter id'))),
            4: lambda: self.cur_database.change_object(int(input('enter_id')), input(
                'enter info about {0}'.format(self.cur_database.cls.__name__)))
        }
        while choice != 5:
            print()
            print('1. Choose database (Options 1:Vehicle 2:Route 3:Driver 4:MaintenanceStaff 5:Garage) NOW IS {0} '
                  'database'.format(self.cur_database.cls.__name__))
            print('2. add {0}'.format(self.cur_database.cls.__name__))
            print('3. delete {0}'.format(self.cur_database.cls.__name__))
            print('4. change {0}'.format(self.cur_database.cls.__name__))
            print('5. EXIT')
            print('choose:')
            choice = int(input())
            if choice in choices:
                choices[choice]()
                self.printDB(self.cur_database)


if __name__ == '__main__':
    AutoCity().run()
