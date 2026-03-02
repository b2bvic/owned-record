# Vault-as-Memory

> Your vault becomes searchable memory. Every file has an address. Every thought can be found.

---

## The Problem

LLMs forget everything between sessions. Every conversation starts fresh. You re-explain context, re-share preferences, re-establish rules. The knowledge exists somewhere in your notes. The model cannot find it.

Copy-pasting context does not scale. Context grows. Conversations vary. What Task A requires differs from Task B.

## The Solution

Structure your knowledge base as searchable memory for an LLM. Files become addressable thoughts. Folders become domains of knowledge. Context files act as memory indexes. Logs preserve continuity.

The vault becomes the brain. The LLM reads what it needs, when it needs it.

---

## Architecture

```
YourVault/
├── CLAUDE.md              # Memory index (always loaded first)
├── _RECENT.md             # Short-term memory (last 24h)
├── .claude/               # Claude Code config
│   └── settings.local.json
├── 00 - System/           # LLM working memory
│   ├── _context.md        # Self-referential context
│   ├── _log.md            # Activity trace
│   ├── Sessions/          # Captured outputs worth keeping
│   ├── Patterns/          # Reusable solutions
│   └── Reference/         # Persistent knowledge
├── 01 - Work/             # First knowledge domain
│   ├── _context.md        # Domain memory index
│   └── _log.md            # Domain activity trace
├── 02 - Personal/         # Second knowledge domain
│   ├── _context.md
│   └── _log.md
└── ...
```

Every folder is a memory region. Every `_context.md` is an index into that region. Every `_log.md` preserves what happened there.

---

## Core Components

### 1. CLAUDE.md — Memory Index

The master index. The LLM reads this first. It answers: who are you working with, what do they care about, where is everything stored?

Contains:

