class Task:
    def __init__(self, name, description, start_time, end_time, date, tags, id=0):
        self.id = id
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
        self.tags = tags

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "date": self.date,
            "tags": self.tags,
        }

    @staticmethod
    def from_dict(data):
        try:
            return Task(
                data['id'],
                data["name"],
                data.get("description", ""),
                data["start_time"],
                data["end_time"],
                data["date"],
                data['tags'],
            )
        except KeyError as e:
            print(f"Ошибка: отсутствует ключ {e} в задаче. Задача будет пропущена.")
            return None