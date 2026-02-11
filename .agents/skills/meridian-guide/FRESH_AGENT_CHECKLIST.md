# Fresh Agent Setup Checklist

This checklist helps verify that a new agent can set up MERIDIAN Brain Enhanced from scratch using only the skill documentation.

## Pre-Flight Checks

Before claiming MERIDIAN is "set up", verify:

### 1. Repository Access
- [ ] Can clone/access the repository
- [ ] Repository contains:
  - [ ] `brain/scripts/` directory with Python files
  - [ ] `brain/personalities/*.md` files
  - [ ] `brain/sliders/*.md` files
  - [ ] `brain/gauges/LIVEHUD.md`
  - [ ] `.agents/skills/meridian-guide/SKILL.md`
  - [ ] `pyproject.toml` (for pip install)

### 2. Installation
```bash
cd meridian
pip install -e .
```
- [ ] Installation completes without errors
- [ ] Can import: `python -c "from brain.scripts import ChunkStore"`

### 3. Run Fresh Setup Test
```bash
python test_fresh_setup.py
```
- [ ] All 5 tests pass:
  - [ ] Imports work
  - [ ] Memory operations (REMEMBER/RECALL)
  - [ ] Original MERIDIAN format (personalities/sliders)
  - [ ] Auto-memory system
  - [ ] Query expansion

### 4. Skill Documentation Review
Read `.agents/skills/meridian-guide/SKILL.md`:
- [ ] Understands what MERIDIAN Brain Enhanced does
- [ ] Can follow the "30-Second Test" example
- [ ] Understands LIVEHUD format
- [ ] Knows how to use REMEMBER/RECALL/REASON
- [ ] Knows how to use AutoMemory
- [ ] Understands query expansion limitations

### 5. Live Test
Create a test file and run it:

```python
#!/usr/bin/env python3
"""Verify MERIDIAN works for your use case."""

from brain.scripts import (
    load_meridian_config, ChunkStore,
    RememberOperation, RecallOperation
)

# Test 1: Personality system
print("Test 1: Personality system...")
config = load_meridian_config()  # Uses default 'brain/'
config.set_mode("TECHNICAL")
hud = config.generate_livehud()
assert "TECHNICAL" in hud
assert "◈ MERIDIAN LIVEHUD ◈" in hud
print("  [OK] Personality system works")

# Test 2: Memory system
print("Test 2: Memory system...")
store = ChunkStore("brain/memory/test")
remember = RememberOperation(store)
result = remember.remember(
    content="User prefers dark mode",
    conversation_id="test",
    tags=["preference", "ui"],
    confidence=0.9
)
assert result['success']
print(f"  [OK] Stored memory ({result['chunks_created']} chunks)")

# Test 3: Recall with query expansion
print("Test 3: Query expansion...")
recall = RecallOperation(store, llm_client=None)
result = recall.recall("what does user like?")
assert len(result.source_chunks) > 0
print(f"  [OK] Found {len(result.source_chunks)} results")

print("\n[OK] All live tests passed!")
```

- [ ] Test file runs without errors
- [ ] All assertions pass

### 6. Project-Specific Adjustments
Does your project need any special configuration?

- [ ] **Different config path?** 
  - Default: `brain`
  - If your MERIDIAN files are elsewhere, update paths

- [ ] **Custom synonyms for query expansion?**
  - Edit `brain/scripts/recall_operation.py` QUERY_SYNONYMS
  - Add domain-specific terms

- [ ] **Memory location?**
  - Default: `brain/memory/`
  - Can be customized per-project

- [ ] **Need real LLM integration?**
  - Currently uses mock LLM for REPL
  - Add API keys for OpenAI/Anthropic in `brain/scripts/llm_client.py`

## Common Issues & Solutions

### "ImportError: No module named 'brain.scripts'"
**Solution:**
```bash
pip install -e .
# OR set PYTHONPATH:
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### "No personalities found" or "No sliders found"
**Solution:**
Check that config files exist:
```python
from pathlib import Path

# Should exist:
assert Path("brain/personalities/BASE.md").exists()
assert Path("brain/sliders/CREATIVITY.md").exists()
assert Path("brain/gauges/LIVEHUD.md").exists()

# Then load with default path:
config = load_meridian_config()  # Uses 'brain/' by default
```

### "Query returns no results"
**Solution:**
- Use broader search terms
- Check what vocabulary is in memories
- Store with rich tags: `tags=["task", "tracking", "beads", "workflow"]`
- Add custom synonyms to `QUERY_SYNONYMS`

### "UnicodeEncodeError with LIVEHUD"
**Solution:**
Set UTF-8 encoding:
```bash
export PYTHONIOENCODING=utf-8  # Linux/Mac
chcp 65001                     # Windows
```

## Success Criteria

MERIDIAN Brain Enhanced is **ready** when:

1. ✓ `pip install -e .` succeeds
2. ✓ `python test_fresh_setup.py` passes all tests
3. ✓ Can import all modules from `brain.scripts`
4. ✓ Can load personalities and generate LIVEHUD
5. ✓ Can store and retrieve memories
6. ✓ Query expansion finds related terms
7. ✓ AutoMemory records without explicit commands
8. ✓ Skill documentation makes sense to you

## Red Flags (Don't Proceed Without Fixing)

- ✗ Import errors after `pip install -e .`
- ✗ Test failures in `test_fresh_setup.py`
- ✗ Can't find personalities/sliders
- ✗ Memories don't persist between runs
- ✗ Query expansion never finds anything
- ✗ LIVEHUD generation crashes

## Next Steps After Setup

1. **Read the full skill:** `.agents/skills/meridian-guide/SKILL.md`
2. **Try the demo:** `python demo_complete.py`
3. **Read HOW_TO_USE.md** for usage patterns
4. **Start building:** Use AutoMemory in your workflow

## For Skill Authors

If you're improving this skill, ensure:
- [ ] Fresh agent can follow setup without asking questions
- [ ] All code examples in skill run without modification
- [ ] Troubleshooting section covers common failures
- [ ] Test scripts verify all major features
- [ ] No hardcoded paths that won't work elsewhere
