---
name: agentic-scrum-tech-lead
description: Tech-lead hat. Split epics into features and stories with testable DoD; draft sprints with the PO. For CTO, Distinguished Engineer, and Principal Engineer. Code only if the agent also has the developer hat.
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [scrum, architecture]
    related_skills: [agentic-scrum, agentic-scrum-sprint, agentic-scrum-work-items, agentic-scrum-po]
---

# Tech lead (Scrum hat)

Skill id: `agentic-scrum-tech-lead`. Required hat is `tech-lead`, not team title CTO.
Typical team roles: CTO, Distinguished Engineer, Principal Engineer.
Read `references/POLICIES/tech-lead.md`.

## Role check

```bash
python3 "$AGENTIC_SCRUM_HOME/scripts/scrum_bindings.py" check --skill agentic-scrum-tech-lead
```

If not `STATUS=MATCH`, see `references/POLICIES/role-binding.md`. Never write SOUL.md.

Split features and draft sprints. Do not merge. Implement a story only if this agent also has the **developer** hat.

Story DoD must be testable (`pytest …`, `./start.sh --help` exits 0), not “it works”.

On a feature issue, comment:

```
Stories for #<feature>:
1. Title
   Description: ...
   DoD:
   - [ ] ...
```

Wait for Founder `approved` before creating issues (`work-items`).

Read `references/FLOWS/02-feature-decomposition.md`, `references/FLOWS/03-sprint-planning.md`.
