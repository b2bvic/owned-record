---
description: Weekly review — reflection on the past week's work with domain breakdown, metrics, and next-week priorities
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Weekly Review

## When to Use

Invoke at the end of a work week (or whenever a week boundary has passed). Generates a structured reflection covering what happened, what patterns emerged, and what to prioritize next.

## Execution

1. **Calculate week boundaries.** Determine the Monday-through-Sunday range for the review period. Use the current date to derive this.

   ```bash
   # Get current week's Monday and Sunday
   date -v-monday "+%Y.%m.%d"  # macOS
   # or: date -d "last monday" "+%Y.%m.%d"  # Linux
   ```

2. **Find all files modified during the week.** Search the vault for files with modification times within the Monday-Sunday range. Exclude system directories.

   ```bash
   find "$(pwd)" -name "*.md" -type f -newermt "YYYY-MM-DD" ! -newermt "YYYY-MM-DD" -not -path "*/node_modules/*" -not -path "*/.obsidian/*" -not -path "*/Archive/*" -exec ls -lt {} +
   ```

3. **Categorize by domain.** Group modified files under their domain folders. Count files per domain to show where effort concentrated.

4. **Review session logs.** Read `00 - System/_log.md` entries from this week. Read any session files from `00 - System/Sessions/` dated within the range. Extract key decisions, accomplishments, and patterns.

5. **Generate reflections.** Three sections:
   - **What went well** — Concrete wins, shipped work, effective patterns
   - **What could improve** — Friction points, repeated mistakes, time sinks
   - **Key learning** — One or two insights that should persist beyond this week

6. **Set next-week priorities.** Based on open items, deadlines, and momentum, propose 3-5 priorities for the coming week. Be specific enough to act on.

7. **Save the review.** Write to `00 - System/Sessions/YYYY-W{WW} - Weekly Review.md` using ISO week number.

## Output Format

```markdown
---
type:: weekly-review
date:: YYYY.MM.DD
week:: YYYY-W{WW}
period:: YYYY.MM.DD to YYYY.MM.DD
---

# Weekly Review — W{WW} (Mon DD - Sun DD)

## Activity Summary
| Domain | Files Modified | Key Work |
|--------|---------------|----------|
| [Domain 1] | X | [Brief summary] |
| [Domain 2] | X | [Brief summary] |
| **Total** | **X** | |

## Accomplishments
- [Concrete outcome 1]
- [Concrete outcome 2]
- [Concrete outcome 3]

## Decisions Made
- **[Decision]:** [What was chosen and why]

## Reflections

### What Went Well
[Paragraph or bullets — specific, not generic]

### What Could Improve
[Paragraph or bullets — honest, actionable]

### Key Learning
[One or two insights worth carrying forward]

## Next Week Priorities
1. [Specific, actionable priority]
2. [Specific, actionable priority]
3. [Specific, actionable priority]

## Open Threads
- [Unresolved item that needs attention eventually but not next week]
```

## Notes

- The review is both artifact and ritual. Writing it forces the synthesis. Don't skip the reflections section even when the week feels uneventful — that itself is a signal.
- If session logs are sparse, the review is shorter. That's fine. Don't fabricate substance.
- Confirm to the user: display a summary and the file path where the review was saved.
