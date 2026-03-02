---
description: Apply Pareto 80/20 analysis to identify the vital few inputs driving disproportionate results
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Pareto 80/20 Analysis

## When to Use

Invoke when asking what matters most, which efforts are wasted, where to concentrate resources, or when a system has too many moving parts and needs ruthless prioritization.

## Execution

1. **Inventory all inputs.** List every activity, resource, habit, client, feature, or effort related to the question at hand. Be exhaustive — hidden inputs often contain the highest leverage.

2. **Estimate impact per input.** For each item, approximate its contribution to the desired outcome. Use available data (revenue per client, time per task, output per feature). Where data is absent, use informed judgment and flag the uncertainty.

3. **Rank by impact density.** Sort inputs by impact-to-effort ratio. The top of this list reveals where a small slice of input generates outsized output.

4. **Identify the vital 20%.** Draw the line: which inputs, if you could only keep a handful, would preserve ~80% of the total result? Name them explicitly.

5. **Identify the trivial 80%.** Everything below the line. For each, ask: what happens if this disappears entirely? If the answer is "not much," it's a candidate for elimination or deprioritization.

6. **Recommend action.** Two moves:
   - **Double down** on the vital few (more time, more budget, more attention)
   - **Cut or reduce** the trivial many (stop doing, automate, delegate, batch)

## Output Format

```
## Pareto Analysis: [Topic]

### Vital 20% (high-impact inputs)
- [Input]: [Impact estimate] — [Recommended action: double down / protect / expand]
- ...

### Trivial 80% (low-impact inputs)
- [Input]: [Impact estimate] — [Recommended action: cut / reduce / automate / delegate]
- ...

### Key Insight
[One sentence: the single most important reallocation to make]
```
