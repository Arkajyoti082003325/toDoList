import json
import os
from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime

@dataclass
class Task:
    title: str
    completed: bool = False
    created_at: str = datetime.now().isoformat()
    due_date: Optional[str] = None
    priority: int = 1
    category: Optional[str] = None

class TodoManager:
    def __init__(self, data_file='data/tasks.json'):
        self.data_file = data_file
        self.tasks: List[Task] = []
        self._ensure_data_file_exists()
        self.load_tasks()

    def _ensure_data_file_exists(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump([], f)

    def load_tasks(self):
        try:
            with open(self.data_file, 'r') as f:
                tasks_data = json.load(f)
                self.tasks = [Task(**task) for task in tasks_data]
        except (json.JSONDecodeError, FileNotFoundError):
            self.tasks = []

    def save_tasks(self):
        with open(self.data_file, 'w') as f:
            tasks_data = [asdict(task) for task in self.tasks]
            json.dump(tasks_data, f, indent=2)

    def add_task(self, title: str, **kwargs):
        task = Task(title=title, **kwargs)
        self.tasks.append(task)
        self.save_tasks()
        return task

    def delete_task(self, task_index: int):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]
            self.save_tasks()
            return True
        return False

    def toggle_task_completion(self, task_index: int):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].completed = not self.tasks[task_index].completed
            self.save_tasks()
            return True
        return False

    def get_tasks(self, filter_completed: Optional[bool] = None):
        if filter_completed is None:
            return self.tasks.copy()
        return [task for task in self.tasks if task.completed == filter_completed]

    def update_task(self, task_index: int, **kwargs):
        if 0 <= task_index < len(self.tasks):
            task = self.tasks[task_index]
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            self.save_tasks()
            return True
        return False