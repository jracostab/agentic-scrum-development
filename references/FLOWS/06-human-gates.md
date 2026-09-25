# Flow 6 — Human gates (cheat sheet)

You (Founder) type these on the GitHub issue or in chat to the agent.

| You type | Meaning |
|----------|---------|
| `approved` | Pass current gate (G1/G2/G3) |
| `proceed` / `handle` | Pass G3 for this issue; start implementation |
| `sprint yes` | Pass G2 |
| `send back` | Gate failed; agent revises plan/RCA, still no code |
| `/plan` | Developer/PO: write plan comment only |
| `/rca` | Developer: RCA comment only |
| `/implement` | Assign Developer; still stop for G3 unless already approved |
| `/assign @tech-lead` | tech-lead (CTO, DE, or PE) should decompose |

Merge on GitHub = G4. Agents never merge.
