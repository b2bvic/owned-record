# voice-calibration

Claude Code hook that injects writing samples before file writes. When Claude is about to write or edit a file, this hook detects the genre (journal, correspondence, outreach, etc.) and injects recent examples of your actual writing as voice calibration context.

Built by [Victor Valentine Romo](https://victorvalentineromo.com) at [Scale With Search](https://scalewithsearch.com).

## What It Does

When Claude writes to a path that matches a genre pattern:

1. Detects the genre from the file path (journal, correspondence, outreach, personal)
2. Queries your vault for recent examples in the same genre
3. Injects those examples as `additionalContext` before the write
4. Throttles at 60 seconds per genre per session (doesn't flood)

Claude's writing output is calibrated against your actual voice — not generic AI tone.

## Install

```bash
cp voice-calibration.sh /path/to/project/.claude/hooks/
chmod +x /path/to/project/.claude/hooks/voice-calibration.sh
```

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/voice-calibration.sh"
          }
        ]
      }
    ]
  }
}
```

## Configuration

Edit the genre detection patterns in the script to match your vault structure. Default patterns detect paths containing journal, correspondence, outreach, and personal keywords.

## Requirements

- [QMD](https://github.com/aethermonkey/qmd) for vault search
- `jq` for JSON encoding

## License

MIT
