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
    - Yes. It changed.


- If yes, describe at least one change and why you made it.
    At first, I only focused on time and priority, but later I added a required field to tasks so important tasks (like medication) are handled first.
    I also moved scheduling decisions into Scheduler so Pet only stores pet/task data.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

