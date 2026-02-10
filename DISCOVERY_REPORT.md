# MERIDIAN Project Discovery Report

**Date:** 2026-02-09  
**Discovery Agent:** Initial system scan  
**Project:** MERIDIAN_Brain Enhanced - RLM Memory System

---

## Executive Summary

The MERIDIAN project is an intelligent agent operating system that combines a structured configuration framework with an advanced **RLM (Recursive Language Model)** memory system. The architecture pivoted from a RAG-based approach to a recursive LLM-driven memory retrieval system.

---

## Tech Stack Detected

### Primary Language
- **Python 3.11+** - Core implementation language

### Package Management
- **uv** - Modern Python package manager (inferred from `pyproject.toml` in subproject)
- No root-level `requirements.txt` or `pyproject.toml` found

### Key Dependencies (Inferred)
Based on code analysis in `.rlm_temp/`:
- Abstract base classes (`abc` module)
- Asyncio for I/O operations
- Typing extensions for type hints
- Dataclasses for structured data

### Task Tracking
- **beads** (bd CLI v0.49.0) - Git-backed issue tracker
- Storage: SQLite + JSONL (`.beads/issues.jsonl`)
- 25+ beads (issues) defined for RLM system implementation

### Configuration
- YAML for beads config (`.beads/config.yaml`)
- JSON for settings (`.claude/settings.json`)

---

## Project Structure

```
C:\Users\Zenchant\gemini\meridian/
├── .agents/                    # Agent skills and orchestration
│   ├── roster.md               # Agent definitions
│   └── skills/                 # Reusable skill modules
│       ├── beads/              # Beads workflow skill
│       ├── create-beads-orchestration/  # Multi-agent bootstrap
│       └── [other skills]/
├── .beads/                     # Beads issue tracking
│   ├── config.yaml             # Beads configuration
│   ├── issues.jsonl            # Issue data (source of truth)
│   └── metadata.json           # Project metadata
├── .claude/                    # Claude-specific configuration
│   ├── agents/                 # Specialized supervisor agents
│   │   ├── architect.md
│   │   ├── code-reviewer.md
│   │   ├── detective.md
│   │   ├── discovery.md
│   │   ├── scout.md
│   │   └── scribe.md
│   └── settings.json           # Project settings
├── .rlm_temp/                  # RLM implementation (WIP)
│   └── rlm/
│       ├── __init__.py
│       ├── rlm.py              # Abstract RLM base class
│       ├── repl.py             # REPL controller
│       ├── rlm_repl.py         # RLM REPL implementation
│       └── utils/              # LLM wrapper, parsing, prompts
├── memory/                     # Religious Memory System
│   ├── project_brief.md        # Core mission and tech stack
│   ├── active_state.md         # Current session state
│   ├── system_patterns.md      # Technical standards
│   └── adr/                    # Architecture Decision Records
├── meridian-prd/               # Product Requirements Documents
│   ├── PRD.md                  # Main PRD
│   ├── PRD-ARCH.md             # Architecture specification
│   ├── PRD-MEMORY.md           # Memory system design
│   ├── PRD-SKILL.md            # Skill interface spec
│   └── PRD-ROADMAP.md          # Implementation phases
├── original_repo/              # Original MERIDIAN_Brain
│   └── brain/                  # Legacy configuration structure
└── skills/                     # Project-specific skills
    └── beads/
```

---

## Key Components

### 1. RLM Core (`.rlm_temp/`)
Abstract base class for Recursive Language Models with:
- `completion(context, query)` - Generate responses with recursive context
- `cost_summary()` - Track LLM usage costs
- `reset()` - Clear state between tasks

### 2. Memory Operations (Planned)
Three core operations:
- **REMEMBER** - Store new memory (auto-chunked + auto-linked)
- **RECALL** - Find memories via RLM recursive search
- **REASON** - Explore reasoning paths (multi-hop)

