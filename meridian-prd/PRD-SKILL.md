# MERIDIAN_Brain Enhanced: Skill Interface Design

## Document Overview

This document defines the skill interface that agents use to interact with the MERIDIAN_Brain Enhanced system. The skill serves as the bridge between agent natural language capabilities and the underlying memory and configuration systems.

**Related Document:** PRD.md, PRD-ARCH.md, PRD-MEMORY.md
**Version:** 1.0

---

## 1. Skill Overview

### 1.1 Purpose

The `meridian-guide` skill enables agents to:

- Understand the MERIDIAN_Brain Enhanced system structure and capabilities
- Perform memory operations through natural language commands
- Manage personality modes and behavioral configurations
- Access configuration options and modify agent behavior
- Onboard to new MERIDIAN_Brain setups automatically

### 1.2 Design Principles

**Natural First:** Agents interact using natural language, not technical commands. The skill translates natural requests into system operations.

**Progressive Disclosure:** Simple operations are easy. Complex operations are available but require explicit requests.

**Contextual Help:** The skill provides relevant information at each step without requiring users to read documentation.

**Error Recovery:** Failed operations include helpful suggestions for recovery.

### 1.3 Skill Structure

```
meridian-guide/
├── SKILL.md                 # Main skill instructions (500 lines max)
├── README.md                # Quick reference card
├── references/
│   ├── COMMANDS.md          # Complete command reference
│   ├── PERSONALITIES.md     # Personality mode descriptions
│   ├── MEMORY_TYPES.md      # Memory type definitions
│   └── CONFIG_FIELDS.md     # Configuration field documentation
├── examples/
│   ├── common_usage.md      # Common interaction patterns
│   └── memory_operations.md # Memory operation examples
└── scripts/
    ├── memory_client.py     # Memory operation helpers
    └── personality_client.py # Personality mode helpers
```

---

## 2. SKILL.md Structure

### 2.1 Frontmatter

```yaml
---
name: meridian-guide
description: Interface for MERIDIAN_Brain Enhanced system - manage memory, personalities, and configuration
argument-hint: describe what you want to do or find
user-invocable: true
allowed-tools: []
---
```

### 2.2 Section Organization

The SKILL.md file is organized into these sections:

**1. Quick Start**
- Most common operations
- Example commands
- Getting help

**2. Memory Operations**
- Creating memories
- Retrieving memories
- Updating memories
- Querying memories
- Managing memories

**3. Personality Modes**
- Listing available modes
- Understanding mode characteristics
- Switching modes
- Customizing modes

**4. Configuration**
- Understanding configuration structure
- Modifying configuration
- Exporting/importing configurations

**5. System Operations**
- Checking system status
- Running maintenance
- Troubleshooting

**6. Reference**
- Command quick reference
- Additional resources

---

## 3. Memory Commands

### 3.1 Command Reference

Agents invoke memory operations through natural language patterns:

**Create Memory**

```
"Remember that [content]"
"Note that [information]"
"Create a memory about [topic]"
"I want to remember [details]"
```

**Example Invocation:**

```
User: "Remember that I prefer dark mode for coding"

Skill interprets: memory.create(
    content="User prefers dark mode for coding",
    type="preference",
    tags=["editor", "coding-style", "ui"],
    confidence=0.95
)
```

**Retrieve Memory**

```
"What do you remember about [topic]?"
"Tell me what you know about [subject]"
"What memories do you have of [context]?"
"Recall any information about [topic]"
```

**Example Invocation:**

```
User: "What do you remember about my code review preferences?"

Skill interprets: memory.retrieve(
    query="code review preferences",
    filters={"type": "preference"},
    limit=5
)
```

**Update Memory**

```
"Update the memory about [topic] to say [new information]"
"Change [memory identifier] to [new content]"
"That information is outdated; [updated information]"
"Correct that memory: [correction]"
```

**Query Memory**

```
"Find all memories about [topic]"
"Search memories with tag [tagname]"
"Show me memories from [time period]"
"List all preferences related to [category]"
```

**Delete Memory**

```
"Forget about [topic]"
"Delete the memory about [topic]"
"Remove that memory"
"That memory is no longer relevant"
```

### 3.2 Command Patterns

Each command type follows consistent patterns:

**Creation Pattern:**

