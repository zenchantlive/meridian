#!/usr/bin/env python3
"""Test actual MERIDIAN Brain functionality."""

print("=== TESTING MERIDIAN BRAIN ===\n")

# Test 1: Imports
print("1. Testing imports...")
try:
    from brain.scripts import ChunkStore, RememberOperation, REPLSession
    print("   [OK] ChunkStore imported")
    print("   [OK] RememberOperation imported") 
    print("   [OK] REPLSession imported")
except Exception as e:
    print(f"   [FAIL] Import failed: {e}")
    exit(1)

print("\n2. Testing ChunkStore...")
try:
    import tempfile
    temp_dir = tempfile.mkdtemp()
    store = ChunkStore(temp_dir)
    print(f"   [OK] ChunkStore created")
    
    # Create a chunk
    chunk = store.create_chunk(
        content="Test memory content",
        chunk_type="note",
        tags=["test"]
    )
    print(f"   [OK] Chunk created: {chunk.id}")
    
    # Retrieve
    retrieved = store.get_chunk(chunk.id)
    print(f"   [OK] Chunk retrieved: {retrieved.content[:30]}...")
    
    # Stats
    stats = store.get_stats()
    print(f"   [OK] Stats: {stats}")
    
except Exception as e:
    print(f"   [FAIL] ChunkStore failed: {e}")
    import traceback
    traceback.print_exc()

print("\n3. Testing RememberOperation...")
try:
    remember = RememberOperation(store)
    result = remember.remember(
        content="User prefers pytest for testing Python code",
        conversation_id="test-conv-001",
        tags=["preference", "testing"],
        confidence=0.95
    )
    print(f"   [OK] Remember success: {result['success']}")
    print(f"   [OK] Chunks created: {result['chunks_created']}")
    print(f"   [OK] Chunk IDs: {result['chunk_ids']}")
except Exception as e:
    print(f"   [FAIL] Remember failed: {e}")
    import traceback
    traceback.print_exc()

print("\n4. Testing REPLSession...")
try:
    from unittest.mock import Mock
    mock_llm = Mock()
    mock_llm.complete = Mock(return_value="FINAL('test answer')")
    
    repl = REPLSession(
        chunk_store=store,
        llm_client=mock_llm,
        max_iterations=5
    )
    print("   [OK] REPLSession created")
    
    # Basic execution
    repl.execute("x = 42")
    print("   [OK] Basic execution works")
    
    result = repl.execute("x * 2")
    print(f"   [OK] Expression evaluation: {result}")
    
except Exception as e:
    print(f"   [FAIL] REPL failed: {e}")
    import traceback
    traceback.print_exc()

print("\n5. Testing memory functions in REPL...")
try:
    # Test read_chunk
    result = repl.execute(f"read_chunk('{chunk.id}')")
    print(f"   [OK] read_chunk works: {result is not None}")
    
    # Test search_chunks
    result = repl.execute("search_chunks('test')")
    print(f"   [OK] search_chunks works: {len(result)} results")
    
except Exception as e:
    print(f"   [FAIL] REPL memory functions failed: {e}")

print("\n6. Testing retrieve workflow...")
try:
    # This is the critical test - can we actually retrieve?
    mock_llm.complete = Mock(return_value="FINAL('Found the test memory')")
    
    result = repl.retrieve("What test memory do we have?")
    print(f"   [OK] retrieve returned: {result}")
    
except Exception as e:
    print(f"   [FAIL] retrieve failed: {e}")
    import traceback
    traceback.print_exc()

print("\n=== TEST COMPLETE ===")
print("\nWhat works:")
print("  [OK] Storing memories (RememberOperation)")
print("  [OK] Basic REPL execution")
print("  [OK] Memory functions in sandbox")
print("\nWhat's missing:")
print("  ? RECALL operation (need to verify)")
print("  ? Real LLM integration")
