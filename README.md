# MERIDIAN Brain Enhanced 🧠

> A Recursive Language Model (RLM) memory system for AI agents, forked from MERIDIAN_Brain.

[![Tests](https://img.shields.io/badge/tests-127%20passing-green)]()
[![Beads](https://img.shields.io/badge/beads-24%20active-blue)]()
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)]()

## 🎯 What is This?

MERIDIAN Brain Enhanced adds an **intelligent memory layer** to the original MERIDIAN_Brain configuration framework. Instead of static configuration files, agents get:

- **Semantic memory storage** - JSON-based chunks with metadata
- **Recursive retrieval** - LLM-driven memory exploration via REPL
- **Automatic linking** - Context, temporal, and tag-based relationships
- **Confidence scoring** - Weighted recall based on reliability

### RLM vs RAG

| Approach | How it works | Best for |
|----------|--------------|----------|
| **RAG** (Vector search) | Embed → Index → Retrieve | Document search |
| **RLM** (This project) | LLM writes code to explore memory | Reasoning, synthesis |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT (Claude/GPT/etc)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                 MERIDIAN Brain Enhanced                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ REMEMBER    │  │ RECALL      │  │ REASON              │ │
│  │ (store)     │  │ (retrieve)  │  │ (explore)           │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
│         │                │                    │            │
│         └────────────────┼────────────────────┘            │
│                          ▼                                 │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              RLM Core (REPL Environment)            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │  │
│  │  │ llm_query│  │  FINAL   │  │ Python Sandbox   │  │  │
│  │  │ (recursive│  │ (result) │  │ (safe execution) │  │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘  │  │
│  └─────────────────────────────────────────────────────┘  │
│                          │                                 │
│         ┌────────────────┼────────────────┐                │
│         ▼                ▼                ▼                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │Chunking     │  │ChunkStore   │  │AutoLinker   │       │
│  │Engine       │  │(JSON)       │  │(Graph)      │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   brain/memory/ (JSON)                      │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ chunks/YYYY-MM/ │  │ index/          │                   │
│  │   chunk-*.json  │  │   metadata.json │                   │
│  └─────────────────┘  └─────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd meridian

# Install dependencies (when we add pyproject.toml)
pip install -e .
```

### Basic Usage

```python
from brain.scripts import ChunkStore, RememberOperation

# Initialize storage
store = ChunkStore("brain/memory")

# Create remember operation
remember = RememberOperation(store)

# Store a memory
result = remember.remember(
    content="User prefers Python over JavaScript for backend work",
    conversation_id="conv-123",
    tags=["preferences", "coding"],
    confidence=0.95
)

print(f"Created {result['chunks_created']} chunks")
# Output: Created 1 chunks
```

### Running Tests

```bash
# Run all tests
python brain/scripts/test_storage.py      # 34 tests
python brain/scripts/test_chunking.py     # 26 tests
python brain/scripts/test_linking.py      # 23 tests
python brain/scripts/test_remember.py     # 44 tests

# Or run specific test
python -m unittest test_remember.TestRememberValidation
```

## 📁 Project Structure

```
meridian/
├── brain/                      # Core memory system
│   ├── memory/                 # Storage
│   │   ├── chunks/YYYY-MM/     # Chunk files (JSON)
│   │   ├── index/              # Indexes (metadata, tags, links)
│   │   └── SCHEMA.md           # Schema documentation
│   ├── scripts/                # Python implementation
│   │   ├── memory_store.py     # ChunkStore (D1.1)
│   │   ├── chunking_engine.py  # ChunkingEngine (D1.2)
│   │   ├── auto_linker.py      # AutoLinker (D1.4)
│   │   ├── remember_operation.py # RememberOperation (D3.1)
│   │   └── test_*.py           # Test suites
│   └── worktrees/              # Development worktrees
├── memory/                     # Project memory (docs)
│   ├── active_state.md         # Current session state
│   ├── project_brief.md        # Mission & tech stack
│   ├── system_patterns.md      # Standards & gotchas
│   └── adr/                    # Architecture decisions
├── meridian-prd/               # Product requirements
│   ├── PRD.md                  # Main PRD
│   ├── PRD-MEMORY.md           # Memory system design
│   ├── PRD-ROADMAP.md          # Implementation roadmap
│   └── ...
├── .agents/                    # Agent configuration
│   └── roster.md               # Persona roster
├── .claude/                    # Claude orchestration
│   ├── agents/                 # Subagent definitions
│   └── hooks/                  # Workflow hooks
├── .beads/                     # Issue tracking (beads)
│   └── issues.jsonl            # Task database
└── README.md                   # This file
```

## 📊 Implementation Status

| Phase | Component | Status | Tests |
|-------|-----------|--------|-------|
| **Phase 1** | Foundation | 🟢 Complete | 127 |
| D1.1 | JSON Storage | ✅ Done | 34 |
| D1.2 | Chunking Engine | ✅ Done | 26 |
| D1.3 | REPL Environment | ⏳ Ready | 75 |
| D1.4 | Auto-Linking | ✅ Done | 23 |
| **Phase 2** | RLM Core | ⏳ Waiting | - |
| D2.1 | LLM Query Wrapper | 🔴 Blocked | - |
| D2.2 | Recursive Traversal | 🔴 Blocked | - |
| D2.3 | Cost Tracking | 🔴 Blocked | - |
| **Phase 3** | Memory Ops | 🟡 Partial | 44 |
| D3.1 | REMEMBER | ✅ Done | 44 |
| D3.2 | RECALL | 🔴 Blocked | - |
| D3.3 | REASON | 🔴 Blocked | - |
| **Phase 4** | Interface | 🔴 Not started | - |
| **Phase 5** | Polish | 🔴 Not started | - |

**Total: 127 tests passing, 75 tests ready**

## 🧠 Key Concepts

### Chunks

The basic unit of memory:

```json
{
  "id": "chunk-2026-02-10-a1b2c3d4",
  "content": "User decided to use RLM instead of RAG",
  "tokens": 15,
  "type": "decision",
  "metadata": {
    "created": "2026-02-10T21:37:00Z",
    "conversation_id": "conv-abc123",
    "confidence": 0.95,
    "access_count": 3
  },
  "links": {
    "context_of": ["conv-abc123"],
    "follows": ["chunk-2026-02-10-previous"],
    "related_to": ["chunk-2026-02-09-architecture"]
  },
  "tags": ["architecture", "rlm", "decision"]
}
```

### Link Types

| Type | Description | Auto |
|------|-------------|------|
| `context_of` | Same conversation | ✅ |
| `follows` | Temporal sequence | ✅ |
| `related_to` | Shared tags | ✅ |
| `supports` | Strengthens another | Manual |
| `contradicts` | Opposes another | Manual |

### Chunking Strategy

**Simple Bounded Semantic:**
1. Split on paragraphs (`\n\n`)
2. Merge small chunks (< 100 tokens)
3. Split large chunks (> 800 tokens) at sentences
4. Auto-detect content type from keywords

## 🔧 Development

### Using Beads (Issue Tracking)

```bash
# See available work
bd ready

# Create a task
bd create "Task name" -d "Description"

# Start work
bd update <id> --status=in_progress

# Complete
bd close <id>

# Sync with git
bd sync
```

### Running the Persona Protocol

The project uses a multi-persona system (see `.agents/roster.md`):

| Persona | Role |
|---------|------|
| Elena | RLM Architecture Sage |
| Marcus | Red Team / Security |
| Amina | Unintended Consequences |
| Jake | Practical Implementer |
| Zoe | Developer Experience |
| Arjun | Cost & Performance |
| Samira | Compatibility Guardian |
| Priya | Ethics & Privacy |

### Code Standards

- **Tests:** Linus-style rigorous tests required for all components
- **Separation:** Never mix tests and implementation
- **Validation:** All inputs validated, all errors handled
- **Documentation:** Docstrings for all public APIs

## 📝 Documentation

- [Product Requirements](meridian-prd/PRD.md)
- [Memory System Design](meridian-prd/PRD-MEMORY.md)
- [Implementation Roadmap](meridian-prd/PRD-ROADMAP.md)
- [Chunk Schema](brain/MEMORY_SCHEMA.md)
- [Active State](memory/active_state.md)

## 🤝 Contributing

This is a research/experimental fork. For the original MERIDIAN_Brain, see the upstream repository.

### Current Priorities

1. **D1.3 REPL Environment** - Critical path, unblocks everything else
2. **D2.1 LLM Query Wrapper** - API integration with cost tracking
3. **D3.2 RECALL Operation** - Memory retrieval workflow

## 📄 License

MIT License - See original MERIDIAN_Brain repository for details.

## 🙏 Acknowledgments

- Original MERIDIAN_Brain framework
- RLM paper: Zhang et al. "Recursive Language Models"
- rlm_repl reference implementation

