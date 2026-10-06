# Owned Record

Owned Record keeps agent context, source readings, and activity logs in files you control.
You use Markdown for current state, visible exchanges, retrieved pages, and writing samples.
You use SQLite and JSON exports when you need searchable transcript records with tool activity.

[Project page](https://scalewithsearch.com/code/owned-record)

## Install

Use Git, Bash, and Python 3.11 or newer.
The shell hooks require `jq`; recall also requires a configured [QMD](https://github.com/tobi/qmd) collection.
Web conversion uses the dependencies in [requirements-dev.txt](components/web2md/requirements-dev.txt).

```sh
git clone https://github.com/b2bvic/owned-record.git
cd owned-record
```

Each component runs from its own folder.
Review its configuration and data boundaries before installing it.
Cloning the repository does not activate optional hooks or install background jobs.

## Quick start

Run the supplied examples with synthetic inputs:

```sh
bash examples/demo.sh
bash components/cc-bridge/examples/demo.sh
bash components/pretool-memory/examples/demo.sh
bash components/voice-calibration/examples/demo.sh
```

The first demo emits a Work candidate with `context_loaded: false`.
The other demos show Markdown export, memory recall, and writing sample retrieval without model credentials.

The existing reference stays at the repository root:

- `_context.md` holds each domain's current state.
- `_log.md` holds each domain's activity history.
- `.agent-oversight/domains.json` maps keywords to candidate domain paths.
- `.claude/hooks/route_domain.py` emits paths without reading context bodies.
- `.claude/commands/` contains reusable procedures.

To personalize a fresh reference, review and run `bash scripts/setup.sh`.
Setup replaces template placeholders and preserves existing custom context files.
Review `CLAUDE.md`, the domain map, and `.claude/settings.json` before starting Claude Code.
The default hook uses pointer routing; recall stays opt-in.
See [context routing](docs/context-routing.md) and [the memory reference](docs/vault-as-memory.md).

## Components

| Stage | Component | Purpose |
|---|---|---|
| Capture | [session-ledger](#session-ledger) | Archive Claude Code and Codex transcripts in SQLite and export JSON. |
| Capture | [cc-bridge](#cc-bridge) | Convert visible Claude Code exchanges to daily Markdown logs. |
| Capture | [web2md](#web2md) | Save returned web content as source-attributed Markdown. |
| Route and retrieve | [route-domain](#route-domain) | Load configured context files for matching prompt keywords. |
| Route and retrieve | [pretool-memory](#pretool-memory) | Retrieve owned records before selected read tools. |
| Voice | [voice-calibration](#voice-calibration) | Retrieve writing samples before Write and Edit calls. |

<a id="session-ledger"></a>

## session-ledger

You archive local Claude Code and Codex CLI transcripts with [session-ledger](components/session-ledger/README.md).
The standard-library CLI stores messages, tool records, file operations, and parse errors in SQLite with FTS5 search.
JSON exports preserve provider identities and parsed source records.
Use `harvest --dry-run --source all` before importing your own history.
Read each coverage receipt; a successful command does not prove complete coverage.

<a id="cc-bridge"></a>

## cc-bridge

You convert Claude Code exchanges to daily Markdown with [cc-bridge](components/cc-bridge/README.md).
Set `CC_BRIDGE_PROJECT`, `CC_BRIDGE_OUTPUT`, and `CC_BRIDGE_STATE` to select your input, output, and resume state.
Each invocation processes the newest root-level transcript in one project.
The export omits thinking and tool results, and truncates assistant text after 2,000 characters per exchange.
Retain the original transcripts when you need complete source history.

<a id="web2md"></a>

## web2md

You convert returned HTML to source-attributed Markdown with [web2md](components/web2md/README.md).
The CLI removes configured boilerplate and retains headings, lists, tables, links, and code blocks.
Use its synthetic quick start before fetching a page.
It does not execute JavaScript; relative links stay relative, and boilerplate removal can discard useful content.

<a id="route-domain"></a>

## route-domain

You map prompt keywords to configured context files with [route-domain](components/route-domain/README.md).
This optional shell hook loads complete matching context bodies and can load several domains for one prompt.
Review its example paths and disclosure rules before registering it.
The root reference's Python router emits candidate paths and remains the default.
Neither router establishes intent or authorization.

<a id="pretool-memory"></a>

## pretool-memory

You retrieve owned records before selected read tools with [pretool-memory](components/pretool-memory/README.md).
The optional hook derives a query from recent thinking, searches QMD, and can query a compatible SQLite ledger.
Set `QMD_BIN` and `LEDGER_DB` to select your sources.
Recall requires readable thinking and can return unsuitable context.
Retrieved text remains untrusted evidence and can enter a hosted-model session after you enable the hook.

<a id="voice-calibration"></a>

## voice-calibration

You retrieve genre-specific writing samples with [voice-calibration](components/voice-calibration/README.md).
The optional hook matches Write and Edit target paths against fixed genre patterns and queries QMD.
Review its patterns, queries, and sample collection before enabling it.
Samples provide examples without guaranteeing a voice match or authorizing a write.

## Portability and limits

Your Markdown files, source transcripts, SQLite database, and JSON exports remain readable outside the original session.
Carry the original records when changing clients, then configure the next client's parser and retrieval adapter.
The supplied hook adapters target Claude Code; portable data does not prove client compatibility.
The reference supplies sample domains and procedures, without a private corpus or hosted service.
It does not implement capability-level approval gates for external actions.

## Verify

Run the root checks and each standard-library component suite:

```sh
python3 -m unittest discover -s tests -v
bash tests/test_setup.sh
for component in session-ledger cc-bridge route-domain pretool-memory voice-calibration; do
  (cd "components/$component" && python3 -m unittest discover -s tests -v) || exit 1
done
shellcheck scripts/setup.sh .claude/hooks/*.sh tests/test_setup.sh examples/demo.sh
ruff check --select F,E9 scripts .claude/hooks/route_domain.py tests
```

Run web conversion checks in a local environment:

```sh
python3 -m venv components/web2md/.venv
components/web2md/.venv/bin/python -m pip install -r components/web2md/requirements-dev.txt
(cd components/web2md && .venv/bin/python -m pytest -q)
```

Install ShellCheck and Ruff 0.16.10 for lint.
The root workflow runs the reference and all component suites.
Imported workflows under component folders remain source records; GitHub runs workflows only from the root `.github/workflows/`.

## Model assistance

The session-ledger and route-domain source READMEs include this disclosure:

> This README was written with model assistance in 2026. The code and tests in this repository are the evidence; read them to judge the tool.

Their component READMEs retain the disclosure.
This consolidated README also uses model assistance.

## Related projects

- [agent-oversight](https://github.com/b2bvic/agent-oversight): Agent supervision, review, and effect boundaries.
- [vault-crawl](https://github.com/b2bvic/vault-crawl): Source retrieval with provenance.

## License

MIT. The reference and all six components use MIT licenses.
The root [LICENSE](LICENSE) and each component's license remain in place.
