import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner + Pet Setup")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)

if st.session_state.owner.name != owner_name:
    st.session_state.owner.name = owner_name

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet age", min_value=0, max_value=50, value=3)

if st.button("Add pet"):
    existing_pet = st.session_state.owner.get_pet(pet_name)
    if existing_pet is None:
        st.session_state.owner.add_pet(Pet(name=pet_name, species=species, age=int(age)))
        st.success(f"Added pet: {pet_name}")
    else:
        st.warning("A pet with that name already exists.")

if st.session_state.owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {"name": pet.name, "species": pet.species, "age": pet.age}
            for pet in st.session_state.owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add tasks to a selected pet. These tasks are stored in your Owner/Pet objects.")

if st.session_state.owner.pets:
    selected_pet_name = st.selectbox(
        "Assign task to pet",
        [pet.name for pet in st.session_state.owner.pets],
    )
else:
    selected_pet_name = None

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    task_time = st.text_input("Time (HH:MM)", value="08:00")

frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=0)

if st.button("Add task"):
    if selected_pet_name is None:
        st.warning("Add a pet first, then add tasks.")
    else:
        pet = st.session_state.owner.get_pet(selected_pet_name)
        if pet is not None:
            pet.add_task(
                Task(
                    description=task_title,
                    time=task_time,
                    duration_minutes=int(duration),
                    priority=priority,
                    frequency=frequency,
                )
            )
            st.success(f"Added task '{task_title}' to {selected_pet_name}")

all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": task.pet_name,
                "task": task.description,
                "time": task.time,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "frequency": task.frequency,
            }
            for task in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a schedule using your backend Scheduler class.")

filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    status_filter = st.selectbox("Status filter", ["pending", "complete", "all"], index=0)
with filter_col2:
    pet_filter_options = ["all"] + [pet.name for pet in st.session_state.owner.pets]
    pet_filter = st.selectbox("Pet filter", pet_filter_options, index=0)

if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)
    today_tasks = scheduler.get_todays_tasks()
    sorted_tasks = scheduler.sort_by_time(today_tasks)

    if pet_filter != "all":
        sorted_tasks = scheduler.filter_by_pet(sorted_tasks, pet_filter)

    if status_filter != "all":
        sorted_tasks = scheduler.filter_by_status(sorted_tasks, complete=(status_filter == "complete"))

    conflict_warnings = scheduler.detect_conflicts(today_tasks)
    if conflict_warnings:
        st.warning("Schedule conflict warnings:")
        for warning in conflict_warnings:
            st.write(f"- {warning}")

    if sorted_tasks:
        st.success("Today's schedule generated.")
        st.table(
            [
                {
                    "pet": task.pet_name,
                    "task": task.description,
                    "time": task.time,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                    "status": "complete" if task.is_complete else "pending",
                }
                for task in sorted_tasks
            ]
        )
    else:
        st.info("No tasks due today.")
