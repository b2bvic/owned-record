# Skill Authoring Guide

> Skills are slash commands — markdown files in `.claude/commands/` that Claude Code executes as structured procedures.

---

## Anatomy of a Skill File

A skill is a markdown file with two parts: YAML frontmatter and step-by-step instructions.

```
.claude/commands/
├── summarize.md          # /summarize
├── daily-report.md       # /daily-report
├── _skill-repair-protocol.md  # Shared reference (underscore prefix = not a command)
```

File name becomes the command name. `brief.md` becomes `/brief`. Hyphens work: `daily-report.md` becomes `/daily-report`. Files prefixed with `_` are shared references, not invocable commands.

---

## Frontmatter Fields

```yaml
---
allowed-tools: Glob, Grep, Read, Write, WebSearch
argument-hint: <topic> [--dry-run]
description: Generate a content summary from a URL or file path
---
```

| Field | Required | Purpose |
|-------|----------|---------|
| `allowed-tools` | Yes | Tools the skill can use. Claude Code enforces this boundary. |
| `argument-hint` | No | Shows in help text. Describes expected arguments. |
| `description` | Yes | One-line description shown in skill listings. |

`allowed-tools` acts as a permission boundary. A skill with `Read, Glob` cannot write files. Scope tightly.

---

## Step Structure

Number steps explicitly. Each step describes one discrete action with expected behavior.

```markdown
### Step 1: Load context
Read `./README.md`. Extract: project name, primary language, purpose.

### Step 2: Search for related files
Glob: `src/**/*.ts`. Grep in results for: `export default`.

### Step 3: Generate summary
Write summary covering: project purpose (1 sentence), file count, key exports from Step 2.

### Step 4: Output
Write to `./docs/summary.md`. Report to user: file path, word count.
```

Steps should be deterministic. "Analyze the codebase" is vague. "Grep for `export default` in all `.ts` files" is executable.

---

## Output Format

Always specify exact output structure. Without it, you get different formats each run.

```markdown
\```markdown
# Summary: {project_name}
**Generated:** {YYYY.MM.DD}
## Overview
{2-3 sentences}
## Key Components
| Component | File | Purpose |
|-----------|------|---------|
{one row per export found}
\```
```

---

## Arguments

User input after the command is available as `$ARGUMENTS`. Reference it explicitly:

```markdown
### Step 1: Parse input
`/summarize $ARGUMENTS` — determine if argument is URL (starts with http) or file path. Check for `--dry-run` flag.
```

---

## Self-Repair

Skills break when files move or folders get renamed. A self-repair section makes skills resilient.

Add to any skill:

```markdown
## Self-Repair Protocol
**Reference:** `.claude/commands/_skill-repair-protocol.md`

### Breakable References
| Reference | Current Path | Failure Code |
|-----------|-------------|--------------|
| Config file | `./config/settings.json` | PATH_MOVED |
| Output directory | `./reports/` | FOLDER_MISSING |

### Failure Modes
| Failure | Detection | Auto-Fix |
|---------|-----------|----------|
| Config moved | Read returns error | Glob for `**/settings.json`, update path |
| Output dir missing | Write fails | `mkdir -p`, retry |
```

The shared `_skill-repair-protocol.md` defines universal repair logic: failure taxonomy, resolution order, repair limits, and logging. Failure codes: `PATH_MOVED`, `PATH_GONE`, `FOLDER_MISSING`, `TOOL_UNAVAILABLE`, `EMPTY_RESULT`.

---

## Full Example: /summarize

```markdown
---
allowed-tools: Read, Write, Glob, WebFetch
argument-hint: <url-or-path> [--dry-run]
description: Summarize a URL or local file into structured markdown
---

# Summarize

### Step 1: Parse arguments
Input: `$ARGUMENTS`. URL (starts with `http`) uses WebFetch. Otherwise Read local file. Check for `--dry-run`.

### Step 2: Fetch content
**URL:** WebFetch, extract title + headings + body.
**File:** Read contents directly.

### Step 3: Generate summary
Title, 3-5 sentence overview, key points (max 10), word count of source.

### Step 4: Write output
**If `--dry-run`:** display in chat, stop.
**Otherwise:** write to `./docs/summaries/{slugified-title}.md`

### Step 5: Report
File path (or dry-run notice), word count, source type.

---

## Self-Repair Protocol
**Reference:** `.claude/commands/_skill-repair-protocol.md`

### Breakable References
| Reference | Current Path | Failure Code |
|-----------|-------------|--------------|
| Output directory | `./docs/summaries/` | FOLDER_MISSING |

### Failure Modes
| Failure | Detection | Auto-Fix |
|---------|-----------|----------|
| Output dir missing | Write fails | mkdir -p, retry |
| URL unreachable | WebFetch error | Report to user |
| File not found | Read error | Glob for filename, retry once |
```

---

## Tips

- **Be explicit about paths.** Absolute paths are unambiguous. Prefer them when the vault location is known.
- **Use `$ARGUMENTS` for user input.** Don't make the skill ask follow-up questions if input can be passed inline.
- **Scope `allowed-tools` tightly.** A read-only skill should not list Write.
- **Name steps with verbs.** "Load context" not "Context."
- **Test the failure path.** Rename a referenced file and run the skill. Does it recover or crash silently?
- **Keep skills under 200 lines.** If a skill exceeds that, it is probably two skills.
