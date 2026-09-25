# Approval policy

The human Founder is the only person who can pass a gate.

| Gate | Needed before | Founder signal |
|------|---------------|----------------|
| G1 | Creating epics in GitHub (after a draft) | `approved` on the draft, or `create the issues` |
| G2 | Sprint commitment | `sprint yes` / `approved` on the sprint comment |
| G3 | Any code, branch, or PR | `approved` / `proceed` / `handle` on plan or RCA |
| G4 | Land on main | GitHub merge (Founder) |

Agents must stop and wait at G1–G3. If the Founder said `proceed` or `handle` on that issue, treat G3 as passed for that issue only.

Do not infer approval from silence.
Do not merge to main.
Do not skip RCA on bugs to “save time”.
