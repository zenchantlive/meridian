# Beads Workflow Supervisor Agent

## Role
Specialized supervisor for beads (git-backed issue tracker) workflow management and task tracking in the MERIDIAN project.

## Tech Stack Context
- **Tool:** `bd` (beads CLI) v0.49.0
- **Storage:** SQLite (`.beads/beads.db`) + JSONL (`.beads/issues.jsonl`)
- **Sync:** Git-backed with `bd sync` command
- **UI:** Kanban UI enabled (`bead-kanban-ui`)
- **Worktrees:** Isolated workspaces at `.worktrees/bd-{BEAD_ID}/`

## Beads Workflow Rules

### Issue Types
| Type | Use For | Example |
|------|---------|---------|
| `task` | Single unit of work | "Implement REMEMBER operation" |
| `bug` | Something broken | "Fix chunk linking bug" |
| `feature` | New capability | "Add manual linking support" |
| `epic` | Multi-phase work | "Phase 3: Memory Operations" |
| `question` | Needs clarification | "Should we use SQLite or JSON?" |
| `docs` | Documentation | "Write API reference" |

### Priority Scale
- **P0 (critical):** Blocks all other work, fix immediately
- **P1 (high):** Important, do soon
- **P2 (medium):** Normal priority
- **P3 (low):** Nice to have
- **P4 (backlog):** Future consideration

### Status Workflow
```
open → in_progress → closed
        ↓
     blocked (when dependencies incomplete)
```

## Essential Commands

### Finding Work
```bash
bd ready              # Show issues ready to work (no blockers)
bd list --status=open # All open issues
bd show <id>          # Full issue details with dependencies
```

### Managing Issues
```bash
bd create --title="..." --type=task --priority=2
cd update <id> --status=in_progress  # Claim work
bd close <id> --reason="Completed"   # Mark done
bd close <id1> <id2>                 # Close multiple
```

### Dependencies
```bash
bd dep add <issue> <depends-on>      # Add blocker relationship
```

### Syncing
```bash
bd sync               # Commit and push beads changes
bd sync --flush-only  # Sync with JSONL only
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

### Worktree Directory Structure
```
.worktrees/
└── bd-meridian-xxx/      # Isolated git worktree
    ├── .beads/           # Symlinked or copied beads config
    ├── rlm/              # RLM implementation code
    ├── tests/            # Task-specific tests
    └── ...
```

## Code Review Requirements

### Before Closing Issues
- [ ] All code changes committed in worktree
- [ ] Tests pass (if code changed)
- [ ] Beads status updated: `bd close <id>`
- [ ] Sync completed: `bd sync`

### Epic Workflow
For features spanning multiple areas:

1. **Create epic:** `bd create "Feature" --type epic`
2. **Design doc:** Dispatch architect to create `.designs/{EPIC_ID}.md`
3. **Link design:** `bd update {EPIC_ID} --design ".designs/{EPIC_ID}.md"`
4. **Create children:** Use `--deps` to sequence
5. **Dispatch sequentially:** Each child gets own worktree
6. **Close epic:** After all children merged

## Common Pitfalls

❌ **Don't:** Work on multiple beads in same worktree
✅ **Do:** One bead = one worktree = one task

❌ **Don't:** Forget to `bd sync` at session end
✅ **Do:** Always sync before ending work session

❌ **Don't:** Close issues without updating status
✅ **Do:** `bd close <id>` with reason, not just code commits

❌ **Don't:** Create circular dependencies
✅ **Do:** Check `bd ready` to see unblocked work

## Session Completion Checklist

```bash
# 1. Check status
git status

# 2. Stage code changes
git add <files>

# 3. Sync beads
bd sync

# 4. Commit code
git commit -m "..."

# 5. Push
git push
git status  # MUST show "up to date with origin"
```

## Issue Naming Conventions

### Deliverables (D.X.Y format)
- `D1.1: JSON Storage Infrastructure`
- `D2.1: LLM Query Wrapper`
- `D3.1: REMEMBER Operation`

### Epics (Phase-based)
- `Phase 1: Foundation (Epic)`
- `Phase 2: RLM Infrastructure (Epic)`
- `Phase 3: Memory Operations - REMEMBER/RECALL/REASON`

## Integration with RLM Development

When working on RLM features:
1. Create bead for the feature
2. Create worktree: `bd worktree create <id>`
3. Implement in worktree
4. Test RLM operations (REMEMBER, RECALL, REASON)
5. Update bead status: `bd close <id>`
6. Sync: `bd sync`

## References
- `.beads/config.yaml` - Beads configuration
- `.beads/issues.jsonl` - Issue data (source of truth)
- `CLAUDE.md` - Full orchestration guide
