---
description: Apply Occam's Razor — select the explanation with fewest assumptions when competing hypotheses exist
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Occam's Razor

## When to Use

Invoke when multiple explanations compete for the same observation, when a diagnosis is spiraling into complexity, when debugging produces exotic theories, or when you suspect overthinking. Occam's Razor doesn't guarantee the simplest answer is correct — it says to prefer it until evidence demands otherwise.

## Execution

1. **State the observation.** What are you trying to explain? Describe the phenomenon, symptom, or result without interpreting it.

2. **List competing explanations.** Generate at least 3 hypotheses that could account for the observation. Include the obvious ones and the creative ones.

3. **Count assumptions per explanation.** For each hypothesis, enumerate every assumption it requires to be true. An assumption is anything that hasn't been directly observed or verified. Be strict — "probably" and "usually" are assumptions.

4. **Rank by assumption count.** Fewer assumptions = higher prior probability. The explanation requiring the least unverified scaffolding ranks first.

5. **Check for disqualifying evidence.** Before selecting the simplest explanation, verify it isn't contradicted by known facts. Simplicity loses to evidence every time.

6. **Select and test.** Choose the surviving explanation with the fewest assumptions. Define a quick test that would confirm or falsify it. If falsified, move to the next candidate.

### Cautions

- Occam's Razor is a heuristic, not a proof. The universe is not obligated to be simple.
- Don't confuse "simple" with "familiar." A novel explanation with 2 assumptions beats a conventional one with 6.
- Avoid false simplicity — collapsing distinct phenomena into one explanation can hide real complexity.

## Output Format

```
## Occam's Razor: [Observation]

### Observation
[What we're trying to explain]

### Competing Explanations
| Hypothesis | Assumptions Required | Count |
|---|---|---|
| [Explanation A] | [List each assumption] | N |
| [Explanation B] | [List each assumption] | N |
| [Explanation C] | [List each assumption] | N |

### Disqualifying Evidence Check
- [Hypothesis]: [Contradicted by evidence? Y/N — detail if Y]

### Selected Explanation
[The surviving hypothesis with fewest assumptions]

### Falsification Test
[One test that would disprove this explanation if it's wrong]
```
