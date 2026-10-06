#!/usr/bin/env bash
# Isolated, synthetic demonstration. Does not install hooks or contact a model.
set -euo pipefail
REPO_ROOT=$(CDPATH="" cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
demo_root=$(mktemp -d)
trap 'rm -rf "$demo_root"' EXIT
cat > "$demo_root/qmd" <<'SEARCH'
#!/bin/sh
printf '%s\n' 'Synthetic writing sample: Keep the source. Review the wording.'
SEARCH
chmod u+x "$demo_root/qmd"
printf '%s\n' '{"tool_name":"Write","tool_input":{"file_path":"Journal.md"},"session_id":"synthetic-demo"}' | QMD_BIN="$demo_root/qmd" VOICE_STATE_DIR="$demo_root/cache" bash "$REPO_ROOT/voice-calibration.sh"
