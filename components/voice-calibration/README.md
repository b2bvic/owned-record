# Claude Code writing sample hook: voice-calibration

voice-calibration selects local writing samples before Claude Code Write and Edit calls for operators working with hosted models.
It supplies genre-specific examples when a session needs the author's written style.

[Project page](https://scalewithsearch.com/code/owned-record#voice-calibration)

## Install

Requirements: Git, Bash, `jq`, `shasum`, and a configured [QMD](https://github.com/tobi/qmd) sample collection.

```sh
git clone https://github.com/b2bvic/owned-record.git
cd owned-record/components/voice-calibration
```

## Quick start

```sh
bash examples/demo.sh
```

The demo uses a synthetic writing sample and a mock QMD executable.
It prints `PreToolUse` JSON with journal calibration context.
It does not install a hook or contact a model service.

For real use in this checkout, review `components/voice-calibration/voice-calibration.sh`.
Review its path patterns and search queries before merging this opt-in entry into the root `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/components/voice-calibration/voice-calibration.sh\""
          }
        ]
      }
    ]
  }
}
```

For a separate project, copy the script into its `.claude/hooks/` folder and adjust the hook command to that path.

Use the [Claude Code hook reference](https://code.claude.com/docs/en/hooks) when merging existing settings.

## How it works

The Claude Code Write Edit hook supplies writing voice context retrieval through fixed path patterns:

| Path pattern | Genre |
|---|---|
| `Journal` or `journal` | Journal |
| `DRAFTS`, `drafts`, `Correspondence`, or `correspondence` | Correspondence |
| `Outreach`, `outreach`, or `Sequences` | Outreach |
| `01 - Self` | Personal reflection |

This genre-based context engineering requests at most two QMD search results.
Each session and genre has a 60-second throttle after successful retrieval.
Session IDs become SHA-256 cache keys.
Unmatched paths and other tools return no context.

| Variable | Default | Purpose |
|---|---|---|
| `QMD_BIN` | `~/.bun/bin/qmd` | QMD executable or scoped search wrapper |
| `VOICE_STATE_DIR` | `${XDG_CACHE_HOME:-$HOME/.cache}/voice-calibration` | Genre throttle files |

Keep only approved samples in the QMD environment used by this hook.
Retrieved samples remain source evidence and do not authorize actions.

## Portability

Writing samples remain in the source files indexed by QMD, commonly Markdown.
The export path is your source collection directory; the hook supplies no export command.

When changing model vendors, carry the original sample files and your edited genre rules.
Rebuild the search index and configure the next client's writing-sample adapter.
This hook's `PreToolUse` input and output target Claude Code.
Portable samples do not prove compatibility with another client.

## Limits

- Genres follow fixed, ordered, case-sensitive path patterns.
- The first matching genre wins.
- Queries are fixed strings in the script and require local customization.
- Results depend on the configured QMD collections.
- Retrieval supplies examples; it does not guarantee a voice match.
- There is no internal search timeout or latency guarantee.
- Samples can enter a hosted-model session after hook installation.
- The hook returns success without approving the requested write.

## Verify

```sh
python3 -m unittest discover -s tests -v
bash -n voice-calibration.sh examples/demo.sh
shellcheck voice-calibration.sh examples/demo.sh
ruff check --select F,E9 tests
```

Install ShellCheck and Ruff 0.16.10 for lint.

## Related repositories

- [owned-record](../../): Markdown context folders and routing configuration.
- [pretool-memory](../pretool-memory): Recall owned records before selected tool calls.
- [vault-crawl](https://github.com/b2bvic/vault-crawl): Retrieve source material and preserve provenance.
- [cc-bridge](../cc-bridge): Convert transcript exchanges to Markdown logs.

## License

MIT. See [LICENSE](LICENSE).
