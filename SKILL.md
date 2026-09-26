---
name: agentic-scrum
description: Human-in-the-loop Scrum for AI agent teams. Product backlog, features, sprints, story implementation, and bug RCA with GitHub Issues. Use when planning work, assigning a story, or enforcing G1–G4 approval gates.
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [scrum, github, sdlc, product, agents]
    related_skills:
      - agentic-scrum-work-items
      - agentic-scrum-sprint
      - agentic-scrum-story-implement
      - agentic-scrum-po
      - agentic-scrum-tech-lead
      - agentic-scrum-developer
      - agentic-scrum-ceo
---

# Agentic Scrum

Human Founder is the only approver (G1–G4). GitHub Issues are the system of record. This pack is one skill bundle for **Hermes** and **Claude Code**.

## Pack root

`$AGENTIC_SCRUM_HOME` or the directory that contains `scripts/workitems.py` (this repo).

```bash
export AGENTIC_SCRUM_HOME="${AGENTIC_SCRUM_HOME:-$HOME/workspace/agentic-scrum-development}"
export REPO="${REPO:?set owner/name}"
```

## Role check (do this first)

Scrum is an add-on. Do not edit `agent/SOUL.md`.

```bash
python3 "$AGENTIC_SCRUM_HOME/scripts/scrum_bindings.py" check --skill <skill-name>
```

`STATUS=MATCH` → continue. Otherwise follow `references/POLICIES/role-binding.md` (ask `bind` / `session` / `stop`).

Persona, ventures, and memory still come from the clone (`agent/SOUL.md`, `agent/AGENTS.md`, `venture` skill).

## Pick a role skill

| Ask | Skill |
|-----|--------|
| Product / epics / backlog | `agentic-scrum-po` |
| Features, stories, sprint draft | `agentic-scrum-tech-lead` + `agentic-scrum-sprint` |
| Strategy only | `agentic-scrum-ceo` |
| Implement story or bug | `agentic-scrum-developer` + `agentic-scrum-story-implement` |
| Create/comment/label issues | `agentic-scrum-work-items` |

## Gates (never skip)

| Gate | Needed before | Founder types |
|------|---------------|----------------|
| G1 | Creating epics | `approved` |
| G2 | Sprint commit | `sprint yes` |
| G3 | Branch / code | `approved` / `proceed` / `handle` |
| G4 | Land on main | GitHub merge (human) |

Task/story: **plan comment**, then stop. Bug: **RCA comment**, then stop. Code only after G3.

## Shared references (read, do not invent process)

- `references/FLOWS/` — 01 product through 06 gates
- `references/POLICIES/` — sdlc, approval, github, coding
- `references/ROLES.md` — RACI

## Scripts

```bash
"$AGENTIC_SCRUM_HOME/scripts/enable_automation.sh"
python3 "$AGENTIC_SCRUM_HOME/scripts/workitems.py" get 35
python3 "$AGENTIC_SCRUM_HOME/scripts/install_skills.py" --hermes --claude
```
