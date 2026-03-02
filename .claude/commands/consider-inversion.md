---
description: Apply Munger's inversion — solve problems backward by mapping how to guarantee failure
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Inversion (Munger)

## When to Use

Invoke when asking what could go wrong, when planning feels too optimistic, when you need a pre-mortem, or when forward reasoning hasn't produced clarity. Inversion exposes blind spots that forward thinking misses.

## Execution

1. **State the goal clearly.** What does success look like? Be specific — vague goals produce vague inversions.

2. **Invert the goal.** Ask: "How would I guarantee failure? What would I do if I wanted this to go as badly as possible?" Take this seriously. Think like an adversary.

3. **List all failure modes.** Be thorough. Categories to consider:
   - Actions that directly cause failure
   - Inactions that allow failure through neglect
   - Environmental conditions that make failure likely
   - Psychological traps (overconfidence, sunk cost, groupthink)
   - Timing failures (too early, too late, wrong sequence)

4. **Rank by likelihood and severity.** Not all failure modes are equal. Which are most probable? Which are most catastrophic? The intersection of high-probability and high-severity is where attention belongs.

5. **Invert again — do the opposite.** For each failure mode, define the corresponding safeguard or positive action. This becomes your plan.

6. **Identify the non-obvious insight.** Inversion often reveals a risk that forward planning would never surface. Name it.

## Output Format

```
## Inversion Analysis: [Goal]

### Goal
[What success looks like]

### How to Guarantee Failure
1. [Action/inaction that ensures failure]
2. ...

### Failure Modes Ranked
| Failure Mode | Likelihood | Severity | Priority |
|---|---|---|---|
| ... | High/Med/Low | High/Med/Low | ... |

### Safeguards (Do the Opposite)
1. [Failure mode] → [Corresponding safeguard]
2. ...

### Non-Obvious Risk
[The insight that only inversion revealed]
```
