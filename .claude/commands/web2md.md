---
allowed-tools: WebFetch, Bash, Write, Read
argument-hint: <url> [--output PATH] [--js]
description: Convert web page to clean markdown.
---

# Web Page to Markdown

## CRITICAL: Execute These Exact Steps

### Step 1: Parse arguments

| Arg | Default |
|-----|---------|
| `<url>` | Required — the page to convert |
| `--output PATH` | `./scraped/{domain-slug}.md` |
| `--js` | If present, use Playwright for JS-rendered pages |

Extract domain slug from URL: `https://example.com/some-page` → `example-com--some-page`

### Step 2: Fetch page content

**Default (no --js flag):**
```
WebFetch: {url}
Prompt: "Return the COMPLETE page content as markdown. Preserve all headings (H1-H6), paragraphs, lists, tables, blockquotes, code blocks, and links. Strip navigation menus, footers, sidebars, ads, cookie banners, and boilerplate. Keep heading hierarchy intact."
```

**With --js flag:**
```
Use Playwright MCP to navigate to {url}, wait for network idle, then extract content.
```

### Step 3: Clean extracted content

Remove:
- Navigation menus, headers, footers
- Cookie consent banners
- Ad blocks and sponsored content
- Social sharing widgets
- Comment sections
- "Related articles" blocks

Preserve:
- Heading hierarchy (H1 → H2 → H3 — sequential, no skipping)
- All paragraph text
- Lists (ordered and unordered)
- Tables (convert to markdown)
- Blockquotes and code blocks
- Image alt text as `![alt text](url)`
- Links as `[text](url)`

### Step 4: Structure output

```markdown
source:: {original URL}
fetched:: {YYYY.MM.DD}
method:: {WebFetch | Playwright}

---

# {Page H1 or title}

{Cleaned markdown content}

---

*Source: [{domain}]({url}) — fetched {YYYY.MM.DD}*
```

### Step 5: Write file

Write to output path. If file exists, overwrite.

### Step 6: Report to user

```
✓ Converted: {url}
  Output: {output path}
  Method: {WebFetch | Playwright}
  Headings: {count}
  Word count: ~{estimate}
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
| WebFetch returns empty | Response is blank | Retry with Playwright (--js fallback) |
| URL unreachable | All methods timeout | FLAG — report to user |
