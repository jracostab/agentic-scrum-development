# Flow 4 — User story development (task)

Board: Task Board. Todo → In Progress → Done.

Actors: Founder (A), Developer (R), tech-lead (CTO, DE, or PE) (C if architecture).

1. Founder or PO labels story `role:developer` `status:ready-for-dev` and comments `/implement`.
2. Developer: `gh issue view N`. Confirm type:story, DoD exists.
3. Developer comments a **plan** (files, CLI, docs, tests). No branch yet.
4. Gate G3: Founder `approved` / `proceed` / `handle`.
5. Card In Progress. `gh issue develop N --checkout --base main`.
6. Implement + tests + docs if user path changed.
7. PR: what changed, tests, DoD, `Closes #N`.
8. Gate G4: Founder reviews and merges. Card Done.

Developer stops at step 3 until G3.
