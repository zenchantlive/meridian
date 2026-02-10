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
python -c "from brain.scripts import ChunkStore, RememberOperation, REPLSession; print('✓ MERIDIAN Brain ready')"
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
| Memory Protocol | Original memory system | `brain/memory/MEMORY_PROTOCOL.md` |

**Key Insight:** The original framework uses **Markdown-based configuration** while the enhanced system uses **JSON-based storage**. They complement each other - personalities/sliders configure *behavior*, while the new memory system provides *persistent storage*.

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

**RECALL** - Retrieve information (requires D3.2 implementation):
```python
# Future API - not yet implemented
from brain.scripts import RecallOperation

recall = RecallOperation(repl_session)
result = recall.recall(
    query="What does the user prefer for testing?",
    conversation_id="conv-123",
    max_results=5
)
```

**REASON** - Analyze and synthesize (requires D3.3 implementation):
```python
# Future API - not yet implemented
from brain.scripts import ReasonOperation

reason = ReasonOperation(repl_session)
result = reason.reason(
    query="Analyze user's testing preferences",
    context_chunks=["chunk-id-1", "chunk-id-2"]
)
```

### Storage Architecture

**Directory Structure:**
```
brain/memory/
├── SCHEMA.md              # Chunk schema documentation
├── 2026-02-10/            # Date-organized storage
│   ├── chunk-001.json
│   ├── chunk-002.json
│   └── index.json         # Daily index
├── tags/                  # Tag indexes
│   └── preference.json
└── links/                 # Link graph indexes
    └── graph.json
```

**Chunk Schema:**
```json
{
  "id": "chunk-2026-02-10-uuid",
  "content": "User prefers pytest for testing",
  "tokens": 12,
  "type": "preference",
  "metadata": {
    "created_at": "2026-02-10T09:00:00Z",
    "confidence": 0.95,
    "conversation_id": "conv-123",
    "access_count": 0
  },
  "links": [
    {"target_id": "chunk-abc", "type": "context_of", "strength": 0.8}
  ],
  "tags": ["preference", "testing", "python"]
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

**BASE** (`brain/personalities/BASE.md`)
- Default balanced configuration
- Moderate values on all sliders
- Use when: Unclear task type, general conversation

**RESEARCH_ANALYST** (`brain/personalities/RESEARCH_ANALYST.md`)
- High Technicality (85), High Patience (80)
- Low Humor (20), Moderate Directness (60)
- Use when: Research, fact-finding, documentation

**CREATIVE_DIRECTOR** (`brain/personalities/CREATIVE_DIRECTOR.md`)
- High Creativity (90), High Humor (70)
- Low Technicality (30), Moderate Directness (50)
- Use when: Brainstorming, content creation, design

**TECHNICAL_COPILOT** (`brain/personalities/TECHNICAL_COPILOT.md`)
- High Technicality (90), High Directness (85)
- Low Creativity (25), Moderate Patience (50)
- Use when: Coding, debugging, technical work

**CONCISE**
- Low Verbosity (20), High Directness (80)
- Use when: Quick answers, status updates

### Switching Modes

Personality modes are **Markdown-based configuration** that guides agent behavior. To switch:

```markdown
# In conversation or prompt:
"Switch to TECHNICAL_COPILOT mode"
"Activate RESEARCH_ANALYST personality"
```

The agent should read the corresponding `brain/personalities/[MODE].md` file and adjust behavior accordingly.

---

## Configuration Sliders

### Slider Reference

Read `brain/sliders/*.md` for detailed specifications.

| Slider | Range | Description | File |
|--------|-------|-------------|------|
| **Creativity** | 0-100 | Tendency toward novel responses | `CREATIVITY.md` |
| **Technicality** | 0-100 | Level of technical detail | `TECHNICALITY.md` |
| **Humor** | 0-100 | Frequency of humor | `HUMOR.md` |
| **Directness** | 0-100 | Conciseness and bluntness | `DIRECTNESS.md` |
| **Verbosity** | 0-100 | Length of responses | *(implied)* |
| **Patience** | 0-100 | Willingness to explore | *(implied)* |
| **Morality** | 0-100 | Ethical emphasis | `MORALITY.md` |
| **Soul** | 0-100 | Personality/character | `SOUL.md` |
| **Identity** | - | Self-concept | `IDENTITY.md` |
| **Tools** | - | Tool usage patterns | `TOOLS.md` |
| **User** | - | User relationship | `USER.md` |

### Adjusting Sliders

Sliders can be adjusted individually:
```markdown
"Set creativity to 80"
"Increase technicality by 20"
"Make responses more direct"
```

Or switched via personality modes (which set multiple sliders).

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
- Memory Schema: See `brain/memory/SCHEMA.md`
- API Reference: See [references/API.md](references/API.md)
- Personality Specs: See `brain/personalities/*.md`
- Slider Specs: See `brain/sliders/*.md`

**Related Skills:**
- `beads` - Task tracking (use `bd` commands)
- `brainstorming` - Design exploration
- `test-driven-development` - For writing tests

---

## Quick Reference Card

### Common Operations

| Task | Command/Code |
|------|--------------|
| Remember something | `remember.remember(content="...", conversation_id="...")` |
| List chunks by tag | `store.list_chunks(tags=["preference"])` |
| Read chunk | `store.get_chunk("chunk-id")` |
| Switch personality | Read `brain/personalities/[MODE].md` |
| Adjust slider | Reference `brain/sliders/[SLIDER].md` |
| Check system status | `store.get_stats()` |

### File Locations

| Component | Location |
|-----------|----------|
| Memory storage | `brain/memory/` |
| Personalities | `brain/personalities/*.md` |
| Sliders | `brain/sliders/*.md` |
| Core scripts | `brain/scripts/*.py` |
| Configuration | `.specify/memory/constitution.md` |

### Key Classes

| Class | Purpose |
|-------|---------|
| `ChunkStore` | JSON storage CRUD |
| `RememberOperation` | High-level memory creation |
| `REPLSession` | Secure LLM sandbox |
| `AutoLinker` | Automatic graph linking |
| `ChunkingEngine` | Text chunking |

---

**Remember**: MERIDIAN Brain is a **framework**, not just a library. It provides structure for agent memory and behavior. Start simple (basic memory operations), then progressively adopt personalities, sliders, and advanced features as needed.
