---
description: Sort tasks into the Eisenhower urgency/importance matrix to clarify what to do, schedule, delegate, or drop
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Eisenhower Matrix

## When to Use

Invoke when overwhelmed by competing priorities, when everything feels urgent, when you suspect you're spending time on busywork instead of meaningful work, or when you need to triage a backlog.

## Execution

1. **List all tasks.** Dump everything on the plate — active work, pending requests, recurring obligations, nagging to-dos. Include items you're avoiding.

2. **Define "important."** Important = contributes to long-term goals, core responsibilities, or irreplaceable outcomes. If it disappeared, would your trajectory change? That's important.

3. **Define "urgent."** Urgent = has an imminent deadline, someone is waiting, or delay creates escalating consequences. Urgency is about timing, not value.

4. **Categorize each task into one of four quadrants:**

   - **Q1: Urgent + Important** — Crises, deadlines, critical problems. These demand immediate action. If your day lives here, something upstream is broken.
   - **Q2: Important + Not Urgent** — Strategic work, relationship building, skill development, prevention. This is where the highest-leverage work lives. Protect this quadrant.
   - **Q3: Urgent + Not Important** — Interruptions, most meetings, other people's priorities disguised as yours. Delegate or batch these ruthlessly.
   - **Q4: Not Urgent + Not Important** — Time sinks, busywork, comfort tasks. Drop these.

5. **Assign actions:**
   - Q1 → **Do now.** Execute immediately or today.
   - Q2 → **Schedule.** Block time. This is the quadrant most people neglect.
   - Q3 → **Delegate.** If no one to delegate to, batch into a single time block and contain it.
   - Q4 → **Drop.** Remove from the list entirely. Stop tracking it.

6. **Diagnose the distribution.** If Q1 dominates, you're in firefighting mode — invest more in Q2 to prevent future crises. If Q3 dominates, boundaries need tightening.

## Output Format

```
## Eisenhower Matrix: [Context]

| | Urgent | Not Urgent |
|---|---|---|
| **Important** | Q1: DO NOW | Q2: SCHEDULE |
| **Not Important** | Q3: DELEGATE | Q4: DROP |

### Q1 — Do Now
- [Task]: [Why it's urgent + important]

### Q2 — Schedule
- [Task]: [When to block time for this]

### Q3 — Delegate / Contain
- [Task]: [Who handles this, or when to batch it]

### Q4 — Drop
- [Task]: [Why it doesn't belong on the list]

### Diagnosis
[Pattern observation: which quadrant is overloaded and what that signals]
```
