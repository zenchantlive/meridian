# MERIDIAN_Brain Enhanced: Memory System Design

## Document Overview

This document provides detailed specifications for the memory system component of MERIDIAN_Brain Enhanced, including data structures, retrieval algorithms, and management operations.

**Related Document:** PRD.md, PRD-ARCH.md
**Version:** 1.0

---

## 1. Memory System Overview

### 1.1 Design Philosophy

The memory system is designed around three core principles:

**Active Memory:** Memories are not passive storage but active components that can be queried, traversed, and refined. The system treats memory as a reasoning substrate rather than a simple log.

**Confidence-Weighted:** Every memory carries a confidence score that influences retrieval priority and indicates reliability. This enables the system to reason about the certainty of its knowledge.

**Self-Improving:** Through autonomous consolidation, refinement, and feedback loops, the memory system improves its quality over time without requiring manual maintenance.

### 1.2 Memory Types

The system supports four primary memory types:

| Type | Description | Example |
|------|-------------|---------|
| **Fact** | Verifiable information about the world or user | "User works as a software engineer" |
| **Preference** | User likes, dislikes, and working preferences | "User prefers TypeScript over JavaScript" |
| **Pattern** | Recurring observations about behavior or context | "User asks for help on Sundays" |
| **Note** | General information without specific categorization | "Project deadline is March 15th" |

### 1.3 Memory Lifecycle

Memories progress through distinct lifecycle stages:

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Created │ → │ Active  │ → │ Aged    │ → │ Archived│
└─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │
     └──────────────┴──────────────┴──────────────┘
                    ↓
              Consolidated
                    ↓
              Merged or Pruned
```

---

## 2. Memory Schema

### 2.1 Core Structure

Each memory consists of two sections: YAML frontmatter for metadata, and Markdown content for the actual memory.

```markdown
---
id: mem-2026-02-10-001
type: preference
tags: [coding, language, workflow]
confidence: 0.90
created: 2026-02-10T10:00:00Z
updated: 2026-02-10T10:00:00Z
expires: 2026-08-10T10:00:00Z
source: interaction
related: []
access_count: 0
last_accessed: 2026-02-10T10:00:00Z
---

# User Prefers TypeScript for Large Projects

The user has expressed a clear preference for using TypeScript
when working on large projects. They cite type safety and
maintainability as key factors.

## Context
This preference was established during a discussion about
project architecture choices.

## Evidence
- "I really prefer TypeScript for anything above 1000 lines"
- Previously chose TypeScript for the dashboard project
```

### 2.2 Field Definitions

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | string | Unique memory identifier (auto-generated) | Yes |
| type | enum | Memory type (fact, preference, pattern, note) | Yes |
| tags | array | Categorization tags for filtering | Yes |
| confidence | float | Reliability score (0.0-1.0) | Yes |
| created | datetime | Creation timestamp (ISO 8601) | Yes |
| updated | datetime | Last update timestamp | Yes |
| expires | datetime | Optional expiration timestamp | No |
| source | enum | How memory was created (interaction, import, derived) | Yes |
| related | array | IDs of related memories | No |
| access_count | int | Number of times memory was retrieved | No |
| last_accessed | datetime | Last retrieval timestamp | No |

### 2.3 Memory Content Guidelines

Memory content should follow these guidelines:

**For Facts:**
- State information objectively
- Include source attribution when available
- Note any uncertainty or caveats

**For Preferences:**
- Quote the user when possible
- Include context about when preference was expressed
- Note any conditions or exceptions

**For Patterns:**
- Describe the observed pattern clearly
- Include example instances if helpful
- Note confidence based on observation count

**For Notes:**
- Organize information logically
- Use headers and lists for readability
- Include relevant context without being verbose

---

## 3. Retrieval System

### 3.1 Retrieval Modes

The system supports multiple retrieval modes for different use cases:

**Semantic Retrieval**

Uses embedding-based similarity to find conceptually related memories:

```
Input: "What programming languages does the user know?"
Process:
  1. Generate query embedding
  2. Compare against all memory embeddings
  3. Return top matches by cosine similarity
Output: Memories about Python, JavaScript, TypeScript
```

**Keyword Retrieval**

Uses BM25 for exact and partial text matching:

```
Input: "TypeScript"
Process:
  1. Tokenize query
  2. Calculate BM25 scores
  3. Return documents with highest term frequency
Output: All memories containing "TypeScript"
```

**Graph Traversal**

Uses memory relationships to find connected information:

```
Input: "What tools does the user have configured?"
Process:
  1. Find memories tagged "tools"
  2. Follow "related" links
  3. Collect connected memories
Output: Tool configurations and their relationships
```

**Hybrid Retrieval**

Combines multiple methods for comprehensive results:

```
Input: "User's React experience"
Process:
  1. Execute semantic search for "React experience"
  2. Execute keyword search for "React" and "frontend"
  3. Execute graph traversal from "React" tagged memories
  4. Merge and deduplicate results
  5. Apply composite scoring