```
Pattern: "Remember/Note/Create that [content]"

Extract:
- Content: Everything after the verb
- Tags: Infer from context or request clarification
- Type: Infer from content or request clarification
- Confidence: Default 0.7, adjust based on user certainty

Response:
✓ Memory created: [ID]
  - Type: [type]
  - Tags: [tags]
  - Confidence: [confidence]
```

**Retrieval Pattern:**

```
Pattern: "What do you know/remember/recall about [query]"

Extract:
- Query: The topic or question
- Filters: Implicit from conversation context
- Limit: Default 5, adjust based on query complexity

Response:
## Relevant Memories

1. [Memory Title] (relevance: 0.XX)
   - Type: [type] | Confidence: 0.XX
   - [First 100 characters]...
```

**Update Pattern:**

```
Pattern: "Update/Change/Correct [memory reference] to [content]"

Extract:
- Memory Reference: ID or description
- New Content: Everything after "to" or ":"
- Confidence: Preserve or adjust based on update source

Response:
✓ Memory updated: [ID]
  - Changes saved
  - Previous confidence: [X] → New confidence: [Y]
```

### 3.3 Response Templates

**Memory Created:**

```
## Memory Created ✓

**ID:** mem-[uuid]
**Type:** [type]
**Tags:** [tag1, tag2, tag3]
**Confidence:** [0.XX]

[Memory content preview]

Use this ID to reference this memory later:
`memory:mem-[uuid]`
```

**Memory Retrieved:**

```
## Found [N] Relevant Memories

### Top Match: [Memory Title]
- **Relevance:** 0.XX
- **Confidence:** 0.XX
- **Type:** [type]
- **Tags:** [tags]

[Full memory content]

---

### Related Memories
- [Memory 2 Title] (relevance: 0.XX)
- [Memory 3 Title] (relevance: 0.XX)
```

**Memory Query Results:**

```
## Query Results: "[query]"

Found [N] memories matching your criteria.

| Title | Type | Confidence | Created |
|-------|------|------------|---------|
| [Title] | [type] | 0.XX | [date] |
| [Title] | [type] | 0.XX | [date] |

Showing [N] of [total] results. Refine query for more specific results.
```

---

## 4. Personality Commands

### 4.1 Command Reference

**List Modes:**

```
"What personality modes are available?"
"List all available modes"
"What modes can you switch between?"
"Show me the personality options"
```

**Describe Mode:**

```
"What is the [mode name] mode like?"
"Describe the [mode name] personality"
"What does [mode name] mode do?"
"Tell me about [mode name] mode"
```

**Switch Mode:**

```
"Switch to [mode name] mode"
"Use [mode name] personality"
"Activate [mode name] mode"
"I want to use [mode name]"
```

**Get Current Mode:**

```
"What mode are you in?"
"Which personality is active?"
"Current mode"
"Show me the active personality"
```

### 4.2 Mode Descriptions

The skill provides descriptions for each personality mode:

**BASE Mode:**
- Default balanced configuration
- Suitable for general conversation
- Moderate values on all sliders
- Recommended for: Initial interactions, unclear task type

**RESEARCH_ANALYST Mode:**
- Optimized for information gathering and analysis
- High Technicality, High Patience
- Low Humor, Moderate Directness
- Recommended for: Research tasks, fact-finding, documentation

**CREATIVE_DIRECTOR Mode:**
- Optimized for creative work and ideation
- High Creativity, High Humor
- Low Technicality, Moderate Directness
- Recommended for: Brainstorming, content creation, design exploration

**TECHNICAL_COPILOT Mode:**
- Optimized for code and technical tasks
- High Technicality, High Directness
- Low Creativity, Moderate Patience
- Recommended for: Coding, debugging, technical explanation

**CONCISE Mode:**
- Optimized for quick, efficient responses
- Low Verbosity, High Directness
- Moderate Technicality, Low Creativity
- Recommended for: Quick questions, status updates, simple tasks

### 4.3 Response Templates

**Mode List:**

```
## Available Personality Modes

| Mode | Description | Best For |
|------|-------------|----------|
| **BASE** | Balanced, general-purpose | General conversation |
| **RESEARCH_ANALYST** | Analytical, thorough | Research, fact-finding |
| **CREATIVE_DIRECTOR** | Creative, expansive | Ideation, content |
| **TECHNICAL_COPILOT** | Precise, direct | Code, technical work |
| **CONCISE** | Brief, efficient | Quick answers |

Current mode: **BASE**

To switch: "Switch to [mode name] mode"
```

