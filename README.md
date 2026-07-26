# SubtleBodhi

A public reference architecture for persistent agent memory, domain routing, and durable operating state inside an Obsidian or Markdown vault.

Part of a larger system: this repository demonstrates **P05 (semantic order lowers retrieval cost)**, **P14 (authority is structured coverage over time)**, and **P16 (one person, one canon, many surfaces)** from the [Seventeen Principles](https://victorvalentineromo.com/principles).

This repository is the architecture layer. It shows how prompts route to bounded domain context, how each domain carries current state and an activity trace, how local retrieval can add relevant memory before a tool call, and how reusable skills become filesystem artifacts instead of one-off prompt text.

> **Repository boundary:** This is a genericized, Claude-first reference snapshot. It is not Victor's current private vault or an exact copy of the current provider/runtime stack. Private data, credentials, customer material, and deployment automation are omitted. The operating system has continued to evolve since this public extraction.

If you arrived through `github.com/b2bvic/scale-with-search`, GitHub redirected you here because the repository was renamed. The redirect remains intentional so older application and portfolio links still land on a useful technical surface.

## Implementation proof path

SubtleBodhi explains the system pattern. These smaller repositories expose bounded implementations that are faster to review:

1. [pretool-memory](https://github.com/b2bvic/pretool-memory): transcript-tail retrieval, local BM25 and FTS5 lookup, throttling, hash deduplication, and fail-open behavior.
2. [safe-api](https://github.com/b2bvic/safe-api): dry-run mutation controls, endpoint scope, duplicate callbacks, circuit breakers, incident artifacts, and JSONL receipts.
3. [declip](https://github.com/b2bvic/declip): a local-first Apple Silicon video CLI for transcription, filler removal, gap compression, EQ, and NLE/SRT export.
4. [observer-protocol](https://github.com/b2bvic/observer-protocol): approval gates, correction history, drift detection, and observable agent loops.

## What this reference implements

- **Domain routing:** a `UserPromptSubmit` hook maps prompt keywords to a bounded `_context.md` file.
- **Persistent state:** each domain carries `_context.md` for current state and `_log.md` for durable activity history.
- **Local recall:** an optional `PreToolUse` hook searches a local Markdown index and session ledger before read-oriented tools.
- **Reusable skills:** command files hold repeatable procedures, decision frameworks, session handoffs, reviews, and utilities.
- **Ground-truth corrections:** a reference surface records durable corrections that future sessions can load.

## Quick start

```bash
git clone https://github.com/b2bvic/subtlebodhi.git
cd subtlebodhi
bash scripts/setup.sh
claude
```

The setup script asks for a name, project name, and domain structure. It replaces template placeholders, creates domain folders, updates the domain table and routing hook, makes hooks executable, and leaves the configured vault in the cloned directory.

Review `scripts/setup.sh` before running it. Use a fresh clone or a backed-up vault because the script edits local template files.

## Manual setup

1. Copy the reference into an Obsidian vault or Markdown directory.
2. Replace the placeholders in `CLAUDE.md`.
3. Customize the keyword and path rules in `.claude/hooks/route-domain.sh`.
4. Put current state in each domain's `_context.md` and append durable activity to `_log.md`.
5. Make the hooks executable with `chmod +x .claude/hooks/*.sh`.
6. Configure only the hooks and commands you intend to run.

## Repository map

```text
subtlebodhi/
├── CLAUDE.md
├── _RECENT.md
├── .claude/
│   ├── settings.json
│   ├── hooks/
│   │   ├── route-domain.sh
│   │   └── pretool-memory.sh
│   └── commands/
├── 00 - System/
│   ├── Sessions/
│   ├── Patterns/
│   └── Reference/
├── 01 - Work/
├── 02 - Personal/
├── docs/
└── scripts/setup.sh
```

## Domain routing

```text
"review the sprint backlog"
  -> route-domain.sh matches a work-domain keyword
  -> the work _context.md is added to the prompt context
  -> the response starts from current domain state
```

Keyword routing is deterministic and inspectable. It is also heuristic. Ambiguous terms can load the wrong domain, so high-risk work still needs explicit context and authorization checks.

## Local memory

```text
assistant thinking block
  -> PreToolUse hook reads a bounded transcript tail
  -> QMD BM25 searches the local Markdown collection
  -> optional SQLite FTS5 searches prior session text
  -> relevant results are injected before a read-oriented tool
```

The included hook is a reference copy. The maintained, tested extraction is [pretool-memory](https://github.com/b2bvic/pretool-memory).

## Skills

The command directory includes decision frameworks, deliberation, handoff and logging procedures, daily and weekly reviews, deep scraping, and web-to-Markdown conversion. Start with [the skill authoring guide](docs/skill-authoring.md) before adding new commands.

## Documentation

- [Vault as memory](docs/vault-as-memory.md)
- [Context routing](docs/context-routing.md)
- [Recursive language system](docs/recursive-language-system.md)
- [Skill authoring](docs/skill-authoring.md)

## Non-guarantees

- The template does not ship a private corpus, QMD index, session ledger, credentials, or hosted service.
- Local retrieval does not guarantee relevant or correct context.
- Keyword routing does not enforce security boundaries.
- Command files do not replace capability-level approval gates for sends, publishing, deletion, payments, or production writes.
- The public Claude-first layout is a reference snapshot, not a promise that the current private system uses the same model, paths, counts, or automation surfaces.

## Origin

SubtleBodhi was extracted from a working private knowledge system and stripped of Victor-specific data. The useful artifact is the pattern: owned Markdown memory, bounded context, observable state, reusable procedures, and explicit side-effect gates.

## License

MIT

Built by [Victor Valentine Romo](https://victorvalentineromo.com).

## How this was built

Specification and judgment: human. Implementation: AI models executing that specification under a build contract, with an adversarial audit before publish. The division of labor is the point; see [P07](https://victorvalentineromo.com/principles).
