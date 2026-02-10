# 🚀 Project Brief: MERIDIAN_Brain Enhanced

## 1. Mission Statement
Create an intelligent agent operating system that combines MERIDIAN_Brain's structured configuration framework with an advanced memory system capable of semantic search, reasoning-guided retrieval, and autonomous memory management.

## 2. Core Problem
Current agent frameworks suffer from passive/unstructured memory, manual configuration burdens, and static reasoning strategies, leading to "session amnesia" and ineffective long-term assistance.

## 3. Solution Overview
- **Intelligent Memory Layer:** REPL-style memory with semantic search and confidence weighting.
- **RLM-Inspired Architecture:** Integration of reasoning structures (chains, trees, graphs) and strategies (MCTS, beam search).
- **Agent Skill Interface:** A dedicated skill (`meridian-guide`) that abstracts system complexity.
- **Backward Compatibility:** Preserves standard MERIDIAN_Brain file structures.

## 4. Key Features (Scope)
*   **Semantic Search:** Across all stored memories with confidence ranking.
*   **Reasoning Integration:** Multi-structure traversal (Chain, Tree, Graph).
*   **Skill Interface:** Natural language memory operations ("Remember that...", "What do you know about...").
*   **Autonomous Management:** Memory consolidation, decay, and refinement.

## 5. Success Metrics
*   Agents can retrieve relevant historical context via natural language.
*   Memory operations are fully abstracted behind the skill interface.
*   Zero manual configuration required for new agent onboarding.
*   System maintains backward compatibility with existing MERIDIAN setups.

## 6. Non-Negotiables
*   **Human-Readable Storage:** All memory must remain in Markdown format.
*   **Local-Only:** No external database dependencies or cloud sync in v1.
*   **Compatibility:** Must work with standard MERIDIAN_Brain file structures.

## 7. Current Phase
**Phase 1: Foundation**
- Establishing core storage infrastructure (`/memory`, `.index`).
- Implementing basic file-based CRUD operations.
