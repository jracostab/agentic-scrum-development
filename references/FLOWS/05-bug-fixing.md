# Flow 5 — Bug fixing

Board: Open Defects. Ready → In progress → In review → Done.

Actors: Founder (A), Developer (R), PO (priority), tech-lead (CTO, DE, or PE) (C on RCA if asked).

1. Founder files `type:bug` with steps, symptoms, expected, DoD. Card Ready.
2. Founder or PO comments `/rca` or `/implement`.
3. Developer reproduces. Comments **root cause**, what it is not, proposed fix. No code.
4. Gate G3: Founder `approved`.
5. Card In progress. Branch from current main.
6. Fix the cause. Regression test that would have failed.
7. PR `Closes #N`. Card In review.
8. Gate G4: Founder merges. Card Done.

TODOs on the bug issue: new RCA mini-loop on the same ticket; mark COMPLETED when fixed.

A bug found mid-story: new bug issue unless Founder says ride this PR.
