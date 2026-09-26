---
name: agentic-scrum-work-items
description: Create and comment on GitHub Issues using issue types and one Project (Roadmap, Sprint, Defects). Use when filing epics, features, stories, or bugs.
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, issues, scrum]
    related_skills: [agentic-scrum, agentic-scrum-po]
---

# Work items

Before create/comment: `scrum_bindings.py check --skill agentic-scrum-work-items`.

Use GitHub issue **types** and **sub-issues**. One Project (`GH_PROJECT`). See `GITHUB/ONCE.md`.

```bash
export REPO="${REPO:?owner/name}"
export GH_PROJECT="${GH_PROJECT:-Venture board}"
export AGENTIC_SCRUM_HOME="${AGENTIC_SCRUM_HOME:-$HOME/workspace/agentic-scrum-development}"
WI="python3 $AGENTIC_SCRUM_HOME/scripts/workitems.py"

$WI create Epic "Title" ./body.md
$WI create Feature "Title" ./body.md --parent 12
$WI create Story "Title" ./body.md --parent 20
$WI create Bug "Title" ./body.md
$WI comment 35 ./comment.md
```

Rules:
- Body always has `## Description`, `## Definition of Done`, and `## Acceptance Criteria`.
- Bugs also have Steps, Symptoms, Expected.
- Parent = `--parent N` (GitHub sub-issue).
- Do not create issues until the matching Founder gate passed.
- Do not add `type:` or `sprint:` labels.
- If `gh` is missing, stop.

Never `shell=True` with user text. Argv only.
