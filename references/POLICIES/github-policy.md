# GitHub policy (adapter)

Use `gh` and `scripts/workitems.py`. Never `shell=True`.

Happy path: GitHub **issue types**, **sub-issues**, **one Project**. Not `type:` / `sprint:` labels.

```bash
export REPO=owner/name
export GH_PROJECT="Venture board"

python3 "$AGENTIC_SCRUM_HOME/scripts/workitems.py" create Epic "Title" ./body.md
python3 "$AGENTIC_SCRUM_HOME/scripts/workitems.py" create Story "Title" ./body.md --parent 12
python3 "$AGENTIC_SCRUM_HOME/scripts/workitems.py" comment 35 ./comment.md
```

If the org has no Story type, create falls back to Task. If no Epic type, falls back to Feature.

One-time UI: `GITHUB/ONCE.md`.
Hats stay in `scrum-bindings.yaml`, not GitHub labels.
Assignee = who does the work.
