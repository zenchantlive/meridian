#!/bin/bash
# enforce-sequential-dispatch.sh
# Blocks dispatch if task has unresolved blockers

BEAD_ID="${1:-$BEAD_ID}"

if [[ -n "$BEAD_ID" ]]; then
    BLOCKERS=$(bd blocked 2>/dev/null | grep -A1 "$BEAD_ID" | grep "Blocked by" || true)
    if [[ -n "$BLOCKERS" ]]; then
        echo "ERROR: $BEAD_ID has unresolved dependencies"
        echo "$BLOCKERS"
        echo "Run 'bd ready' to find unblocked tasks"
        exit 1
    fi
fi
