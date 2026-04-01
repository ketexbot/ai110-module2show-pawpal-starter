from pawpal_system import Pet, Task


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
