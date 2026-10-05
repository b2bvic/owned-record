# Web page to Markdown CLI: web2md

Web2md converts returned HTML into Markdown for researchers and content teams. Use source-attributed files to retain readable inputs for records and retrieval.

[Project page](https://scalewithsearch.com/code/web2md)

## Install

Requirements: Python 3.11 or later.

```bash
gh repo clone b2bvic/web2md
cd web2md
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
```

## Quick start

```bash
.venv/bin/python - <<'PY'
import runpy
tool = runpy.run_path('web2md')
print(tool["html_to_markdown"](tool["clean_html"]("<h1>Demo</h1><p>Portable text.</p>")))
PY
```

This example uses synthetic input without fetching a website.

## How it works

- Fetch HTML with a bounded request timeout.
- Remove configured boilerplate tags and matching elements.
- Write Markdown with the source URL and fetch date.

## Limits

- The tool does not execute JavaScript or bypass access controls.
- Boilerplate matching can remove useful content.
- Images are omitted, and relative links are not rewritten to absolute URLs.

## Related repositories

- [twitter-bookmarks](https://github.com/b2bvic/twitter-bookmarks)
- [sws-skills](https://github.com/b2bvic/sws-skills)

## Development

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m ruff check --select E9,F63,F7,F82 web2md tests
```

CI runs the portable tests and checks syntax-related Python lint rules.

## License

MIT. See [LICENSE](LICENSE).
