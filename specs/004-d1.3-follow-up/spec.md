# D1.3 Follow-up: Complete REPL Test Coverage

> Complete the remaining 34 tests for D1.3 REPL Environment.

**Priority:** P1 (D1.3 core is done, this polishes edge cases)
**Bead:** meridian-dws (continuation)

---

## Background

D1.3 REPL Environment core is implemented with 41/75 tests passing. This follow-up completes the remaining test coverage for production readiness.

---

## Remaining Test Failures (34 tests)

### 1. TestLLMQuery (4 errors)

**Issues:**
- Error handling for API failures not graceful
- Context chunks not properly serialized in prompt
- Cost tracking needs mock response support
- Max depth checking needs implementation

**Fixes needed:**
```python
# _llm_query_wrapper needs:
- try/except around API call with graceful degradation  
- Proper context serialization (chunk IDs → content)
- Check _current_depth vs max_depth before calling
- Extract cost from response object
```

### 2. TestSecurity (6 errors, 1 fail)

**Issues:**
- `__class__.__bases__` exploitation not blocked
- `type(compile(...))` code object creation allowed
- `del __builtins__.open` not prevented
- `getattr(__builtins__, "__import__")` works
- `globals()["__builtins__"]` manipulation works
- `setattr(__builtins__, ...)` not blocked

**Fixes needed:**
- Add AST visitor checks for attribute access chains
- Block `.__class__`, `.__bases__`, `.__subclasses__` access
- Block direct `type()` calls with code objects
- Make builtins dict immutable or validate mutations

### 3. TestREPLFunctions (2 fails)

**Issues:**
- `list_chunks_by_tag(["tag1", "tag2"])` list argument not handled
- Path traversal in chunk ID not validated

**Fixes needed:**
- Handle list argument in wrapper
- Validate chunk IDs match pattern (no `../`)

### 4. TestRetrieveWorkflow (3 fails)

**Issues:**
- `retrieve()` doesn't execute code
- Iteration count not incremented in workflow

**Fixes needed:**
- `retrieve()` should run query loop until FINAL or max iterations
- Track iterations properly in workflow mode

### 5. TestStatePersistence (1 error)

**Issues:**
- `import sys` blocked for stderr capture test

**Decision:** Test expects sys import to work for stderr. Options:
1. Add sys to allowed imports (dangerous)
2. Remove/modify the test
3. Provide mock sys module in sandbox

**Recommendation:** Option 3 - provide limited sys module with only stderr.

### 6. TestCostTracking (3 errors)

**Issues:**
- Tests expect cost tracking methods that don't exist
- `get_cost_breakdown()` missing

**Fixes needed:**
- Add `get_cost_breakdown()` method
- Track per-call costs in list

### 7. TestEdgeCases (14 tests - not run yet)

Likely issues:
- Infinite loop detection
- Memory exhaustion prevention
- Recursion limit enforcement
- Special character handling

---

## Acceptance Criteria

1. **AC1:** All 75 tests pass
2. **AC2:** No security exploits work (block all attack vectors)
3. **AC3:** Error messages are clear and helpful
4. **AC4:** Performance acceptable (no infinite hangs)

---

## Implementation Order

1. **High Priority:** Security fixes (block exploits)
2. **Medium:** LLM query improvements (context, error handling)
3. **Medium:** retrieve() workflow implementation
4. **Low:** Cost tracking, edge cases, stderr capture

---

## Notes

- Core functionality works (41 tests pass)
- This is polish for production readiness
- Can proceed with D2.1 using current implementation
- Security fixes are most important
