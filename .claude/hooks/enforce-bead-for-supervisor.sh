#!/bin/bash
# enforce-bead-for-supervisor.sh
# Requires BEAD_ID for all supervisor dispatches

if [[ "$CLAUDE_ROLE" == "supervisor" && -z "$BEAD_ID" ]]; then
    echo "ERROR: Supervisors must have BEAD_ID set"
    echo "Use: bd worktree create <bead-id> or set BEAD_ID manually"
    exit 1
fi
