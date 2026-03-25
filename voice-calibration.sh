#!/bin/bash
# PreToolUse Voice Calibration Hook
#
# When Claude writes/edits files in Victor-voice paths, automatically
# injects recent examples of Victor's actual writing from the vault
# in the same genre. Forces calibration against real voice samples,
# not abstract rules.
#
# Fires on: Write, Edit
# Matches: journal, correspondence, outreach, personal reflection paths
# Injects: 2 recent QMD results from same genre as calibration
# Throttle: 60s per genre per session
#
# 2026.03.08 — Created to address Observer Protocol drift in Victor-voice output.
# See: System-Harness.md failure mode "Observer Protocol drift"

trap 'exit 0' ERR

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""' 2>/dev/null)

# Only fire for Write and Edit — output actions where voice matters
case "$TOOL_NAME" in
  Write|Edit)
    ;;
  *)
    exit 0
    ;;
esac

# Extract file path from tool input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""' 2>/dev/null)

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# ===== GENRE DETECTION =====
# Map file path to writing genre. Only Victor-voice paths trigger calibration.
# Order matters — more specific patterns first.
GENRE=""
QUERY=""

case "$FILE_PATH" in
  *Journal*|*journal*)
    GENRE="journal"
    QUERY="journal entry daily reflection personal"
    ;;
  *DRAFTS*|*drafts*|*Correspondence*|*correspondence*)
    GENRE="correspondence"
    QUERY="email draft letter response Victor Romo"
    ;;
  *Outreach*|*outreach*|*Sequences*)
    GENRE="outreach"
    QUERY="outreach email prospect pitch Victor"
    ;;
  *01\ -\ Self*)
    GENRE="personal"
    QUERY="personal reflection self Victor writing"
    ;;
  *)
    # Not a Victor-voice path — skip silently
    exit 0
    ;;
esac

# ===== THROTTLE (60s per genre per session) =====
# Once calibrated for a genre, don't re-inject for 60s.
# Different genres throttle independently — writing a journal
# then switching to correspondence should calibrate for both.
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "default"' 2>/dev/null)
THROTTLE_DIR="/tmp/claude-voice-cal"
mkdir -p "$THROTTLE_DIR" 2>/dev/null
THROTTLE_FILE="$THROTTLE_DIR/${SESSION_ID}.${GENRE}"

if [ -f "$THROTTLE_FILE" ]; then
  LAST_FIRE=$(cat "$THROTTLE_FILE" 2>/dev/null)
  NOW=$(date +%s)
  ELAPSED=$(( NOW - LAST_FIRE ))
  if [ "$ELAPSED" -lt 60 ]; then
    exit 0
  fi
fi

# ===== QUERY QMD (BM25) =====
RESULTS=$(~/.bun/bin/qmd search "$QUERY" -n 2 --min-score 0.3 2>/dev/null)

if [ -z "$RESULTS" ] || echo "$RESULTS" | grep -qi "no results found"; then
  exit 0
fi

# ===== INJECT CALIBRATION CONTEXT =====
CONTEXT="# Voice Calibration — ${GENRE}
You are writing to a Victor-voice path. These are samples of Victor's actual writing in the same genre. Match this voice — his cadence, vocabulary, sentence rhythm. Not Claude's.

${RESULTS}

---
Observer Protocol active. Victor's narrative is Victor's. Claude is the instrument, not the protagonist."

date +%s > "$THROTTLE_FILE"

if command -v jq &> /dev/null; then
  ESCAPED=$(echo "$CONTEXT" | jq -Rs .)
  echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"additionalContext\":$ESCAPED}}"
fi

exit 0
