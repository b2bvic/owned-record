# route-domain

A shell hook for selecting bounded local context from prompt keywords.

The shipped domain names, keywords, and paths are examples. Edit them before
installing the script as a Claude Code `UserPromptSubmit` hook.

## Principle cluster

This repository demonstrates **P03 (continuity compounds)** and **P05 (semantic order lowers retrieval cost)** because it matches prompt text to configured categories and can warn when a selected context file is stale.

[Read the principles](https://victorvalentineromo.com/principles).

## Worked example

```bash
demo_root=$(mktemp -d)
mkdir -p "$demo_root/01 - Work"
printf '%s\n' 'release:: ready' > "$demo_root/01 - Work/_context.md"
CLAUDE_PROJECT_DIR="$demo_root" CLAUDE_USER_PROMPT="review the release" ./route-domain.sh
```

The command emits hook JSON containing the demo context.

## Requirements and boundaries

- Requires `jq` to emit hook JSON.
- Loads only context files that exist under `CLAUDE_PROJECT_DIR`.
- Keyword matching is heuristic and does not enforce authorization.
- Review every configured path before using the hook in a real vault.

## License

MIT.

## How this was built

This 2026 README refit used model assistance.

No claim is made about how the underlying code was authored or reviewed.
