---
name: meridian-guide
description: >
  Complete guide for setting up and using MERIDIAN Brain Enhanced - an intelligent agent 
  operating system with RLM-based memory, personality modes, and configuration management.
  Use when: (1) Setting up MERIDIAN Brain for the first time, (2) Configuring memory systems,
  (3) Managing personality modes and sliders, (4) Understanding MERIDIAN architecture,
  (5) Troubleshooting MERIDIAN issues, (6) Integrating MERIDIAN into agent workflows.
  This skill covers both the enhanced memory system (RLM-based) and the original 
  MERIDIAN Brain framework (personalities, sliders, gauges).
---

# MERIDIAN Brain Enhanced - Complete Guide

## Quick Start

MERIDIAN Brain Enhanced combines a **recursive language model (RLM) memory system** with the original **MERIDIAN Brain configuration framework**. It solves "session amnesia" by giving agents persistent, queryable memory.

### Original MERIDIAN Format

The original framework uses **Markdown-based configuration** with:

1. **LIVEHUD.md** - Box-style gauge dashboard (MANDATORY for every response)
2. **Personalities/** - Behavioral mode definitions (BASE, RESEARCH, CREATIVE, TECHNICAL)
3. **Sliders/** - 6 cognitive dimension controls (0-100% range each)

**Example LIVEHUD output:**
```
╔══════════════════════════════════════════════════════════════════════════════╗
║  ◈ MERIDIAN LIVEHUD ◈                                                        ║
║  Session: Active  │  Mode: TECHNICAL                                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ▸ COGNITIVE SLIDERS                              Current   Default          ║
║  ├─ 🔊 Verbosity   [████░░░░░░░░░░░░]        28%       28%                   ║
║  ├─ 😂 Humor       [██░░░░░░░░░░░░░░]        15%       45%                   ║
║  ├─ 🎨 Creativity  [████████░░░░░░░░]        55%       55%                   ║
║  ├─ ⚖️ Morality    [█████████░░░░░░░]        60%       60%                   ║
║  ├─ 🎯 Directness  [████████████░░░░]        80%       65%                   ║
║  └─ 🔬 Technicality [██████████████░░]        90%       50%                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ▸ MEMORY PROTOCOL                                                           ║
║  ├─ 🧠 Past:    [Stored user preferences]                                    ║
║  ├─ 👁️ Present: [Analyzing patterns]                                         ║
║  └─ 🔮 Future:  [Generate insights]                                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ▸ SYSTEM STATE                                                              ║
║  ├─ 💾 Context: [Stable] │ 🔧 Tools: [Standby]                               ║
║  ├─ 📂 Memory:  [3 files loaded] │ [0 pending write]                         ║
║  └─ ⚡ Vibe:    [Analytical]                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### What You Get

- **RLM Memory System**: JSON-based chunks with auto-linking, semantic search, and confidence scoring
- **Personality Modes**: Pre-configured behavioral profiles (BASE, RESEARCH_ANALYST, CREATIVE_DIRECTOR, TECHNICAL_COPILOT, CONCISE)
- **Configuration Sliders**: Fine-tune 8 behavioral dimensions (creativity, technicality, humor, etc.)
- **Live Gauges**: Real-time system monitoring and status displays

### Installation

```bash
# Clone the repository
git clone https://github.com/zenchantlive/meridian.git
cd meridian

# Set up Python environment (3.11+)
pip install -e .

# Verify installation
python test_fresh_setup.py
```

**For Fresh Agents:** See `FRESH_AGENT_CHECKLIST.md` for complete setup verification. This ensures you can:
- Import all modules
- Load personalities/sliders
- Store and recall memories
- Generate LIVEHUD dashboard

**Quick Verification:**
```python
from brain.scripts import ChunkStore, RememberOperation
store = ChunkStore("brain/memory/test")
remember = RememberOperation(store)
result = remember.remember(content="Test", conversation_id="verify")
print(f"Setup OK: {result['success']}")
```

### 30-Second Test

```python
from brain.scripts import ChunkStore, RememberOperation

# Initialize memory store
store = ChunkStore("brain/memory/test")
remember = RememberOperation(store)

# Create a memory
result = remember.remember(
    content="User prefers dark mode for coding",
    conversation_id="test-001",
    tags=["preference", "ui"],
    confidence=0.95
)

print(f"✓ Memory created: {result['chunk_ids']}")
```

### Auto-Memory (No Explicit Commands Needed)

The auto-memory system records things as you work, without "remember this" commands:

```python
from auto_memory import AutoMemory

auto_mem = AutoMemory('brain/memory')
auto_mem.start_session("Working on feature X")

# These happen automatically as you work:
auto_mem.record_task_completion(
    task_id="bead-123",
    what_was_done="Implemented user authentication",
    outcome="success",
    files_modified=["auth.py", "models.py"]
)

auto_mem.record_preference(
    what_was_learned="User prefers explicit error handling",
    context="Saw user add try/except to all examples"
)

auto_mem.record_decision(
    decision="Use PostgreSQL over MySQL",
    rationale="Better JSON support for our use case",
    alternatives=["MySQL with JSON columns", "MongoDB"]
)

auto_mem.end_session("Authentication feature complete")
```

### Using Original MERIDIAN Format

```python
from brain.scripts import load_meridian_config, activate_mode

# Load configuration from original repo format
config = load_meridian_config()  # Uses default 'brain/'

# Switch personality mode (adjusts sliders automatically)
config.set_mode("TECHNICAL")  # BASE, RESEARCH, CREATIVE, TECHNICAL, CONCISE

# Generate LIVEHUD dashboard
livehud = config.generate_livehud()
print(livehud)  # Output the gauge dashboard

# Manual slider adjustment
config.set_slider("creativity", 80)
config.set_slider("technicality", 90)

# Update memory protocol
config.memory.past = "Retrieved user preferences"
config.memory.present = "Processing request"
config.memory.future = "Generate response"

# Update system state
config.system.memory_files = 5
config.system.vibe = "Analytical"

# Generate updated LIVEHUD
updated_livehud = config.generate_livehud()
```

---

## System Architecture

MERIDIAN Brain has two integrated subsystems:

### 1. Enhanced Memory System (New)

**Core Components:**

| Component | Purpose | Key Files |
|-----------|---------|-----------|
| `ChunkStore` | JSON storage with CRUD operations | `brain/scripts/memory_store.py` |
| `ChunkingEngine` | Semantic text chunking (100-800 tokens) | `brain/scripts/chunking_engine.py` |
| `AutoLinker` | Automatic graph linking between chunks | `brain/scripts/auto_linker.py` |
| `REPLSession` | Secure sandbox for recursive LLM execution | `brain/scripts/repl_environment.py` |

**Data Flow:**
```
User Input → ChunkingEngine → ChunkStore → AutoLinker
                                          ↓
Query → REPLSession → LLM → Memory Functions → Results
```

**Storage Schema:**
- Chunks stored as JSON in `brain/memory/` organized by date
- Each chunk has: id, content, tokens, type, metadata, links, tags
- Links support: context_of, follows, related_to, supports, contradicts

### 2. Original MERIDIAN Framework

**Core Components:**

| Component | Purpose | Location |
|-----------|---------|----------|
| Personalities | Behavioral mode definitions | `brain/personalities/*.md` |
| Sliders | Configuration dimension controls | `brain/sliders/*.md` |
| Gauges | Live system monitoring | `brain/gauges/LIVEHUD.md` |
| Memory Protocol | Legacy original memory system | `brain/MEMORY_PROTOCOL_LEGACY.md` |

**Key Insight:** The original framework uses **Markdown-based configuration** while the enhanced system uses **JSON-based storage**. They complement each other - personalities/sliders configure *behavior*, while the new memory system provides *persistent storage*.

---

## LIVEHUD Format

### Required Output Format

**Every response MUST begin with the LIVEHUD dashboard.** This is the canonical format:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  ◈ MERIDIAN LIVEHUD ◈                                                        ║
║  Session: [Active/New]  │  Mode: [Active Personality Name]                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ▸ COGNITIVE SLIDERS                              Current   Default          ║
║  │                                                                           ║
║  ├─ 🔊 Verbosity      [████████░░░░░░░░░░░░]       40%       28%             ║
║  ├─ 😂 Humor          [██████░░░░░░░░░░░░░░]       30%       45%             ║
║  ├─ 🎨 Creativity     [████████████░░░░░░░░]       60%       55%             ║
║  ├─ ⚖️ Morality       [████████████████░░░░]       80%       60%             ║
║  ├─ 🎯 Directness     [██████████████░░░░░░]       70%       65%             ║
║  └─ 🔬 Technicality   [██████████░░░░░░░░░░]       50%       50%             ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ▸ MEMORY PROTOCOL                                                           ║
║  │                                                                           ║
║  ├─ 🧠 Past:    [3-9 words: Last retrieved context/fact]                     ║
║  ├─ 👁️ Present: [3-9 words: Current active task/focus]                       ║
║  └─ 🔮 Future:  [3-9 words: Next scheduled action/goal]                      ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ▸ SYSTEM STATE                                                              ║
║  │                                                                           ║
║  ├─ 💾 Context: [Stable/XX%]  │  🔧 Tools: [Standby/Active/Executing]        ║
║  ├─ 📂 Memory:  [X files loaded] │ [X pending write]                         ║
║  └─ ⚡ Vibe:    [Direct/Elevated/Focused/Creative/Analytical]                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Generating LIVEHUD

```python
from brain.scripts import load_meridian_config

config = load_meridian_config()  # Uses default 'brain/'

# Set mode (adjusts sliders)
config.set_mode("RESEARCH")

# Update memory protocol
config.memory.past = "Retrieved Python preferences"
config.memory.present = "Analyzing code structure"
config.memory.future = "Suggest refactor"

# Update system state
config.system.context = "Stable"
config.system.tools = "Active"
config.system.memory_files = 12
config.system.vibe = "Analytical"

# Generate LIVEHUD
livehud = config.generate_livehud()
print(livehud)
```

### LIVEHUD Sections

**Cognitive Sliders** - 6 behavioral dimensions with visual bars
**Memory Protocol** - Past/Present/Future context (3-9 words each)
**System State** - Context utilization, tool status, memory stats, vibe

### Box Drawing Characters

The LIVEHUD uses Unicode box drawing:
- `╔ ═ ╗` - Top border
- `╠ ═ ╣` - Section dividers
- `╚ ═ ╝` - Bottom border
- `║` - Side borders
- `├ └` - Tree connectors

---

## Memory System Deep Dive

### Core Operations

**REMEMBER** - Store information:
```python
from brain.scripts import RememberOperation

remember = RememberOperation(chunk_store)
result = remember.remember(
    content="Information to store",
    conversation_id="conv-123",
    tags=["tag1", "tag2"],
    confidence=0.85,  # 0.0-1.0
    chunk_type="preference"  # preference, fact, pattern, note
)
# Returns: {success, chunk_ids, total_tokens, chunks_created}
```

**RECALL** - Retrieve information:
```python
from brain.scripts import RecallOperation

recall = RecallOperation(store, llm_client=None)
result = recall.recall(
    query="What does the user prefer for testing?",
    max_results=5
)

print(f"Answer: {result.answer}")
print(f"Confidence: {result.confidence}")
print(f"Sources: {result.source_chunks}")
```

**Query Expansion**: RECALL automatically expands queries with synonyms:
- "task tracking" → finds memories about "beads", "workflow", "issues"
- "remember" → finds memories about "store", "save", "record"
- "project status" → finds memories about "progress", "complete", "done"

**REASON** - Analyze and synthesize:
```python
from brain.scripts import ReasonOperation

reason = ReasonOperation(store, llm_client=None)
result = reason.reason(
    query="Analyze user's testing preferences",
    analysis_type="pattern"  # or "synthesis", "gap", "contradiction"
)

print(f"Synthesis: {result.synthesis}")
print(f"Insights: {result.insights}")
print(f"Confidence: {result.confidence}")
```

### Storage Architecture

**Directory Structure:**
```
brain/memory/
├── chunks/              # Chunk files by month
│   └── YYYY-MM/
│       └── chunk-*.json
├── index/               # Lookup indexes
│   ├── metadata_index.json
│   ├── tag_index.json
│   └── link_graph_index.json
└── archive/             # Soft-deleted chunks
    └── chunk-*.json
```

**Chunk Schema:**
```json
{
  "id": "chunk-2026-02-10-a1b2c3d4",
  "content": "User decided to use RLM architecture instead of RAG...",
  "tokens": 145,
  "type": "decision",
  "metadata": {
    "created": "2026-02-10T21:37:00Z",
    "conversation_id": "conv-abc123",
    "source": "interaction",
    "confidence": 0.95,
    "access_count": 3,
    "last_accessed": "2026-02-10T22:15:00Z"
  },
  "links": {
    "context_of": ["conv-abc123"],
    "follows": ["chunk-2026-02-10-x9y8z7w6"],
    "related_to": ["chunk-2026-02-09-p4q5r6s7"],
    "supports": [],
    "contradicts": []
  },
  "tags": ["architecture", "rlm", "decision"]
}
```

### Auto-Linking

The system automatically creates links when chunks are created:

- **context_of**: Same conversation
- **follows**: Temporal proximity (within 5 minutes)
- **related_to**: Shared tags

Manual links can also be added:
```python
from brain.scripts import add_manual_link

add_manual_link(
    chunk_store=store,
    source_id="chunk-1",
    target_id="chunk-2",
    link_type="supports",
    strength=0.9,
    reasoning="These preferences are consistent"
)
```

---

## Personality Modes

### Available Modes

Read `brain/personalities/*.md` for full specifications.

| Mode | File | Slider Adjustments | Best For |
|------|------|-------------------|----------|
| **BASE** | `BASE.md` | All defaults | General conversation, unclear tasks |
| **RESEARCH** | `RESEARCH_ANALYST.md` | 🔬↑85%, 🎯↑75%, 😂↓25% | Research, fact-finding, documentation |
| **CREATIVE** | `CREATIVE_DIRECTOR.md` | 🎨↑90%, 😂↑70%, 🔊↑60% | Brainstorming, content creation, design |
| **TECHNICAL** | `TECHNICAL_COPILOT.md` | 🔬↑90%, 🎯↑80%, 😂↓15% | Coding, debugging, technical work |
| **CONCISE** | - | 🔊↓15%, 🎯↑85% | Quick answers, status updates |

### BASE Personality (Core Identity)

**Core Traits (always active):**
- 🎯 **Direct** - Say what needs to be said, lead with answers
- 🔬 **Receipts-Backed** - Ground claims in evidence, cite sources
- 🔧 **Practical** - Focus on actionable insights, work-ready outputs
- 🎨 **Creative** - Use metaphors, offer unconventional angles
- 🤝 **Collaborative** - Treat user as capable partner

**Anti-Patterns (Never Do):**
- ❌ "Great question!" - Empty sycophancy
- ❌ "I'd be happy to help!" - Robotic filler
- ❌ "As an AI language model..." - Breaks presence
- ❌ Excessive hedging - Wastes user's time

### Switching Modes

**Via code:**
```python
from brain.scripts import load_meridian_config

config = load_meridian_config()  # Uses default 'brain/'
config.set_mode("TECHNICAL")  # Apply preset adjustments
livehud = config.generate_livehud()
```

**Via conversation:**
```markdown
"Switch to TECHNICAL mode"
"Activate RESEARCH personality"
"Go CREATIVE for this brainstorm"
```

Mode switching automatically adjusts sliders to preset values.

---

## Configuration Sliders

### The 6 Cognitive Sliders

Each slider controls a behavioral dimension with 0-100% range:

| Slider | Emoji | Default | Description |
|--------|-------|---------|-------------|
| **Verbosity** | 🔊 | 28% | Output length. Low = concise. High = expansive. |
| **Humor** | 😂 | 45% | Comedic injection. 0% = serious. 100% = actively funny. |
| **Creativity** | 🎨 | 55% | Divergent thinking. Low = conventional. High = experimental. |
| **Morality** | ⚖️ | 60% | Ethical framing depth. Higher = more explicit ethics. |
| **Directness** | 🎯 | 65% | Bluntness. Low = diplomatic. High = razor-sharp. |
| **Technicality** | 🔬 | 50% | Technical depth. Low = accessible. High = PhD-level. |

### Calibration Levels

Each slider has defined calibration levels. Example from CREATIVITY.md:

| Range | Mode | Behavior |
|-------|------|----------|
| **0-20%** | Conservative | Stick to known patterns. Literal interpretation. |
| **20-40%** | Incremental | Slight variations on proven approaches. |
| **40-60%** | Exploratory | Cross-domain connections. Metaphors and analogies. |
| **60-80%** | Bold | Experimental framing. "What if we tried..." territory. |
| **80-100%** | Unbound | Full creative latitude. Genre-bending. Art mode. |

### Adjusting Sliders

**Via code:**
```python
# Direct value assignment
config.set_slider("creativity", 80)
config.set_slider("technicality", 90)

# Generate updated LIVEHUD
print(config.generate_livehud())
```

**Via conversation:**
```markdown
"Set creativity to 80%"
"Max technicality"
"Min humor"
"Reset sliders"
"Increase directness by 20"
```

**Context-adaptive calibration** (automatic):

| Context | Adjustment |
|---------|------------|
| Quick question | 🔊↓15-25% |
| Deep research | 🔬↑70-85%, 🔊↑50% |
| Brainstorming | 🎨↑80-95%, 😂↑60% |
| Debugging | 😂↓20%, 🎯↑85%, 🔬↑80% |
| Casual chat | 😂↑65%, 🔬↓30% |

### Visual Progress Bars

The LIVEHUD displays sliders with visual bars:

```
├─ 🎨 Creativity  [████████░░░░░░░░░░░░]  40%  55%
```

Bar characters:
- `█` = Filled (each = 5%)
- `░` = Empty

Reference:
| Percentage | Visual (20 chars) |
|------------|-------------------|
| 0% | `░░░░░░░░░░░░░░░░░░░░` |
| 25% | `█████░░░░░░░░░░░░░░░` |
| 50% | `██████████░░░░░░░░░░` |
| 75% | `███████████████░░░░░` |
| 100% | `████████████████████` |

---

## Setup Workflows

### Workflow 1: Fresh Installation

Use when: Setting up MERIDIAN Brain on a new system

```python
# Step 1: Verify Python version
python --version  # Requires 3.11+

# Step 2: Clone repository
git clone https://github.com/zenchantlive/meridian.git
cd meridian

# Step 3: Install dependencies
pip install -e .

# Step 4: Verify components
python -c "
from brain.scripts import (
    ChunkStore, ChunkingEngine, AutoLinker,
    RememberOperation, REPLSession
)
print('✓ All core components imported successfully')
"

# Step 5: Test memory operations
from brain.scripts import ChunkStore, RememberOperation
store = ChunkStore('brain/memory/test')
remember = RememberOperation(store)
result = remember.remember(
    content='Test memory',
    conversation_id='setup-test'
)
assert result['success'], "Memory test failed"
print('✓ Memory system operational')
```

### Workflow 2: Configuration Setup

Use when: Configuring personalities and sliders for a project

```markdown
# Step 1: Read default personality
Read: brain/personalities/BASE.md

# Step 2: Select appropriate mode based on project type
- Coding project → TECHNICAL_COPILOT
- Research/analysis → RESEARCH_ANALYST  
- Creative work → CREATIVE_DIRECTOR
- Mixed/unknown → BASE

# Step 3: Fine-tune with sliders if needed
Read relevant: brain/sliders/[SLIDER].md
Adjust values based on project requirements

# Step 4: Document configuration in memory
Use remember_operation to store:
- Selected personality mode
- Slider adjustments
- Project-specific preferences
```

### Workflow 3: Memory Integration

Use when: Integrating memory operations into agent workflow

```python
# Pattern 1: Remember user preferences
from brain.scripts import ChunkStore, RememberOperation

class MeridianMemory:
    def __init__(self, base_path="brain/memory"):
        self.store = ChunkStore(base_path)
        self.remember = RememberOperation(self.store)
    
    def record_preference(self, content, tags=None, confidence=0.8):
        """Record a user preference."""
        return self.remember.remember(
            content=content,
            conversation_id=self.current_conversation,
            tags=tags or ["preference"],
            confidence=confidence,
            chunk_type="preference"
        )
    
    def record_fact(self, content, tags=None, confidence=0.9):
        """Record a factual piece of information."""
        return self.remember.remember(
            content=content,
            conversation_id=self.current_conversation,
            tags=tags or ["fact"],
            confidence=confidence,
            chunk_type="fact"
        )
```

---

## Advanced Usage

### Using the REPL Environment

The REPL provides a secure sandbox for recursive LLM operations:

```python
from brain.scripts import REPLSession, ChunkStore
from unittest.mock import Mock

# Setup
store = ChunkStore("brain/memory")
llm_client = Mock()  # Replace with actual LLM client
llm_client.complete = Mock(return_value="FINAL('answer')")

# Create REPL session
repl = REPLSession(
    chunk_store=store,
    llm_client=llm_client,
    max_iterations=10,
    timeout_seconds=60
)

# Execute code in sandbox
result = repl.execute("""
# Search for relevant chunks
chunks = search_chunks('python testing')

# Read first chunk
if chunks:
    data = read_chunk(chunks[0])
    FINAL(data['content'])
else:
    FINAL('No memories found')
""")

print(f"Result: {repl.get_result()}")
```

**Security Features:**
- Blocks dangerous imports (os, sys, subprocess)
- Blocks eval/exec/compile/open
- Blocks attribute exploitation (__class__, __bases__, etc.)
- Memory limits (10MB for string operations)
- Timeout protection

### Custom Chunk Types

Define project-specific chunk types:

```python
# In your application code
CUSTOM_CHUNK_TYPES = {
    'api_endpoint': 'API endpoint documentation',
    'database_schema': 'Database structure information',
    'deployment_config': 'Deployment configuration',
    'user_story': 'User requirement or story'
}

# Use when creating memories
remember.remember(
    content="POST /api/users creates new user",
    conversation_id="api-docs",
    chunk_type="api_endpoint",  # Custom type
    tags=["api", "users", "post"]
)
```

---

## Troubleshooting

### Common Issues

**Issue: ImportError for brain.scripts**
```
Solution: Ensure you're in the repo root and run:
pip install -e .
# Or set PYTHONPATH:
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Issue: Permission denied on memory directory**
```
Solution: Check directory permissions:
ls -la brain/memory/
chmod 755 brain/memory/
```

**Issue: ChunkStore initialization fails**
```
Solution: Verify path exists:
mkdir -p brain/memory/default
# Or specify full path:
store = ChunkStore("/absolute/path/to/memory")
```

**Issue: REPL sandbox blocks legitimate code**
```
Solution: The sandbox is intentionally restrictive. If you need
specific functionality, modify ALLOWED_BUILTINS in repl_environment.py
or use the memory functions directly instead of sandbox execution.
```

**Issue: RECALL returns no results when searching**
```
Problem: You search for "task tracking" but stored memory says "uses beads"

Explanation: The basic search uses keyword matching with synonym expansion,
but it's not semantic search. Query expansion helps but has limits.

Solution 1: Use broader terms
  Instead of: "How does task tracking work?"
  Try: "How do we manage work?"

Solution 2: Search using stored vocabulary
  Check what terms are in memories:
  chunk = store.get_chunk(chunk_id)
  print(chunk.content)

Solution 3: Store memories with rich tags
  remember.remember(
      content="Uses beads for task tracking",
      tags=["workflow", "beads", "task", "tracking", "project-management"]
  )

Synonyms that auto-expand:
  - task → task, bead, issue, work item, todo
  - tracking → tracking, management, workflow, organization
  - memory → memory, storage, remember, chunk
  - remember → remember, store, save, record
  - project → project, system, meridian, brain
  - status → status, state, progress, complete
  - architecture → architecture, design, structure
  - test → test, testing, validate, verify
  - file → file, document, code, script
  - format → format, structure, layout

Solution 4: Extend QUERY_SYNONYMS in recall_operation.py
  Add domain-specific terms:
  ```python
  # In brain/scripts/recall_operation.py
  QUERY_SYNONYMS = {
      # ... existing synonyms ...
      'auth': ['auth', 'authentication', 'login', 'signin'],
      'database': ['database', 'db', 'postgres', 'mysql', 'storage'],
  }
  ```
```

### Debug Checklist

When MERIDIAN Brain isn't working:

1. **Verify imports**: `python -c "from brain.scripts import ChunkStore"`
2. **Check storage path**: Ensure memory directory exists and is writable
3. **Test basic operations**: Create a test memory and read it back
4. **Check chunk schema**: Verify JSON files match expected schema
5. **Review logs**: Look for errors in console output

---

## Integration Patterns

### Pattern 1: Conversation Memory

Store conversation context automatically:

```python
class ConversationMemory:
    def __init__(self, conversation_id):
        self.store = ChunkStore("brain/memory")
        self.remember = RememberOperation(self.store)
        self.conversation_id = conversation_id
    
    def store_exchange(self, user_msg, assistant_msg):
        """Store a conversation exchange."""
        content = f"User: {user_msg}\nAssistant: {assistant_msg}"
        return self.remember.remember(
            content=content,
            conversation_id=self.conversation_id,
            tags=["conversation", "exchange"],
            chunk_type="note"
        )
```

### Pattern 2: Project Context

Store and retrieve project-specific information:

```python
class ProjectMemory:
    def __init__(self, project_name):
        self.store = ChunkStore(f"brain/memory/projects/{project_name}")
        self.remember = RememberOperation(self.store)
        self.project_name = project_name
    
    def store_decision(self, decision, rationale, confidence=0.9):
        """Record an architectural decision."""
        content = f"Decision: {decision}\nRationale: {rationale}"
        return self.remember.remember(
            content=content,
            conversation_id=f"project-{self.project_name}",
            tags=["decision", "architecture"],
            confidence=confidence,
            chunk_type="decision"
        )
```

### Pattern 3: Agent Configuration

Use personalities and sliders to configure agent behavior:

```python
class ConfiguredAgent:
    def __init__(self, personality_mode="BASE"):
        self.personality = self._load_personality(personality_mode)
        self.memory = ConversationMemory("agent-001")
    
    def _load_personality(self, mode):
        """Load personality configuration from Markdown."""
        # Read: brain/personalities/{mode}.md
        # Parse slider values
        # Apply to agent behavior
        pass
    
    def process_request(self, user_input):
        # 1. Retrieve relevant memories
        # 2. Apply personality configuration
        # 3. Generate response
        # 4. Store exchange
        pass
```

---

## Reference Materials

**Detailed Documentation:**
- Architecture: See [references/ARCHITECTURE.md](references/ARCHITECTURE.md)
- Memory Schema: See `brain/MEMORY_SCHEMA.md`
- API Reference: See [references/API.md](references/API.md)
- Personality Specs: See `brain/personalities/*.md`
- Slider Specs: See `brain/sliders/*.md`

**Related Skills:**
- `beads` - Task tracking (use `bd` commands)
- `brainstorming` - Design exploration
- `test-driven-development` - For writing tests

---

## Quick Reference Card

### Memory System Operations

| Task | Code |
|------|------|
| Initialize config | `config = load_meridian_config()  # Uses default 'brain/'` |
| Switch mode | `config.set_mode("TECHNICAL")`  # BASE, RESEARCH, CREATIVE, TECHNICAL |
| Adjust slider | `config.set_slider("creativity", 80)` |
| Generate LIVEHUD | `print(config.generate_livehud())` |
| Update memory protocol | `config.memory.past = "Retrieved context"` |
| Update system state | `config.system.memory_files = 5` |
| Store memory | `remember.remember(content="...", conversation_id="...")` |
| Recall | `recall.recall(query="...", max_results=5)` |
| Recall (with synonyms) | `"task"` finds memories with `bead`, `issue`, `todo` |
| Reason | `reason.reason(query="...", analysis_type="pattern")` |

### LIVEHUD Format Elements

| Element | Format | Example |
|---------|--------|---------|
| Top border | `╔═╗` | `╔══════════════════╗` |
| Section divider | `╠═╣` | `╠══════════════════╣` |
| Side border | `║` | `║ Content ║` |
| Bottom border | `╚═╝` | `╚══════════════════╝` |
| Slider bar | `[██░░]` | `[████████░░░░░░░░]` |
| Tree connector | `├ └` | `├─ 🎨 Creativity` |

### Personality Mode Presets

| Mode | Trigger | Adjustments |
|------|---------|-------------|
| BASE | Default | All defaults |
| RESEARCH | `"research mode"` | 🔬↑85%, 🎯↑75%, 😂↓25% |
| CREATIVE | `"creative mode"` | 🎨↑90%, 😂↑70%, 🔊↑60% |
| TECHNICAL | `"technical mode"` | 🔬↑90%, 🎯↑80%, 😂↓15% |
| CONCISE | `"concise mode"` | 🔊↓15%, 🎯↑85% |

### File Locations

| Component | Location | Format |
|-----------|----------|--------|
| Personalities | `brain/personalities/*.md` | Markdown |
| Sliders | `brain/sliders/*.md` | Markdown |
| LIVEHUD spec | `brain/gauges/LIVEHUD.md` | Markdown |
| Memory storage | `brain/memory/` | JSON |
| Core scripts | `brain/scripts/*.py` | Python |

### Key Classes

| Class | Purpose |
|-------|---------|
| `MeridianConfig` | Parse original MERIDIAN format, generate LIVEHUD |
| `ChunkStore` | JSON storage CRUD |
| `RememberOperation` | High-level memory creation |
| `RecallOperation` | Natural language retrieval |
| `ReasonOperation` | Pattern analysis & synthesis |
| `REPLSession` | Secure LLM sandbox |
| `MemoryCache` | Multi-tier caching |

---

**Remember**: MERIDIAN Brain is a **framework**, not just a library. It provides structure for agent memory and behavior. Start simple (basic memory operations), then progressively adopt personalities, sliders, and advanced features as needed.