**Mode Description:**

```
## [Mode Name] Mode

**Description:** [One-line description]

**Slider Settings:**
- Creativity: [XX/100]
- Technicality: [XX/100]
- Humor: [XX/100]
- Directness: [XX/100]
- Verbosity: [XX/100]
- Patience: [XX/100]

**Best For:**
- [Use case 1]
- [Use case 2]
- [Use case 3]

**Characteristics:**
- [Characteristic 1]
- [Characteristic 2]
```

---

## 5. Configuration Commands

### 5.1 Command Reference

**View Configuration:**

```
"What is my current configuration?"
"Show me the active settings"
"What are the current parameter values?"
"Display configuration"
```

**View Specific Setting:**

```
"What is my [slider name] setting?"
"How is [parameter] configured?"
"Show me [setting name] value"
"What is the current [parameter]?"
```

**Modify Setting:**

```
"Set [slider name] to [value]"
"Change [parameter] to [value]"
"Adjust [setting] to [level]"
"Make [parameter] more [adjective]"
```

**Reset Configuration:**

```
"Reset to BASE personality"
"Restore default settings"
"Reset all sliders to default"
"Go back to default configuration"
```

### 5.2 Slider Reference

| Slider | Range | Description |
|--------|-------|-------------|
| Creativity | 0-100 | Tendency toward novel, unconventional responses |
| Technicality | 0-100 | Level of technical detail in explanations |
| Humor | 0-100 | Frequency and type of humor in responses |
| Directness | 0-100 | Conciseness and bluntness of communication |
| Verbosity | 0-100 | Length and depth of responses |
| Patience | 0-100 | Willingness to explore alternatives before concluding |
| Morality | 0-100 | Emphasis on ethical considerations |
| Soul | 0-100 | Personality and character in responses |

### 5.3 Response Templates

**Configuration Display:**

```
## Current Configuration

**Personality:** BASE

| Slider | Value | Visual |
|--------|-------|--------|
| Creativity | 65 | ████████░░ |
| Technicality | 50 | ██████░░░░ |
| Humor | 50 | ██████░░░░ |
| Directness | 50 | ██████░░░░ |
| Verbosity | 60 | ███████░░░ |
| Patience | 55 | ███████░░░ |
| Morality | 70 | ████████░░ |
| Soul | 60 | ███████░░░ |

To change: "Set [slider] to [value]" or "Make [slider] more [adjective]"
```

---

## 6. System Commands

### 6.1 Command Reference

**System Status:**

```
"What is the system status?"
"How is the memory system doing?"
"Check memory health"
"System status"
```

**Memory Statistics:**

```
"How many memories do you have?"
"Memory statistics"
"Show me memory stats"
"How much memory is stored?"
```

**Consolidation:**

```
"Consolidate memories"
"Run memory consolidation"
"Clean up memories"
"Optimize memory storage"
```

**Export:**

```
"Export memories"
"Backup my memories"
"Save configuration"
"Export to MERIDIAN format"
```

### 6.2 Response Templates

**System Status:**

```
## System Status

**Memory:**
- Total memories: [N]
- Active memories: [N]
- Archived memories: [N]
- Last consolidation: [date]

**Index:**
- Index size: [X] MB
- Index status: Healthy
- Last rebuild: [date]

**Configuration:**
- Current mode: [mode]
- Modified: [date]
- Unsaved changes: [Y/N]

**Status:** ✓ All systems operational
```

---

## 7. Help and Guidance

### 7.1 Help Commands

```
"Help me with memory"
"What can you do?"
"Show me commands"
"How do I [task]?"
"I need assistance"
```

### 7.2 Help Response

```
## MERIDIAN_Brain Enhanced - Help

Welcome! I help you interact with the MERIDIAN_Brain Enhanced system.

### Quick Start

**Memory Operations**
- "Remember that [information]" - Create a memory
- "What do you know about [topic]?" - Retrieve memories
- "Update the memory about [topic] to [new info]" - Update memory

**Personality Modes**
- "Switch to [mode] mode" - Change personality
- "What modes are available?" - List modes
- "Describe [mode] mode" - Get mode details

**Configuration**
- "Show me current settings" - View configuration
- "Set [slider] to [value]" - Modify setting
- "Reset to BASE" - Restore defaults

**System**
- "System status" - Check health
- "Memory statistics" - View stats
- "Consolidate memories" - Optimize storage

### Need More Help?
Ask about specific operations:
- "How do I create memories?"
- "How do I switch modes?"
- "What are the personality modes?"
```

