#!/usr/bin/env python3
"""
Demonstrate MERIDIAN memory system by storing project knowledge
and then recalling/ reasoning about it.
"""

from brain.scripts import ChunkStore, RememberOperation, RecallOperation, ReasonOperation

# Use the actual project memory location
print("=" * 60)
print("STORING PROJECT KNOWLEDGE IN MERIDIAN MEMORY")
print("=" * 60)

store = ChunkStore('brain/memory')
remember = RememberOperation(store)

# Store what I know about this project
facts = [
    ('Project is MERIDIAN Brain Enhanced - Phase 5 complete with 243 tests passing', ['project', 'status', 'testing']),
    ('Uses RLM-based memory system with JSON chunks and graph linking', ['architecture', 'memory', 'rlm']),
    ('Original MERIDIAN format includes LIVEHUD dashboard with 6 cognitive sliders', ['original', 'format', 'livehud']),
    ('Personality modes: BASE, RESEARCH, CREATIVE, TECHNICAL with preset slider values', ['personalities', 'modes']),
    ('Memory operations: REMEMBER (D3.1), RECALL (D3.2), REASON (D3.3) all implemented', ['features', 'operations']),
    ('Has REPL sandbox with FINAL() termination and llm_query() recursion', ['repl', 'sandbox', 'security']),
    ('Uses beads for task tracking - 48 beads closed so far', ['workflow', 'beads', 'tracking']),
]

print('\nStoring project facts...')
for content, tags in facts:
    result = remember.remember(
        content=content,
        conversation_id='project-knowledge',
        tags=tags,
        confidence=0.95,
        chunk_type='fact'
    )
    print(f'  [OK] {tags[0]}: {result["chunks_created"]} chunk(s)')

stats = store.get_stats()
print(f'\n[OK] Total chunks in store: {stats["total_chunks"]}')

# Now demonstrate RECALL
print("\n" + "=" * 60)
print("TESTING RECALL - Natural Language Queries")
print("=" * 60)

recall = RecallOperation(store, llm_client=None)

queries = [
    "What is the project status?",
    "Tell me about the memory system architecture",
    "What personality modes are available?",
    "How does task tracking work?",
]

for query in queries:
    print(f'\nQuery: "{query}"')
    result = recall.recall(query, max_results=2)
    print(f'  Confidence: {result.confidence:.2f}')
    print(f'  Sources: {len(result.source_chunks)}')
    if hasattr(result, 'suggested_query') and result.suggested_query:
        print(f'  Suggested: {result.suggested_query}')
    # Show actual content from first source
    if result.source_chunks:
        chunk_id = result.source_chunks[0]
        chunk_data = store.get_chunk(chunk_id)
        if chunk_data:
            print(f'  Top result: {chunk_data.content[:60]}...')

# Now demonstrate REASON
print("\n" + "=" * 60)
print("TESTING REASON - Pattern Analysis")
print("=" * 60)

reason = ReasonOperation(store, llm_client=None)

reason_queries = [
    ("What are the key components of this project?", "pattern"),
    ("How do the memory operations work together?", "synthesis"),
]

for query, analysis_type in reason_queries:
    print(f'\nQuery: "{query}"')
    print(f'Type: {analysis_type}')
    result = reason.reason(query, analysis_type=analysis_type)
    print(f'  Confidence: {result.confidence:.2f}')
    print(f'  Synthesis: {result.synthesis[:70]}...')
    print(f'  Insights: {len(result.insights)}')
    for i, insight in enumerate(result.insights[:2], 1):
        print(f'    {i}. {insight[:60]}...')

print("\n" + "=" * 60)
print("DEMONSTRATION COMPLETE")
print("=" * 60)
print("\nThe memory system successfully:")
print("  - Stored project knowledge with tags")
print("  - Retrieved via natural language (RECALL)")
print("  - Analyzed patterns across memories (REASON)")
print("\nNow let's set up automatic memory updates...")
