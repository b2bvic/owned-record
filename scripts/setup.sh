#!/bin/bash
# Scale With Search — Vault Setup Script
# Creates a personalized Claude Code vault from this template.
#
# Usage: ./scripts/setup.sh
# Or:    bash scripts/setup.sh

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo ""
echo "  Scale With Search — Vault-as-Memory Setup"
echo "  ==========================================="
echo ""
echo "  This script personalizes your CLAUDE.md and creates"
echo "  domain folders with _context.md files."
echo ""

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

EXTRA_DOMAINS=()
EXTRA_KEYWORDS=()

for (( i=1; i<=DOMAIN_COUNT; i++ )); do
  echo ""
  read -rp "  Domain $i name (e.g., 'Clients', 'Learning', 'Creative'): " DNAME
  [ -z "$DNAME" ] && continue
  read -rp "  Domain $i keywords (comma-separated, e.g., 'client,invoice,proposal'): " DKEYS
  [ -z "$DKEYS" ] && DKEYS="$DNAME"
  EXTRA_DOMAINS+=("$DNAME")
  EXTRA_KEYWORDS+=("$DKEYS")
done

echo ""
echo "  ─── Creating your vault ───"
echo ""

# ─── Personalize CLAUDE.md ──────────────────────────────────

CLAUDE_MD="$REPO_ROOT/CLAUDE.md"

if [ -f "$CLAUDE_MD" ]; then
  sed -i.bak "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" "$CLAUDE_MD"
  sed -i.bak "s/{{YOUR_NAME}}/$USER_NAME/g" "$CLAUDE_MD"
  sed -i.bak "s/{{ONE_LINE_DESCRIPTION}}/$USER_DESC/g" "$CLAUDE_MD"
  rm -f "${CLAUDE_MD}.bak"
  echo "  ✓ CLAUDE.md personalized"
fi

# ─── Create extra domain folders ────────────────────────────

DOMAIN_NUM=3  # Start after 00-System, 01-Work, 02-Personal
ROUTE_ADDITIONS=""

for (( i=0; i<${#EXTRA_DOMAINS[@]}; i++ )); do
  DNAME="${EXTRA_DOMAINS[$i]}"
  DKEYS="${EXTRA_KEYWORDS[$i]}"
  DNUM=$(printf "%02d" $DOMAIN_NUM)
  DFOLDER="$REPO_ROOT/${DNUM} - ${DNAME}"

  mkdir -p "$DFOLDER"

  # Create _context.md
  cat > "$DFOLDER/_context.md" << CTXEOF
# ${DNAME} Context

last_verified:: $(date +%Y.%m.%d)

Your ${DNAME} domain. Customize this file with current state and priorities.

## Current State

- (Add your current ${DNAME} priorities here)
CTXEOF

  # Create _log.md
  cat > "$DFOLDER/_log.md" << LOGEOF
# ${DNAME} Log

Activity log for the ${DNAME} domain.

---

(Entries will appear here as you work.)
LOGEOF

  echo "  ✓ Created ${DNUM} - ${DNAME}/ with _context.md and _log.md"

  # Build route-domain.sh addition
  # Convert comma-separated keywords to grep pattern
  GREP_PATTERN=$(echo "$DKEYS" | tr ',' '|' | tr -d ' ')

  ROUTE_ADDITIONS+="
# DOMAIN: ${DNAME}
if echo \"\$PROMPT_LOWER\" | grep -qiE \"${GREP_PATTERN}\"; then
  CONTEXT_PATH=\"\$VAULT_ROOT/${DNUM} - ${DNAME}/_context.md\"
  if [ -f \"\$CONTEXT_PATH\" ]; then
    STALE_WARN=\$(check_staleness \"\$CONTEXT_PATH\" \"${DNAME}\")
    CONTEXT+=\"\${STALE_WARN}\"
    CONTEXT+=\"# ${DNAME} Context\"
    CONTEXT+=\$'\\n\\n'
    CONTEXT+=\$(cat \"\$CONTEXT_PATH\")
    CONTEXT+=\$'\\n\\n---\\n\\n'
    DOMAINS_LOADED+=\"${DNAME} \"
  fi
fi
"

  # Add to CLAUDE.md domain table
  if [ -f "$CLAUDE_MD" ]; then
    # Insert before the "Add more domains" note
    sed -i.bak "/^> Add more domains/i\\
| **${DNAME}** | \`${DNUM} - ${DNAME}/_context.md\` | ${DKEYS} |" "$CLAUDE_MD"
    rm -f "${CLAUDE_MD}.bak"
  fi

  DOMAIN_NUM=$((DOMAIN_NUM + 1))
done

# ─── Inject extra domains into route-domain.sh ──────────────

if [ -n "$ROUTE_ADDITIONS" ]; then
  HOOK_FILE="$REPO_ROOT/.claude/hooks/route-domain.sh"
  if [ -f "$HOOK_FILE" ]; then
    # Insert before the "ADD MORE DOMAINS HERE" comment
    TEMP_FILE=$(mktemp)
    awk -v additions="$ROUTE_ADDITIONS" '
      /^# ADD MORE DOMAINS HERE/ { print additions }
      { print }
    ' "$HOOK_FILE" > "$TEMP_FILE"

    # Also uncomment the commented domain example since we have real ones now
    mv "$TEMP_FILE" "$HOOK_FILE"
    chmod +x "$HOOK_FILE"
    echo "  ✓ route-domain.sh updated with ${#EXTRA_DOMAINS[@]} domain(s)"
  fi
fi

# ─── Make hooks executable ──────────────────────────────────

chmod +x "$REPO_ROOT/.claude/hooks/"*.sh 2>/dev/null
echo "  ✓ Hooks made executable"

# ─── Done ───────────────────────────────────────────────────

echo ""
echo "  ─── Setup complete ───"
echo ""
echo "  Your vault is ready. Next steps:"
echo ""
echo "  1. cd $(basename "$REPO_ROOT")"
echo "  2. Review CLAUDE.md — update the NOW section with your current state"
echo "  3. Edit domain _context.md files with your actual priorities"
echo "  4. Run: claude"
echo ""
echo "  Optional:"
echo "  - Install QMD (https://github.com/aethermonkey/qmd) for semantic memory"
echo "  - Run 'qmd index' to index your vault for the PreToolUse hook"
echo ""
echo "  For the full architecture explanation, see docs/"
echo ""
