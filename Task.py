class Task:
    def __init__(self, name, description, start_time, end_time, date, tags, done=0, id=0):
        self.id = id
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
        self.tags = tags
        self.done = done

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "date": self.date,
            "tags": self.tags,
            "done": self.done
        }

    @staticmethod
    def from_dict(data):
        try:
            return Task(

                data["name"],
                data.get("description", ""),
                data["start_time"],
                data["end_time"],
                data["date"],
                data['tags'],
                data['id'],
                data['done']
            )
        except KeyError as e:
            print(f"Ошибка: отсутствует ключ {e} в задаче. Задача будет пропущена.")
            return None