# AGENTS.md — Developer

Load POLICIES/sdlc-policy.md, approval-policy.md, coding-policy.md, github-policy.md.
Skills: work-items + story-implement.
Flows: FLOWS/04-story-development.md and FLOWS/05-bug-fixing.md.

## Take a ticket

```text
1. workitems.sh get N
2. If type:story → plan comment, STOP
   If type:bug → reproduce, RCA comment, STOP
3. Wait until issue comments contain approved|proceed|handle
4. gh issue develop N --checkout --base main
5. Implement + tests
6. gh pr create ... Closes #N
7. Stop. Founder merges.
```

## Plan comment shape

```markdown
## Plan
- Files: ...
- Tests: ...
- Docs: ... (or none)
Waiting for G3.
```

## RCA comment shape

```markdown
## Root cause
...
## Not the cause
...
## Proposed fix
...
Waiting for G3.
```
