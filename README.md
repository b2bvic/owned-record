# cc-bridge

Convert Claude Code JSONL transcripts to readable daily markdown logs. Zero dependencies.

Every Claude Code session generates a JSONL transcript. This tool incrementally parses them into clean, timestamped markdown — one file per day, with user messages blockquoted and assistant responses formatted.

Built by [Victor Valentine Romo](https://victorvalentineromo.com) at [Scale With Search](https://scalewithsearch.com).

## Install

```bash
curl -o ~/.local/bin/cc-bridge https://raw.githubusercontent.com/b2bvic/cc-bridge/main/cc-bridge
chmod +x ~/.local/bin/cc-bridge
```

Requirements: Python 3.11+ (stdlib only).

## Usage

```bash
# Run once — processes new transcript entries
cc-bridge

# Set up as a cron job (every 60 seconds)
# crontab -e:
# * * * * * ~/.local/bin/cc-bridge

# Or macOS launchd (see below)
```

## Output

Daily markdown files in `~/claude-logs/` (configurable):

```markdown
type:: claude-log
date:: 2026.03.25
user:: User
sources:: claude-code

# Claude Code — User — 2026.03.25

---

### 8:14 PM — User (💻 terminal) `claude-code`

> How do I fix the authentication bug?

**Claude:**

The issue is in `auth.py` line 42. The token validation...

---

### 8:22 PM — User (💻 terminal) `claude-code`

> Can you also add rate limiting?

**Claude:**

Here's a rate limiter using a sliding window...
```

## How It Works

1. **Discover** — Finds the most recently modified JSONL transcript in `~/.claude/projects/`
2. **Incremental** — Tracks byte position. Only processes new lines since last run.
3. **Exchange boundary** — Waits for a subsequent user message before flushing an exchange (proves the assistant finished). Stale sessions (>2 min idle) auto-flush.
4. **Filter** — Strips tool results, system meta, and thinking blocks. Only captures visible user text and assistant text.
5. **Truncate** — Long responses capped at 2,000 chars with `[...truncated]` marker.
6. **State** — Persists position in `~/.claude/cc-bridge-state.json`. Safe to restart.

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `CC_BRIDGE_PROJECT` | auto-detected | Claude Code project directory |
| `CC_BRIDGE_OUTPUT` | `~/claude-logs/` | Output directory for markdown files |
| `CC_BRIDGE_TZ` | `America/New_York` | Timezone for timestamps |
| `CC_BRIDGE_USER` | `User` | Username in log headers |

## macOS launchd

Create `~/Library/LaunchAgents/com.cc-bridge.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cc-bridge</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/YOU/.local/bin/cc-bridge</string>
    </array>
    <key>StartInterval</key>
    <integer>60</integer>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.cc-bridge.plist
```

## License

MIT
