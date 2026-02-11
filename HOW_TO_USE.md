# How to Use MERIDIAN Brain Enhanced

## The Big Picture

MERIDIAN Brain Enhanced has **two integrated systems**:

1. **Original MERIDIAN Format** - Configurable personality/behavior (LIVEHUD, sliders, personalities)
2. **RLM Memory System** - Persistent storage with natural language retrieval (REMEMBER, RECALL, REASON)

## How It Works in Practice

### Scenario: Working on a Feature

**Without MERIDIAN:**
```
You: "Remember I want to use PostgreSQL"
[Next day, new conversation]
You: "What database should I use?"
AI: "What are your requirements?"
You: "I told you yesterday! PostgreSQL!"
```

**With MERIDIAN:**
```
[AI automatically records decision]
You: "Let's use PostgreSQL for JSON support"
AI: [Stores: "Decision: Use PostgreSQL. Rationale: JSON support"]

[Next day, new conversation]
You: "What database are we using?"
AI: [Recalls stored decision] "You chose PostgreSQL for its JSON support."
```

## Key Features

### 1. Automatic Memory (No "Remember This" Commands)

```python
from auto_memory import AutoMemory

auto_mem = AutoMemory('brain/memory')
auto_mem.start_session("Feature work")

# Automatic recordings:
- Task completions → what was done, files changed, outcome
- Decisions → what was decided, why, alternatives considered  
- Preferences → what we learned about user preferences
- Issues → problems encountered and how they were fixed

auto_mem.end_session("Summary of work")
```

### 2. Natural Language Recall (Synonym Expansion)

```python
from brain.scripts import RecallOperation

recall = RecallOperation(store)

# Query expansion happens automatically:
"task tracking" → finds "beads", "workflow", "tickets"
"store data" → finds "remember", "save", "memory"
"project status" → finds "progress", "complete", "done"

result = recall.recall("How do we track tasks?")
# Returns: "Uses beads for task tracking - 48 beads closed so far"
```

### 3. Pattern Analysis (REASON)

```python
from brain.scripts import ReasonOperation

reason = ReasonOperation(store)
result = reason.reason("What technologies does user prefer?")

# Returns synthesis across multiple memories:
# "Found 3 patterns:
#   1. Python for backend
#   2. React for frontend  
#   3. Dark mode for UI"
```

### 4. Configurable Personality (LIVEHUD)

```python
from brain.scripts import load_meridian_config

config = load_meridian_config()

# Switch modes - automatically adjusts sliders:
config.set_mode("TECHNICAL")  # 🔬↑90%, 🎯↑80%, 😂↓15%
config.set_mode("CREATIVE")   # 🎨↑90%, 😂↑70%, 🔊↑60%

# Generate dashboard
print(config.generate_livehud())
```

Output:
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
║  ├─ 🧠 Past:    [Retrieved tech preferences]                                 ║
║  ├─ 👁️ Present: [Implementing feature]                                       ║
║  └─ 🔮 Future:  [Test implementation]                                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ▸ SYSTEM STATE                                                              ║
║  ├─ 💾 Context: [Stable] │ 🔧 Tools: [Active]                                ║
║  ├─ 📂 Memory:  [15 files] │ [0 pending]                                     ║
║  └─ ⚡ Vibe:    [Focused]                                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Typical Workflow

1. **Start Session** → AutoMemory records session start
2. **Work on Tasks** → Automatic recordings of:
   - Files modified
   - Decisions made
   - Issues resolved
   - Preferences learned
3. **Ask Questions** → RECALL finds relevant memories
4. **Analyze** → REASON synthesizes patterns
5. **End Session** → Summary stored for future reference

## What's Actually Implemented

✅ **Working Now:**
- REMEMBER: Store with chunking & auto-linking
- RECALL: Natural language retrieval with synonym expansion
- REASON: Pattern analysis & synthesis
- AutoMemory: Automatic recording without explicit commands
- LIVEHUD: Personality dashboard with mode switching
- Sliders: 6 cognitive dimensions with presets
- Query expansion: "task" finds "beads", etc.

⚠️ **Limitations:**
- No semantic search (embeddings) - uses keyword + synonyms
- Requires mock LLM for REPL (no real OpenAI/Anthropic integration yet)
- Keyword search not as smart as true semantic search

## Example: Complete Session

```python
from brain.scripts import (
    load_meridian_config, AutoMemory, 
    ChunkStore, RecallOperation
)

# Setup
config = load_meridian_config()
config.set_mode("TECHNICAL")
print(config.generate_livehud())  # Show current state

# Start auto-recording
auto_mem = AutoMemory('brain/memory')
auto_mem.start_session("Adding auth feature")

# As you work, record automatically:
auto_mem.record_decision(
    decision="Use JWT tokens for auth",
    rationale="Stateless, works well with React frontend",
    alternatives=["Session cookies", "OAuth2"]
)

auto_mem.record_preference(
    what_was_learned="User wants 1-hour token expiry",
    confidence=0.9
)

# Later, recall without explicit context:
recall = RecallOperation(auto_mem.store)
result = recall.recall("What did we decide about authentication?")
print(result.answer)
# "Decision: Use JWT tokens for auth. Rationale: Stateless..."

auto_mem.end_session("Auth feature implemented")
```

## The Point

**MERIDIAN Brain Enhanced** means:
- ✅ I automatically remember what we're doing
- ✅ You don't have to repeat yourself
- ✅ I can synthesize patterns across our work
- ✅ My behavior is configurable (personalities/sliders)
- ✅ You can see my "state" via LIVEHUD

**No more:** "I told you that yesterday!"
**Instead:** "Based on our previous decision to use PostgreSQL..."
