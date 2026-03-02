---
description: Quantify what you forfeit by choosing one path over another
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Opportunity Cost Analysis

## When to Use

Invoke when choosing between competing paths, when a commitment locks up resources (time, money, attention), when "yes" to one thing means "no" to something else, or when the cost of a decision hides in what's given up rather than what's spent.

## Execution

1. **List all options.** Include the implicit ones people forget:
   - Doing nothing (the status quo has a cost too)
   - Delayed action (choosing later, but with less information or worse timing)
   - The option you're avoiding (often the highest-return choice)

2. **For each option, identify what you gain.** Be specific. Revenue, time freed, skills acquired, relationships built, positioning achieved.

3. **For each option, identify what you forfeit.** This is the core of the analysis. When you choose Option A, what does Option B (and C, and D) offer that you no longer get? Consider:
   - Direct financial cost or revenue foregone
   - Time that can't be recovered
   - Attention and cognitive bandwidth consumed
   - Doors that close or opportunities that expire
   - Compounding effects lost (the earlier you miss a compounding opportunity, the more expensive it becomes)

4. **Quantify where possible.** Attach numbers, even rough ones. "Probably $500/month in lost revenue" is more useful than "some financial impact." Where quantification is impossible, describe the magnitude qualitatively (trivial, moderate, significant, severe).

5. **Compare net positions.** For each option, subtract forfeited value from gained value. The option with the highest net position — accounting for what's gained AND what's lost — is the rational choice.

6. **Flag irreversibility.** Some opportunity costs are permanent (you can't un-spend time). Others are temporary (you can revisit later at a higher price). Permanent forfeitures deserve extra weight.

## Output Format

```
## Opportunity Cost Analysis: [Decision]

### Options
| Option | What You Gain | What You Forfeit | Net Assessment |
|---|---|---|---|
| [A] | [Gains] | [Costs — including what B/C offer] | [Net] |
| [B] | [Gains] | [Costs — including what A/C offer] | [Net] |
| [C / Do Nothing] | [Gains] | [Costs] | [Net] |

### Irreversibility Check
- [Option]: [Reversible / Partially reversible / Permanent]

### Highest-Return Path
[The option with the lowest true opportunity cost — what to choose and why]

### Hidden Cost
[The forfeiture most likely to be overlooked or underweighted]
```
