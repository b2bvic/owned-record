---
description: Run a SWOT analysis to evaluate strategic position across strengths, weaknesses, opportunities, and threats
allowed-tools:
  - Read
  - Glob
  - Grep
---

# SWOT Analysis

## When to Use

Invoke when evaluating a strategy, entering a new market, assessing competitive position, making a go/no-go decision, or when you need a structured snapshot of where things stand before committing resources.

## Execution

1. **Define the subject.** What entity, project, product, or decision is being analyzed? SWOT without a clear subject produces vague output.

2. **Map Strengths (internal, positive).** What advantages exist? Consider:
   - Unique capabilities or resources
   - Proven track record or expertise
   - Cost advantages or proprietary assets
   - Strong relationships or reputation

   Be honest. Only list genuine differentiators, not aspirational qualities.

3. **Map Weaknesses (internal, negative).** Where are the gaps? Consider:
   - Resource constraints (time, money, people)
   - Skill gaps or knowledge deficits
   - Process inefficiencies
   - Dependencies or single points of failure

   The most useful weaknesses are the ones you'd rather not write down.

4. **Map Opportunities (external, positive).** What favorable conditions exist? Consider:
   - Market shifts or emerging demand
   - Competitor vulnerabilities
   - Technology changes that create openings
   - Regulatory or cultural tailwinds

5. **Map Threats (external, negative).** What could undermine success? Consider:
   - Competitive pressure or new entrants
   - Market contraction or demand shifts
   - Regulatory or economic headwinds
   - Technology disruption

6. **Cross-reference for the highest-leverage play.** The real insight lives at the intersections:
   - **Strength + Opportunity** = offensive plays (lean in hard)
   - **Strength + Threat** = defensive plays (protect position)
   - **Weakness + Opportunity** = investment plays (shore up to capture)
   - **Weakness + Threat** = vulnerabilities (mitigate or exit)

7. **Recommend action.** Based on the cross-reference, name the single highest-leverage strategic move.

## Output Format

```
## SWOT Analysis: [Subject]

|  | Positive | Negative |
|---|---|---|
| **Internal** | **Strengths** | **Weaknesses** |
|  | - [S1] | - [W1] |
|  | - [S2] | - [W2] |
| **External** | **Opportunities** | **Threats** |
|  | - [O1] | - [T1] |
|  | - [O2] | - [T2] |

### Strategic Intersections
- **S + O (Offense):** [Play]
- **S + T (Defense):** [Play]
- **W + O (Invest):** [Play]
- **W + T (Vulnerability):** [Play]

### Highest-Leverage Move
[The single strategic action that best exploits position]
```
