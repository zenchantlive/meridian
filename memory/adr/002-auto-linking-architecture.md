# ADR 002: Auto-Linking Architecture for RLM Memory

## Status
Accepted

## Context
The MERIDIAN Brain memory system needs to automatically establish relationships between memory chunks as they are created. This enables graph traversal for context retrieval during agent reasoning.

### Requirements
1. **Automatic linking** on chunk creation without manual intervention
2. **Bidirectional links** for context (chunks in same conversation) and related content (shared tags)
3. **Unidirectional links** for temporal sequences (chunk B follows chunk A)
4. **Manual links** for user/agent assertions (supports, contradicts)
5. **Fast traversal** for retrieving related context during reasoning

## Decision

### Link Types

| Type | Direction | Auto/Manual | Trigger |
|------|-----------|-------------|---------|
| context_of | Bidirectional | Auto | Same conversation_id |
| follows | Unidirectional | Auto | Within 5 min window, same conv |
| related_to | Bidirectional | Auto | Shared tags |
| supports | Unidirectional | Manual | User/agent assertion |
| contradicts | Unidirectional | Manual | User/agent assertion |

### Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  ChunkStore │────▶│ AutoLinker  │────▶│  LinkGraph  │
│  (create)   │     │(link_on_    │     │  (index)    │
│             │     │  create)    │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                   │
       ▼                    ▼                   ▼
  chunks/              Chunk.links        link_graph.json
  (storage)            (JSON field)      (traversal index)
```

### Implementation Details

1. **AutoLinker.link_on_create()** called after chunk creation
2. Three search strategies:
   - `_find_conversation_chunks()`: Same conversation_id
   - `_find_temporal_predecessors()`: Within configurable window (default 5 min)
   - `_find_tag_related()`: Shared tags via tag index

3. **LinkGraph** maintains separate bidirectional index:
   - `_forward`: chunk_id → {link_type → [target_ids]}
   - `_reverse`: chunk_id → {link_type_reverse → [source_ids]}
   - Enables O(1) lookup for outgoing/incoming links
   - Supports BFS traversal with depth and type filters

4. **Bidirectional link maintenance**:
   - When new chunk links to existing chunk, existing chunk is updated
   - Both Chunk.links (JSON) and LinkGraph (index) are synchronized

## Consequences

### Positive
- Automatic context retrieval without manual linking
- Fast graph traversal via indexed LinkGraph
- Flexible link types support different reasoning patterns
- Bidirectional links ensure discoverability from any direction

### Negative
- Additional storage overhead for LinkGraph index
- Chunk save overhead (2x writes for bidirectional updates)
- Temporal window coupling may miss links across sessions

## Alternatives Considered

### Alternative 1: Lazy Link Resolution
- Compute links on-demand during traversal
- **Rejected**: Too slow for real-time reasoning

### Alternative 2: Single Directional Links Only
- Only store outgoing links, compute incoming on demand
- **Rejected**: Makes "find what links to this" queries expensive

### Alternative 3: Database Triggers
- Use SQLite triggers for automatic linking
- **Rejected**: Adds external dependency, violates "No DB" constraint

## References
- `brain/scripts/auto_linker.py` - Implementation
- `brain/scripts/test_linking.py` - Test suite
- D1.4 Auto-Linking System (bead: meridian-dcw)
