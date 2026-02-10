#!/bin/bash
# validate-completion.sh
# Verifies worktree, push, bead status before supervisor completes

BEAD_ID="${1:-$BEAD_ID}"

if [[ -z "$BEAD_ID" ]]; then
    echo "WARNING: No BEAD_ID set, skipping validation"
    exit 0
fi

# Check worktree exists
WORKTREE=".worktrees/$BEAD_ID"
if [[ ! -d "$WORKTREE" ]]; then
    echo "ERROR: Worktree $WORKTREE does not exist"
    exit 1
fi

# Check for uncommitted changes
cd "$WORKTREE" || exit 1
if [[ -n $(git status --porcelain) ]]; then
    echo "WARNING: Uncommitted changes in worktree"
    echo "Run: git add . && git commit -m '...'"
fi

# Check if pushed
if [[ -n $(git log origin/$(git branch --show-current)..HEAD 2>/dev/null) ]]; then
    echo "INFO: Commits not yet pushed"
fi

echo "Validation complete for $BEAD_ID"
