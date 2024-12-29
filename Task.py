class Task:
    def __init__(self, name, description, start_time, end_time, date, tags, done=0, notified=0, date_notif='', id=0):
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

    def to_dict(self):
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
    def from_dict(data):
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
            print(f"Ошибка: отсутствует ключ {e} в задаче. Задача будет пропущена.")
            return None