# Context Routing Architecture

> Enterprise infrastructure teams and solo practitioners independently converge on the same pattern. Context routing is not overengineering — it is the minimum viable structure for quality LLM output.

---

## Core Principle

Language models assemble probable sequences. The quality of output depends entirely on what is available to assemble from.

Context routing solves the relevance problem: what context should be active for this specific query?

| Strategy | Result |
|----------|--------|
| Load everything | Context window bloat, irrelevant noise, diluted attention |
| Load nothing | Generic responses, no domain specificity |
| Manual loading | User overhead, inconsistent, error-prone |
| **Keyword routing** | **Automatic, relevant, no manual intervention** |

---

## Architecture Layers

### Layer 1: Router (CLAUDE.md)

Central configuration file. Contains:

1. Keyword-to-domain mapping
2. Context file paths
3. Global defaults (voice, rules, state)

```markdown
## Domains

| Domain | Context File | Keywords |
|--------|--------------|----------|
| **Engineering** | `01 - Engineering/_context.md` | deploy, API, incident, sprint |
| **Marketing** | `02 - Marketing/_context.md` | campaign, content, SEO, launch |
| **Finance** | `03 - Finance/_context.md` | budget, invoice, forecast, P&L |
```

The router is the first file read. It determines what else gets loaded.

### Layer 2: Context Files (_context.md)

Domain-specific configuration. Each domain has one. Contains:

1. **Domain rules** — what applies only here
2. **Active state** — current projects, blockers, warnings
3. **Key paths** — where to find things in this domain
4. **Interaction patterns** — how to behave in this domain

```markdown
# Engineering Context

## RULES
- Production API is READ-ONLY in staging
- Always include ticket ID with any deploy reference
- Check test suite before recommending changes

## STATE
- v3.2 migration: 11 of 47 endpoints complete
- CI pipeline broken on ARM runners (since Jan 14)
- DevOps lead is primary contact for infra approvals

## PATHS
| Type | Location |
|------|----------|
| Incident reports | `Incidents/` |
| Architecture docs | `Architecture/` |
| Sprint logs | `Sprints/` |
```

### Layer 3: Recency Layer (_RECENT.md)

Auto-generated list of recently modified files. Solves "what changed?"

```bash
find "/path/to/vault" -name "*.md" -type f -mmin -1440 | grep -v ".obsidian"
```

Prevents working on outdated versions, missing recent context, and re-doing completed work.

### Layer 4: Log Layer (_log.md)

Domain-specific activity log. Captures what was done, when, and which files were affected. Logs enable future sessions to understand past sessions without re-reading everything.

---

## Implementation

### Step 1: Define Domains

List distinct areas of work. Each should have:
- Clear boundaries (what's in, what's out)
- Unique vocabulary (keywords that only appear here)
- Separate state (different projects, different rules)

### Step 2: Build the Router

Create your central configuration file:

```markdown
# Router

## Domains
| Domain | Context File | Keywords |
|--------|--------------|----------|
| WORK-A | `work-a/_context.md` | project-a, sprint, deploy |
| WORK-B | `work-b/_context.md` | project-b, milestone, client |
| PERSONAL | `personal/_context.md` | budget, health, task |

## How to Route
1. Match prompt keywords to domain
2. Read that domain's _context.md
3. Only load deeper if stuck
```

### Step 3: Create Context Files

For each domain, create `_context.md`:

```markdown
# [Domain] Context

## Rules
- [Domain-specific constraints]

## State
- [Current projects]
- [Blockers/warnings]

## Paths
| Type | Location |
|------|----------|
| [File type] | [Path] |
```

### Step 4: Establish Logging

Create `_log.md` for each domain. Entry format:

```markdown
## YYYY.MM.DD

**Session Work**
- [What was done]
- Files: [paths]
- Decisions: [Why X instead of Y]
```

---

## Code Patterns

### Keyword Extraction

```python
def extract_domains(prompt: str, domain_map: dict) -> list[str]:
    """Match prompt keywords to domains."""
    prompt_lower = prompt.lower()
    matched = []
    for domain, keywords in domain_map.items():
        if any(kw in prompt_lower for kw in keywords):
            matched.append(domain)
    return matched

# Example domain map
DOMAINS = {
    "engineering": ["deploy", "api", "incident", "sprint", "CI"],
    "marketing": ["campaign", "content", "seo", "launch"],
    "finance": ["budget", "invoice", "forecast", "P&L"],
}
```

### Context Loading

```python
def load_context(domains: list[str], base_path: str) -> str:
    """Load _context.md files for matched domains."""
    context_paths = {
        "engineering": "01 - Engineering/_context.md",
        "marketing": "02 - Marketing/_context.md",
        "finance": "03 - Finance/_context.md",
    }

    loaded = []
    for domain in domains:
        path = f"{base_path}/{context_paths[domain]}"
        with open(path, 'r') as f:
            loaded.append(f"# {domain.upper()} CONTEXT\n{f.read()}")

    return "\n\n---\n\n".join(loaded)
```

---

## Anti-Patterns

### Monolithic Context

Loading everything at once. "Here's my entire knowledge base, help me with this task."

Fails because attention dilutes. The model weighs irrelevant context against relevant context. Quality drops as context grows.

### No Keywords, Pure Inference

Expecting the model to figure out which domain applies from the prompt alone.

Fails on ambiguity. "Help me with the report" could match multiple domains. Wrong context loads, or nothing loads.

### Stale State

Context files written once, never updated.

The model operates on outdated assumptions. Suggests actions that no longer apply. Misses completed work.

### Redundant Logging

Logging everything everywhere instead of domain-specific logs.

Noise accumulates. Finding relevant history requires reading everything. The log becomes ignored because it cannot be trusted to surface what matters.

---

## Convergence

Multiple teams working independently arrive at this architecture. Enterprise organizations building LLM tooling and individual practitioners structuring personal knowledge bases both converge on keyword-triggered context loading. The pattern is structural, not incidental — the problem of "what context should the model see?" has a narrow solution space, and most serious implementations land in the same region.

Anthropic's own product features (Projects, system prompts) are context routing with different names. The pattern is worth understanding before the interface abstracts it away.

---

## Next Steps

1. **Map your domains** — list distinct areas with unique vocabulary
2. **Build your router** — central file with keyword-to-context mapping
3. **Create context files** — domain rules, state, paths
4. **Establish logging** — one log per domain, update after significant work
5. **Add recency** — script or manual process to track recent changes

The architecture compounds over time. Early sessions feel like overhead. Later sessions feel like the model already knows your work. That is the point. It does. You told it.
