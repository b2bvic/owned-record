# owned-record

Keep what your agents know in files you control. Domain context lives in Markdown, Claude Code and Codex CLI transcripts land in a SQLite database with full-text search, and three opt-in hooks hand the right file or search result to Claude Code before it acts.
When you change model, vendor, or client, the Markdown, the database, and the JSON exports stay where they are.

[Project page](https://scalewithsearch.com/code/owned-record)

A hosted-model session starts without your business context unless you supply it, and the vendor's transcript format is the only record of what was decided.
This repository is a reference vault you can personalize plus six components: three that capture records, two that route and retrieve them, and one that supplies writing samples.

## Quick start

Use Git, Bash, and Python 3.11 or newer. The shell hooks need `jq`; recall needs a [QMD](https://github.com/tobi/qmd) collection.

```bash
git clone https://github.com/b2bvic/owned-record.git
cd owned-record
bash examples/demo.sh
```

The demo sends the prompt `review sprint backlog` through the routing hook. It returns the `01 - Work` candidate with `context_loaded: false`; the hook names the file and reads nothing.

Archive transcripts into an empty, isolated database:

```bash
cd components/session-ledger
demo_record=$(mktemp -d)
mkdir -p "$demo_record/claude/projects" "$demo_record/codex/sessions"
export LEDGER_DB="$demo_record/sessions.db" LEDGER_CLAUDE="$demo_record/claude" LEDGER_CODEX="$demo_record/codex"
unset LEDGER_PROJECT LEDGER_VAULT
python3 ./ledger init
python3 ./ledger harvest --source all
python3 ./ledger search "authentication bug"
```

The empty run reports unknown coverage and no matches. Point `LEDGER_CLAUDE` at `~/.claude` and `LEDGER_CODEX` at `~/.codex` when you want your own history, and run `harvest --dry-run --source all` first.

Run the other component demos; each uses synthetic input and a mock QMD, and none needs model credentials:

```bash
cd ../..
bash components/cc-bridge/examples/demo.sh
bash components/pretool-memory/examples/demo.sh
bash components/voice-calibration/examples/demo.sh
```

## The reference vault

The repository root is a working Claude Code project. `CLAUDE.md` holds the domain table, voice rules, and a `NOW` section. `01 - Work/` and `02 - Personal/` each hold `_context.md` for current state and `_log.md` for history. `.agent-oversight/domains.json` maps keywords to domain folders. `.claude/commands/` holds 20 command files, including 12 `/consider-*` thinking frameworks.

`bash scripts/setup.sh` asks for your name, project, and extra domains, then fills the placeholders and extends `domains.json`. It keeps any `_context.md` you already edited.
The only hook registered in `.claude/settings.json` is the pointer router. Cloning installs no background job and enables no recall. See [context routing](docs/context-routing.md) and [vault as memory](docs/vault-as-memory.md).

## Components

| Stage | Component | Purpose |
|---|---|---|
| Capture | [session-ledger](#session-ledger) | Archive Claude Code and Codex transcripts in SQLite; export JSON. |
| Capture | [cc-bridge](#cc-bridge) | Convert visible Claude Code exchanges to daily Markdown logs. |
| Capture | [web2md](#web2md) | Save fetched web pages as source-attributed Markdown. |
| Route and retrieve | [route-domain](#route-domain) | Load matching context files into the prompt by keyword. |
| Route and retrieve | [pretool-memory](#pretool-memory) | Search owned records before Read, Grep, and other read tools. |
| Voice | [voice-calibration](#voice-calibration) | Supply writing samples before Write and Edit calls. |

<a id="session-ledger"></a>

## session-ledger

A standard-library CLI that imports local Claude Code and Codex CLI JSONL transcripts into SQLite with FTS5 search.
`ledger` stores messages, tool records, file operations, and parse errors, keeps the two providers separate when session identifiers collide, and exports JSON.
Read each coverage receipt; a zero exit does not mean complete coverage. [README](components/session-ledger/README.md)

<a id="cc-bridge"></a>

## cc-bridge

Converts the newest transcript in one Claude Code project into `YYYY.MM.DD.md` logs of visible exchanges.
Set `CC_BRIDGE_PROJECT`, `CC_BRIDGE_OUTPUT`, and `CC_BRIDGE_STATE`. The export omits thinking and tool results and truncates assistant text at 2,000 characters per exchange, so keep the original JSONL. [README](components/cc-bridge/README.md)

<a id="web2md"></a>

## web2md

Fetches a page, strips configured boilerplate, and writes Markdown with the source URL and fetch date.
It does not execute JavaScript, and boilerplate removal can drop useful content. [README](components/web2md/README.md)

<a id="route-domain"></a>

## route-domain

A `UserPromptSubmit` hook that matches prompt keywords against configured domains and places the full body of each matching `_context.md` in `additionalContext`.
It can load several domains for one prompt. The root vault ships the pointer router instead; switch to this hook after you review what each context file discloses. [README](components/route-domain/README.md)

<a id="pretool-memory"></a>

## pretool-memory

A `PreToolUse` hook for `Read`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, and `Task`. It derives a query from the last 1,500 bytes of recent thinking, runs QMD search for up to three results and an optional SQLite ledger query for two, and returns the matches as context.
Enable it by adding the settings block in its README. Retrieved text is untrusted evidence, and it enters your hosted-model session once the hook is on. [README](components/pretool-memory/README.md)

<a id="voice-calibration"></a>

## voice-calibration

A `PreToolUse` hook for `Write` and `Edit`. It matches the target path against fixed genre patterns (`Journal`, `drafts`, `Outreach`, `01 - Self`) and returns up to two QMD samples of your own writing in that genre.
Samples are style evidence. They do not guarantee a voice match and do not authorize a write. [README](components/voice-calibration/README.md)

## Portability

Your Markdown files, source transcripts, SQLite database, and JSON exports remain readable outside the original session.
Carry the records when you change clients, then configure the next client's parser and retrieval adapter.
The hook adapters target Claude Code; the data is portable, the adapters are not.
This repository ships no private corpus, no hosted service, and no capability-level approval gate for external actions.

## Verify

```bash
python3 -m unittest discover -s tests -v
bash tests/test_setup.sh
for component in session-ledger cc-bridge route-domain pretool-memory voice-calibration; do
  (cd "components/$component" && python3 -m unittest discover -s tests -v) || exit 1
done
shellcheck scripts/setup.sh .claude/hooks/*.sh tests/test_setup.sh examples/demo.sh
```

web2md needs its own environment:

```bash
python3 -m venv components/web2md/.venv
components/web2md/.venv/bin/python -m pip install -r components/web2md/requirements-dev.txt
(cd components/web2md && .venv/bin/python -m pytest -q)
```

The root CI workflow runs the reference and every component suite. Workflows inside component folders are history; GitHub runs only `.github/workflows/` at the root.

## Model assistance

This README was written with model assistance in 2026. The code and tests in this repository are the evidence; read them to judge the tool.
The session-ledger and route-domain component READMEs carry the same disclosure.

## Related projects

- [agent-oversight](https://github.com/b2bvic/agent-oversight): response scores, process status, review receipts, and dry-run API writes.
- [vault-crawl](https://github.com/b2bvic/vault-crawl): Rust retrieval core that stores fetched pages with provenance.

## License

MIT. The reference and all six components use MIT licenses. The root [LICENSE](LICENSE) and each component license remain in place.
