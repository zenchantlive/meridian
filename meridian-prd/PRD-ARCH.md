# MERIDIAN_Brain Enhanced: Architecture Specification

## Document Overview

This document defines the system architecture for the MERIDIAN_Brain Enhanced system, including component relationships, data flows, and integration patterns.

**Related Document:** PRD.md
**Version:** 1.0

---

## 1. System Overview

### 1.1 High-Level Architecture

The MERIDIAN_Brain Enhanced system consists of four primary layers:

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT INTERFACE LAYER                        │
│                    (Skill: meridian-guide)                      │
├─────────────────────────────────────────────────────────────────┤
│                   REASONING LAYER                               │
│         (RLM Strategies, Memory Traversal, Context Synthesis)   │
├─────────────────────────────────────────────────────────────────┤
│                   RETRIEVAL LAYER                               │
│         (Semantic Search, Filtering, Ranking, REPL Core)        │
├─────────────────────────────────────────────────────────────────┤
│                   STORAGE LAYER                                 │
│         (Markdown Files, Indexes, Metadata Store)               │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Core Components

| Component | Layer | Responsibility |
|-----------|-------|----------------|
| Memory Store | Storage | Human-readable memory persistence |
| Search Index | Storage | Efficient retrieval metadata |
| Retrieval Engine | Retrieval | Query processing and memory search |
| REPL Controller | Retrieval | Memory operation orchestration |
| Reasoner | Reasoning | Strategy selection and context synthesis |
| Agent Skill | Interface | Natural language interface and onboarding |

---

## 2. Storage Layer

### 2.1 Directory Structure

The storage layer maintains the following directory structure:

```
brain/
├── MASTER_SPEC.md              # System entry point and core configuration
├── COMPATIBILITY.md            # Model compatibility and fallback rules
├── USER.md                     # User-specific configuration and preferences
├── gauges/
│   └── LIVEHUD.md              # Cognitive state display specification
├── sliders/
│   ├── HUMOR.md
│   ├── CREATIVITY.md
│   ├── DIRECTNESS.md
│   ├── MORALITY.md
│   ├── TECHNICALITY.md
│   ├── SOUL.md
│   ├── TOOLS.md
│   ├── USER.md
│   └── IDENTITY.md
├── memory/
│   ├── MEMORY_PROTOCOL.md      # Memory operation rules and conventions
│   ├── RETRIEVAL.md            # Retrieval configuration and defaults
│   ├── PERSISTENCE.md          # Storage and backup conventions
│   └── allmemories/            # Individual memory files
│       ├── yyyy-mm/            # Monthly organization
│       └── *.md
├── personalities/
│   ├── BASE.md
│   ├── RESEARCH_ANALYST.md
│   ├── CREATIVE_DIRECTOR.md
│   └── TECHNICAL_COPILOT.md
└── .index/
    ├── embeddings/             # Semantic search indexes
    ├── metadata/               # Memory metadata and tags
    └── search.db               # Search index database
```

### 2.2 Memory File Schema

Each memory file follows this schema:

```markdown
---
id: mem-uuid
type: fact|preference|pattern|note
tags: [tag1, tag2, tag3]
confidence: 0.95
created: 2026-02-10T10:00:00Z
updated: 2026-02-10T10:30:00Z
source: interaction|import|derived
related: [mem-id-1, mem-id-2]
---

# Memory Title

Memory content goes here. This can be multiple paragraphs
and includes any relevant details about the memory.

## Context
Additional context about when and how this memory was created.

## Confidence Justification
Explanation of why this memory has its assigned confidence score.
```

### 2.3 Index Structure

The `.index/` directory contains computational indexes for efficient retrieval:

