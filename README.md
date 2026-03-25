# SubtleBodhi

**Your AI forgets everything between sessions. This fixes that.**

An open-source Claude Code + Obsidian vault architecture that gives Claude persistent memory across conversations. Domain routing loads the right context automatically. Semantic search surfaces past sessions when relevant. Skills extend Claude's capabilities without re-explaining them every time.

---

## What This Does

1. **Domain Routing** — Keywords in your prompt trigger automatic loading of relevant context files. Say "budget" and your personal finance context loads. Say "sprint" and your work context loads. No manual copy-pasting.

2. **Semantic Memory** — A PreToolUse hook extracts Claude's current thinking, searches your vault via BM25, and injects relevant past sessions and patterns before tool execution. ~200ms, invisible to you.

3. **Persistent State** — Each domain has a `_context.md` (current state) and `_log.md` (activity trace). Claude reads these every session, so it knows what happened last time.

4. **Skills** — 17 slash commands that extend Claude's capabilities: thinking frameworks (`/consider-pareto`, `/consider-inversion`), session management (`/handoff`, `/log`), and utilities (`/scrape-deep`, `/web2md`).

5. **Self-Repair** — Skills detect and fix their own broken paths. If a folder moves, the skill finds it, updates its reference, logs the fix, and continues.

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/b2bvic/subtlebodhi.git
cd subtlebodhi

# Run interactive setup
bash scripts/setup.sh

# Start Claude Code
claude
```

The setup script asks your name, project name, and domain structure. It personalizes `CLAUDE.md`, creates domain folders, and wires up the routing hook.

---

## Manual Setup

If you prefer to configure manually:

1. Copy this repo into your Obsidian vault (or any folder)
2. Edit `CLAUDE.md` — replace `{{placeholders}}` with your info
3. Edit `.claude/hooks/route-domain.sh` — customize keywords and domain paths
4. Edit domain `_context.md` files with your actual state
5. Make hooks executable: `chmod +x .claude/hooks/*.sh`
6. Run `claude` from the vault root

---

## Architecture

```
subtlebodhi/
├── CLAUDE.md              ← Master index (loaded every session)
├── _RECENT.md             ← Recently modified files
├── .claude/
│   ├── settings.json      ← Hook configuration
│   ├── hooks/
│   │   ├── route-domain.sh    ← UserPromptSubmit: keyword → context loading
│   │   └── pretool-memory.sh  ← PreToolUse: semantic recall from vault
│   └── commands/              ← 17 slash commands
├── 00 - System/           ← Claude's working memory
│   ├── Sessions/          ← Captured session outputs
│   ├── Patterns/          ← Reusable solutions
│   └── Reference/         ← Ground truth corrections
├── 01 - Work/             ← Your work domain
└── 02 - Personal/         ← Your personal domain
```

### How Domain Routing Works

```
You type: "review the sprint backlog"
                    ↓
route-domain.sh detects "sprint" keyword
                    ↓
Loads 01 - Work/_context.md into Claude's context
                    ↓
Claude responds with your work context loaded
```

### How Semantic Memory Works

```
Claude is thinking about your question
                    ↓
pretool-memory.sh fires before each Read/Glob/Grep
                    ↓
Extracts Claude's current thinking from transcript
                    ↓
Queries vault via QMD BM25 (~166ms)
                    ↓
Injects matching vault content as mid-stream context
                    ↓
Claude's next action is informed by relevant past sessions
```

---

## Skills (Slash Commands)

### Thinking Frameworks

| Command | Framework | Use When |
|---------|-----------|----------|
| `/consider-pareto` | 80/20 analysis | What matters most? |
| `/consider-first-principles` | First principles | Rebuild from ground truth |
| `/consider-inversion` | Munger's inversion | What could go wrong? |
| `/consider-second-order` | Domino chain | What happens next? |
| `/consider-5-whys` | Root cause analysis | Why does this keep breaking? |
| `/consider-eisenhower` | Urgency/importance | What to do first? |
| `/consider-occam` | Occam's Razor | Am I overthinking this? |
| `/consider-one-thing` | Lead domino | What single action unlocks everything? |
| `/consider-swot` | SWOT mapping | Strengths, weaknesses, opportunities, threats |
| `/consider-10-10-10` | Time horizons | 10 min / 10 months / 10 years |
| `/consider-opportunity-cost` | Tradeoff analysis | What am I giving up? |
| `/consider-via-negativa` | Subtraction | What should I stop doing? |

### Utilities

| Command | What It Does |
|---------|--------------|
| `/deliberate` | Multi-agent debate on a decision |
| `/handoff` | Capture session state for next conversation |
| `/log` | Update session log with current work |
| `/morning` | Generate daily orientation dashboard |
| `/review` | Generate weekly review with metrics |
| `/scrape-deep` | Multi-tier URL fetching (WebFetch → Playwright → curl) |
| `/web2md` | Convert any web page to clean markdown |

---

## Optional: Semantic Memory with QMD

The `pretool-memory.sh` hook uses [QMD](https://github.com/aethermonkey/qmd) for BM25 search. Without QMD, this hook exits silently — everything else works fine.

To enable semantic memory:

```bash
# Install QMD (requires Bun)
bun install -g qmd

# Index your vault
cd /path/to/your/vault
qmd index

# Set up periodic reindexing (macOS)
# Add a launchd agent or cron job to run `qmd index` hourly
```

---

## Docs

- [Vault-as-Memory Specification](docs/vault-as-memory.md) — The full architecture spec
- [Context Routing Architecture](docs/context-routing.md) — How keyword routing works at scale
- [Recursive Language System](docs/recursive-language-system.md) — The theory behind outputs-become-inputs
- [Skill Authoring Guide](docs/skill-authoring.md) — How to write your own skills

---

## Origin

This system runs in production. It manages:
- 3,130+ vault files across 5 domains
- Two concurrent jobs (real estate operations + AI consulting)
- Client delivery pipeline with automated dispatch
- Daily operations via VPS + Telegram bot integration
- 73+ documented sessions with compounding context

The repo is a genericized extract of the production system. Everything Victor-specific has been stripped. What remains is the architecture pattern — usable by anyone running Claude Code.

---

## Adding Your Own Domains

1. Create a folder: `03 - Learning/` (or whatever)
2. Add `_context.md` and `_log.md` inside it
3. Edit `.claude/hooks/route-domain.sh` — add a new keyword block
4. Update the domain table in `CLAUDE.md`
5. Run `qmd index` if using semantic memory

---

## Adding Your Own Skills

See [docs/skill-authoring.md](docs/skill-authoring.md) for the full guide.

Quick version: create a `.md` file in `.claude/commands/` with YAML frontmatter and step-by-step instructions. Claude reads it when you invoke `/your-skill-name`.

---

## License

MIT — do whatever you want with it.

---

## Author

**Victor Valentine Romo** — [victorvalentineromo.com](https://victorvalentineromo.com) · [scalewithsearch.com](https://scalewithsearch.com)

I build AI memory systems for people who run businesses. If you want this customized to your workflow: [get in touch](https://scalewithsearch.com).