### 3. Storage Layer
- **Format:** JSON-based chunk storage (not Markdown primary)
- **Structure:** Chunks with metadata, links, and content
- **Index:** Metadata index for fast lookup
- **Compatibility:** Markdown export for MERIDIAN_Brain compatibility

### 4. Beads Issue Tracking
- 25+ beads defined across 5 implementation phases
- Currently in Phase 1: Foundation (JSON storage infrastructure)
- Architecture pivot completed: RAG → RLM

---

## Supervisors Created

### 1. `supervisor-python.md`
**Location:** `.claude/agents/supervisor-python.md`

Specialized guidance for:
- Python code style (PEP 8, type hints, docstrings)
- RLM-specific patterns (async, ABC, cost tracking)
- Memory operation implementation
- Testing requirements
- Virtual environment handling

### 2. `supervisor-beads.md`
**Location:** `.claude/agents/supervisor-beads.md`

Specialized guidance for:
- Beads workflow (bd CLI commands)
- Issue lifecycle management
- Worktree workflow
- Epic handling
- Session completion checklist

### 3. `supervisor-memory.md`
**Location:** `.claude/agents/supervisor-memory.md`

Specialized guidance for:
- RLM vs RAG architecture differences
- JSON chunk storage schema
- REMEMBER/RECALL/REASON operation specs
- Auto-linking rules
- Data integrity checks
- Performance targets

---

## Recommendations

### Immediate Actions
1. **Create `pyproject.toml`** at root level with:
   - Python version requirement (>=3.11)
   - Core dependencies (asyncio, typing)
   - Dev dependencies (pytest, mypy)
   - UV configuration

2. **Set up pre-commit hooks** for:
   - Python linting (ruff/flake8)
   - Type checking (mypy)
   - Beads workflow validation

3. **Create test infrastructure**:
   - `tests/` directory
   - pytest configuration
   - Mock LLM for deterministic RLM testing

### Architecture Priorities
1. **Complete Phase 1 Foundation:**
   - D1.1: JSON Storage Infrastructure (`meridian-8mh`)
   - D1.4: Auto-Linking System (`meridian-dcw`)

2. **Implement Core RLM:**
   - D2.1: LLM Query Wrapper (`meridian-7gv`)
   - D2.2: Recursive Traversal Engine (`meridian-ail`)
   - D2.3: Cost Tracking (`meridian-81t`)

3. **Build Memory Operations:**
   - D3.1: REMEMBER (`meridian-emo`)
   - D3.2: RECALL (`meridian-nvr`)
   - D3.3: REASON (`meridian-dd1`)

### Tooling Suggestions
- **Linting:** ruff (fast, modern replacement for flake8/black)
- **Type Checking:** mypy (strict mode)
- **Testing:** pytest with asyncio support
- **Documentation:** mkdocs or sphinx
- **CI/CD:** GitHub Actions for testing and beads sync

---

## Current Status

| Aspect | Status |
|--------|--------|
| Architecture Design | ✅ Complete (PRD-ARCH.md) |
| Issue Tracking | ✅ Active (25 beads) |
| RLM Core | 🚧 In Progress (`.rlm_temp/`) |
| Storage Layer | 🚧 Phase 1 (JSON infrastructure) |
| Memory Operations | ⏳ Planned (Phases 2-3) |
| Testing | ⏳ Not started |
| Documentation | 🚧 In Progress |

---

## Next Steps

1. Run `bd ready` to find available work
2. Claim D1.1 (JSON Storage Infrastructure) or D2.1 (LLM Query Wrapper)
3. Create worktree: `bd worktree create <id>`
4. Implement with supervisor guidance
5. Close and sync when complete

---

## References

- **Project Brief:** `memory/project_brief.md`
- **Architecture:** `meridian-prd/PRD-ARCH.md`
- **Active State:** `memory/active_state.md`
- **Beads Config:** `.beads/config.yaml`
- **Orchestration:** `CLAUDE.md`

---

*Report generated by Discovery Agent*
*Use `bd ready` to find available work*
