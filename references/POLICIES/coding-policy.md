# Coding policy (Developer)

Follow the story flow or bug flow in FLOWS/. Never mix them.

## Before code

- Story: plan on the issue (files, CLI, docs, tests). Stop.
- Bug: reproduce, RCA on the issue (cause, not-cause, proposed fix). Stop.
- Wait for Founder `approved` / `proceed` / `handle`.

## During code

- Branch: `gh issue develop N --checkout --base main`
- Implement only this issue.
- Tests for the new behavior or the regression.
- Docs only if the user path or prerequisites changed. Do not edit files the Founder forbade.
- Unique Hermes test profile. Never live `co-founder` / production profile.

## After code

- PR with what changed, tests, DoD, `Closes #N`.
- Story: Task Board In Progress until merge (board has no In review).
- Bug: Open Defects → In review while PR is open.
- Do not merge.

## Blockers

If a tool fails, say so. Do not invent command output.
