#!/usr/bin/env bash
# Isolated, synthetic demonstration. Does not install hooks or contact a model.
set -euo pipefail
REPO_ROOT=$(CDPATH="" cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
demo_root=$(mktemp -d)
trap 'rm -rf "$demo_root"' EXIT
mkdir "$demo_root/input"
python3 - "$demo_root/input/session.jsonl" <<'TRANSCRIPT'
import json
import sys
from pathlib import Path
records = [
    {"type": "user", "message": {"content": "Keep this decision in the owned record."}},
    {"type": "assistant", "message": {"content": [{"type": "text", "text": "Record the decision and its source."}]}},
    {"type": "user", "message": {"content": "What comes next?"}},
]
for record in records:
    record["timestamp"] = "2026-10-05T12:00:00Z"
Path(sys.argv[1]).write_text("".join(json.dumps(record) + "\n" for record in records))
TRANSCRIPT
CC_BRIDGE_PROJECT="$demo_root/input" CC_BRIDGE_OUTPUT="$demo_root/logs" CC_BRIDGE_STATE="$demo_root/state.json" "$REPO_ROOT/cc-bridge"
cat "$demo_root/logs/"*.md
