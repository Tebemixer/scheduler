import customtkinter as ctk

class EditTaskWindow(ctk.CTkToplevel):
    def __init__(self, parent, date, task):
        super().__init__(parent)

        self.parent = parent
        self.date = date
        self.task = task
        self.title("Редактировать задачу")
        self.geometry("400x400")

        # Поля для редактирования данных
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Название задачи")
        self.name_entry.insert(0, task.name)
        self.name_entry.pack(pady=5, fill="x", padx=20)

        self.description_entry = ctk.CTkEntry(self, placeholder_text="Описание задачи")
        self.description_entry.insert(0, task.description)
        self.description_entry.pack(pady=5, fill="x", padx=20)

        self.start_time_entry = ctk.CTkEntry(self, placeholder_text="Время начала (HH:MM)")
        self.start_time_entry.insert(0, task.start_time)
        self.start_time_entry.pack(pady=5, fill="x", padx=20)

        self.end_time_entry = ctk.CTkEntry(self, placeholder_text="Время окончания (HH:MM)")
        self.end_time_entry.insert(0, task.end_time)
        self.end_time_entry.pack(pady=5, fill="x", padx=20)

        self.tags_entry = ctk.CTkEntry(self, placeholder_text="Теги (через запятую)")
        self.tags_entry.insert(0, ",".join(task.tags))
        self.tags_entry.pack(pady=5, fill="x", padx=20)

        # Кнопки для сохранения или удаления задачи
        self.save_button = ctk.CTkButton(self, text="Сохранить изменения", command=self.save_task)
        self.save_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(self, text="Удалить задачу", fg_color="red", command=self.delete_task)
        self.delete_button.pack(pady=10)



    def save_task(self):
        self.task.name = self.name_entry.get().strip()
        self.task.description = self.description_entry.get().strip()
        self.task.start_time = self.start_time_entry.get().strip()
        self.task.end_time = self.end_time_entry.get().strip()
        self.task.tags = [tag.strip() for tag in self.tags_entry.get().strip().split(",")]

        self.save_all_tasks()
        self.parent.update_task_list()
        self.destroy()

    def delete_task(self):
        self.parent.tasks[self.date].remove(self.task)
        if not self.parent.tasks[self.date]:
            del self.parent.tasks[self.date]

        self.parent.save_all_tasks()
        self.parent.update_task_list()
        self.destroy()

    def save_all_tasks(self):
        serialized_tasks = {date: [task.to_dict() for task in task_list] for date, task_list in self.tasks.items()}
        self.save_tasks(serialized_tasks)