| Section | Purpose |
|---------|---------|
| **WHO** | User identity, roles, schedule |
| **WHEN** | Current date (timestamp for this memory state) |
| **WHAT** | Domain routing table (keyword triggers to memory regions) |
| **VOICE** | Output calibration rules |
| **NOW** | Current state snapshot (live memory of what's active) |
| **HOW** | Operating instructions |
| **RULES** | Universal constraints |

Keep this file between 200-400 lines. Dense and scannable.

### 2. Domain _context.md — Regional Memory Indexes

Each domain has its own index. Loaded when keywords match. They tell the LLM what to know about a specific region:

- Domain purpose and scope
- Active projects/entities
- Domain-specific rules
- Tool/API access notes
- Current blockers or warnings

Think of these as table of contents for memory regions.

### 3. Domain _log.md — Memory Traces

Reverse-chronological activity logs. Preserve what happened so future sessions can recall it.

```markdown
## 2026.01.15

**Work Done**
- Completed database migration for Project Alpha
- Files: `01 - Work/Projects/alpha-migration.md`
- Decision: chose PostgreSQL over MySQL (latency benchmarks in Reference/)

**Blockers/Notes**
- Staging environment down until Thursday
```

### 4. _RECENT.md — Short-Term Memory

Auto-generated list of files modified in the last 24 hours. Recency bias, formalized. The LLM sees what's "hot" without searching the entire vault.

```bash
find "/path/to/vault" -name "*.md" -type f -mmin -1440 \
  | grep -v node_modules | grep -v ".obsidian"
```

### 5. System Folder — Working Memory

The LLM's own memory region for persisting outputs worth keeping:

| Folder | Purpose |
|--------|---------|
| `Sessions/` | Captured outputs worth finding later |
| `Patterns/` | Solutions that worked once, searchable for reuse |
| `Reference/` | Persistent knowledge: decisions, preferences, specs |

This is where the LLM writes to memory, not just reads from it.

---

## Domain Routing

The core mechanism. Your words trigger memory access.

CLAUDE.md contains a routing table:

```markdown
| Domain | Context File | Load when prompt mentions... |
|--------|--------------|------------------------------|
| **Work** | `01 - Work/_context.md` | project, client, deadline, sprint |
| **Personal** | `02 - Personal/_context.md` | budget, health, family, task |
| **Research** | `03 - Research/_context.md` | paper, hypothesis, dataset, experiment |
```

The LLM matches keywords in your prompt to domains, then loads the relevant `_context.md`. You say "client," it finds the client knowledge.

---

## Setup Guide

### Step 1: Create Folder Structure

```
YourVault/
├── CLAUDE.md
├── _RECENT.md
├── 00 - System/
│   ├── _context.md
│   ├── _log.md
│   ├── Sessions/
│   ├── Patterns/
│   └── Reference/
├── 01 - [DOMAIN-1]/
│   ├── _context.md
│   └── _log.md
├── 02 - [DOMAIN-2]/
│   ├── _context.md
│   └── _log.md
```

### Step 2: Write CLAUDE.md

1. Fill in WHO section with your identity/roles
2. Define your domains and routing keywords
3. Establish VOICE rules (how the LLM should write)
4. Document date format, file naming, etc.
5. Add universal rules that apply everywhere

### Step 3: Write Domain _context.md Files

For each domain:
1. One-line purpose statement
2. Current active work
3. Domain-specific rules and constraints
4. Tool access notes
5. Known issues or warnings

### Step 4: Initialize

```bash
cd /path/to/YourVault
claude
```

Claude Code auto-reads CLAUDE.md on session start.

### Step 5: Establish Logging

After significant sessions, tell Claude: "Log this session."

The LLM updates domain `_log.md` with work done, the NOW section if state changed, and any session artifacts worth preserving.

---

## Templates

### CLAUDE.md Template

```markdown
# [Your Name]'s Vault

---

## WHO
[Your name]. [Brief role description].

## WHEN
Today: YYYY.MM.DD

## WHAT (Domains)

| Domain | Context File | Load when prompt mentions... |
|--------|--------------|------------------------------|
| **[DOMAIN-1]** | `01 - [Name]/_context.md` | keyword1, keyword2, keyword3 |
| **[DOMAIN-2]** | `02 - [Name]/_context.md` | keyword1, keyword2, keyword3 |

## VOICE
1. No sycophancy — don't open with agreement or praise
2. Dense output — no filler phrases
3. [Your rules]

## NOW (Current State)
**[DOMAIN-1]:** [Current status, blockers, active work]
**[DOMAIN-2]:** [Current status, blockers, active work]

## HOW
1. Route first — match keywords to domain, READ that _context.md
2. Check recency — READ _RECENT.md for recently modified files
3. Update state — after significant work, update NOW section

## RULES
1. Read before edit — never modify without reading first
2. No assumptions — ask if unclear
3. Date format — YYYY.MM.DD (dots not dashes)
```

### Domain _context.md Template

```markdown
# [Domain Name] Context

> [One-line purpose]

---

## CURRENT STATE
**Active:** [What's in progress]
**Blocked:** [Any blockers or warnings]
**Next:** [Upcoming priorities]

## RULES (Domain-Specific)
1. [Rule 1]
2. [Rule 2]

## TOOLS & ACCESS

| Tool | Access | Notes |
|------|--------|-------|
| [Tool] | [How to access] | [Constraints] |

## KEY ENTITIES

| Entity | Context |
|--------|---------|
| [Person/Project] | [Brief context] |
```

---

## Best Practices

### Keep CLAUDE.md Scannable
Under 400 lines. Use tables. The LLM reads this every session. Make it fast to parse.

### Frontload Domain Keywords
More keywords = better routing accuracy. Include proper nouns (people, projects, tools), verbs you use (cleanup, review, schedule), and domain jargon.

### Date Format Consistency
Pick one format. Use it everywhere. `YYYY.MM.DD` recommended — sorts correctly, no ambiguity.

### Update NOW After Sessions
The NOW section is live memory. Update it after significant work. Next session reads it.

### Don't Over-Log
Logs are for searchable continuity, not documentation. Reference material belongs in Reference/. Reusable patterns belong in Patterns/. Logs are timestamped activity traces.

### Protect Vault Integrity
Knowledge bases with cloud sync are fragile to bulk file operations. Moving/renaming/deleting files can corrupt indexes. Warn the LLM about this in RULES.

---

## Failure Modes

### Context Overload
**Symptom:** LLM gets confused, mixes domains, gives generic responses.
**Cause:** Too much loaded at once.
**Fix:** Tighten routing keywords. Make domain boundaries clearer.

### Stale State
**Symptom:** LLM references outdated information.
**Cause:** NOW section not updated.
**Fix:** Update NOW after significant sessions. Make it a habit.

### Routing Misses
**Symptom:** LLM doesn't load context when it should.
**Cause:** Keywords don't match prompt language.
**Fix:** Add more keywords to routing table. Use terms you actually use.

### Log Bloat
**Symptom:** Logs become unreadable, too much noise.
**Cause:** Logging trivial activity.
**Fix:** Only log state changes, decisions, blockers. Not every action.

---

## Why This Works

1. **Searchable memory** — every file has an address, keywords trigger retrieval
2. **Progressive disclosure** — context loads on-demand, not all at once
3. **Persistent state** — NOW section and logs carry information forward
4. **Two-way memory** — the LLM reads from and writes to the vault
5. **Self-indexing** — context files explain the vault to the LLM

The vault becomes a shared brain. You write for yourself and for the LLM. The LLM searches for what it needs and writes what should persist.