Output: Comprehensive set of React-related memories
```

### 3.2 Query Language

The retrieval system supports a simple query language:

**Basic Queries**

```
"search text"              # Full text search
tag:python                 # Filter by tag
type:preference            # Filter by type
confidence:>0.8            # Filter by confidence
created:last_week          # Temporal filter
```

**Compound Queries**

```
"search text" AND tag:python
tag:frontend OR tag:backend
("search text") AND confidence:>0.7
```

**Temporal Queries**

```
created:last_hour
created:today
created:last_week
created:last_month
created:between(2026-01-01, 2026-02-01)
```

### 3.3 Retrieval Response

Retrieval responses include:

```json
{
  "query": "user preferences for code reviews",
  "memories": [
    {
      "id": "mem-2026-02-10-001",
      "title": "User Prefers Detailed Code Comments",
      "confidence": 0.90,
      "relevance": 0.95,
      "type": "preference",
      "tags": ["code-style", "documentation"],
      "snippet": "The user prefers detailed comments in code..."
    },
    {
      "id": "mem-2026-02-08-003",
      "title": "Review Style Preferences",
      "confidence": 0.85,
      "relevance": 0.88,
      "type": "preference",
      "tags": ["code-review", "workflow"],
      "snippet": "User likes asynchronous code reviews..."
    }
  ],
  "stats": {
    "total_found": 12,
    "returned": 5,
    "search_time_ms": 45
  }
}
```

---

## 4. Memory Management

### 4.1 Memory Creation

When creating a new memory, the system:

1. Generates a unique identifier
2. Validates and normalizes all fields
3. Generates embedding for semantic search
4. Creates the Markdown file
5. Updates search indexes
6. Updates metadata store
7. Triggers consolidation check if memory count threshold is met

**Creation Command:**

```python
async def create_memory(
    content: str,
    memory_type: str,
    tags: List[str],
    confidence: float = 0.7,
    related: List[str] = None,
    source: str = "interaction"
) -> MemoryReference:
    """
    Create a new memory in the system.

    Args:
        content: The main memory content (Markdown)
        memory_type: One of fact, preference, pattern, note
        tags: List of categorization tags
        confidence: Reliability score 0.0-1.0
        related: Optional list of related memory IDs
        source: How the memory was created

    Returns:
        MemoryReference with ID and confirmation
    """
```

### 4.2 Memory Update

Updates modify existing memories while preserving history:

1. Retrieve current memory content
2. Create update record with timestamp
3. Modify specified fields
4. Regenerate embedding if content changed
5. Update search indexes
6. Maintain related memory links

**Update Command:**

```python
async def update_memory(
    memory_id: str,
    content: Optional[str] = None,
    tags: Optional[List[str]] = None,
    confidence: Optional[float] = None,
    related: Optional[List[str]] = None
) -> MemoryReference:
    """
    Update an existing memory.

    Args:
        memory_id: ID of memory to update
        content: New content (replaces entirely)
        tags: New tags (replaces entirely)
        confidence: New confidence score
        related: New related memories list

    Returns:
        Updated MemoryReference
    """
```

### 4.3 Memory Deletion

The system supports soft deletion for data recovery:

1. Mark memory as deleted in metadata
2. Remove from active search indexes
3. Move to deleted/ directory
4. Log deletion for audit trail
5. Update related memories' links

**Deletion is permanent after 30 days.**

### 4.4 Memory Consolidation

Consolidation runs periodically to improve memory quality:

**Consolidation Triggers:**
- 100 new memories created since last consolidation
- 24 hours since last consolidation
- Manual trigger via skill command

**Consolidation Process:**

1. Identify similar memories (high semantic similarity)
2. For each cluster:
   - Merge common content
   - Calculate aggregate confidence
   - Preserve unique details
   - Create relationships between merged memories
3. Flag low-confidence memories for review
4. Archive memories past retention period
5. Optimize index structure

---

## 5. Confidence System

### 5.1 Confidence Calibration

Initial confidence scores are assigned based on:

| Source Type | Default Confidence | Adjustment Factors |
|-------------|-------------------|-------------------|
| Direct user statement | 0.95 | -0.10 if vague, +0.05 if repeated |
| Agent observation | 0.70 | +0.10 per confirmation, -0.10 if contradicted |
| Derived inference | 0.50 | Based on source confidence |
| Import from MERIDIAN | 0.80 | Based on original confidence |

### 5.2 Confidence Updates

Confidence scores are updated based on:

**Reinforcement:**
- Memory retrieved and used positively: +0.02
- Memory confirmed by user: +0.10
- Memory contradicted by user: -0.20

**Decay:**
- 30 days without access: -0.05
- Contradictory memory created: -0.15
- Memory marked as outdated: -0.30

### 5.3 Confidence Thresholds

The system uses confidence thresholds for quality control:

| Threshold | Action |
|-----------|--------|
| confidence >= 0.9 | High confidence, featured in retrieval |
| confidence >= 0.7 | Standard confidence, normal retrieval |
| confidence >= 0.5 | Low confidence, returned with warning |
| confidence < 0.5 | Very low, only returned if no alternatives |

---

## 6. Temporal Management

### 6.1 Temporal Decay

Memories lose retrieval priority over time using exponential decay:

```
Recency_Score = e^(-λ × days_since_update)

