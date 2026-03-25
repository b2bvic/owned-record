# web2md

Convert any web page to clean markdown. Single command, zero install.

Strips navigation, ads, cookie banners, sidebars, and boilerplate. Preserves heading hierarchy, lists, tables, links, blockquotes, and code blocks.

Built by [Victor Valentine Romo](https://victorvalentineromo.com) at [Scale With Search](https://scalewithsearch.com).

## Install

```bash
curl -o ~/.local/bin/web2md https://raw.githubusercontent.com/b2bvic/web2md/main/web2md
chmod +x ~/.local/bin/web2md
```

Requirements: Python 3.11+ and [uv](https://docs.astral.sh/uv/). Dependencies resolve automatically on first run.

## Usage

```bash
# Convert page to markdown file
web2md https://example.com/blog-post

# Specify output path
web2md https://example.com/page -o article.md

# Print to stdout (pipe to other tools)
web2md https://example.com/page --stdout

# Pipe to clipboard
web2md https://example.com/page --stdout | pbcopy
```

## Output

```markdown
source:: https://example.com/blog-post
fetched:: 2026.03.25

# Blog Post Title

Content converted to clean markdown...

*Source: [example.com](https://example.com/blog-post) — fetched 2026.03.25*
```

## What Gets Stripped

- Navigation menus and headers
- Footer content
- Cookie consent banners
- Ad containers and sponsored content
- Social sharing widgets
- Comment sections (Disqus, etc.)
- Newsletter signup forms
- Related post blocks
- Sidebar widgets
- Empty elements
- HTML comments

## What Gets Preserved

- Heading hierarchy (H1 through H6)
- Paragraphs
- Ordered and unordered lists
- Tables
- Blockquotes
- Code blocks with language tags
- Links (as markdown `[text](url)`)
- Bold and italic text
- Horizontal rules

## How It Works

1. Fetch page with proper headers (User-Agent, Accept)
2. Parse HTML with lxml (fast, fault-tolerant)
3. Strip boilerplate by tag name (script, style, nav, footer, aside)
4. Strip boilerplate by class/ID pattern matching (40+ patterns)
5. Find main content area (article > main > [role=main] > body)
6. Convert to markdown via markdownify
7. Clean up whitespace, fix heading spacing
8. Add source frontmatter

## License

MIT
