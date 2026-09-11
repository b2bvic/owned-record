#!/bin/bash
# Owned Record vault setup.
# Personalizes CLAUDE.md and writes .agent-oversight/domains.json.
# Does not rewrite hook scripts. Does not overwrite existing custom state.
#
# Usage: ./scripts/setup.sh
# Or:    bash scripts/setup.sh

set -euo pipefail

REPO_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
SETUP_CONFIG="$REPO_ROOT/scripts/setup_config.py"

echo ""
echo "  Owned Record vault setup"
echo "  ==========================================="
echo ""
echo "  This script personalizes CLAUDE.md and writes"
echo "  domain folders plus .agent-oversight/domains.json."
echo ""

if ! command -v python3 >/dev/null 2>&1; then
  echo "  python3 is required."
  exit 1
fi

# ─── Gather Info ────────────────────────────────────────────

read -rp "  Your name: " USER_NAME
[ -z "$USER_NAME" ] && { echo "  Name required."; exit 1; }

read -rp "  Project name (e.g., 'My Vault', 'Ops Center'): " PROJECT_NAME
[ -z "$PROJECT_NAME" ] && PROJECT_NAME="My Vault"

read -rp "  One-line description of what you do: " USER_DESC
[ -z "$USER_DESC" ] && USER_DESC="Building things."

echo ""
echo "  How many domains? (The template includes Work + Personal.)"
echo "  Enter 0 to keep defaults, or a number to add more."
read -rp "  Additional domains (0-8): " DOMAIN_COUNT
DOMAIN_COUNT=${DOMAIN_COUNT:-0}
case "$DOMAIN_COUNT" in
  ''|*[!0-9]*) DOMAIN_COUNT=0 ;;
esac
if [ "$DOMAIN_COUNT" -gt 8 ]; then
  DOMAIN_COUNT=8
fi

EXTRAS_FILE="$(mktemp)"
cleanup() { rm -f "$EXTRAS_FILE"; }
trap cleanup EXIT
printf '%s\n' '[]' > "$EXTRAS_FILE"

for (( i=1; i<=DOMAIN_COUNT; i++ )); do
  echo ""
  read -rp "  Domain $i name (e.g., 'Clients', 'Learning', 'Creative'): " DNAME
  [ -z "$DNAME" ] && continue
  read -rp "  Domain $i keywords (comma-separated, e.g., 'client,invoice,proposal'): " DKEYS
  [ -z "$DKEYS" ] && DKEYS="$DNAME"
  python3 - "$EXTRAS_FILE" "$DNAME" "$DKEYS" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
name = sys.argv[2]
keywords = sys.argv[3]
data = json.loads(path.read_text(encoding="utf-8"))
data.append({"name": name, "keywords": keywords})
path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
PY
done

echo ""
echo "  ─── Creating your vault ───"
echo ""

python3 "$SETUP_CONFIG" \
  --root "$REPO_ROOT" \
  --name "$USER_NAME" \
  --project "$PROJECT_NAME" \
  --description "$USER_DESC" \
  --extras "$EXTRAS_FILE"

if [ -f "$REPO_ROOT/CLAUDE.md" ]; then
  echo "  ✓ CLAUDE.md checked (placeholders replaced only when still present)"
fi
if [ -f "$REPO_ROOT/.agent-oversight/domains.json" ]; then
  echo "  ✓ .agent-oversight/domains.json merged (existing custom domains kept)"
fi

ROUTE_HOOK="$REPO_ROOT/.claude/hooks/route-domain.sh"
if [ -f "$ROUTE_HOOK" ]; then
  chmod u+x "$ROUTE_HOOK"
  echo "  ✓ route-domain.sh is executable"
fi

echo ""
echo "  ─── Setup complete ───"
echo ""
echo "  Your vault is ready. Next steps:"
echo ""
echo "  1. cd $(basename "$REPO_ROOT")"
echo "  2. Review CLAUDE.md — update the NOW section with your current state"
echo "  3. Edit domain _context.md files with your actual priorities"
echo "  4. Add domains in .agent-oversight/domains.json, not in the hook script"
echo "  5. Run: claude"
echo ""
echo "  Optional:"
echo "  - Opt in to PreToolUse memory by adding pretool-memory.sh in .claude/settings.json"
echo "  - Install QMD (https://github.com/aethermonkey/qmd) if you enable that hook"
echo ""
echo "  For the full architecture explanation, see docs/"
echo ""