---

## 8. Error Handling

### 8.1 Common Errors

**Memory Not Found:**

```
⚠️ Memory Not Found

I couldn't find a memory matching "[description]".

Suggestions:
- Try a different search query
- List recent memories: "What memories do you have?"
- Create a new memory if this is new information

Did you mean one of these?
- [Memory 1]
- [Memory 2]
```

**Invalid Query:**

```
⚠️ Invalid Query

I couldn't understand your query "[query]".

Suggestions:
- Try rephrasing: "What do you remember about [topic]?"
- Use simpler terms
- Check spelling

Command formats:
- "Remember that [information]"
- "What do you know about [topic]?"
- "Find memories with tag [tagname]"
```

**Mode Not Found:**

```
⚠️ Mode Not Found

"[modename]" is not a recognized personality mode.

Available modes:
- BASE
- RESEARCH_ANALYST
- CREATIVE_DIRECTOR
- TECHNICAL_COPILOT
- CONCISE

To switch: "Switch to [mode name] mode"
```

**System Error:**

```
⚠️ System Error

An error occurred while processing your request.

Error: [error type]
Details: [error description]

Suggestions:
- Try again in a moment
- If the issue persists, check system status
- Report this if it continues

System Status: [status]
```

---

## 9. Context Integration

### 9.1 Automatic Context Injection

The skill automatically injects relevant context when:

- A new conversation session begins
- A user references past interactions
- A configuration change affects current behavior
- A memory is retrieved that affects the current topic

### 9.2 Context Format

```
## Context from Memory

Based on our previous interactions:

- [Memory summary 1]
- [Memory summary 2]
- [Memory summary 3]

[User preference context]

---
Relevant memories: [count]
Confidence: [average confidence]
```

---

## 10. Example Interactions

### 10.1 Creating a Memory

```
User: Remember that I prefer pytest for testing Python code

Assistant: ✓ Memory created: mem-2026-02-10-001

**Type:** preference
**Tags:** python, testing, tools
**Confidence:** 0.95

To reference this later: "memory:mem-2026-02-10-001"
```

### 10.2 Retrieving Information

```
User: What do you know about my coding preferences?

Assistant: ## Found 3 Relevant Memories

### 1. Prefers pytest for Python testing (relevance: 0.95)
- **Confidence:** 0.95
- **Tags:** python, testing, tools
- **Created:** 2026-02-10

User prefers pytest over unittest for Python testing.
Values pytest's fixture system and readable assertions.

### 2. Likes dark mode for coding (relevance: 0.82)
- **Confidence:** 0.90
- **Tags:** editor, ui, preferences
- **Created:** 2026-02-08

User prefers dark theme in code editors.
Reduces eye strain during long sessions.

### 3. Prefers TypeScript for large projects (relevance: 0.75)
- **Confidence:** 0.85
- **Tags:** typescript, javascript, project-size
- **Created:** 2026-02-05

User prefers TypeScript for projects over 1000 lines.
Cites type safety and maintainability.
```

### 10.3 Switching Personality

```
User: Switch to TECHNICAL_COPILOT mode

Assistant: ✓ Personality changed to TECHNICAL_COPILOT

**Activated:** TECHNICAL_COPILOT
**Description:** Optimized for code and technical tasks

Slider adjustments:
- Technicality: 85 (↑35)
- Directness: 80 (↑30)
- Creativity: 30 (↓35)
- Patience: 50 (↓5)

Ready for technical work. Ask me about code, debugging,
or technical concepts.
```

### 10.4 Querying Memories

```
User: Find all memories with tag python

Assistant: ## Query Results: tag:python

Found 5 memories tagged "python":

| Title | Type | Confidence | Created |
|-------|------|------------|---------|
| Prefers pytest for testing | preference | 0.95 | 2026-02-10 |
| Uses VS Code for editing | preference | 0.90 | 2026-02-09 |
| Django project context | note | 0.85 | 2026-02-08 |
| Virtual environment pattern | pattern | 0.80 | 2026-02-07 |
| FastAPI preference | preference | 0.88 | 2026-02-06 |

To view a memory: "Show me memory [id]"
To search within results: "Search within python memories for [query]"
```
