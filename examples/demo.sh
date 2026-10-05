#!/usr/bin/env bash
# Isolated, synthetic demonstration. Does not install hooks or contact a model.
set -euo pipefail
REPO_ROOT=$(CDPATH="" cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
python3 - "$REPO_ROOT" <<'PYINPUT' | CLAUDE_PROJECT_DIR="$REPO_ROOT" bash "$REPO_ROOT/.claude/hooks/route-domain.sh"
import json
import sys
print(json.dumps({"prompt": "review sprint backlog", "cwd": sys.argv[1]}))
PYINPUT
