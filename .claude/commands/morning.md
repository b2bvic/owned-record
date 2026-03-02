---
description: Morning dashboard — daily orientation with recent activity, staleness checks, deadlines, and prioritized tasks
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Morning Dashboard

## When to Use

Invoke at the start of a work session to get oriented. Surfaces what changed recently, what's stale, what's due, and what to prioritize today.

## Execution

1. **Find recently modified files.** Search for files modified in the last 24 hours across the vault. Exclude system directories (node_modules, .obsidian, archive folders). Group results by domain folder.

   ```bash
   find "$(pwd)" -name "*.md" -type f -mmin -1440 -not -path "*/node_modules/*" -not -path "*/.obsidian/*" -not -path "*/Archive/*" -exec ls -lt {} + | head -40
   ```

2. **Check domain context staleness.** For each domain that has a `_context.md` file, check the `last_verified::` timestamp. If older than 48 hours, flag it as stale. Read each context file to extract current state summaries.

3. **Surface deadlines.** Scan context files and recent session files for dates, deadlines, and time-sensitive items within the next 14 days. Extract and sort chronologically.

4. **Summarize domain state.** For each active domain, provide a 2-3 sentence status based on its `_context.md` and recent file activity. Note what's active, blocked, or idle.

5. **Generate prioritized task list.** Based on deadlines, staleness, and domain state, produce a ranked list of today's priorities. Distinguish between urgent (deadline-driven), important (high-impact), and maintenance (staleness fixes, cleanup).

## Output Format

```markdown
# Morning Dashboard — YYYY.MM.DD

## Recent Activity (last 24h)
### [Domain 1]
- `file1.md` — [brief description of change]
- `file2.md` — [brief description of change]

### [Domain 2]
- ...

## Staleness Alerts
| Domain | Last Verified | Status |
|--------|---------------|--------|
| [Domain] | YYYY.MM.DD | Current / ⚠️ Stale (X days) |

## Upcoming Deadlines
| Date | Item | Domain | Status |
|------|------|--------|--------|
| YYYY.MM.DD | [What's due] | [Domain] | [On track / At risk / Overdue] |

## Domain State
### [Domain 1]
[2-3 sentence status summary]

### [Domain 2]
[2-3 sentence status summary]

## Today's Priorities
1. 🔴 [Urgent — deadline-driven task]
2. 🟡 [Important — high-impact task]
3. ⚪ [Maintenance — staleness fix or cleanup]
```

## Notes

- The dashboard is ephemeral — it's displayed to the user, not saved to a file (unless they request it).
- If no `_context.md` files exist yet, note this and suggest creating them as a first task.
- Keep the output scannable. This is a triage tool, not a report. Dense beats thorough.
