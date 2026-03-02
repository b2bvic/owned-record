---
description: Session logging — appends a structured entry to the system log and optionally archives full session output
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Session Log

## When to Use

Invoke when a session produced work worth tracking. Not every session needs logging — use judgment. Good candidates: sessions that changed state, made decisions, produced artifacts, or surfaced patterns.

## Execution

1. **Read the system log.** Open `00 - System/_log.md`. Understand the existing format and most recent entries so the new entry maintains consistency.

2. **Summarize current session work.** Distill into a compact entry: what domains were touched, what was produced, what decisions were made. One to three sentences for the summary line, expanded detail below.

3. **Append the log entry.** Add to the top of the log (reverse chronological). Each entry follows the format below. Do not modify existing entries.

4. **Evaluate archival value.** If the session produced substantial output — a detailed analysis, a significant build, a complex deliberation — write the full output to `00 - System/Sessions/YYYY.MM.DD - {topic}.md` and cross-link from the log entry.

5. **Confirm to user.** State what was logged and whether a session file was archived.

## Log Entry Format

```markdown
## YYYY.MM.DD — [Brief Title]

**Domains:** [list]
**Files modified:** [count or list]

[2-4 sentence summary of what happened, what was decided, what changed]

**Decisions:**
- [Key decision, if any]

**Next:** [What follows from this session]

---
```

## Session Archive Format (optional, for high-value sessions)

```markdown
---
type:: session
date:: YYYY.MM.DD
domains:: [list]
---

# [Session Title]

## Summary
[Paragraph-length overview]

## Work Done
[Detailed accounting of what was produced]

## Files Touched
- [file paths]

## Decisions
- [Decision]: [Reasoning]

## Next Steps
- [What follows]
```

## Notes

- The log is an append-only ledger. Never edit past entries except to correct factual errors.
- If `00 - System/_log.md` doesn't exist, create it with a header: `# System Log` and a blank line before the first entry.
- Keep log entries scannable. Someone skimming should grasp a week of activity in 30 seconds.
