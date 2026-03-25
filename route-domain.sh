#!/bin/bash
# route-domain — Claude Code UserPromptSubmit context router
# 🌐 Victor Valentine Romo · victorvalentineromo.com · scalewithsearch.com
#
# Detects keywords in user prompts and injects relevant context files.
# Includes staleness detection — warns when context is >2 days old.
#
# Install: Add to .claude/settings.json as a UserPromptSubmit hook.
# Configure: Edit the DOMAINS section below with your vault structure.
#
# Architecture:
#   User types prompt → this hook fires → keyword match → load _context.md → inject
#
# Reads CLAUDE_USER_PROMPT from Claude Code hook environment.
# Outputs JSON with additionalContext for injection.

VAULT_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
USER_PROMPT="$CLAUDE_USER_PROMPT"

# Convert to lowercase for matching
PROMPT_LOWER=$(echo "$USER_PROMPT" | tr '[:upper:]' '[:lower:]')

CONTEXT=""

# ===== STALENESS DETECTION =====
# Portable date-to-epoch: handles macOS (date -j) and Linux (date -d)
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

# check_staleness <context_file> <domain_label>
# Returns warning text if last_verified:: is >2 days stale
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
Warning: STALE CONTEXT (${days_stale} days since last_verified: ${last_verified})
Update _context.md before ending this session:
1. Correct any changed facts
2. Set last_verified:: to today
File: ${ctx_file#"$VAULT_ROOT"/}

"
  fi
}

# ═══════════════════════════════════════════════════════════════
# DOMAINS — Configure your vault structure below
#
# Pattern for each domain:
#   1. grep -qE "keyword1|keyword2|keyword3"  (lowercase matching)
#   2. Load the _context.md file for that domain
#   3. Check staleness
#
# Replace these examples with your actual domains and keywords.
# ═══════════════════════════════════════════════════════════════

# ===== DOMAIN: WORK =====
# Example: your day job, main project, or primary client
if echo "$PROMPT_LOWER" | grep -qE "sprint|standup|jira|deploy|prod|staging|api|endpoint|release"; then
  CTX="$VAULT_ROOT/01 - Work/_context.md"
  if [ -f "$CTX" ]; then
    STALE_WARN=$(check_staleness "$CTX" "Work")
    CONTEXT+="${STALE_WARN}
# Work Context

$(cat "$CTX")

"
  fi
fi

# ===== DOMAIN: SIDE PROJECT =====
# Example: your startup, SaaS, open source project
if echo "$PROMPT_LOWER" | grep -qE "startup|saas|launch|pricing|landing page|waitlist|stripe|billing"; then
  CTX="$VAULT_ROOT/02 - Side Project/_context.md"
  if [ -f "$CTX" ]; then
    STALE_WARN=$(check_staleness "$CTX" "Side Project")
    CONTEXT+="${STALE_WARN}
# Side Project Context

$(cat "$CTX")

"
  fi
fi

# ===== DOMAIN: PERSONAL =====
# Example: household, finances, health, family
if echo "$PROMPT_LOWER" | grep -qE "budget|finances|household|health|insurance|tax|journal|personal"; then
  CTX="$VAULT_ROOT/03 - Personal/_context.md"
  if [ -f "$CTX" ]; then
    STALE_WARN=$(check_staleness "$CTX" "Personal")
    CONTEXT+="${STALE_WARN}
# Personal Context

$(cat "$CTX")

"
  fi
fi

# ===== DOMAIN: LEARNING =====
# Example: courses, books, research
if echo "$PROMPT_LOWER" | grep -qE "course|tutorial|book|research|study|learn|certificate"; then
  CTX="$VAULT_ROOT/04 - Learning/_context.md"
  if [ -f "$CTX" ]; then
    STALE_WARN=$(check_staleness "$CTX" "Learning")
    CONTEXT+="${STALE_WARN}
# Learning Context

$(cat "$CTX")

"
  fi
fi

# ===== CROSS-SESSION REFERENCE =====
# When user asks about previous sessions, hint the lookup tools
if echo "$PROMPT_LOWER" | grep -qE "previous session|last session|remember when|earlier today|yesterday.*session"; then
  CONTEXT+="
Cross-Session Lookup: search session transcripts or vault files for context from past conversations.

"
fi

# ===== SKILL DETECTION =====
# Detect prompt patterns and hint available skills
SKILL_HINT=""

if echo "$PROMPT_LOWER" | grep -qE "landing page|sales page"; then
  SKILL_HINT+="
Skill hint: /sales-page may help here.
"
fi

if echo "$PROMPT_LOWER" | grep -qE "video script|demo script|recording script"; then
  SKILL_HINT+="
Skill hint: /video-script may help here.
"
fi

if [ -n "$SKILL_HINT" ]; then
  CONTEXT+="$SKILL_HINT"
fi

# ===== OUTPUT =====
# Emit JSON for Claude Code hook injection
if [ -n "$CONTEXT" ]; then
  if command -v jq &> /dev/null; then
    ESCAPED=$(echo "$CONTEXT" | jq -Rs .)
    echo "{\"hookSpecificOutput\":{\"hookEventName\":\"UserPromptSubmit\",\"additionalContext\":$ESCAPED}}"
  fi
fi

exit 0
