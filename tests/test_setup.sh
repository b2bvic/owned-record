#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
TEST_DIR=$(mktemp -d)
trap 'rm -rf "$TEST_DIR"' EXIT

cp -R "$ROOT_DIR" "$TEST_DIR/subtlebodhi"

printf 'Test User\nTest Vault\nTest description\n1\nClients\nclient,invoice\n' | \
  bash "$TEST_DIR/subtlebodhi/scripts/setup.sh" > "$TEST_DIR/setup.out"

rg -q '^# Test Vault$' "$TEST_DIR/subtlebodhi/CLAUDE.md"
rg -q 'Test User\. Test description\.' "$TEST_DIR/subtlebodhi/CLAUDE.md"
rg -q '\| \*\*Clients\*\* \| `03 - Clients/_context.md` \| client,invoice \|' "$TEST_DIR/subtlebodhi/CLAUDE.md"
rg -q '^# DOMAIN: Clients$' "$TEST_DIR/subtlebodhi/.claude/hooks/route-domain.sh"
rg -q '03 - Clients/_context.md' "$TEST_DIR/subtlebodhi/.claude/hooks/route-domain.sh"
test -f "$TEST_DIR/subtlebodhi/03 - Clients/_context.md"
test -f "$TEST_DIR/subtlebodhi/03 - Clients/_log.md"
test -x "$TEST_DIR/subtlebodhi/.claude/hooks/route-domain.sh"

printf 'PASS: SubtleBodhi setup smoke test\n'
