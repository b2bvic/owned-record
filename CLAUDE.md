# {{PROJECT_NAME}}

> Claude Code project instructions. This file is loaded automatically at the start of every session.

---

## WHO

{{YOUR_NAME}}. {{ONE_LINE_DESCRIPTION}}.

---

## WHAT (Domains)

| Domain | Context File | Triggers (keywords) |
|--------|--------------|---------------------|
| **Work** | `01 - Work/_context.md` | project, deadline, meeting, standup, sprint |
| **Personal** | `02 - Personal/_context.md` | family, health, budget, journal, home |

> Add more domains by editing this table AND `.claude/hooks/route-domain.sh`.

---

## VOICE

Default voice calibration. Edit these rules to match how you want Claude to communicate.

1. **No sycophancy** — Don't open with agreement or praise
2. **No filler** — Cut "Let me unpack," "It's worth noting," "That said"
3. **Dense output** — No fluff, no disclaimers
4. **Read before edit** — Never modify a file without reading it first
5. **Ask if unclear** — Don't guess, don't assume

---

## NOW (Current State)

Update this section as your situation evolves. Claude reads it every session.

**Work:** (current work priorities)
**Personal:** (current personal state)
**System:** Hooks active (domain routing + semantic memory). QMD indexed.

---

## SEARCH (Vault Content)

**Default to QMD for vault searches** when available.

| Need | Tool | Example |
|------|------|---------|
| Keyword/exact | `mcp__qmd__search` | `type:: deliverable` |
| Conceptual | `mcp__qmd__vsearch` | "files about project planning" |
| Best quality | `mcp__qmd__query` | "how does the routing hook work" |
| Get full file | `mcp__qmd__get` | `file: "path/to/file.md"` |

**Fallback to Glob/Grep** if QMD is unavailable or returns no results.

---

## HOW

### Session Orientation

When starting a session, find recently modified files:

```bash
find "$(pwd)" -name "*.md" -type f -mmin -1440 \
  -not -path "*/node_modules/*" \
  -not -path "*/.obsidian/*" \
  | sort
```

Then read the relevant ones. Synthesize after.

### Standard Operation

1. **Route first** — Match prompt keywords to domain, read that `_context.md`
2. **Search with QMD** — Before Glob/Grep
3. **Read actual files** — Don't rely on summaries
4. **Update state** — After significant work, update the NOW section

---

## RULES

1. **Read before edit** — Never modify a file without reading it first
2. **No assumptions** — Ask if unclear
3. **Date format** — `YYYY.MM.DD` (dots, not dashes)
4. **Frontmatter format** — `field:: value` (double colon, space)
5. **Corrections are permanent** — When you correct a fact, propagate to all files containing the old info
6. **Confirm before bulk edits** — Before modifying 3+ files, state planned changes and wait for approval

---

## KEY FILES

| File | Purpose |
|------|---------|
| `_RECENT.md` | Files modified in last 24h |
| `{domain}/_context.md` | Domain-specific rules and state |
| `{domain}/_log.md` | Domain activity log |
| `00 - System/Sessions/` | Valuable session outputs |
| `00 - System/Patterns/` | Reusable solutions |
| `00 - System/Reference/Ground-Truth.md` | Permanent factual corrections |

---

## SLASH COMMANDS

Commands in `.claude/commands/` — invoke with `/command-name`.

### Thinking Frameworks

| Command | When to Use |
|---------|-------------|
| `/consider-pareto` | Which 20% drives 80% of results? |
| `/consider-first-principles` | Rebuild from ground truth |
| `/consider-inversion` | What could go wrong? |
| `/consider-second-order` | What happens after the first result? |
| `/consider-5-whys` | Root cause analysis |
| `/consider-eisenhower` | Urgency vs importance |
| `/consider-occam` | Simplest explanation |
| `/consider-one-thing` | What single action unlocks everything? |
| `/consider-swot` | Strengths, weaknesses, opportunities, threats |
| `/consider-10-10-10` | 10 minutes / 10 months / 10 years |
| `/consider-opportunity-cost` | What am I giving up? |
| `/consider-via-negativa` | Improve by subtraction |

### Utilities

| Command | What It Does |
|---------|--------------|
| `/deliberate` | Multi-agent debate on a decision |
| `/handoff` | Session continuity — capture state for next session |
| `/log` | Update session log with current work |
| `/morning` | Generate daily dashboard |
| `/review` | Generate weekly review |
| `/scrape-deep` | Multi-tier URL fetching |
| `/web2md` | Convert web page to markdown |

---

## Vault Structure

```
{{PROJECT_NAME}}/
├── CLAUDE.md              ← You are here
├── _RECENT.md             ← Recently modified files
├── .claude/
│   ├── settings.json      ← Hook configuration
│   ├── hooks/             ← Domain routing + semantic memory
│   └── commands/          ← Slash commands (skills)
├── 00 - System/           ← Claude's operational state
│   ├── _context.md
│   ├── _log.md
│   ├── Sessions/          ← Full session outputs
│   ├── Patterns/          ← Reusable solutions
│   └── Reference/         ← Ground truth corrections
├── 01 - Work/             ← Your work domain
│   ├── _context.md
│   └── _log.md
└── 02 - Personal/         ← Your personal domain
    ├── _context.md
    └── _log.md
```

> Add more domain folders as needed. Each domain needs `_context.md` and `_log.md`.
> Update `route-domain.sh` with keywords for each new domain.
