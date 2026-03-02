# Recursive Language System (RLS)

> A framework for human-AI knowledge systems where outputs become inputs, creating compounding intelligence through structured feedback loops.

---

## Definition

A Recursive Language System is an architecture where:

1. **Human generates context** (documents, decisions, patterns)
2. **LLM processes context** (reads, reasons, produces output)
3. **Output persists as new context** (written back to system)
4. **New context informs future processing** (loop closes)

The system compounds. Each cycle adds signal. The LLM improves at your specific domain because it operates on its own successful outputs within your context.

---

## Core Distinction from RAG

| Aspect | Standard RAG | Recursive Language System |
|--------|--------------|---------------------------|
| **Data flow** | One-way (retrieve, generate) | Circular (retrieve, generate, store, retrieve) |
| **Knowledge source** | Static corpus | Living corpus that grows with use |
| **LLM role** | Consumer of context | Consumer AND producer of context |
| **Quality trajectory** | Flat (depends on corpus quality) | Compounding (successful outputs improve future outputs) |
| **Session relationship** | Independent | Cumulative |
| **Memory** | None between sessions | Persistent, structured |

RAG asks: "What do we know that helps answer this?"

RLS asks: "What do we know, what did we learn, and how does this session improve the next?"

---

## The Three Loops

### Loop 1: Session Persistence

```
User prompt -> LLM processing -> Output -> Written to vault -> Available next session
```

A decision made in January is documented. In March, the LLM reads that decision and maintains consistency without the user re-explaining.

### Loop 2: Pattern Extraction

```
Repeated successful outputs -> Pattern recognized -> Pattern documented -> Pattern applied to new contexts
```

A problem-solving approach works across three projects. The approach gets extracted, named, documented. Future sessions load the pattern directly instead of re-deriving it.

### Loop 3: Architecture Evolution

```
System limitation encountered -> Solution built -> Solution documented -> Solution becomes default behavior
```

Context routing was needed. A domain routing system was built. Now all sessions auto-load relevant context without manual specification. The architecture improved itself.

---

## Five Principles

### 1. Write-Forward

Every significant output should persist. If the LLM generates something valuable, it goes into the vault. Next session starts richer.

**Implementation:** Session outputs stored as `Sessions/YYYY.MM.DD-Topic.md`

### 2. Context Routing

Don't load everything. Load what is relevant based on signal in the prompt.

**Implementation:** Keywords trigger domain context loading. See [Context Routing](context-routing.md).

### 3. Calibrated Voice

The LLM's default patterns (sycophancy, filler, performance language) degrade signal over recursions. A voice calibration layer prevents drift. Define what the output should NOT sound like, and enforce those negations at the system level.

**Implementation:** Voice rules in CLAUDE.md applied to all output. Quality floor maintained across cycles.

### 4. Structured Feedback

Outputs follow consistent formats so future retrieval is predictable. Unstructured outputs create retrieval noise.

**Implementation:** Frontmatter standards, file naming conventions, folder taxonomy.

### 5. Human-in-Loop Curation

Not everything recurses. The human decides what persists, what archives, what gets deleted. The system compounds human judgment, not raw volume.

**Implementation:** Explicit write decisions. No auto-persistence of everything.

---

## Advantages

### Over Vanilla LLM

| Problem | RLS Solution |
|---------|--------------|
| Amnesia between sessions | Vault persists context |
| Repeating yourself | Decisions documented, loaded automatically |
| Inconsistent voice | Calibration layer enforced at system level |
| Starting from zero | Previous outputs bootstrap new sessions |

### Over Standard RAG

| Problem | RLS Solution |
|---------|--------------|
| Static knowledge | Corpus grows with successful outputs |
| No learning | Patterns extracted and formalized |
| Generic retrieval | Context routing based on prompt signal |
| Quality plateau | Compounding through curated recursion |

### Over Fine-Tuning

| Problem | RLS Solution |
|---------|--------------|
| Expensive and slow | Zero-cost iteration |
| Irreversible | Context can be edited or removed |
| Requires datasets | Works from day one |
| Model-specific | Works across any LLM |

---

## The Compounding Effect

Session 1: You explain your business, preferences, constraints.
Session 10: Those are loaded automatically from vault.
Session 50: Patterns extracted from sessions 1-49 inform approach.
Session 100: The LLM knows this domain better than most human consultants because it operates on 100 sessions of curated, structured context.

You do not get smarter at prompting. The system gets smarter at responding. The gap widens with each cycle.

---

## Risks and Mitigations

**Garbage recursion** — bad outputs persist, inform future bad outputs. Mitigated by human curation. Not everything recurses. Explicit write decisions.

**Context bloat** — too much context, retrieval becomes noise. Mitigated by archival discipline and recency tracking.

**Voice drift** — LLM patterns compound across cycles. Mitigated by a voice calibration layer with negation rules at the system level.

**Single point of failure** — vault corruption collapses the system. Mitigated by cloud sync, version control, backup discipline.

---

## Implementation Checklist

- [ ] Root instruction file (CLAUDE.md equivalent)
- [ ] Domain context files (`_context.md` per area)
- [ ] Session output folder (`Sessions/`)
- [ ] Pattern extraction folder (`Patterns/`)
- [ ] Voice calibration layer (quality controls in system instructions)
- [ ] Routing logic (keyword-to-context mapping)
- [ ] Curation discipline (human decides what persists)
