# GitHub commands

```bash
export REPO=owner/name
export GH_PROJECT="Venture board"
export AGENTIC_SCRUM_HOME="$HOME/work/dev/agentic-scrum-development"
gh auth refresh -s project   # once, if project scope is missing
```

One-time UI: **ONCE.md**.

```bash
python3 "$AGENTIC_SCRUM_HOME/scripts/workitems.py" setup-project --title "Venture board"
python3 "$AGENTIC_SCRUM_HOME/scripts/install_agent_config.py" --clone /path/to/repo
python3 "$AGENTIC_SCRUM_HOME/scripts/workitems.py" create Epic "Title" ./body.md
python3 "$AGENTIC_SCRUM_HOME/scripts/workitems.py" create Story "Title" ./body.md --parent 12
python3 "$AGENTIC_SCRUM_HOME/scripts/workitems.py" create Bug "Title" ./body.md
gh issue create --repo "$REPO" --type Epic --title "…" --body-file ./body.md --project "$GH_PROJECT"
gh project mark-template N --owner OWNER
gh issue develop 35 --repo "$REPO" --checkout --base main
gh pr create --repo "$REPO" --base main --title "..." --body "Closes #35"
```
