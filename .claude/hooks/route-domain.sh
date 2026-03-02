#!/bin/bash
# Vault-as-Memory: Domain Routing Hook
# Fires on UserPromptSubmit — detects keywords in user prompts
# and injects the relevant domain _context.md into Claude's context.
#
# CUSTOMIZE: Edit the keyword patterns and domain paths below.
# Add/remove domains to match your vault structure.

VAULT_ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
PROMPT="${CLAUDE_USER_PROMPT:-}"
PROMPT_LOWER=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

CONTEXT=""
DOMAINS_LOADED=""

# ============================================================
# STALENESS DETECTION
# Warns when a _context.md file hasn't been verified recently.
# Portable: handles macOS (date -j) and Linux (date -d).
# ============================================================

date_to_epoch() {
  local datestr="$1"
  local normalized
  normalized=$(echo "$datestr" | tr '.' '-')
  if [[ "$(uname)" == "Darwin" ]]; then
    date -j -f "%Y-%m-%d" "$normalized" "+%s" 2>/dev/null || echo 0
  else
    date -d "$normalized" "+%s" 2>/dev/null || echo 0
  fi
}

check_staleness() {
  local ctx_file="$1"
  local domain="$2"
  [ -f "$ctx_file" ] || return

  local last_verified
  last_verified=$(grep -m1 'last_verified::' "$ctx_file" 2>/dev/null | sed 's/.*last_verified::[[:space:]]*//' | tr -d '[:space:]')
  [ -z "$last_verified" ] && return

  local verified_epoch now_epoch days_stale
  verified_epoch=$(date_to_epoch "$last_verified")
  [ "$verified_epoch" -eq 0 ] && return
  now_epoch=$(date "+%s")
  days_stale=$(( (now_epoch - verified_epoch) / 86400 ))

  if [ "$days_stale" -gt 2 ]; then
    echo "
⚠️ STALE CONTEXT (${days_stale} days — last_verified: ${last_verified})
Update _context.md before session ends:
1. Correct any changed facts
2. Set last_verified:: to today (YYYY.MM.DD)
File: ${ctx_file#"$VAULT_ROOT"/}

"
  fi
}

# ============================================================
# DOMAIN DEFINITIONS — CUSTOMIZE THESE
# ============================================================
# Format: grep pattern → context file path
#
# Tips:
# - Use specific keywords, not generic ones ("jira sprint" not "work")
# - Pipe-separate alternatives: "project|deadline|standup"
# - Each domain loads its _context.md when keywords match

# DOMAIN 1: Work
if echo "$PROMPT_LOWER" | grep -qiE "project|deadline|meeting|standup|sprint|boss|office|work"; then
  CONTEXT_PATH="$VAULT_ROOT/01 - Work/_context.md"
  if [ -f "$CONTEXT_PATH" ]; then
    STALE_WARN=$(check_staleness "$CONTEXT_PATH" "Work")
    CONTEXT+="${STALE_WARN}"
    CONTEXT+="# Work Context"
    CONTEXT+=$'\n\n'
    CONTEXT+=$(cat "$CONTEXT_PATH")
    CONTEXT+=$'\n\n---\n\n'
    DOMAINS_LOADED+="Work "
  fi
fi

# DOMAIN 2: Personal
if echo "$PROMPT_LOWER" | grep -qiE "family|health|budget|home|personal|self|journal"; then
  CONTEXT_PATH="$VAULT_ROOT/02 - Personal/_context.md"
  if [ -f "$CONTEXT_PATH" ]; then
    STALE_WARN=$(check_staleness "$CONTEXT_PATH" "Personal")
    CONTEXT+="${STALE_WARN}"
    CONTEXT+="# Personal Context"
    CONTEXT+=$'\n\n'
    CONTEXT+=$(cat "$CONTEXT_PATH")
    CONTEXT+=$'\n\n---\n\n'
    DOMAINS_LOADED+="Personal "
  fi
fi

# ============================================================
# ADD MORE DOMAINS HERE
# ============================================================
# Copy one of the blocks above and change:
# 1. The grep pattern (keywords that trigger this domain)
# 2. The CONTEXT_PATH (where this domain's _context.md lives)
# 3. The domain label in DOMAINS_LOADED
#
# Example:
#
# # DOMAIN 3: Learning
# if echo "$PROMPT_LOWER" | grep -qiE "course|book|study|notes|learning"; then
#   CONTEXT_PATH="$VAULT_ROOT/03 - Learning/_context.md"
#   if [ -f "$CONTEXT_PATH" ]; then
#     STALE_WARN=$(check_staleness "$CONTEXT_PATH" "Learning")
#     CONTEXT+="${STALE_WARN}"
#     CONTEXT+="# Learning Context"
#     CONTEXT+=$'\n\n'
#     CONTEXT+=$(cat "$CONTEXT_PATH")
#     CONTEXT+=$'\n\n---\n\n'
#     DOMAINS_LOADED+="Learning "
#   fi
# fi

# ============================================================
# CROSS-SESSION SIGNAL (Optional)
# ============================================================
# If you log activity in dated files, surface a count here so
# future sessions know what happened earlier today.
#
# Example: Telegram bot logs, voice transcripts, etc.
# Uncomment and adapt the paths below:
#
# LOG_FILE="$VAULT_ROOT/Logs/$(date +%Y.%m.%d).md"
# if [ -f "$LOG_FILE" ]; then
#   ENTRY_COUNT=$(grep -c "^### " "$LOG_FILE" 2>/dev/null || echo 0)
#   if [ "$ENTRY_COUNT" -gt 0 ]; then
#     CONTEXT+="[CROSS-SESSION — ${ENTRY_COUNT} entries today in $(basename "$LOG_FILE")]"
#     CONTEXT+=$'\n\n---\n\n'
#   fi
# fi

# ============================================================
# OUTPUT (don't modify below this line)
# ============================================================

if [ -n "$CONTEXT" ]; then
  if command -v jq &> /dev/null; then
    ESCAPED=$(echo "$CONTEXT" | jq -Rs .)
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": $ESCAPED
  }
}
EOF
  else
    echo "$CONTEXT"
  fi
fi

exit 0
