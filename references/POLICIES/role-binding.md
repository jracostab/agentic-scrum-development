# Team role vs Scrum hats

Skills are add-ons. They never write `agent/SOUL.md`, `AGENTS.md`, or `MEMORY_SEEDS.md`.

## Two layers

**Team role** (who you are): `co-founder`, `ceo`, `cto`, `distinguished-engineer`, `principal-engineer`.
From optional `$COFOUNDER_ROOT/agent/config/role.txt`, else the sidecar `team_role:`.

**Scrum hats** (what process you may run), list on the sidecar:

| Hat | Skill |
|-----|--------|
| product-owner | agentic-scrum-po |
| developer | agentic-scrum-developer |
| tech-lead | agentic-scrum-tech-lead (split features / draft sprints) |

CEO skill checks team role `ceo`, not a hat.
Tool skills (work-items, sprint, story-implement) need any hat already bound.

See `references/POLICIES/tech-lead.md` for tech-lead duties.

## Defaults when you bind a team role

| Team role | Hats you get unless you change them |
|-----------|--------------------------------------|
| co-founder | product-owner |
| cto | tech-lead |
| distinguished-engineer, principal-engineer | tech-lead + developer |
| ceo | none |

Add a hat without dropping others: `bind hat product-owner`.

## Lookup

1. `role.txt` in the clone (team role only, optional)
2. Sidecar: Hermes `~/.hermes/profiles/<profile>/scrum-bindings.yaml` or Claude `~/.claude/agentic-scrum-bindings.yaml`

## Agent procedure

```bash
python3 "$AGENTIC_SCRUM_HOME/scripts/scrum_bindings.py" check --skill <skill>
```

MATCH → continue. UNSET/MISMATCH → ask the Founder. Do not edit persona files.

| Founder types | Command |
|---------------|---------|
| `bind co-founder` (or cto / ceo / distinguished-engineer / principal-engineer) | `bind --team-role … --skill …` (applies default hats) |
| `bind hat product-owner` (or developer / tech-lead) | `bind --hat … --skill …` (adds hat) |
| `session tech-lead` | This chat only; no write |
| `stop` | Stop |

## Sidecar example

```yaml
team_role: principal-engineer
hats:
  - developer
  - tech-lead
  - product-owner
skills:
  - agentic-scrum-developer
  - agentic-scrum-tech-lead
  - agentic-scrum-po
```
