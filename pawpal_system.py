"""PawPal+ System — Backend logic layer for pet care management."""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    """Represents a single pet care activity."""

    description: str
    time: str  # HH:MM format
    duration_minutes: int
    priority: str = "medium"  # low, medium, high
    frequency: str = "once"  # once, daily, weekly
    is_complete: bool = False
    pet_name: str = ""
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark this task as completed."""
        self.is_complete = True

    def __str__(self) -> str:
        """Return a readable string representation."""
        status = "done" if self.is_complete else "pending"
        return (
            f"[{self.time}] {self.description} "
            f"({self.duration_minutes} min, {self.priority}, {status})"
        )


@dataclass
class Pet:
    """Stores pet details and manages its task list."""

    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, description: str):
        """Remove a task by description."""
        for i, task in enumerate(self.tasks):
            if task.description == description:
                del self.tasks[i]
                return True
        return False

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        return list(self.tasks)

    def get_pending_tasks(self) -> list:
        """Return only incomplete tasks."""
        return [task for task in self.tasks if not task.is_complete]


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str):
        """Initialize an owner with a name and empty pet list."""
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, name: str):
        """Remove a pet by name."""
        for i, pet in enumerate(self.pets):
            if pet.name == name:
                del self.pets[i]
                return True
        return False

    def get_pet(self, name: str) -> Optional[Pet]:
        """Retrieve a pet by name."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self) -> list:
        """Retrieve all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """The 'brain' — retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def get_todays_tasks(self) -> list:
        """Get all tasks due today."""
        today = date.today()
        return [task for task in self.owner.get_all_tasks() if task.due_date == today]

    def sort_by_time(self, tasks: list) -> list:
        """Sort tasks chronologically by time (HH:MM)."""
        return sorted(tasks, key=lambda task: task.time)

    def sort_by_priority(self, tasks: list) -> list:
        """Sort tasks by priority (high > medium > low)."""
        priority_rank = {"high": 3, "medium": 2, "low": 1}
        return sorted(tasks, key=lambda task: priority_rank.get(task.priority, 0), reverse=True)

    def filter_by_pet(self, tasks: list, pet_name: str) -> list:
        """Filter tasks belonging to a specific pet."""
        return [task for task in tasks if task.pet_name == pet_name]

    def filter_by_status(self, tasks: list, complete: bool = False) -> list:
        """Filter tasks by completion status."""
        return [task for task in tasks if task.is_complete == complete]

    def detect_conflicts(self, tasks: list) -> list:
        """Detect scheduling conflicts (tasks at the same time)."""
        warnings = []
        seen_by_time = {}

        for task in tasks:
            if task.time in seen_by_time:
                other = seen_by_time[task.time]
                warnings.append(
                    (
                        f"Conflict at {task.time}: {other.pet_name} - {other.description} "
                        f"and {task.pet_name} - {task.description}"
                    )
                )
            else:
                seen_by_time[task.time] = task

        return warnings

    def handle_recurrence(self, task: Task) -> Optional[Task]:
        """Create next occurrence for recurring tasks."""
        if task.frequency == "daily":
            return Task(
                description=task.description,
                time=task.time,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                frequency=task.frequency,
                pet_name=task.pet_name,
                due_date=task.due_date + timedelta(days=1),
            )
        if task.frequency == "weekly":
            return Task(
                description=task.description,
                time=task.time,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                frequency=task.frequency,
                pet_name=task.pet_name,
                due_date=task.due_date + timedelta(days=7),
            )
        return None

    def mark_task_complete(self, pet_name: str, description: str):
        """Mark a specific task as complete, handling recurrence."""
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            return False

        for task in pet.tasks:
            if task.description == description and not task.is_complete:
                task.mark_complete()
                next_task = self.handle_recurrence(task)
                if next_task is not None:
                    pet.add_task(next_task)
                return True

        return False
