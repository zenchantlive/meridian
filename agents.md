\# Agent Instructions



This project uses \*\*bd\*\* (beads) for issue tracking and a \*\*Religious Memory System\*\* in `/memory` for persistent context.



\## 🧠 Memory System Protocol (MANDATORY)



You MUST treat the `/memory` directory as your primary source of truth. 



\### 1. Session Start

Before doing any work, you MUST read:

1\. `memory/project\_brief.md`: The core mission and tech stack.

2\. `memory/active\_state.md`: Exactly where we left off.

3\. `memory/system\_patterns.md`: Technical standards and "gotchas."

4\. `memory/adr/`: Recent architectural decisions.



\### 2. During Work

\- \*\*Architectural Change?\*\* → You MUST create a new ADR in `memory/adr/`.

\- \*\*New Learning?\*\* → Update `memory/system\_patterns.md` if you find a new "gotcha."

\- \*\*Milestone Reached?\*\* → Update `memory/active\_state.md` as you go.



\### 3. Session Conclusion

Before ending, you MUST:

1\. Update `memory/active\_state.md`: Mark completed work and define "Next Actions."

2\. Verify all technical decisions made are documented in an ADR.



---



\## Quick Reference



```bash

bd ready              # Find available work

bd show <id>          # View issue details

bd update <id> --status in\_progress  # Claim work

bd close <id>         # Complete work

bd sync --flush-only  # Sync with JSONL

```



\## Landing the Plane (Session Completion)



\*\*When ending a work session\*\*, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.



\*\*MANDATORY WORKFLOW:\*\*



1\. \*\*File issues for remaining work\*\* - Create issues for anything that needs follow-up

2\. \*\*Run quality gates\*\* (if code changed) - Tests, linters, builds

3\. \*\*Update issue status\*\* - Close finished work, update in-progress items

4\. \*\*PUSH TO REMOTE\*\* - This is MANDATORY:

&nbsp;  ```bash

&nbsp;  git pull --rebase

&nbsp;  bd sync

&nbsp;  git push

&nbsp;  git status  # MUST show "up to date with origin"

&nbsp;  ```

5\. \*\*Clean up\*\* - Clear stashes, prune remote branches

6\. \*\*Verify\*\* - All changes committed AND pushed

7\. \*\*Hand off\*\* - Provide context for next session



\*\*CRITICAL RULES:\*\*

\- Work is NOT complete until `git push` succeeds

\- NEVER stop before pushing - that leaves work stranded locally

\- NEVER say "ready to push when you are" - YOU must push

\- If push fails, resolve and retry until it succeeds





<!-- bv-agent-instructions-v1 -->



---



\## Beads Workflow Integration



This project uses \[beads\_viewer](https://github.com/Dicklesworthstone/beads\_viewer) for issue tracking. Issues are stored in `.beads/` and tracked in git.



\### Essential Commands



```bash

\# View issues (launches TUI - avoid in automated sessions)

bv



\# CLI commands for agents (use these instead)

bd ready              # Show issues ready to work (no blockers)

bd list --status=open # All open issues

bd show <id>          # Full issue details with dependencies

bd create --title="..." --type=task --priority=2

bd update <id> --status=in\_progress

bd close <id> --reason="Completed"

bd close <id1> <id2>  # Close multiple issues at once

bd sync               # Commit and push changes

```



\### Workflow Pattern



1\. \*\*Start\*\*: Run `bd ready` to find actionable work

2\. \*\*Claim\*\*: Use `bd update <id> --status=in\_progress`

3\. \*\*Work\*\*: Implement the task

4\. \*\*Complete\*\*: Use `bd close <id>`

5\. \*\*Sync\*\*: Always run `bd sync` at session end



\### Key Concepts



\- \*\*Dependencies\*\*: Issues can block other issues. `bd ready` shows only unblocked work.

\- \*\*Priority\*\*: P0=critical, P1=high, P2=medium, P3=low, P4=backlog (use numbers, not words)

\- \*\*Types\*\*: task, bug, feature, epic, question, docs

\- \*\*Blocking\*\*: `bd dep add <issue> <depends-on>` to add dependencies



\### Session Protocol



\*\*Before ending any session, run this checklist:\*\*



```bash

git status              # Check what changed

git add <files>         # Stage code changes

bd sync                 # Commit beads changes

git commit -m "..."     # Commit code

bd sync                 # Commit any new beads changes

git push                # Push to remote

```



\### Best Practices



\- Check `bd ready` at session start to find available work

\- Update status as you work (in\_progress → closed)

\- Create new issues with `bd create` when you discover tasks

\- Use descriptive titles and set appropriate priority/type

\- Always `bd sync` before ending session



<!-- end-bv-agent-instructions -->



