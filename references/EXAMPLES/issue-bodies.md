# Copy-paste examples

## Epic draft (chat, before G1)

```markdown
## Description
Founders can run a co-founder clone on a blank Linux host with only Python 3.11+, git, and Hermes.

## Definition of Done
- [ ] README lists Linux/macOS/Windows prerequisites
- [ ] First `./start.sh` creates .venv without preinstalled pydantic
```

## Story body (after G2)

```markdown
Parent: #40

## Description
As a founder, I want `./start.sh --help` on a fresh clone so I know flags before bootstrap.

## Definition of Done
- [ ] `./start.sh --help` exits 0
- [ ] pytest covers the help path
```

## Founder on the issue

```
approved
```

```
/implement
```

```
sprint yes
```

## Developer plan

```markdown
## Plan
- Files: start.sh (unchanged shim), tests/test_cofounder.py
- Tests: test_cli_start_help
- Docs: none
Waiting for G3.
```

## Developer RCA

```markdown
## Root cause
`hermes gateway install` prompts on TTY while stdout is captured; 120s TimeoutExpired is uncaught.

## Not the cause
venv, Obsidian vault name.

## Proposed fix
install --start-now --start-on-login, stdin=DEVNULL, map timeout to CofounderError.
Waiting for G3.
```

## You to Developer (Claude Code)

```
Take GitHub issue #41. REPO=jracostab/ai-co-founder-workspace.
Follow $HOME/workspace/agentic-scrum-development/AGENTS/developer/AGENTS.md
and SKILLS/story-implement. Stop after the plan comment.
```
