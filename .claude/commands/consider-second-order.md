---
description: Map cascading consequences of a decision across multiple time horizons
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Second-Order Thinking

## When to Use

Invoke when a decision has ripple effects, when an action seems obviously good (suspiciously so), when policy changes affect interconnected systems, or when you need to anticipate unintended consequences before committing.

## Execution

1. **State the action or decision.** Be precise about what is being proposed, changed, or implemented.

2. **Map first-order effects.** These are the immediate, obvious, intended consequences. What happens directly as a result of this action? These are typically what the decision-maker is optimizing for.

3. **Map second-order effects.** For each first-order effect, ask: "And then what?" How do other actors, systems, or incentives respond to the first-order change? Second-order effects often work against the original intention.

4. **Map third-order effects.** Push one layer deeper. These are the consequences of the consequences of the consequences. They're harder to predict but often determine whether a decision ages well or poorly.

5. **Identify hidden consequences.** Look for:
   - Incentive distortions (people gaming the new system)
   - Feedback loops (effects that amplify themselves)
   - Delayed effects (consequences that take months/years to materialize)
   - Transfer effects (problems that move rather than disappear)
   - Cobra effects (interventions that worsen the original problem)

6. **Net assessment.** Weigh the full cascade. Does the decision still look good when you account for all orders of effect?

## Output Format

```
## Second-Order Analysis: [Decision]

### The Action
[What is being proposed]

### First-Order Effects (immediate)
- [Effect]: [Who/what is impacted]
- ...

### Second-Order Effects (responses and ripples)
- [First-order effect] → [Second-order consequence]
- ...

### Third-Order Effects (downstream cascade)
- [Second-order effect] → [Third-order consequence]
- ...

### Hidden Consequences
- [Type: incentive distortion / feedback loop / delayed / transfer / cobra]: [Description]

### Net Assessment
[Does this decision survive scrutiny across all orders? Recommend proceed / modify / abandon]
```
