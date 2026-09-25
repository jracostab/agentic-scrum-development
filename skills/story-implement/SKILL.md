---
name: agentic-scrum-story-implement
description: Take one GitHub story or bug, write a plan or RCA, wait for Founder approval, then implement and open a PR. Never merge.
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [scrum, github, implementation]
    related_skills: [agentic-scrum, agentic-scrum-work-items, agentic-scrum-developer]
---

# Story / bug implement

Requires a bound role (`scrum_bindings.py check --skill agentic-scrum-story-implement`). Usually used with `agentic-scrum-developer`.

Read `references/POLICIES/coding-policy.md`.
Stories: `references/FLOWS/04-story-development.md`.
Bugs: `references/FLOWS/05-bug-fixing.md`.

```bash
export REPO AGENTIC_SCRUM_HOME
N=35
python3 "$AGENTIC_SCRUM_HOME/scripts/workitems.py" get "$N"
```

If `type:bug` → RCA comment, STOP.
Else → plan comment, STOP.

After Founder `approved|proceed|handle`:

```bash
gh issue develop "$N" --repo "$REPO" --checkout --base main
# implement + tests
gh pr create --repo "$REPO" --base main --title "..." --body "Closes #$N"
```

Never merge. Never a second issue on the same branch.
