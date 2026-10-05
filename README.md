# Owned AI agent memory in Markdown: owned-record

Owned Record keeps agent context and activity logs in Markdown for operators and teams using hosted models.
Use it when each new session needs the correct project and decision history.

[Project page](https://scalewithsearch.com/code/owned-record)

## Install

Requirements: Git, Bash, and Python 3. Claude Code is required to use the supplied hook integration.

```sh
git clone https://github.com/b2bvic/owned-record.git
cd owned-record
```

## Quick start

Run the routing demo before editing the reference:

```sh
bash examples/demo.sh
```

The demo emits a `Work` candidate with `context_loaded: false`.
It does not read `_context.md` bodies or start a model session.

To personalize a fresh clone, review the setup script first:

```sh
bash scripts/setup.sh
```

Setup asks for a name, project, and additional domains.
It replaces remaining template placeholders and keeps existing custom context files.
Review `CLAUDE.md`, `.agent-oversight/domains.json`, and `.claude/settings.json` before starting Claude Code.

## How it works

The reference supplies patterns a team can adopt for persistent memory for AI agents.
Its Markdown context engineering separates current state from activity history:

- `_context.md` holds each domain's current context.
- `_log.md` holds each domain's activity history.
- `.agent-oversight/domains.json` maps keywords to domain directories.
- `.claude/hooks/route_domain.py` emits candidate paths for matched, ambiguous, or unmatched prompts.
- `.claude/commands/` contains reusable procedures.

Default settings enable pointer routing through `UserPromptSubmit`.
The optional memory hook remains disabled until you configure it.
The model or user selects a candidate before reading its record.
See [context routing](docs/context-routing.md) and [the memory reference](docs/vault-as-memory.md).

## Portability

Portable agent context resides in UTF-8 Markdown files and a JSON domain map.
The export path is the reference directory itself; there is no separate export command.
Copy the domain folders, procedures, correction records, and domain map when changing model vendors.
Preserve hidden configuration files when copying the directory.

The Markdown records remain readable without Claude Code.
Configure a new client's adapter and instruction files separately.
The supplied hook integration targets Claude Code; data portability does not prove compatibility with another client.

## Limits

- This is a single-operator reference snapshot with generic sample domains.
- The repository does not include a private corpus, hosted service, or installed QMD index.
- Keyword matches can be ambiguous or miss relevant records.
- Candidate paths do not enforce authorization or load context bodies.
- Optional recall can send selected records into a hosted-model session.
- Procedures do not implement capability-level approval gates for external actions.

## Verify

```sh
python3 -m unittest discover -s tests -v
bash tests/test_setup.sh
shellcheck scripts/setup.sh .claude/hooks/*.sh tests/test_setup.sh examples/demo.sh
ruff check --select F,E9 scripts .claude/hooks/route_domain.py tests
```

Install ShellCheck and Ruff 0.16.10 for the lint commands.

## Related repositories

- [pretool-memory](https://github.com/b2bvic/pretool-memory): Recall owned records before selected tool calls.
- [vault-crawl](https://github.com/b2bvic/vault-crawl): Retrieve source material and preserve provenance.
- [cc-bridge](https://github.com/b2bvic/cc-bridge): Convert transcript exchanges to Markdown logs.
- [voice-calibration](https://github.com/b2bvic/voice-calibration): Recall writing samples for a target file genre.

## License

MIT. See [LICENSE](LICENSE).
