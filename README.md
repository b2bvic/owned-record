# voice-calibration

A write hook that selects local writing samples by file genre.

## Principle cluster

This repository demonstrates **P11 (voice is a written standard)** because it limits processing to write and edit events, then maps the target path to a configured genre.

[Read the principles](https://victorvalentineromo.com/principles).

## Worked example

```bash
printf '%s\n' '{"tool_name":"Write","tool_input":{"file_path":"Journal.md"}}' | ./voice-calibration.sh
```

## License

MIT.

## How this was built

This 2026 README refit used model assistance.

No claim is made about how the underlying code was authored or reviewed.
