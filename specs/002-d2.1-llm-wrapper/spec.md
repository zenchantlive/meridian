# D2.1: LLM Query Wrapper

> Create a clean interface for LLM calls with retry logic, cost tracking, and integration with the REPL environment.

**Priority:** P1 (Blocked on D1.3)
**Bead:** meridian-7gv

---

## Background

The LLM Query Wrapper provides a standardized interface for making LLM calls throughout the system. It handles:
- API abstraction (swappable providers)
- Retry logic with exponential backoff
- Cost tracking (input/output tokens)
- Timeout handling
- Response parsing

---

## Requirements

### 1. LLMClient Interface

```python
class LLMClient:
    def __init__(self, provider: str, api_key: str, model: str = None)
    def complete(self, prompt: str, **kwargs) -> LLMResponse
    def get_usage_stats() -> dict
```

- **R1.1:** Support multiple providers (openai, anthropic, local)
- **R1.2:** Provider can be swapped via configuration
- **R1.3:** Model selection per-provider with sensible defaults
- **R1.4:** API key management (env var or explicit)

### 2. LLMResponse Object

```python
@dataclass
class LLMResponse:
    text: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float
    latency_ms: int
    provider: str
    model: str
```

- **R2.1:** Include full usage metadata
- **R2.2:** Calculate cost based on provider rates
- **R2.3:** Track latency for performance monitoring

### 3. Retry Logic

- **R3.1:** Retry on transient errors (rate limit, timeout)
- **R3.2:** Exponential backoff (1s, 2s, 4s, 8s...)
- **R3.3:** Max 3 retries by default
- **R3.4:** Don't retry on auth errors or invalid requests

### 4. Integration with REPL

- **R4.1:** LLMClient can be passed to REPLSession
- **R4.2:** REPL's llm_query() uses the wrapper
- **R4.3:** Cost tracking accumulates across recursive calls

### 5. Error Handling

- **R5.1:** Raise LLMError on API failures
- **R5.2:** Include retry count in error
- **R5.3:** Distinguish transient vs permanent errors

---

## Acceptance Criteria

1. **AC1:** Can instantiate LLMClient with different providers
2. **AC2:** complete() returns LLMResponse with all fields
3. **AC3:** Retry logic works with mocked failures
4. **AC4:** Cost tracking accumulates correctly
5. **AC5:** Integrates cleanly with REPLSession

---

## Dependencies

- **Depends on:** D1.3 (REPL Environment)
- **Blocks:** D2.2 (Recursive Traversal), D3.2 (RECALL)

---

## Notes

- Start with mock/test provider for testing
- Real providers can be added later
- Cost tracking needs provider rate tables
