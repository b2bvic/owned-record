# voice-calibration

A write hook that selects local writing samples by file genre.

The shipped hook handles Claude Code `Write` and `Edit` events. It maps a fixed
set of path patterns to local `qmd` searches. Review those patterns and queries
before installing it in another vault.

## Principle cluster

This repository demonstrates **P11 (voice is a written standard)** because it limits processing to write and edit events, then maps the target path to a configured genre.

[Read the principles](https://victorvalentineromo.com/principles).

## Worked example

```bash
printf '%s\n' '{"tool_name":"Write","tool_input":{"file_path":"Journal.md"}}' | ./voice-calibration.sh
```

## Requirements and boundaries

- Requires `jq` and a working local `qmd` command.
- Requires a configured `qmd` collection containing the writing samples.
- Ignores tools other than `Write` and `Edit`.
- Returns no samples when the target path does not match a configured genre.

## License

MIT.

## How this was built

This 2026 README refit used model assistance.

No claim is made about how the underlying code was authored or reviewed.
