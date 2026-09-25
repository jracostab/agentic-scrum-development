# SDLC policy (paste into every agent AGENTS.md)

You work in an agentic scrum with a human Founder. GitHub Issues are the system of record.

## Issue types

- `type:epic` — product outcome. Product backlog.
- `type:feature` — slice of an epic. Feature backlog.
- `type:story` — implementable. Task Board. Use the **story/task flow**.
- `type:bug` — defect. Open Defects. Use the **bug flow**.

Every issue must have Description and Definition of Done. Stories and bugs without DoD are not ready.

## One item, one change

- One issue → one branch from `main` (`gh issue develop`) → one PR `Closes #N`.
- Do not implement a second issue on the same branch unless the Founder says to ride the current PR.
- Do not use the live co-founder Hermes profile for tests.

## Task vs bug

- Task/story: plan comment first. Then code.
- Bug: reproduce + root-cause comment first. Then code.
- Founder approval is G3. Words that count: `approved`, `proceed`, `handle`. Not “looks interesting”.

## Quality

- Tests are in scope of the issue.
- Python: pytest coverage ≥90%, ruff, pylint, mypy when that package exists.
- Stdout: prompts, errors, ready. Internals → profile log.
- No secrets, no `.env.local` in git.

## Boards

- Task Board: Todo → In Progress → Done.
- Open Defects: Ready → In progress → In review → Done.
