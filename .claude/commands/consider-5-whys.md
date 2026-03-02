---
description: Drill to root cause by asking "why" five times in sequence
allowed-tools:
  - Read
  - Glob
  - Grep
---

# 5 Whys — Root Cause Analysis

## When to Use

Invoke when a problem keeps recurring, when surface-level fixes haven't stuck, when a symptom is obvious but its origin is not, or when you suspect the real issue is buried several layers beneath the presenting complaint.

## Execution

1. **State the symptom.** Describe what went wrong or what keeps happening. Be specific — "things are slow" is too vague. "Deploy times increased from 3 minutes to 18 minutes after the migration" is workable.

2. **Ask Why #1.** Why did this symptom occur? Answer with a direct, factual cause — not a guess, not a blame assignment.

3. **Ask Why #2.** Why did that cause exist? Take the answer from #1 and interrogate it. Each "why" should move deeper, not sideways.

4. **Ask Why #3.** Continue drilling. By the third why, you're typically past the technical layer and into process or organizational territory.

5. **Ask Why #4.** At this depth, root causes often involve missing feedback loops, absent ownership, or misaligned incentives.

6. **Ask Why #5.** The final why usually reaches a structural or systemic condition — something that, if fixed, would prevent the entire chain from recurring.

7. **Identify the root cause.** Name it plainly. It should feel deeper and more fundamental than the original symptom.

8. **Propose a structural fix.** The fix should address the root cause, not the symptom. A good structural fix makes the symptom impossible, not just unlikely.

### Guardrails

- If an answer to "why" branches into multiple causes, follow the most impactful branch first. Note the others for separate analysis.
- Stop before 5 if you genuinely reach bedrock. Don't force artificial depth.
- Go beyond 5 if the fifth why still feels superficial.

## Output Format

```
## 5 Whys: [Problem]

### Symptom
[What happened / keeps happening]

### Chain
1. **Why?** [Answer]
2. **Why?** [Answer]
3. **Why?** [Answer]
4. **Why?** [Answer]
5. **Why?** [Answer]

### Root Cause
[The structural or systemic condition at the bottom of the chain]

### Structural Fix
[What to change so the entire chain cannot recur]

### Branches Not Explored
- [Other causal paths identified but not followed — for separate analysis]
```
