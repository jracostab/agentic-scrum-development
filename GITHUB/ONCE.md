# GitHub setup (least friction)

One command does the former “click through GitHub” work:

```bash
export REPO=owner/name
export GH_PROJECT="Venture board"
export AGENTIC_SCRUM_HOME="$HOME/workspace/agentic-scrum-development"
gh auth refresh -s project   # once if gh lacks project scope

python3 "$AGENTIC_SCRUM_HOME/scripts/setup_github.py" \
  --repo "$REPO" \
  --title "$GH_PROJECT" \
  --clone /path/to/your/repo
```

It will:
- Create issue types **Epic** and **Story** (organization owners only)
- Create or reuse the Project, link the repo
- Add **Iteration** (14-day) when the API allows
- Create views **Roadmap** (Epic), **Sprint** (board), **Defects** (Bug)
- Mark as template when the owner is an organization
- Copy `.github/ISSUE_TEMPLATE/*.yml` into `--clone`

Re-running reuses a project with the same title (does not duplicate).

Then commit `.github/` yourself.

## Personal GitHub account

No issue types. The script uses **labels** `Epic`, `Feature`, `Story`, `Bug` (not an error). Views:

- Roadmap → `label:Epic`
- Sprint → `-label:Epic` (iteration board without epics)
- Defects → `label:Bug`

`workitems.py create Epic|Story|Bug` applies those labels (no `--type`).

## Still manual

The script prints **Still manual**. Typical:
- Commit the copied issue templates
- If Iteration API failed: Project → add Iteration
- If a view filter did not stick: set Type = Epic / Bug on that view

You should not create a second project or `type:` labels.
