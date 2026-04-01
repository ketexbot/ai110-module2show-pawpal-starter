from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_updates_status():
    task = Task(description="Give meds", time="07:00", duration_minutes=5)
    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    initial_count = len(pet.tasks)

    pet.add_task(Task(description="Evening walk", time="18:00", duration_minutes=30))

    assert len(pet.tasks) == initial_count + 1


def test_sorting_returns_chronological_order():
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_task(Task(description="Late task", time="10:00", duration_minutes=15))
    pet.add_task(Task(description="Early task", time="08:00", duration_minutes=20))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(scheduler.get_todays_tasks())

    assert [task.description for task in sorted_tasks] == ["Early task", "Late task"]


def test_daily_recurrence_creates_next_day_task():
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", species="dog", age=3)
    task = Task(
        description="Morning walk",
        time="08:00",
        duration_minutes=20,
        frequency="daily",
        due_date=date.today(),
    )
    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    result = scheduler.mark_task_complete("Mochi", "Morning walk")

    assert result is True
    assert len(pet.tasks) == 2
    assert pet.tasks[0].is_complete is True
    assert pet.tasks[1].due_date == date.today() + timedelta(days=1)
    assert pet.tasks[1].is_complete is False


def test_conflict_detection_flags_duplicate_times():
    owner = Owner("Jordan")
    dog = Pet(name="Mochi", species="dog", age=3)
    cat = Pet(name="Luna", species="cat", age=2)
    dog.add_task(Task(description="Walk", time="08:00", duration_minutes=20))
    cat.add_task(Task(description="Play", time="08:00", duration_minutes=15))
    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts(scheduler.get_todays_tasks())

    assert len(warnings) == 1
    assert "Conflict at 08:00" in warnings[0]


def test_no_tasks_for_pet_is_handled():
    owner = Owner("Jordan")
    owner.add_pet(Pet(name="Mochi", species="dog", age=3))

    scheduler = Scheduler(owner)

    assert scheduler.get_todays_tasks() == []
