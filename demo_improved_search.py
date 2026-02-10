#!/usr/bin/env python3
"""Test improved search with query expansion."""

from brain.scripts import ChunkStore, RecallOperation

store = ChunkStore('brain/memory')
recall = RecallOperation(store, llm_client=None)

print("=" * 60)
print("TESTING IMPROVED SEARCH WITH QUERY EXPANSION")
print("=" * 60)

test_queries = [
    "How does task tracking work?",      # Should find "beads"
    "What is the project status?",        # Should find status info
    "Tell me about the memory system",    # Should find architecture
    "What components are there?",         # Should find features list
]

for query in test_queries:
    print(f'\nQuery: "{query}"')
    result = recall.recall(query, max_results=2)
    print(f'  Confidence: {result.confidence:.2f}')
    print(f'  Sources: {len(result.source_chunks)}')
    if result.source_chunks:
        chunk = store.get_chunk(result.source_chunks[0])
        if chunk:
            print(f'  Found: {chunk.content[:70]}...')
    else:
        print('  No results found')

print("\n" + "=" * 60)
print("Test complete!")
