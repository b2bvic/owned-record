---
description: Multi-agent deliberation — three virtual agents debate a decision, then synthesize a recommendation
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# Multi-Agent Deliberation

## When to Use

Invoke with a decision, dilemma, or open question as the argument. Useful when a choice has non-obvious tradeoffs, when you're anchored on one option, or when the stakes warrant structured adversarial thinking.

## Execution

1. **Define the question.** Restate the user's input as a precise, debatable proposition. If the argument is vague, sharpen it into a binary or multi-option frame before proceeding.

2. **Agent 1 — The Advocate (argues FOR).** Build the strongest possible case for the proposition or the default/preferred option. Steelman it. Use evidence from the vault if available — search relevant context files, session history, domain state. No strawmen.

3. **Agent 2 — The Challenger (argues AGAINST).** Dismantle the Advocate's case. Surface hidden costs, second-order effects, failure modes, and opportunity costs. Identify assumptions that crack under pressure. Draw from different frameworks or historical patterns if applicable.

4. **Agent 3 — The Synthesizer (weighs both).** Neither cheerleader nor contrarian. Weigh the strongest arguments from each side. Identify where the disagreement is real vs. semantic. Name what additional information would change the calculus. Render a verdict.

5. **Output the recommendation.** Structured markdown with each agent's position, the synthesis, and a confidence level (High / Medium / Low) with reasoning for that confidence.

6. **Save the deliberation.** Write the output to `00 - System/Sessions/` with a date-prefixed filename:
   - Format: `YYYY.MM.DD - Deliberation - {short topic}.md`
   - Include frontmatter: `type:: deliberation`, `date:: YYYY.MM.DD`, `question:: {the proposition}`

## Output Format

```markdown
---
type:: deliberation
date:: YYYY.MM.DD
question:: [The precise proposition]
---

# Deliberation: [Short Topic]

## The Question
[Precise, debatable proposition]

## Agent 1 — Advocate (FOR)
[Steelmanned case. Evidence, logic, upside.]

## Agent 2 — Challenger (AGAINST)
[Counter-case. Hidden costs, failure modes, alternatives.]

## Agent 3 — Synthesizer
[Weighing. Where is the real disagreement? What would change the answer?]

## Recommendation
**Position:** [Clear recommendation]
**Confidence:** [High / Medium / Low]
**Reasoning:** [Why this confidence level — what's known vs. uncertain]
**Conditions:** [Under what circumstances this recommendation reverses]
```

## Notes

- Each agent argues its position genuinely, not performatively. The value is in surfacing what you'd miss thinking alone.
- If vault context is relevant, agents should cite specific files or data points rather than speaking abstractly.
- The Synthesizer is not required to split the difference. A lopsided verdict is fine when the evidence supports it.
