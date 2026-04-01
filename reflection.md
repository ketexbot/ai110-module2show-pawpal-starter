# PawPal+ Project Reflection

## 1. System Design

Core user actions:
- Enter owner and pet information.
- Add or edit pet care tasks with duration and priority.
- Generate and review today's schedule.



**a. Initial design**

- Briefly describe your initial UML design.
    The UML design has one class for the owner, one for the pet, one for each care task, and one planner class that picks which tasks fit the day based on time and priority.

- What classes did you include, and what responsibilities did you assign to each?
    I included four classes:
    Owner stores the owner’s name, available time, and care preferences.
    Pet stores pet details and keeps the pet’s task list.
    Task represents one care activity with fields like duration, priority, category, and required status.
    Scheduler retrieves and organizes tasks from the owner's pets.
    
**b. Design changes**

- Did your design change during implementation?
    Yes.

- If yes, describe at least one change and why you made it.
    I added recurrence handling so daily and weekly tasks create the next task automatically when completed.
    I also added conflict detection so the scheduler can warn when tasks are at the same time.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    My scheduler uses task time, priority, pet name, and completion status.
- How did you decide which constraints mattered most?
    I sort tasks by time and can also sort by priority.
    I use filters to show tasks by pet or by complete/pending status.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    One tradeoff is that conflict detection only checks exact same times.
- Why is that tradeoff reasonable for this scenario?
    This is reasonable because it keeps the logic simple and still catches common schedule issues fast.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    I used AI to brainstorm class design, generate method stubs, and improve algorithms.
- What kinds of prompts or questions were most helpful?
    Specific prompts were most helpful, like "add conflict detection" or "sort tasks by HH:MM time".

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    I did not accept a version of conflict detection that was too complex for this project.
- How did you evaluate or verify what the AI suggested?
    I verified by running pytest and checking terminal output from the demo script.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    I tested task completion, adding tasks to pets, sorting by time, recurrence creation, and conflict detection.
- Why were these tests important?
    These tests are important because they verify the main scheduler behaviors and common edge cases.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    I am confident because tests pass and the demo outputs match expected behavior.
- What edge cases would you test next if you had more time?
    I would test invalid time formats, overlapping durations, and many tasks at the same time.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I am most satisfied with turning the UML design into a working app with clear scheduling output.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    I would improve conflict detection to check time overlaps and add better UI controls for task editing.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    I learned that AI speeds up development, but I still need to verify every suggestion with tests.

