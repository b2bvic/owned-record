---
allowed-tools: WebFetch, Bash, Write, Read
argument-hint: <url> [--output PATH] [--format md|json]
description: Multi-tier URL fetching with 3-tier fallback.
---

# Deep Scrape — Multi-Tier URL Fetching

## CRITICAL: Execute These Exact Steps

### Step 1: Parse arguments

| Arg | Default |
|-----|---------|
| `<url>` | Required — the page to scrape |
| `--output PATH` | `./scraped/{domain-slug}.{format}` |
| `--format` | `md` (markdown) or `json` |

### Step 2: Tier 1 — WebFetch

```
WebFetch: {url}
Prompt: "Return the full page content including: page title, meta description, all headings with hierarchy, all paragraph text, all links with href and anchor text, all images with alt text, any structured data or tables. Preserve the complete content structure."
```

**If WebFetch succeeds** → proceed to Step 4 with extracted content.

**If WebFetch fails or returns empty/partial** → proceed to Tier 2.

### Step 3a: Tier 2 — Playwright (if available)

```
Use Playwright MCP browser:
1. Navigate to {url}
2. Wait for networkidle
3. Extract: document.title, meta description, full body HTML
4. Convert HTML to structured content
```

**If Playwright succeeds** → proceed to Step 4.

**If Playwright fails or unavailable** → proceed to Tier 3.

### Step 3b: Tier 3 — curl fallback

```bash
curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Accept: text/html" \
  --max-time 30 \
  "{url}" | head -c 500000
```

Parse raw HTML: extract `<title>`, `<meta name="description">`, all `<h1>`-`<h6>`, `<p>`, `<a>`, `<table>`, `<ul>/<ol>`.

### Step 4: Structure output

**Markdown format (default):**
```markdown
source:: {url}
fetched:: {YYYY.MM.DD}
method:: {WebFetch | Playwright | curl}
status:: {success | partial | degraded}

---

# {Page Title}

> {Meta description}

{Structured content with headings, paragraphs, lists, tables}

## Links Found

| Anchor Text | URL | Type |
|-------------|-----|------|
| {text} | {href} | internal/external |

---

*Scraped from [{domain}]({url}) via {method} — {YYYY.MM.DD}*
```

### Step 5: Write file

```bash
mkdir -p "./scraped"
```

Write to output path.

### Step 6: Report to user

```
✓ Scraped: {url}
  Method: {tier used} (Tier {1|2|3})
  Output: {path}
  Format: {md|json}
  Content: ~{word count} words, {heading count} headings, {link count} links
  Status: {success | partial — missing: {what}}
```

---

## Self-Repair Protocol

**Reference:** `.claude/commands/_skill-repair-protocol.md`

### Breakable References

| Reference | Current Path | Failure Code |
|-----------|-------------|--------------|
| Output folder | `./scraped/` | FOLDER_MISSING |

### Skill-Specific Failure Modes

| Failure | Detection | Auto-Fix |
|---------|-----------|----------|
| Output folder missing | Write fails | `mkdir -p` the folder, retry |
| All 3 tiers fail | WebFetch + Playwright + curl all error | FLAG — site may be down or blocking |
| Playwright MCP unavailable | Tool call errors | Skip Tier 2, fall through to Tier 3 |
