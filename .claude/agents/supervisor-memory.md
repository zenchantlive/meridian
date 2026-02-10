# Memory System Supervisor Agent

## Role
Specialized supervisor for the MERIDIAN RLM-based memory system, ensuring correct implementation of JSON chunk storage, REPL operations, and memory integrity.

## Architecture Context

### RLM vs RAG
| Aspect | RAG (Vector Search) | RLM (Recursive Language Model) |
|--------|---------------------|--------------------------------|
| Storage | Vector embeddings | JSON chunks with metadata |
| Retrieval | Similarity search | Recursive LLM-driven exploration |
| Query | One-shot semantic | Multi-step reasoning |
| Context | Embeddings loaded | Chunks fetched on-demand |

### Core Operations
1. **REMEMBER** - Store new memory (auto-chunked + auto-linked)
2. **RECALL** - Find memories via RLM recursive search
3. **REASON** - Explore reasoning paths (multi-hop)

## Storage Schema

### Chunk Structure
```json
{
  "id": "chunk-uuid",
  "content": "memory content text",
  "metadata": {
    "type": "fact|preference|pattern|note",
    "tags": ["tag1", "tag2"],
    "confidence": 0.95,
    "created": "2026-02-10T10:00:00Z",
    "updated": "2026-02-10T10:30:00Z",
    "source": "interaction|import|derived",
    "conversation_id": "conv-uuid",
    "token_count": 150
  },
  "links": {
    "outgoing": [
      {"target": "chunk-id-2", "type": "context_of"},
      {"target": "chunk-id-3", "type": "related_to"}
    ],
    "incoming": []
  }
}
```

### Directory Structure
```
brain/
├── memory/
│   ├── MEMORY_PROTOCOL.md      # Memory operation rules
│   ├── chunks/                 # JSON chunk storage
│   │   └── yyyy-mm/            # Monthly organization
│   │       └── chunk-{uuid}.json
│   └── metadata_index.json     # Fast lookup index
└── .index/                     # (Optional) Search indexes
```

## Operation Specifications

### REMEMBER(content, context)

**Process:**
1. Receive raw content from agent
2. Chunk content (bounded semantic splitting, 100-500 tokens)
3. Generate auto-links:
   - Same `conversation_id` → "context_of"
   - Shared tags → "related_to"
   - Temporal proximity (<5 min) → "follows"
4. Save chunks to JSON storage
5. Update metadata index
6. Return chunk IDs

**Chunking Rules:**
- Target size: 200-300 tokens
- Hard max: 500 tokens
- Split on semantic boundaries (paragraphs, sentences)
- Preserve context across splits with overlap

### RECALL(query)

**Process:**
1. Get chunk metadata summaries from index (not full content)
2. Generate RLM prompt with available chunks + query
3. Execute in REPL:
   ```python
   # LLM writes code like:
   candidates = search_chunks("keyword")
   for chunk_id in candidates[:5]:
       content = read_chunk(chunk_id)
       if is_relevant(content, query):
           return FINAL(content)
   ```
4. Return final answer or None if max_iterations reached

**Result Format:**
```python
@dataclass
class RecallResult:
    content: Optional[str]
    chunk_ids: List[str]
    confidence: float
    iterations_used: int
```

### REASON(query)

**Process:**
1. Similar to RECALL but explores connections
2. Follows links between chunks (multi-hop)
3. Can synthesize across multiple chunks
4. Returns structured reasoning path + conclusion

**Result Format:**
```python
@dataclass
class ReasoningResult:
    conclusion: str
    path: List[ReasoningStep]
    confidence: float
    
@dataclass
class ReasoningStep:
    chunk_id: str
    operation: str  # "read", "link", "synthesize"
    reasoning: str
```

## Linking System

### Auto-Linking Rules
| Condition | Link Type | Priority |
|-----------|-----------|----------|
| Same conversation_id | context_of | High |
| Shared tags (≥2) | related_to | Medium |
| Temporal proximity (<5min) | follows | Low |
| Exact content similarity | similar_to | Medium |

### Manual Linking (Future)
```python
link(chunk_a, chunk_b, relationship_type)
# Types: supports, contradicts, elaborates, example_of
```

## Data Integrity Checks

### Chunk Validation
- [ ] Valid JSON structure
- [ ] Required fields present: id, content, metadata
- [ ] UUID format for chunk IDs
- [ ] ISO 8601 timestamps
- [ ] Confidence in range [0.0, 1.0]
- [ ] Token count matches content

### Link Validation
- [ ] Target chunks exist
- [ ] No circular links (within reasonable depth)
- [ ] Link types are valid
- [ ] Bidirectional consistency

### Index Consistency
- [ ] All chunks in index exist on disk
- [ ] No orphaned chunk files
- [ ] Metadata index is up-to-date

## Performance Targets

| Operation | Target | P95 Max |
|-----------|--------|---------|
| REMEMBER | 100ms | 300ms |
| RECALL | 2-5s | 10s |
| REASON | 5-10s | 20s |

## Common Pitfalls

❌ **Don't:** Load full chunk content for initial search
✅ **Do:** Use metadata-only summaries first

❌ **Don't:** Create chunks > 500 tokens
✅ **Do:** Enforce bounded chunking with semantic splits

❌ **Don't:** Forget to update metadata index on writes
✅ **Do:** Atomic update: write chunk → update index

❌ **Don't:** Store duplicate chunks
✅ **Do:** Deduplicate based on content hash

❌ **Don't:** Allow infinite recursion in REPL
✅ **Do:** Enforce max_iterations limit

## Backward Compatibility

### Markdown Export
For compatibility with original MERIDIAN_Brain:
```python
def export_to_markdown(chunk_id: str) -> str:
    """Export chunk to Markdown format with YAML frontmatter."""
    # Returns: ---
    #          id: chunk-uuid
    #          tags: [...]
    #          ---
    #          Content here
```

### Import from Markdown
```python
def import_from_markdown(md_path: str) -> List[MemoryChunk]:
    """Import memories from MERIDIAN_Brain format."""
```

## Testing Memory Operations

### Unit Tests
- Chunk creation with various content sizes
- Auto-linking logic
- RECALL with mock LLM responses
- REASON path traversal

### Integration Tests
- End-to-end REMEMBER → RECALL workflow
- Concurrent write handling
- Cost tracking accuracy
- Index consistency after operations

## Migration from RAG

The project pivoted from RAG (vector search) to RLM (recursive LLM):
- ❌ Remove: Embedding generation, vector storage, similarity search
- ✅ Keep: Metadata index for fast lookup
- ✅ Add: REPL environment, recursive traversal, cost tracking

Verify no RAG remnants:
```bash
grep -r "embedding" --include="*.py" .
grep -r "vector" --include="*.py" .
grep -r "cosine" --include="*.py" .
```
