# Claude Code transcript to Markdown: cc-bridge

cc-bridge converts Claude Code JSONL transcripts to daily Markdown logs for operators preserving hosted-model session records.
It keeps visible exchanges readable outside the original client when you need an owned activity history.

[Project page](https://scalewithsearch.com/code/owned-record#cc-bridge)

## Install

Requirements: Git, Bash for the demo, and Python 3 with `zoneinfo` and timezone data.
The converter uses the Python standard library.

```sh
git clone https://github.com/b2bvic/owned-record.git
cd owned-record/components/cc-bridge
chmod u+x cc-bridge
```

## Quick start

```sh
bash examples/demo.sh
```

The demo creates a synthetic JSONL transcript and prints one daily Markdown log.
It uses isolated output and state paths, then removes its temporary files.

For your own transcripts, set the project and output paths explicitly:

```sh
CC_BRIDGE_PROJECT=/path/to/transcripts \
CC_BRIDGE_OUTPUT=/path/to/session-logs \
CC_BRIDGE_STATE=/path/to/bridge-state.json \
./cc-bridge
```

## How it works

The JSONL transcript converter selects the newest root-level transcript from one project directory.
It skips nested subagent transcripts, metadata user messages, tool results, and assistant thinking blocks.

A subsequent user message completes the preceding exchange.
The final exchange also completes when the transcript has been unchanged for more than 120 seconds.
The converter retains the oldest unfinished user's position for the next run.
Partial JSONL records remain unread until a complete line arrives.
A truncated transcript restarts from its beginning.

| Variable | Default | Purpose |
|---|---|---|
| `CC_BRIDGE_PROJECT` | Newest directory in `~/.claude/projects/` | Transcript directory |
| `CC_BRIDGE_OUTPUT` | `~/claude-logs/` | Daily Markdown export directory |
| `CC_BRIDGE_STATE` | `~/.claude/cc-bridge-state.json` | Resume state JSON |
| `CC_BRIDGE_TZ` | `America/New_York` | Timestamp timezone |
| `CC_BRIDGE_USER` | `User` | Log header name |

New output files use a private creation mask.
The converter runs once; it does not install a timer.

## Portability

Portable agent session logs use UTF-8 Markdown files named `YYYY.MM.DD.md`.
The export path is the directory selected by `CC_BRIDGE_OUTPUT`.
These owned AI session records require no original model client to read.

When changing model vendors, carry the Markdown logs and retain the original JSONL transcripts for complete source history.
The JSON resume state contains a source path and file position; reset it when starting a different source corpus.
A new transcript format needs a new parser or adapter.
This converter reads Claude Code transcripts only.

## Limits

- Each invocation inspects one project and its newest root-level transcript.
- Assistant text is truncated after 2,000 characters in each exported exchange.
- Tool results and thinking remain outside the Markdown export.
- Reprocessing a corpus with reset state can append duplicate exchanges.
- The transcript parser follows the shipped Claude Code record shape.
- Concurrent writers and exactly-once delivery are not implemented.
- The logs remain plaintext records that you must select before sending to a hosted model.

## Verify

```sh
python3 -m py_compile cc-bridge
python3 -m unittest discover -s tests -v
ruff check --select F,E9 cc-bridge tests
shellcheck examples/demo.sh
```

Install ShellCheck and Ruff 0.16.10 for lint.

## Related repositories

- [owned-record](../../): Markdown context folders and routing configuration.
- [pretool-memory](../pretool-memory): Recall owned records before selected tool calls.
- [vault-crawl](https://github.com/b2bvic/vault-crawl): Retrieve source material and preserve provenance.
- [voice-calibration](../voice-calibration): Recall writing samples for a target file genre.

## License

MIT. See [LICENSE](LICENSE).
