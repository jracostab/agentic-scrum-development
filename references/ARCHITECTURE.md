# Architecture

## Loop

```
Founder ⟷ Co-Founder (PO)
              ↓ product backlog (epics)
Founder ⟷ Co-Founder + CTO
              ↓ features → user stories → sprint
Founder ⟷ Developer
              ↓ one story or bug
         GitHub Issue → plan/RCA comment → approve
         → branch → implement + tests → PR → merge
```

Nothing starts from chat-only. The Issue is the system of record.

## Work-item model (tool-agnostic)

```
WorkItem
  id            # GitHub number today
  type          # epic | feature | story | bug
  title
  body          # Description + DoD (required)
  parent_id     # feature→epic, story→feature
  sprint        # label sprint:YYYY-WNN or milestone
  board         # product | task | defects
  status        # see boards
  assignee_role # founder | po | cto | developer
  labels[]
  url
```

GitHub mapping (v0):

| Field | GitHub |
|-------|--------|
| id | issue number |
| type | label `type:epic` `type:feature` `type:story` `type:bug` |
| parent | issue form field + comment `Parent: #N` |
| sprint | label `sprint:2026-w39` or milestone |
| role | label `role:developer` etc. |
| board | Project v2 (see GITHUB/project-setup.md) |

Swap later: implement the same verbs in `scripts/workitems.sh` (or a Python adapter) for Linear/Jira: `create`, `comment`, `label`, `status`.

## Agent homes

| Role | Now | Later |
|------|-----|--------|
| Co-Founder | Hermes profile (existing clone) | same |
| CEO | Claude Code agent + AGENTS/ceo | Hermes profile or skill |
| CTO | Claude Code agent + AGENTS/cto | Hermes profile |
| Developer | Claude Code agent + AGENTS/developer | Hermes, or Hermes skill that calls Claude Code |

Each role loads: SOUL.md (identity) + AGENTS.md (operating rules) + POLICIES/* + the skills it needs.

## Trigger model (2-day)

Do not wait on a custom orchestrator.

1. Founder or PO comments a slash command on the issue (`TRIGGERS/comment-commands.md`).
2. The owning agent is invoked in chat: “Take issue #N” and must use the work-items skill (gh).
3. Optional: GitHub Action on comment `/implement` posts a checklist (does not run the agent yet).

Auto-dev later: Hermes cron or gateway watches labeled issues `status:ready-for-dev`.

## Human gates (cannot be skipped)

| Gate | Who | On |
|------|-----|-----|
| G1 Product / epic | Founder | issue comment `approved` |
| G2 Feature split + sprint | Founder | sprint issue or comment |
| G3 Story plan or bug RCA | Founder | `approved` / `proceed` |
| G4 PR merge | Founder | GitHub merge |
