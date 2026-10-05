# Claude Code context routing hook: route-domain

Route-domain loads matching Markdown context files for Claude Code operators who use hosted models.
It reduces repeated context selection by mapping prompt keywords to example domain paths.

[Project page](https://scalewithsearch.com/code/route-domain)

## Install

Use Bash, jq, and Git. The regression tests use Python 3.11 or newer.

```bash
git clone https://github.com/b2bvic/route-domain.git
cd route-domain
```

Review the domain names, keyword expressions, and paths in `route-domain.sh` before registering a hook.
The shipped domain paths are examples.

## Quick start

Run a Claude Code UserPromptSubmit input with a temporary context file:

```bash
demo_record=$(mktemp -d)
unset CLAUDE_USER_PROMPT
mkdir -p "$demo_record/01 - Work"
printf '%s\n' 'release:: ready' > "$demo_record/01 - Work/_context.md"
printf '%s\n' '{"hook_event_name":"UserPromptSubmit","prompt":"review the release"}' \
  | CLAUDE_PROJECT_DIR="$demo_record" bash ./route-domain.sh
```

The command emits hook JSON containing the demo context.
`CLAUDE_USER_PROMPT` overrides stdin when set for legacy examples.

## How it works

The hook reads a string `prompt` from stdin JSON unless `CLAUDE_USER_PROMPT` is set.
It uses `CLAUDE_PROJECT_DIR` as the root, with the current directory as fallback.
Keyword context loading matches lowercase prompt text against the configured domain expressions.
Existing matching files become `hookSpecificOutput.additionalContext` in the output JSON.
A `last_verified::` date older than two days adds a staleness warning.
The hook also emits configured lookup or skill hints for matching phrases.

This is a context engineering hook pattern a team can adopt after it reviews its paths and disclosure rules.
See the [Claude Code hooks reference](https://code.claude.com/docs/en/hooks) for the hook input and output contract.

Run the checks:

```bash
bash -n route-domain.sh
shellcheck route-domain.sh
python3 -m unittest discover -s tests -v
```

## Limits

- Keyword matching is heuristic and includes substring matches. It does not establish intent or authorization.
- Multiple matching domains load multiple files. This hook does not ask you to resolve ambiguity.
- The output can contain complete context bodies. Review what each configured file can disclose to the model.
- Configured files and symlinks must be trusted. The hook has no filesystem sandbox or maximum context size.
- Missing context files produce no context body. Invalid stdin input returns a failing status before loading context.
- The shipped paths and skill hints require customization. This repository ships no Codex CLI hook adapter.

For path-only selection without context loading, inspect the `vault-route` helper in the skills repository.

## Related repositories

- [agent-oversight](https://github.com/b2bvic/agent-oversight): orchestration cluster and evidence boundaries.
- [skills](https://github.com/b2bvic/skills): path selection and local artifact checks.
- [owned-record](https://github.com/b2bvic/owned-record): owned memory cluster.

## License

[MIT](LICENSE).
