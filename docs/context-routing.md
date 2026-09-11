# Context Routing Architecture

> Context routing selects which domain file is relevant for a prompt. The hook emits a candidate path. Retrieval of that file is a separate step.

---

## Core Principle

Language models assemble probable sequences. The quality of output depends entirely on what is available to assemble from.

Context routing solves the relevance problem: what context should be active for this specific query?

| Strategy | Result |
|----------|--------|
| Load everything | Context window bloat, irrelevant noise, diluted attention |
| Load nothing | Generic responses, no domain specificity |
| Manual loading | User overhead, inconsistent, error-prone |
| **Keyword routing** | Emits a candidate path. The model or user reads the selected `_context.md`. |

---

## Architecture Layers

### Layer 1: Router (CLAUDE.md + domains.json)

Human-readable map in `CLAUDE.md`. Machine map in `.agent-oversight/domains.json`. Format:

```json
{"domains":[{"name":"Work","path":"01 - Work","keywords":["sprint"]}]}
```

The `UserPromptSubmit` hook reads the JSON map and emits candidate paths. It does not load file bodies. `CLAUDE.md` still contains:

1. Keyword-to-domain mapping for humans
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

The router names the candidate file. The model or user reads that file after selection.

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
2. Emit the candidate path. Do not inject the file body.
3. Read that domain's `_context.md` only after selection
4. Only load deeper if stuck
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
import re

def extract_domains(prompt: str, domain_map: dict) -> list[str]:
    """Match prompt keywords to domains using word boundaries."""
    matched = []
    for domain, keywords in domain_map.items():
        for keyword in keywords:
            pattern = r"(?<![A-Za-z0-9_])" + re.escape(keyword) + r"(?![A-Za-z0-9_])"
            if re.search(pattern, prompt, flags=re.IGNORECASE):
                matched.append(domain)
                break
    return matched

# Example domain map
DOMAINS = {
    "engineering": ["deploy", "api", "incident", "sprint", "CI"],
    "marketing": ["campaign", "content", "seo", "launch"],
    "finance": ["budget", "invoice", "forecast", "P&L"],
}
```

### Candidate pointers

The hook emits paths. It does not open `_context.md`.

```python
def emit_candidates(domains: list[str], context_paths: dict) -> dict:
    """Return candidate paths. Do not read file bodies."""
    candidates = [
        {"name": domain, "path": context_paths[domain]}
        for domain in domains
        if domain in context_paths
    ]
    if not candidates:
        status = "unmatched"
    elif len(candidates) > 1:
        status = "ambiguous"
    else:
        status = "matched"
    return {
        "status": status,
        "context_loaded": False,
        "candidates": candidates,
    }
```

---

## Anti-Patterns

### Monolithic Context

Loading everything at once. "Here's my entire knowledge base, help me with this task."

Fails because attention dilutes. The model weighs irrelevant context against relevant context. Quality drops as context grows.

### No Keywords, Pure Inference

Expecting the model to figure out which domain applies from the prompt alone.

Fails on ambiguity. "Help me with the report" could match multiple domains. The hook then returns `ambiguous` or `unmatched`. It does not guess a body to inject.

### Stale State

Context files written once, never updated.

The model operates on outdated assumptions. Suggests actions that no longer apply. Misses completed work.

### Redundant Logging

Logging everything everywhere instead of domain-specific logs.

Noise accumulates. Finding relevant history requires reading everything. The log becomes ignored because it cannot be trusted to surface what matters.

---

## Convergence

Multiple teams working independently arrive at this architecture. Enterprise organizations building LLM tooling and individual practitioners structuring personal knowledge bases both converge on keyword-triggered candidate selection. The pattern is structural, not incidental. The problem of "which file should the model read next?" has a narrow solution space, and most serious implementations land in the same region.

Anthropic's own product features (Projects, system prompts) are context routing with different names. The pattern is worth understanding before the interface abstracts it away.

---

## Next Steps

1. **Map your domains** — list distinct areas with unique vocabulary
2. **Build your router** — central file with keyword-to-context mapping
3. **Create context files** — domain rules, state, paths
4. **Establish logging** — one log per domain, update after significant work
5. **Add recency** — script or manual process to track recent changes

The architecture compounds over time. Early sessions feel like overhead. Later sessions can recover the relevant record without another full explanation.

---

## Migration from body injection

Older routing hooks grepped keywords in shell and concatenated `_context.md` into `additionalContext`. That is no longer the default.

Move the domain map to `.agent-oversight/domains.json`. Keep the hook as a pointer emitter. Selected domain retrieval stays a model or user `Read`. Default `.claude/settings.json` enables only quoted `UserPromptSubmit` routing. `pretool-memory.sh` is opt-in. Template permission allow-lists are omitted.
