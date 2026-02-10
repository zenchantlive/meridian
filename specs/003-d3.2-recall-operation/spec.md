# D3.2: RECALL Operation

> Implement the high-level RECALL operation for memory retrieval using RLM recursive traversal.

**Priority:** P1 (Blocked on D2.2)
**Bead:** meridian-nvr

---

## Background

RECALL is the inverse of REMEMBER. It uses the RLM architecture to recursively search and synthesize information from memory:
- Parse natural language query
- Traverse memory graph (chunks + links)
- Use LLM to synthesize answer
- Return confidence-weighted results

---

## Requirements

### 1. RecallOperation Interface

```python
class RecallOperation:
    def __init__(self, repl_session: REPLSession)
    def recall(self, query: str, conversation_id: str = None, 
               max_results: int = 5) -> RecallResult
```

- **R1.1:** Require REPLSession (which has LLM + memory)
- **R1.2:** Accept natural language query
- **R1.3:** Optional conversation context filter
- **R1.4:** Configurable max results

### 2. RecallResult Object

```python
@dataclass
class RecallResult:
    answer: str
    confidence: float
    source_chunks: List[str]  # chunk IDs used
    traversal_path: List[str]  # how answer was found
    iterations_used: int
    cost_usd: float
```

- **R2.1:** Natural language answer
- **R2.2:** Confidence score (0.0-1.0)
- **R2.3:** Source attribution (which chunks)
- **R2.4:** Traversal transparency

### 3. RLM Traversal Strategy

- **R3.1:** Start with keyword search for candidate chunks
- **R3.2:** Follow links (context_of, follows, related_to)
- **R3.3:** Use LLM to evaluate relevance at each step
- **R3.4:** Prune low-confidence paths
- **R3.5:** Synthesize final answer from collected evidence

### 4. Prompt Engineering

- **R4.1:** System prompt guides traversal strategy
- **R4.2:** Include chunk content + metadata in context
- **R4.3:** Instruct LLM to use FINAL() when satisfied
- **R4.4:** Include cost/iteration budget constraints

### 5. Failure Modes

- **R5.1:** No relevant chunks found → return "no memory of this"
- **R5.2:** Max iterations exceeded → return partial result
- **R5.3:** Low confidence → indicate uncertainty in answer

---

## Acceptance Criteria

1. **AC1:** Can recall information from stored chunks
2. **AC2:** Returns confidence score with answer
3. **AC3:** Traversal respects max_iterations
4. **AC4:** Source chunks are trackable
5. **AC5:** Works with linked memory graph

---

## Dependencies

- **Depends on:** D2.2 (Recursive Traversal), D3.1 (REMEMBER)
- **Blocks:** D3.3 (REASON), D4.x (Interface)

---

## Notes

- This is where the RLM magic happens
- Start simple: keyword search + link following
- LLM synthesis is key to quality answers
- Tests should verify actual recall accuracy