Where λ = 0.01 (1% decay per day)
```

**Example Decay:**
- Today: 1.00
- 7 days: 0.93
- 30 days: 0.74
- 90 days: 0.41
- 365 days: 0.03

### 6.2 Access-Driven Reinforcement

Accessing memories prevents decay:

```
Decay_Prevention = min(access_count × 0.02, 0.5)
```

Memories that are frequently accessed maintain higher retrieval priority.

### 6.3 Retention Policy

| Memory Age | Status | Action |
|------------|--------|--------|
| 0-90 days | Active | Full indexing and retrieval |
| 90-180 days | Aging | Reduced indexing, normal retrieval |
| 180-365 days | Aged | Archived index, on-demand loading |
| 365+ days | Archived | Full archive, explicit query only |

---

## 7. Memory Operations API

### 7.1 Core Operations

```python
class MemorySystem:
    """Main memory system interface"""

    async def create(
        self,
        content: str,
        memory_type: str,
        tags: List[str],
        confidence: float = 0.7,
        related: List[str] = None,
        source: str = "interaction"
    ) -> MemoryReference:
        """Create a new memory"""

    async def retrieve(
        self,
        query: str,
        filters: Optional[dict] = None,
        limit: int = 5,
        mode: str = "hybrid"
    ) -> RetrievalResult:
        """Search and retrieve memories"""

    async def update(
        self,
        memory_id: str,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        confidence: Optional[float] = None,
        related: Optional[List[str]] = None
    ) -> MemoryReference:
        """Update an existing memory"""

    async def delete(
        self,
        memory_id: str,
        permanent: bool = False
    ) -> bool:
        """Delete (or archive) a memory"""

    async def query(
        self,
        query: str,
        filters: Optional[QueryFilters] = None,
        sort: str = "relevance",
        limit: int = 10
    ) -> RetrievalResult:
        """Advanced query with full filter support"""

    async def consolidate(self) -> ConsolidationResult:
        """Run memory consolidation"""
```

### 7.2 Query Filters

```python
class QueryFilters:
    """Filters for memory queries"""

    types: Optional[List[str]] = None        # Memory types to include
    tags: Optional[List[str]] = None         # Tags to filter by
    confidence_min: float = 0.0              # Minimum confidence
    confidence_max: float = 1.0              # Maximum confidence
    created_after: Optional[datetime] = None # Temporal filter
    created_before: Optional[datetime] = None
    exclude_ids: Optional[List[str]] = None  # IDs to exclude
    include_archived: bool = False           # Include archived memories
```

---

## 8. Search Index Design

### 8.1 Index Types

**Semantic Index:**
- Stores embeddings for all active memories
- Supports similarity search queries
- Updated incrementally on memory creation/update
- Size estimate: ~100KB per 1000 memories

**Keyword Index:**
- Stores inverted index for keyword search
- Supports BM25 scoring
- Updated incrementally
- Size estimate: ~50KB per 1000 memories

**Metadata Index:**
- Stores structured metadata for filtering
- Supports rapid filtered queries
- Fully updated on consolidation
- Size estimate: ~20KB per 1000 memories

### 8.2 Index Maintenance

**Daily Tasks:**
- Remove deleted memories from indexes
- Update access counts
- Apply temporal decay to scores

**Weekly Tasks:**
- Rebuild semantic index (full)
- Optimize keyword index
- Verify index integrity

**Monthly Tasks:**
- Archive old memories from indexes
- Clean up orphaned index entries
- Generate index statistics

---

## 9. Error Handling

### 9.1 Error Types

| Error Code | Description | Handling |
|------------|-------------|----------|
| MEMORY_NOT_FOUND | Memory ID doesn't exist | Return empty result |
| INVALID_QUERY | Query syntax error | Return error with help |
| INDEX_ERROR | Index operation failed | Retry with fallback |
| STORAGE_ERROR | File operation failed | Log and return error |
| CONFLICT_ERROR | Concurrent modification | Retry with version check |

### 9.2 Retry Strategy

For transient errors:
1. First failure: Retry immediately
2. Second failure: Wait 100ms, retry
3. Third failure: Wait 500ms, retry
4. Fourth failure: Return error with suggestion

---

## 10. Performance Targets

### 10.1 Operation Latencies

| Operation | P50 | P95 | P99 |
|-----------|-----|-----|-----|
| Create Memory | 100ms | 200ms | 500ms |
| Retrieve (1 result) | 50ms | 150ms | 300ms |
| Retrieve (10 results) | 100ms | 250ms | 500ms |
| Update Memory | 100ms | 200ms | 400ms |
| Query (complex) | 150ms | 400ms | 800ms |
| Consolidate | 2s | 5s | 10s |

### 10.2 Capacity Targets

| Metric | Target | Maximum |
|--------|--------|---------|
| Active Memories | 10,000 | 50,000 |
| Index Size | 500MB | 2GB |
| Daily Operations | 1,000 | 10,000 |
| Concurrent Queries | 10 | 50 |
