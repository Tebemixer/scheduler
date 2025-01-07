import logging

logging.basicConfig(level=logging.ERROR)


class Task:
    def __init__(self, name: str, description: str, start_time: str, end_time: str, date: str,
                 tags: str, done=0, notified=0, date_notif='', id=0):
        self.id = id
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
        self.tags = tags
        self.done = done
        self.notified = notified
        self.date_notif = date_notif

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return (
                self.name == other.name and
                self.description == other.description and
                self.start_time == other.start_time and
                self.end_time == other.end_time and
                self.date == other.date and
                self.tags == other.tags and
                self.done == other.done and
                self.notified == other.notified and
                self.date_notif == other.date_notif and
                self.id == other.id
        )

    def to_dict(self) -> dict:
        """Возвращает задачу в виде словаря с ключами-атрибутами."""
        return {
            "name": self.name,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "date": self.date,
            "tags": self.tags,
            "done": self.done,
            "notified": self.notified,
            "id": self.id,
            "date_notif": self.date_notif
        }

    @staticmethod
    def from_dict(data: dict):
        """Возвращает задачу с параметрами из словаря."""
        try:
            return Task(
                data["name"],
                data["description"],
                data["start_time"],
                data["end_time"],
                data["date"],
                data['tags'],
                data['done'],
                data['notified'],
                data['date_notif'],
                data['id']
            )
        except KeyError as e:
            logging.error(f"Ошибка: отсутствует ключ {e} в задаче. Задача будет пропущена.")
            return None
