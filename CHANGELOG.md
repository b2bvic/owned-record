# Changelog

## 2026-09-11

- Domain routing emits candidate paths only. The hook does not read or inject `_context.md` bodies.
- Domain map moved to `.agent-oversight/domains.json` with `{domains:[{name,path,keywords}]}`.
- `UserPromptSubmit` uses stdin JSON `prompt`/`cwd` plus `CLAUDE_PROJECT_DIR`. Hook commands are quoted for paths with spaces.
- Default settings keep pointer routing only. `pretool-memory.sh` remains available and opt-in. Template permission allow-lists are removed.
- Setup merges domain config instead of editing hook shell. Existing custom state is preserved.
- Tests cover sentinel leakage, zero context body reads, ambiguity, word boundaries, bad stdin, missing config, path and symlink escape, and setup quotes/spaces plus repeated-run preservation.

## 2026-07-20

- Reframe the README as a public reference architecture with an explicit private-system boundary.
- Preserve the `scale-with-search` redirect context and add a direct implementation proof path.
- Fix additional-domain insertion on macOS `awk` by passing multiline content through a temporary file.
- Add a deterministic setup smoke test and read-only GitHub Actions CI.