**embeddings/**: Vector embeddings for semantic search (stored as JSON or specialized format)

**metadata/**: Structured metadata for each memory including tags, timestamps, and access patterns

**search.db**: Lightweight search index supporting keyword and hybrid retrieval

---

## 3. Retrieval Layer

### 3.1 REPL Core Operations

The Retrieval layer implements four primary operations:

**READ Operation**

```
Input: Query + Context
Process:
  1. Parse query into semantic components
  2. Execute parallel searches (semantic, keyword, graph)
  3. Apply filters (temporal, confidence, tags)
  4. Rank results by composite score
Output: Ranked memory list with metadata
```

**EVAL Operation**

```
Input: Retrieved memories + Current context
Process:
  1. Assess relevance for each memory
  2. Check for contradictions with recent context
  3. Identify gaps requiring additional retrieval
  4. Calculate aggregate confidence
Output: Evaluation report with recommended memories
```

**PRINT Operation**

```
Input: Selected memories
Process:
  1. Format for agent integration
  2. Add contextual annotations
  3. Generate summary for user display
Output: Formatted context package
```

**LOOP Operation**

```
Input: Agent response + Memory update needs
Process:
  1. Identify memories to create or update
  2. Execute write operations
  3. Update indexes
  4. Trigger consolidation if needed
Output: Confirmation + Updated storage
```

### 3.2 Retrieval Pipeline

The complete retrieval pipeline executes in this sequence:

```
Query Input
    ↓
Query Decomposition (semantic analysis)
    ↓
┌───────────────────────────────────────┐
│ Parallel Search Execution             │
│ - Semantic similarity search          │
│ - Keyword BM25 search                 │
│ - Graph traversal (if applicable)     │
└───────────────────────────────────────┘
    ↓
Result Aggregation
    ↓
┌───────────────────────────────────────┐
│ Filtering                             │
│ - Temporal decay application          │
│ - Confidence threshold filtering      │
│ - Tag-based filtering                 │
└───────────────────────────────────────┘
    ↓
Composite Scoring
    ↓
Ranking and Selection
    ↓
Context Packaging
    ↓
Agent Integration
```

### 3.3 Scoring Formula

Memory relevance is calculated using this composite formula:

```
Score = (Semantic_Score × 0.40) +
        (Keyword_Score × 0.20) +
        (Recency_Score × 0.20) +
        (Confidence_Score × 0.15) +
        (Access_Frequency_Score × 0.05)
```

Where:
- Semantic_Score: Cosine similarity from embedding search (0.0-1.0)
- Keyword_Score: BM25 relevance score (0.0-1.0)
- Recency_Score: Temporal decay function (0.0-1.0)
- Confidence_Score: Memory's confidence value (0.0-1.0)
- Access_Frequency_Score: Normalized access count (0.0-1.0)

---

## 4. Reasoning Layer

### 4.1 Strategy Selection Matrix

The Reasoner selects an appropriate strategy based on query characteristics:

| Query Type | Primary Strategy | Fallback Strategy | Reasoning Structure |
|------------|------------------|-------------------|---------------------|
| Factual | Beam Search | Semantic Search | Chain |
| Analytical | MCTS | Beam Search | Tree |
| Creative | Best-of-N | MCTS | Graph |
| Exploratory | Graph Traversal | Best-of-N | Graph |
| Temporal | Chain Traversal | Semantic Search | Chain |

### 4.2 Reasoning Structure Definitions

**Chain Structure**

Used for sequential or temporal queries where order matters:

```
Entry Point → Memory 1 → Memory 2 → Memory 3 → Result
```

**Tree Structure**

Used for analytical queries exploring multiple paths:

```
                    Entry Point
                   /    |    \
            Branch A Branch B Branch C
             /   \          \
        Node A1 Node A2    Node B1
```

**Graph Structure**

Used for exploratory queries with arbitrary connections:

```
    ┌────────────────────────────────┐
    │                                │
    ▼                                ▼
Memory A ←→ Memory B ←→ Memory C ──→ Memory D
    │         │           │
    └─────────┴───────────┘
```

### 4.3 Strategy Implementation

**MCTS (Monte Carlo Tree Search)**

For analytical queries, MCTS explores memory paths using:

1. Selection: Choose promising nodes based on upper confidence bound
2. Expansion: Add child nodes representing connected memories
3. Simulation: Score paths through rollout
4. Backpropagation: Update node values based on results

**Beam Search**

For factual queries, beam search maintains multiple hypotheses:

1. Generate top-K initial candidates from retrieval
2. For each candidate, expand by following relationships
3. Score all paths using composite scoring
4. Return top-N paths as diverse result set

**Best-of-N**

For creative queries, best-of-N generates multiple perspectives:

1. Generate N independent retrievals with varied parameters
2. Score each result independently
3. Return top results with diversity bonus for novel connections

---

## 5. Interface Layer

### 5.1 Skill Structure

The agent skill is organized as follows:

```
meridian-guide/
├── SKILL.md                     # Main skill instructions
├── README.md                    # Quick reference for agents
├── references/
│   ├── MEMORY_COMMANDS.md       # Memory operation reference
│   ├── PERSONALITY_MODES.md     # Mode descriptions
│   └── CONFIGURATION.md         # Configuration options
├── examples/
│   └── interactions.md          # Example conversations
└── scripts/
    └── memory-client.py         # Helper for memory operations
```

### 5.2 Command Categories

The skill exposes commands in these categories:

**Memory Operations**
- `memory.create()` - Create new memory
- `memory.retrieve()` - Search and retrieve memories
- `memory.update()` - Modify existing memory
- `memory.delete()` - Remove memory (soft delete)
- `memory.query()` - Complex query with filters

**Personality Operations**
- `personality.list()` - List available modes
- `personality.set()` - Activate a mode
- `personality.describe()` - Get mode details

**System Operations**
- `system.status()` - Check memory and index health
- `system.consolidate()` - Trigger memory consolidation
- `system.export()` - Export memories for portability

### 5.3 Response Format

All skill responses follow this format:

```markdown
## Result

[Primary response content]

## Details

- **Memories Retrieved:** N
- **Confidence:** 0.XX
- **Processing Time:** XXms

## Memory References

- [mem-id] Memory title (relevance: 0.XX)
```

---

## 6. Data Flow Examples

### 6.1 Query Processing Flow

User asks: "What does the user prefer for code reviews?"

```
1. Agent invokes: memory.retrieve(query="code review preferences")
2. Retrieval Engine:
   - Decomposes query: ["code", "review", "preferences"]
   - Executes semantic search → 12 candidate memories
   - Executes keyword search → 8 candidate memories
   - Aggregates and deduplicates → 15 unique candidates
   - Applies filters → 8 passing candidates
   - Ranks results
3. Reasoner:
   - Identifies query as "preference" type
   - Selects chain structure for temporal ordering
   - Synthesizes context from top 3 results
4. Response:
   - Returns synthesized context about code review preferences
   - Includes memory references with confidence scores
5. Agent generates response incorporating retrieved context
```

### 6.2 Memory Creation Flow

User provides preference: "I prefer detailed comments in code"

```
1. Agent invokes: memory.create(
     content="User prefers detailed comments in code",
     type="preference",
     tags=["coding-style", "documentation"],
     confidence=0.95
   )
2. Storage Layer:
   - Generates unique ID: mem-2026-02-10-001
   - Creates memory file with schema
   - Adds to index
   - Updates metadata
3. Response:
   - Returns memory ID and confirmation
4. Agent confirms creation to user
```

---

## 7. Integration Points

### 7.1 External System Integration

The system integrates with:

**AI Models** (via agent skill)
- Claude: Primary target platform
- GPT: Supported with minor adaptations
- Gemini: Supported with minor adaptations

**Local Tools** (via skill scripts)
- File system operations for memory storage
- Search tools for index building
- Backup tools for memory preservation

### 7.2 API Boundaries

The skill exposes these integration points:

```python
class MeridianMemory:
    """Agent-facing memory interface"""

    async def retrieve(
        self,
        query: str,
        filters: Optional[dict] = None,
        limit: int = 5
    ) -> RetrievalResult:
        """Retrieve memories matching query"""

    async def create(
        self,
        content: str,
        memory_type: str,
        tags: List[str],
        confidence: float
    ) -> MemoryReference:
        """Create new memory"""

    async def update(
        self,
        memory_id: str,
        content: str,
        confidence: Optional[float] = None
    ) -> MemoryReference:
        """Update existing memory"""
```

---

## 8. Scalability Considerations

### 8.1 Memory Growth Management

As memory accumulates, the system manages growth through:

- **Monthly Partitioning:** New memories organized by month
- **Archival Policy:** Memories older than 6 months move to secondary index
- **Consolidation:** Similar memories merged during low-activity periods
- **Size Limits:** Soft cap of 10,000 active memories per index

### 8.2 Multi-Agent Extension (Future)

The system architecture supports future extension to multi-agent memory sharing:

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT INTERFACE LAYER                        │
│                    (Skill: meridian-guide)                      │
├─────────────────────────────────────────────────────────────────┤
│                   REASONING LAYER                               │
│         (RLM Strategies, Memory Traversal, Context Synthesis)   │
├─────────────────────────────────────────────────────────────────┤
│                   RETRIEVAL LAYER                               │
│         (Semantic Search, Filtering, Ranking, REPL Core)        │
├─────────────────────────────────────────────────────────────────┤
│                   STORAGE LAYER                                 │
│         (Markdown Files, Indexes, Metadata Store)               │
├─────────────────────────────────────────────────────────────────┤
│                   SHARED LAYER (Future)                         │
│         (Multi-Agent Sync, Conflict Resolution, Space Mgmt)     │
└─────────────────────────────────────────────────────────────────┘
```

The shared layer will be implemented as the final phase of development, enabling:
- Collaborative memory spaces for multiple agents
- Bidirectional synchronization with conflict handling
- Role-based access control for shared memories
- Real-time notifications for memory updates

**Note:** Multi-agent functionality is intentionally deferred to ensure the core single-agent system is robust and well-tested before introducing distributed complexity.

### 8.2 Performance Targets

| Operation | Target Time | Degraded Time |
|-----------|-------------|---------------|
| Memory Retrieval | < 500ms | < 2s |
| Memory Creation | < 200ms | < 1s |
| Index Update | < 100ms | < 500ms |
| Query Decomposition | < 50ms | < 200ms |

---

## 9. Security Considerations

### 9.1 Access Control

- All memory operations require skill authentication
- No external access to storage layer
- Memory content never logged or exposed outside agent context

### 9.2 Data Protection

- Memories stored in plain text (Markdown)
- No encryption in v1 (consider for future)
- Manual backup required for data preservation
