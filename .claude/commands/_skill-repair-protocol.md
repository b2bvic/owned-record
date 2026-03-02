# Skill Repair Protocol

> Shared reference document for skill self-repair. Not a slash command — this is consumed by other skills when they encounter failures during execution.

## Failure Mode Taxonomy

| Code | Failure | Description | Auto-Fixable? |
|------|---------|-------------|---------------|
| `PATH_MOVED` | File exists but at a different location | Renamed, relocated, or restructured | Yes — search and update |
| `PATH_GONE` | File no longer exists anywhere | Deleted, archived, or never created | Depends — may recreate |
| `FOLDER_MISSING` | Expected output directory absent | Hasn't been created yet or was removed | Yes — create if known pattern |
| `TOOL_UNAVAILABLE` | Required tool not accessible | MCP server down, tool removed, permissions | No — flag to user |
| `FORMAT_CHANGED` | File exists but structure differs from expectation | Frontmatter schema changed, sections renamed | Partial — adapt if minor |
| `EMPTY_RESULT` | Search or read returned nothing | Query too narrow, index stale, or content absent | Yes — broaden search |
| `OUTPUT_CONFLICT` | Target file already exists with different content | Naming collision, duplicate run | No — flag to user |

## Universal Repair Flow

```
DETECT failure
  → CHECK: Is this auto-fixable per the taxonomy above?
    → YES: REPAIR (within limits below)
    → NO: FLAG to user with failure code, attempted path, and what was expected
```

Every repair attempt follows this sequence. No silent failures. No infinite retry loops.

## Path Resolution Strategy

When a file path fails, attempt resolution in this order:

1. **Exact path** — Try the path as specified
2. **Same folder** — Search the parent directory for similar filenames (Glob: `parent/*.md`)
3. **Domain folder** — Search one level up from the expected domain root
4. **Vault-wide** — Glob search across the entire vault for the filename
5. **Content search** — If a keyword search tool is available, search by expected file content or title
6. **Give up** — Flag `PATH_GONE` to user with the original path and search attempts made

Stop at the first match. If multiple matches appear at any step, flag `OUTPUT_CONFLICT` and present options to the user rather than guessing.

## Folder Creation Rules

Auto-create directories **only** for known output patterns:

| Folder | Safe to Create | Reason |
|--------|---------------|--------|
| `00 - System/Sessions/` | Yes | Standard session output location |
| `00 - System/Patterns/` | Yes | Pattern documentation location |
| Any folder that already has siblings | Yes | Parent structure confirmed |
| Arbitrary new paths | **No** | Requires user confirmation |

When creating a folder, log the creation. If the parent directory itself doesn't exist, do not create nested structures — flag to user.

## Repair Limits

These limits prevent runaway repair loops from consuming context or making cascading changes:

| Limit | Value | On Exceeded |
|-------|-------|-------------|
| Repairs per skill execution | 3 | Stop, report all failures, ask user for guidance |
| Glob searches per repair | 3 | Accept failure, flag `PATH_GONE` |
| File creations per repair | 1 | Only the missing output target, nothing upstream |
| Retries of same operation | 1 | Different approach or flag |

## Logging

All repair actions append to `00 - System/Patterns/_feedback-queue.md` with:

```markdown
## [YYYY.MM.DD] Skill Repair — [Failure Code]

- **Skill:** [which skill triggered the repair]
- **Expected:** [what was expected]
- **Found:** [what was actually found, or "nothing"]
- **Action:** [what repair was performed, or "flagged to user"]
- **Result:** [resolved / unresolved]
```

If `_feedback-queue.md` doesn't exist, create it with a header: `# Feedback Queue` and a note that this file tracks automated repair actions and pattern observations.

## Integration

Skills should reference this protocol when they encounter failures. The pattern:

```
1. Attempt the operation
2. If it fails, classify the failure using the taxonomy
3. If auto-fixable, follow the repair flow (within limits)
4. If not auto-fixable or limits exceeded, report to user with:
   - The failure code
   - What was attempted
   - What the skill needs to proceed
5. Log the repair attempt regardless of outcome
```

This protocol assumes nothing about the vault structure beyond the `00 - System/` convention. Skills that use domain-specific paths should handle their own path resolution before falling back to this protocol.
