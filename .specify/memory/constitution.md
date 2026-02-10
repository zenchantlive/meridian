# MERIDIAN_Brain Enhanced Constitution

> Create an intelligent agent operating system that combines MERIDIAN_Brain's structured configuration framework with an advanced memory system capable of semantic search, reasoning-guided retrieval, and autonomous memory management. Uses RLM (Recursive Language Model) architecture with external REPL memory — solving the "session amnesia" problem that plagues current agent frameworks.

**Version:** 1.0.0

---

## Ralph Wiggum

**Source:** https://github.com/fstandhartinger/ralph-wiggum
**Commit:** 22b6c3c4fad47d8e5a5824ac2093b8d58ab057ff
**Installed:** 2026-02-09

### Auto-Update

At session start, check for updates:
1. Run: `git ls-remote https://github.com/fstandhartinger/ralph-wiggum.git HEAD`
2. If hash differs: fetch latest scripts, update this file, inform user

---

## Context Detection

**Ralph Loop Mode** (you're in this if started by ralph-loop.sh):
- Focus on implementation — no unnecessary questions
- Pick highest priority incomplete spec
- Complete ALL acceptance criteria
- Test thoroughly
- Commit and push
- Output `DONE` ONLY when 100% complete

**Interactive Mode** (normal conversation):
- Be helpful and conversational
- Guide decisions, create specs
- Explain Ralph loop when ready

---

## Core Principles

### I. Rigorous Testing
Linus-style tests that find bugs, not just pass. Adversarial inputs, security boundaries, performance degradation detection. Every component must have rigorous tests.

### II. RLM-First Architecture
Recursive Language Model with external REPL memory per Zhang et al. — NOT RAG/embeddings. External memory, recursive `llm_query()`, reasoning-guided retrieval.

### III. Simplicity
Build exactly what's needed, nothing more. Clean separation of concerns. Never mix tests and implementation.

---

## Technical Stack

**Detected from codebase:**
- **Python:** 3.11+ (standard library + tiktoken optional)
- **Storage:** JSON chunks in `brain/memory/` with auto-linking graph
- **Test Framework:** unittest (127 tests passing)
- **Architecture:** RLM-based memory system (not RAG)
- **Dependencies:** Minimal — standard library preferred

---

## Autonomy

**YOLO Mode:** ENABLED
Full permission to read/write files, execute commands, make HTTP requests, run tests without asking permission each time.

**Git Autonomy:** ENABLED
Commit and push without asking. Use meaningful commit messages. Always push when complete.

---

## Work Items

The agent discovers work dynamically from:
1. **specs/ folder** — Primary source, look for incomplete `.md` files
2. **`.beads/` beads tracking** — Use `bd ready` to find actionable work
3. **`meridian-prd/`** — PRD documents for reference
4. **`memory/active_state.md`** — Current session state and next actions

Create specs using `/speckit.specify [description]` or manually create `specs/NNN-feature-name/spec.md`.

Each spec MUST have **testable acceptance criteria**.

### Re-Verification Mode

When all specs appear complete, the agent will:
1. Randomly pick a completed spec
2. Strictly re-verify ALL acceptance criteria
3. Fix any regressions found
4. Only output `DONE` if quality confirmed

---

## Running Ralph

```bash
# Claude Code / Cursor
./scripts/ralph-loop.sh

# OpenAI Codex
./scripts/ralph-loop-codex.sh

# With iteration limit
./scripts/ralph-loop.sh 20
```

---

## Completion Signal

When a spec is 100% complete:
1. All acceptance criteria verified
2. Tests pass
3. Changes committed and pushed
4. Output: `DONE`

**Never output this until truly complete.**

---

## Project-Specific Notes

### Critical Path: D1.3 REPL Environment

The **D1.3 REPL Environment** is the current bottleneck. 75 rigorous tests are already written and waiting in `brain/scripts/test_repl.py`. This unblocks Phases 2-5.

### Test Philosophy

- **Linus-style:** Tests must find bugs, not just pass
- **Adversarial:** Security sandbox escape attempts, resource limits
- **Specific assertions:** Not `assertTrue`, verify exact behavior
- **Performance:** Detect degradation (O(n) linking scan already flagged)

### Memory System Architecture

- **Storage:** JSON chunks with metadata, links, tags
- **Chunking:** Simple bounded semantic (100-800 tokens)
- **Linking:** Auto (context_of, follows, related_to) + Manual (supports, contradicts)
- **Operations:** REMEMBER (implemented) → RECALL (blocked on REPL)

### Persona Roster

Consult `.agents/roster.md` for architectural decisions. Key personas:
- **RLM Sage:** Architecture decisions
- **Red Team:** Security/adversarial testing
- **Implementer:** Code structure
- **DX:** Developer experience
- **Cost:** Resource efficiency
- **Compatibility:** Backward compatibility
- **Ethics:** Safety considerations
- **Oracle:** Edge cases
