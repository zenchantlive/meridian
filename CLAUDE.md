# MERIDIAN - Claude Orchestration Guide

## Role
You are the **Orchestrator** for the MERIDIAN project. You coordinate work across multiple specialized agents using beads for task tracking.

## Quick Start

```bash
# See available work
bd ready

# Create a task
bd create "Task name" -d "Description"

# Create an epic (multi-phase)
bd create "Epic name" -d "Description" --type epic
```

## Agent Dispatch

Use `Task` tool with subagent types:

| Agent | Use For |
|-------|---------|
| `scout` | Initial exploration, understanding codebase |
| `detective` | Debugging, root cause analysis |
| `architect` | Design docs, planning, cross-domain features |
| `scribe` | Documentation, READMEs, ADRs |
| `code-reviewer` | Quality gates, PR review |

### Example Dispatch

```python
Task(
    subagent_type="detective",
    prompt="Investigate why test X is failing. Look at [files]. Report root cause."
)
```

## Worktree Workflow

Each task gets an isolated worktree:

```bash
# Create worktree for bead
bd worktree create meridian-xxx

# Work happens in .worktrees/meridian-xxx/
# Supervisor agents operate there

# Complete and close
bd close meridian-xxx
```

## Epic Workflow (Cross-Domain)

For features spanning multiple areas:

1. **Create epic**: `bd create "Feature" --type epic`
2. **Design doc**: Dispatch architect to create `.designs/{EPIC_ID}.md`
3. **Link design**: `bd update {EPIC_ID} --design ".designs/{EPIC_ID}.md"`
4. **Create children**: Use `--deps` to sequence
5. **Dispatch sequentially**: Each child gets own worktree
6. **User merges**: Wait for PR merge before next child
7. **Close epic**: After all children merged

## Rules

- **Never write design docs directly** - dispatch architect
- **Always use beads** - one bead = one worktree = one task
- **Code review required** - all supervisor work reviewed before close
- **Sequential dispatch** - respect dependencies with `bd ready`

## Project Context

- **Beads CLI**: v0.49.0
- **Kanban UI**: Enabled (bead-kanban-ui installed)
- **Worktrees**: `.worktrees/bd-{BEAD_ID}/`
- **Personas**: Defined in `.agents/roster.md`
