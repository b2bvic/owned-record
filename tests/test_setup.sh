#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(CDPATH= cd -- "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
TEST_DIR=$(mktemp -d)
trap 'rm -rf "$TEST_DIR"' EXIT

mkdir "$TEST_DIR/vault"
for entry in CLAUDE.md .agent-oversight .claude scripts "01 - Work" "02 - Personal"; do
  cp -R "$ROOT_DIR/$entry" "$TEST_DIR/vault/"
done
VAULT="$TEST_DIR/vault"

# Names with quotes and spaces must not break interpolation.
printf '%s\n' \
  'Ada "Quote" User' \
  'My "Test" Vault' \
  'Building "things".' \
  '1' \
  'Client Work' \
  'client, invoice' | \
  bash "$VAULT/scripts/setup.sh" > "$TEST_DIR/setup.out"

python3 - "$VAULT" <<'PY'
import json
import sys
from pathlib import Path

vault = Path(sys.argv[1])
claude = (vault / "CLAUDE.md").read_text(encoding="utf-8")
assert claude.startswith("# My \"Test\" Vault\n"), claude.splitlines()[0]
assert "Ada \"Quote\" User. Building \"things\"." in claude
assert "| **Client Work** | `03 - Client Work/_context.md` | client, invoice |" in claude
assert "{{PROJECT_NAME}}" not in claude

config = json.loads((vault / ".agent-oversight" / "domains.json").read_text())
names = [item["name"] for item in config["domains"]]
assert names[:2] == ["Work", "Personal"], names
assert "Client Work" in names
client = next(item for item in config["domains"] if item["name"] == "Client Work")
assert client["path"] == "03 - Client Work"
assert client["keywords"] == ["client", "invoice"]

work = next(item for item in config["domains"] if item["name"] == "Work")
assert work["keywords"] == ["project", "deadline", "meeting", "standup", "sprint"]

hook = (vault / ".claude" / "hooks" / "route-domain.sh").read_text(encoding="utf-8")
assert "cat \"$CONTEXT_PATH\"" not in hook
assert "# DOMAIN: Client Work" not in hook
assert "03 - Client Work/_context.md" not in hook

context = vault / "03 - Client Work" / "_context.md"
log = vault / "03 - Client Work" / "_log.md"
assert context.is_file()
assert log.is_file()
assert (vault / ".claude" / "hooks" / "route-domain.sh").stat().st_mode & 0o100
print("quotes/spaces checks passed")
PY

# Custom state must survive a second setup run with different answers.
CUSTOM_SENTINEL="CUSTOM_STATE_PRESERVED_7b1e"
printf '\n%s\n' "$CUSTOM_SENTINEL" >> "$VAULT/03 - Client Work/_context.md"
python3 - "$VAULT" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1]) / ".agent-oversight" / "domains.json"
data = json.loads(path.read_text(encoding="utf-8"))
for item in data["domains"]:
    if item["name"] == "Work":
        item["keywords"].append("customkw")
path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY

printf '%s\n' \
  'Other User' \
  'Other Vault' \
  'other description' \
  '1' \
  'Client Work' \
  'client,invoice' | \
  bash "$VAULT/scripts/setup.sh" > "$TEST_DIR/setup-repeat.out"

python3 - "$VAULT" "$CUSTOM_SENTINEL" <<'PY'
import json
import sys
from pathlib import Path

vault = Path(sys.argv[1])
sentinel = sys.argv[2]
claude = (vault / "CLAUDE.md").read_text(encoding="utf-8")
assert "Ada \"Quote\" User" in claude
assert "Other User" not in claude
assert claude.count("| **Client Work** |") == 1

config = json.loads((vault / ".agent-oversight" / "domains.json").read_text())
work = next(item for item in config["domains"] if item["name"] == "Work")
assert "customkw" in work["keywords"]
names = [item["name"] for item in config["domains"]]
assert names.count("Client Work") == 1

context = (vault / "03 - Client Work" / "_context.md").read_text(encoding="utf-8")
assert sentinel in context
print("repeated setup preservation passed")
PY

printf 'PASS: setup quotes/spaces and preservation\n'

# A case-variant duplicate must preserve a map the router accepts.
printf '%s\n' 'Other User' 'Other Vault' 'Description' '1' 'work' 'new-keyword' | \
  bash "$VAULT/scripts/setup.sh" > "$TEST_DIR/setup-case.out"
python3 - "$VAULT" <<'PYTEST'
import json, sys
from pathlib import Path
vault = Path(sys.argv[1])
data = json.loads((vault / ".agent-oversight/domains.json").read_text())
assert sum(d["name"].casefold() == "work" for d in data["domains"]) == 1
sys.path.insert(0, str(vault / ".claude/hooks"))
from route_domain import route
assert route("sprint", vault)["status"] == "matched"
print("case-variant setup remains routable")
PYTEST
