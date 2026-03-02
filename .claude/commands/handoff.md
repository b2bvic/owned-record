---
description: Session continuity handoff — captures state so the next session picks up cold without re-discovery
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# Session Handoff

## When to Use

Invoke at the end of a productive session, especially when work spans multiple files, crosses domains, or leaves threads open. The handoff document becomes the cold-start briefing for the next session.

## Execution

1. **Summarize accomplishments.** What was done this session — concrete outcomes, not activity descriptions. "Built the pipeline parser" not "worked on pipeline stuff." If nothing concrete shipped, say so honestly.

2. **List files touched.** Every file created, modified, or deleted. Use full paths relative to the vault root. Group by domain if multiple domains were involved.

3. **List decisions made.** Explicit choices with reasoning. Future-you needs to know *why*, not just *what*. Include decisions that were considered and rejected — those prevent re-litigation.

4. **List open questions and next steps.** What remains undone? What's blocked and on what? What should the next session tackle first? Be specific enough that someone with no context can pick up the thread.

5. **Capture domain state.** For each domain touched this session, read its `_context.md` and note any state changes that occurred. If `_context.md` needs updating, flag it.

6. **Write the handoff file.** Save to `00 - System/Sessions/YYYY.MM.DD - Handoff.md` with structured frontmatter.

## Output Format

```markdown
---
type:: handoff
date:: YYYY.MM.DD
domains:: [list of domains touched]
---

# Session Handoff — YYYY.MM.DD

## Accomplished
- [Concrete outcome 1]
- [Concrete outcome 2]

## Files Touched
| File | Action |
|------|--------|
| `path/to/file.md` | Created / Modified / Deleted |

## Decisions Made
- **[Decision]:** [Choice made] — [Reasoning]
- **[Decision]:** [Rejected alternative] — [Why not]

## Open Questions
- [Question or ambiguity that needs resolution]

## Next Steps
1. [Most important next action — specific enough to execute without re-reading everything]
2. [Second priority]
3. [Third priority]

## Domain State
### [Domain Name]
- Current state: [brief summary]
- Changed this session: [what shifted]
- Context file status: [current / needs update]
```

## Notes

- The handoff should be readable by someone with zero context about this session. Over-explain rather than under-explain.
- If the session was interrupted or cut short, note what was in-progress and where it stopped.
- Handoff files accumulate in Sessions/ and serve as an episodic memory layer. Don't delete old ones.
