# RACI

R = does the work. A = accountable (one). C = consulted. I = informed.
H = human Founder always A on gates G1–G4.

| Work | Founder | Co-Founder (PO) | CEO | CTO | Developer |
|------|---------|-----------------|-----|-----|-----------|
| Product vision | A | R | C | I | I |
| Product backlog (epics) | A | R | C | C | I |
| Feature backlog | A | R | I | R | I |
| Story split + DoD | A | C | I | R | C |
| Sprint commit | A | R | I | R | I |
| Story plan (task flow) | A | I | I | C | R |
| Implement + tests + PR | A (merge) | I | I | C if architecture | R |
| Bug RCA | A | C (priority) | I | C | R |
| Bug fix | A (merge) | I | I | I | R |
| Release notes | C | R | C | C | I |

## Hard stops (Founder only)

- Spending, legal, public launch, equity (from co-founder SOUL).
- Merge to main.
- Skipping G3 (plan/RCA) unless Founder wrote `proceed` or `handle`.
