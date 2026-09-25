# tech-lead (Scrum hat)

`tech-lead` is a **Scrum hat**, not a job title. Team titles stay Co-Founder, CTO, Distinguished Engineer (DE), Principal Engineer (PE).

## Who wears it

Default hats when you `bind` that team role:

| Team role | Default hats |
|-----------|----------------|
| cto | **tech-lead** only |
| distinguished-engineer | **tech-lead**, developer |
| principal-engineer | **tech-lead**, developer |
| co-founder | product-owner only (no tech-lead unless you add it) |
| ceo | none |

DE, PE, and CTO are responsible for splitting features and drafting sprints. That work is the tech-lead hat.

They can also add `product-owner` (`bind hat product-owner`) when they own a product slice. They keep their title.

## What the hat is allowed to do

Skill: `agentic-scrum-tech-lead` (required hat `tech-lead`).

- Decompose an epic into features, then features into stories with **testable** Definition of Done.
- Draft a sprint with the Product Owner. Wait for Founder `sprint yes` (G2).
- Comment story lists on the feature issue. Create GitHub issues only after `approved`.
- Use `agentic-scrum-sprint` after G2.

## What it must not do

- Merge to main.
- Implement a story unless the agent also has the **developer** hat (CTO/DE/PE have that by default).
- Replace the Product Owner: backlog priority and G1 epics stay `product-owner` unless this agent also has that hat.
- Rewrite `SOUL.md`.

## Dual-hat example (PE who is also PO)

```yaml
team_role: principal-engineer
hats:
  - developer
  - tech-lead
  - product-owner
```

This agent may load `agentic-scrum-developer`, `agentic-scrum-tech-lead`, and `agentic-scrum-po` without a prompt.
