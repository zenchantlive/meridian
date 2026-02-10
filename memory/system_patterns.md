# ⚙️ System Patterns

## Architecture Guidelines
*   **Storage Format:** All memory data must be stored in **Markdown** files for human readability and portability.
*   **No External DBs:** The system must function without external database servers (SQLite/JSON files acceptable for indexes, but primary storage is MD).
*   **Skill-Based Interface:** All agent interactions must go through the `meridian-guide` skill interface, not direct file manipulation.

## Code Style & Standards
*   **Python:** Follow PEP 8 standards. Type hinting is mandatory.
*   **Async:** Use `asyncio` for all I/O operations to prevent blocking the agent loop.
*   **Error Handling:** Fail gracefully with informative messages; never crash the agent.

## Known "Gotchas" / Edge Cases
*   **Pathing:** Always use absolute paths or robust relative path resolution to avoid issues between CLI and execution contexts.
*   **File Locking:** Concurrent writes to Markdown files can cause race conditions; implement simple locking or retry logic if needed.

## UX Patterns
*   **Natural Language:** The interface should feel conversational ("Remember that...") rather than command-line-like (`memory --create ...`).
*   **Confirmation:** Always confirm successful memory creation with the generated ID.
