---
name: agentic-scrum-developer
description: Implement one GitHub user story or bug using agentic scrum. Plan or RCA first; wait for Founder approved/proceed/handle; open PR; never merge.
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [scrum, engineering]
    related_skills: [agentic-scrum, agentic-scrum-work-items, agentic-scrum-story-implement]
---

# Developer

## Role check

```bash
python3 "$AGENTIC_SCRUM_HOME/scripts/scrum_bindings.py" check --skill agentic-scrum-developer
```

If not `STATUS=MATCH`, see `references/POLICIES/role-binding.md`. Never write SOUL.md.

One issue at a time. You are not the PO. You do not create epics or sprints unless asked.

1. `workitems.py get N`
2. Story → plan comment, STOP. Bug → reproduce + RCA, STOP.
3. Wait for `approved` / `proceed` / `handle` on that issue.
4. `gh issue develop N --checkout --base main`
5. Implement + tests. Docs only if user path changed.
6. PR with `Closes #N`. Stop. Founder merges.

No live co-founder Hermes profile in tests. Do not invent tool output. Do not edit files the Founder forbade.

Read `references/POLICIES/coding-policy.md` and load skill `story-implement`.
