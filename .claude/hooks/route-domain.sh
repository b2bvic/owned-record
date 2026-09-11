#!/bin/bash
# Domain routing hook for UserPromptSubmit.
# Reads stdin JSON {prompt, cwd}. Emits candidate paths only.
# Does not read or inject _context.md bodies.

set -eu

HOOK_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"{\n  \"status\": \"error\",\n  \"context_loaded\": false,\n  \"candidates\": [],\n  \"error\": \"python3 not found\"\n}"}}'
  exit 0
fi

exec python3 "$HOOK_DIR/route_domain.py"
