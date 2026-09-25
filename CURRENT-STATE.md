# Current state

Where the work lives
Everything is in `/home/jracosta/work/dev/agentic-scrum-development`. The Co-Founder clone (`ai-co-founder-workspace`) was not changed. Your GitHub org/repo was not changed either — the new setup script exists but has **not** been run against your live GitHub.

What we decided
Scrum on GitHub should look like GitHub, not like extra labels.

- One Project per venture
- Three views: Roadmap (epics), Sprint (current iteration), Defects (bugs)
- Issue types: Epic, Feature, Story, Bug
- Stories hang off epics as sub-issues
- Hats (PO / developer / tech-lead) stay in the sidecar file, not as GitHub labels

---

What is already automated (code in the pack)

1. Skills for Hermes and Claude Code  
   `install_skills.py` — already run on this machine (symlinks under `~/.hermes/skills` and `~/.claude/skills`). Restart those apps so they see the skills.

2. Role binding  
   First time a skill loads, you type `bind co-founder` (or PE, etc.). That writes `scrum-bindings.yaml` next to the agent. Not in git. Not SOUL.md.

3. Filing issues (after GitHub is set up)  
   `workitems.py create Epic|Story|Bug …` uses GitHub types, `--parent` for sub-issues, `--project` for the board. If Story/Epic types do not exist, it falls back to Task/Feature.

4. One-shot GitHub setup script (written, not executed on your account)  
   `scripts/setup_github.py` is meant to replace most of the old “click ONCE.md” list. When **you** run it, it will try to:
   - create issue types Epic and Story (only if the owner is an **organization**)
   - create or reuse a Project named e.g. Venture board
   - link that Project to the repo
   - add an Iteration field
   - create views Roadmap, Sprint, Defects
   - mark the Project as a template (org only)
   - copy issue form files into a clone folder

   Re-running should reuse the same Project title, not create a second one.

---

What is still manual (you or GitHub’s limits)

A. You must run the setup once (we did not run it for you)

```bash
export REPO=your-org-or-user/your-repo
export GH_PROJECT="Venture board"
gh auth refresh -s project    # if gh says it cannot touch Projects
python3 "$HOME/work/dev/agentic-scrum-development/scripts/setup_github.py" \
  --repo "$REPO" --title "$GH_PROJECT" \
  --clone /path/to/your/repo
```

B. After it finishes, you still:
- Commit `.github/ISSUE_TEMPLATE` in that clone (script never pushes)
- Read the printed **Still manual** lines — only if something failed (e.g. Iteration field or a view filter)

C. GitHub cannot do on a personal (non-org) account
- Create issue types Epic/Story. Then agents use Feature instead of Epic and Task instead of Story. Same Project. Views still work.

D. Day to day you still (by design, human in the loop)
- Type `approved` / `sprint yes` / merge PRs
- First bind of each agent (`bind principal-engineer`, etc.)

You do **not** need to invent `type:story` labels or a second Defects project.

---

Suggested next action
When you want GitHub wired for real, run the command in A on the repo you care about, then paste the script output here if any “Still manual” lines appear. Until then, skills and hats work; filing typed issues waits on that one run.
