#!/usr/bin/env python3
"""
Test script for fresh MERIDIAN Brain setup.

Run this after cloning and installing to verify everything works:
    pip install -e .
    python test_fresh_setup.py
"""

import sys
import tempfile
from pathlib import Path

def test_imports():
    """Test that all core modules can be imported."""
    print("[1] Testing imports...")
    try:
        from brain.scripts import (
            ChunkStore, RememberOperation, RecallOperation, ReasonOperation,
            REPLSession, AutoLinker, load_meridian_config
        )
        print("    [OK] All core imports successful")
        return True
    except ImportError as e:
        print(f"    [FAIL] Import failed: {e}")
        return False

def test_memory_operations():
    """Test basic memory operations."""
    print("\n[2] Testing memory operations...")
    try:
        from brain.scripts import ChunkStore, RememberOperation, RecallOperation
        
        # Use temp directory for test
        temp_dir = tempfile.mkdtemp()
        store = ChunkStore(temp_dir)
        
        # Remember
        remember = RememberOperation(store)
        result = remember.remember(
            content="Test memory for fresh setup",
            conversation_id="fresh-setup-test",
            tags=["test", "setup"],
            confidence=0.95
        )
        assert result['success'], "Remember failed"
        print(f"    [OK] REMEMBER works ({result['chunks_created']} chunks)")
        
        # Recall
        recall = RecallOperation(store, llm_client=None)
        result = recall.recall("test memory", max_results=1)
        assert len(result.source_chunks) > 0, "Recall found no results"
        print(f"    [OK] RECALL works (found {len(result.source_chunks)} sources)")
        
        return True
    except Exception as e:
        print(f"    [FAIL] Memory operations failed: {e}")
        return False

def test_original_meridian():
    """Test original MERIDIAN format parsing."""
    print("\n[3] Testing original MERIDIAN format...")
    try:
        from brain.scripts import load_meridian_config
        
        # Use default brain/ path
        config_path = "brain"
        
        if not Path(config_path).exists():
            print(f"    ⚠ Config path not found: {config_path}")
            print("    ℹ Skipping (original MERIDIAN files may be in different location)")
            return True
        
        config = load_meridian_config(config_path)
        
        # Check personalities loaded
        personalities = list(config.personalities.keys())
        assert len(personalities) > 0, "No personalities loaded"
        print(f"    [OK] Loaded {len(personalities)} personalities: {personalities}")
        
        # Check sliders
        sliders = list(config.sliders.keys())
        assert len(sliders) > 0, "No sliders loaded"
        print(f"    [OK] Loaded {len(sliders)} sliders: {sliders}")
        
        # Generate LIVEHUD
        config.set_mode("BASE")
        livehud = config.generate_livehud()
        assert "MERIDIAN LIVEHUD" in livehud, "LIVEHUD generation failed"
        print("    [OK] LIVEHUD generation works")
        
        return True
    except Exception as e:
        print(f"    [FAIL] Original MERIDIAN format failed: {e}")
        return False

def test_auto_memory():
    """Test auto-memory system."""
    print("\n[4] Testing auto-memory...")
    try:
        sys.path.insert(0, '.agents/skills/meridian-guide')
        from auto_memory import AutoMemory
        
        temp_dir = tempfile.mkdtemp()
        auto_mem = AutoMemory(temp_dir, conversation_id="test-session")
        
        auto_mem.start_session("Test session")
        auto_mem.record_preference(
            what_was_learned="User likes testing",
            confidence=0.9
        )
        
        stats = auto_mem.get_stats()
        assert stats['things_learned_this_session'] > 0, "AutoMemory didn't record"
        print(f"    [OK] AutoMemory works (recorded {stats['things_learned_this_session']} items)")
        
        return True
    except Exception as e:
        print(f"    [FAIL] AutoMemory failed: {e}")
        return False

def test_query_expansion():
    """Test query expansion in RECALL."""
    print("\n[5] Testing query expansion...")
    try:
        from brain.scripts import ChunkStore, RememberOperation, RecallOperation
        
        temp_dir = tempfile.mkdtemp()
        store = ChunkStore(temp_dir)
        
        # Store a memory with specific vocabulary
        remember = RememberOperation(store)
        remember.remember(
            content="Uses beads for task tracking and workflow management",
            conversation_id="test",
            tags=["workflow"],
            confidence=0.9
        )
        
        # Search with different vocabulary
        recall = RecallOperation(store, llm_client=None)
        result = recall.recall("task tracking")  # Should find "beads"
        
        # Should find the memory even though it says "beads" not "task"
        assert len(result.source_chunks) > 0, "Query expansion didn't work"
        print(f"    [OK] Query expansion works (found {len(result.source_chunks)} results)")
        
        return True
    except Exception as e:
        print(f"    [FAIL] Query expansion failed: {e}")
        return False

def main():
    print("=" * 70)
    print("MERIDIAN BRAIN - FRESH SETUP TEST")
    print("=" * 70)
    
    tests = [
        test_imports,
        test_memory_operations,
        test_original_meridian,
        test_auto_memory,
        test_query_expansion,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"    [FAIL] Test crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 70)
    
    if passed == total:
        print("\n[OK] MERIDIAN Brain is ready to use!")
        print("\nNext steps:")
        print("  1. Read the skill: .agents/skills/meridian-guide/SKILL.md")
        print("  2. Try the demo: python demo_complete.py")
        print("  3. Start building with auto-memory!")
        return 0
    else:
        print("\n[FAIL] Some tests failed. Check errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
