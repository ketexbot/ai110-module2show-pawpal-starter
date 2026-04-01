from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(tasks):
    print("Today's Schedule")
    print("-" * 40)
    if not tasks:
        print("No tasks due today.")
        return

    for i, task in enumerate(tasks, start=1):
        print(
            f"{i}. {task.pet_name}: {task.description} at {task.time} "
            f"({task.duration_minutes} min, {task.priority})"
        )


def main():
    owner = Owner("Jordan")

    dog = Pet(name="Mochi", species="dog", age=3)
    cat = Pet(name="Luna", species="cat", age=2)

    dog.add_task(Task(description="Morning walk", time="08:00", duration_minutes=20, priority="high"))
    dog.add_task(Task(description="Breakfast", time="08:30", duration_minutes=10, priority="high"))
    cat.add_task(Task(description="Play time", time="09:00", duration_minutes=25, priority="medium"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    todays_tasks = scheduler.get_todays_tasks()
    ordered_tasks = scheduler.sort_by_time(todays_tasks)

    print_schedule(ordered_tasks)


if __name__ == "__main__":
    main()
