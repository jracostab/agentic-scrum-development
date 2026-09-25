---
name: agentic-scrum-sprint
description: Propose a sprint from ready stories; apply sprint labels only after the Founder says sprint yes.
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [scrum, sprint]
    related_skills: [agentic-scrum, agentic-scrum-work-items, agentic-scrum-tech-lead, agentic-scrum-po]
---

# Sprint

Requires any bound Scrum role (`scrum_bindings.py check --skill agentic-scrum-sprint`).

1. List open `type:story` with DoD.
2. Propose 1–3 stories (one Developer agent + Founder review).
3. Stop until `sprint yes` or `approved`.
4. Then:

```bash
export REPO AGENTIC_SCRUM_HOME
python3 "$AGENTIC_SCRUM_HOME/scripts/workitems.py" sprint sprint:2026-w39 41 42
```

5. Comment each story: `Sprint sprint:YYYY-wNN committed.`

Do not `/implement` unless the Founder asked to start development.
Read `references/FLOWS/03-sprint-planning.md`.
