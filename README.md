# route-domain

Claude Code hook that automatically loads relevant context based on keywords in your prompt. Say "deploy" and your infrastructure context loads. Say "budget" and your personal finance context loads.

Built by [Victor Valentine Romo](https://victorvalentineromo.com) at [Scale With Search](https://scalewithsearch.com).

## What It Does

A `UserPromptSubmit` hook that:

1. Reads your prompt text
2. Matches keywords against configured domains
3. Loads the matching domain's `_context.md` file
4. Checks if the context is stale (>2 days since `last_verified::`)
5. Injects the context + any staleness warnings
6. Detects skill-relevant patterns and suggests slash commands

## Install

```bash
cp route-domain.sh /path/to/project/.claude/hooks/
chmod +x /path/to/project/.claude/hooks/route-domain.sh
```

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/route-domain.sh"
          }
        ]
      }
    ]
  }
}
```

## Configuration

Edit the `DOMAINS` section in the script. Each domain needs:

1. A keyword regex (matched against lowercase prompt)
2. A path to the domain's `_context.md` file

Example domain:

```bash
if echo "$PROMPT_LOWER" | grep -qE "deploy|kubernetes|docker|infra"; then
  CTX="$VAULT_ROOT/Infrastructure/_context.md"
  if [ -f "$CTX" ]; then
    CONTEXT+="$(cat "$CTX")"
  fi
fi
```

## Staleness Detection

Add `last_verified:: 2026.03.25` to your `_context.md` frontmatter. The hook warns when context is >2 days old, prompting you to update it.

## Requirements

- `jq` for JSON output encoding
- A vault with `_context.md` files per domain

## License

MIT
