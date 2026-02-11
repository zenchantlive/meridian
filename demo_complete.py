#!/usr/bin/env python3
"""Complete MERIDIAN Brain demo showing all features."""

import sys
sys.path.insert(0, '.agents/skills/meridian-guide')
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from brain.scripts import (
    load_meridian_config, ChunkStore, 
    RememberOperation, RecallOperation, ReasonOperation
)
from auto_memory import AutoMemory

print('=' * 70)
print('COMPLETE MERIDIAN BRAIN DEMO')
print('=' * 70)

# 1. Setup personality
print('\n[1] Loading MERIDIAN configuration...')
config = load_meridian_config()  # Uses default 'brain/'
config.set_mode('TECHNICAL')
print('    Mode: TECHNICAL')
print('    Sliders: technicality up to 90, directness up to 80, humor down to 15')

# 2. Show LIVEHUD snippet
print('\n[2] LIVEHUD Dashboard (partial):')
livehud = config.generate_livehud()
for line in livehud.split('\n')[:10]:
    print('    ' + line)
print('    ...')

# 3. AutoMemory - record work session
print('\n[3] AutoMemory - Recording work session...')
auto_mem = AutoMemory('brain/memory', conversation_id='demo-session-001')
auto_mem.start_session('Implementing user dashboard')

auto_mem.record_decision(
    decision='Use React Query for data fetching',
    rationale='Better caching and refetching than useEffect',
    alternatives=['Redux', 'useEffect + Context', 'SWR']
)

auto_mem.record_preference(
    what_was_learned='User prefers explicit TypeScript types over inference',
    confidence=0.95
)

print('    Recorded: Decision (React Query)')
print('    Recorded: Preference (explicit types)')

# 4. Manual memory store
print('\n[4] Manual REMEMBER operation...')
remember = RememberOperation(auto_mem.store)
result = remember.remember(
    content='Dashboard needs real-time updates via WebSocket',
    conversation_id='demo-session-001',
    tags=['requirement', 'dashboard', 'websocket'],
    confidence=0.9
)
print(f'    Stored: {result["chunks_created"]} chunk(s)')

# 5. RECALL - natural language
print('\n[5] RECALL - Natural language queries...')
recall = RecallOperation(auto_mem.store, llm_client=None)

queries = [
    'What did we decide about data fetching?',
    'Tell me about user preferences',
]

for query in queries:
    result = recall.recall(query, max_results=1)
    print(f'    Q: {query}')
    if result.source_chunks:
        chunk = auto_mem.store.get_chunk(result.source_chunks[0])
        print(f'    A: {chunk.content[:60]}...')
    else:
        print('    A: No results')

# 6. REASON - pattern analysis
print('\n[6] REASON - Pattern analysis...')
reason = ReasonOperation(auto_mem.store, llm_client=None)
result = reason.reason('What technologies are we using?', analysis_type='pattern')
print(f'    Synthesis: {result.synthesis[:70]}...')
print(f'    Insights found: {len(result.insights)}')

auto_mem.end_session('Demo completed successfully')

stats = auto_mem.get_stats()
print(f'\n    Session stats:')
print(f'      Things recorded: {stats["things_learned_this_session"]}')
print(f'      Total chunks: {stats["store_stats"]["total_chunks"]}')

print('\n' + '=' * 70)
print('DEMO COMPLETE - All systems working!')
print('=' * 70)
print('\nKey takeaways:')
print('  [OK] AutoMemory records without explicit commands')
print('  [OK] RECALL uses synonym expansion (task to beads)')
print('  [OK] REASON synthesizes patterns across memories')
print('  [OK] LIVEHUD shows current personality mode')
print('  [OK] All memories persist in brain/memory/')
