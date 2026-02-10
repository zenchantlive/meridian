# D1.3: REPL Environment

> Implement the RLM REPL sandbox environment with secure code execution, FINAL() termination, and state persistence.

**Priority:** P0 (Critical Path - blocks Phases 2-5)
**Bead:** meridian-dws

---

## Background

The RLM (Recursive Language Model) architecture requires an external REPL memory system. The REPL Environment provides a secure sandbox where the LLM can execute Python code to:
- Query memory (read chunks, search, traverse links)
- Process and transform data
- Decide when to return a final answer via `FINAL()`

---

## Requirements

### 1. REPL Session Management

```python
class REPLSession:
    def __init__(self, chunk_store, llm_client, max_iterations=10, timeout_seconds=60)
    def execute(self, query: str) -> dict  # Main entry point
    def get_state() -> dict
    def get_result() -> Optional[str]
```

- **R1.1:** Require ChunkStore and LLM client on initialization
- **R1.2:** Fresh REPL starts with empty state, no result, iteration_count=0
- **R1.3:** Accept configuration: max_iterations, timeout_seconds
- **R1.4:** Track iteration count across recursive calls

### 2. Secure Sandbox Execution

- **R2.1:** Block dangerous imports (os, sys, subprocess, etc.)
- **R2.2:** Block file system access outside brain/memory/
- **R2.3:** Block network operations
- **R2.4:** Block eval/exec/code compilation
- **R2.5:** Raise SandboxViolation with clear message on violation
- **R2.6:** Allow safe built-ins (len, range, dict, list, etc.)
- **R2.7:** Allow math operations and string manipulation

### 3. FINAL() Termination

```python
def FINAL(answer: str) -> None:
    """Signal that REPL has reached final answer."""
```

- **R3.1:** FINAL() sets the result and stops execution
- **R3.2:** REPL detects FINAL() call and returns result
- **R3.3:** Result is accessible via get_result()
- **R3.4:** FINAL() can only be called once per session

### 4. llm_query() Function

```python
def llm_query(prompt: str, context: dict = None) -> str:
    """Recursive LLM call within REPL."""
```

- **R4.1:** llm_query calls the configured LLM client
- **R4.2:** Response is returned as string (not auto-executed)
- **R4.3:** Iteration count increments on each call
- **R4.4:** Raise if max_iterations exceeded
- **R4.5:** Include context in prompt if provided

### 5. REPL Functions (Memory Access)

```python
def read_chunk(chunk_id: str) -> dict
def search_chunks(query: str, limit: int = 10) -> list
def list_chunks_by_tag(tag: str) -> list
def get_linked_chunks(chunk_id: str, link_type: str = None) -> list
```

- **R5.1:** All functions are available in REPL namespace
- **R5.2:** read_chunk returns chunk data or None
- **R5.3:** search_chunks returns matching chunk IDs
- **R5.4:** list_chunks_by_tag returns chunks with tag
- **R5.5:** get_linked_chunks follows links (optionally filtered by type)

### 6. State Persistence

- **R6.1:** State dict persists across iterations
- **R6.2:** User can store intermediate results in state
- **R6.3:** State is isolated per REPL session
- **R6.4:** State survives recursive llm_query() calls

### 7. Error Handling

- **R7.1:** Syntax errors in code are caught and reported
- **R7.2:** Runtime errors are caught and reported
- **R7.3:** SandboxViolation has descriptive message
- **R7.4:** Timeout after timeout_seconds
- **R7.5:** Max iterations protection

---

## Acceptance Criteria

1. **AC1:** All 75 tests in `test_repl.py` pass
2. **AC2:** REPLSession can be created with ChunkStore and LLM mock
3. **AC3:** Sandbox blocks all dangerous operations (security tests pass)
4. **AC4:** FINAL() correctly terminates and returns result
5. **AC5:** llm_query() increments iteration and returns LLM response
6. **AC6:** Memory functions work within REPL namespace
7. **AC7:** State persists across iterations

---

## Dependencies

- **Depends on:** D1.1 (JSON Storage), D1.4 (Auto-Linking)
- **Blocks:** D2.1 (LLM Query Wrapper)

---

## Notes

- Tests are already written in `brain/scripts/test_repl.py`
- Look at tests for exact expected behavior
- Security is critical - sandbox must be robust
- Keep it simple - don't over-engineer

---

## Completion

**Status:** COMPLETE (75/75 tests passing)
**Date:** 2026-02-10
**Commit:** a6b73bc, d0982a5

Core REPL functionality implemented:
- ✅ REPLSession with secure sandbox
- ✅ FINAL() termination mechanism
- ✅ llm_query() recursive function with depth tracking
- ✅ Memory access functions (read_chunk, search_chunks, list_chunks_by_tag, get_linked_chunks)
- ✅ State persistence across iterations
- ✅ Comprehensive security sandbox:
  - Blocks dangerous imports (os, sys, subprocess, etc.)
  - Blocks eval/exec/compile/open
  - Blocks __class__/__bases__/__subclasses__ exploitation
  - Blocks getattr/setattr/delattr on builtins
  - Blocks globals()/locals() manipulation
  - Memory exhaustion prevention (10MB limit)
- ✅ Error handling with proper exception propagation
- ✅ Context manager support
- ✅ Cost tracking and output capture

<promise>DONE</promise>
