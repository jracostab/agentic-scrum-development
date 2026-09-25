# Agentic Scrum — user guide

This pack adds Scrum (backlog, sprints, stories, bugs) to agents you already have. It does **not** replace the Co-Founder persona in `ai-co-founder-workspace`. Personality, memory, and ventures stay in that clone. These skills are add-ons.

Location: `$HOME/work/dev/agentic-scrum-development`

Works with **Hermes Agent** and **Claude Code**.

---

## 1. What you need

- Python 3.11+
- Hermes and/or Claude Code
- `gh` only when you are ready to file GitHub issues (not required to bind a role)

```bash
export AGENTIC_SCRUM_HOME="$HOME/work/dev/agentic-scrum-development"
chmod +x "$AGENTIC_SCRUM_HOME/scripts/"*.sh "$AGENTIC_SCRUM_HOME/scripts/"*.py
```

---

## 2. Install the skills (once)

```bash
python3 "$AGENTIC_SCRUM_HOME/scripts/install_skills.py" --hermes --claude
```

Optional: also attach them to one Hermes profile and one git clone:

```bash
python3 "$AGENTIC_SCRUM_HOME/scripts/install_skills.py" \
  --hermes --claude \
  --profile tinto \
  --project "$HOME/work/dev/ai-co-founder-workspace"
```

Restart Hermes / Claude Code so they reload skills.

Check:

```bash
cat ~/.config/agentic-scrum/home
ls ~/.hermes/skills/agentic-scrum-po/SKILL.md
ls ~/.claude/skills/agentic-scrum-developer/SKILL.md
```

You did **not** have to add `agent/config/role.txt` to the clone.

---

## 3. Team roles vs Scrum hats

**Team role** = who the agent is (Co-Founder, CEO, CTO, Distinguished Engineer, Principal Engineer). Lives in the clone persona. Skills do not overwrite it.

**Scrum hat** = which process the agent may run. Stored on the sidecar as a list. An agent can wear several hats.

| Hat | Who usually has it | Skill |
|-----|-------------------|--------|
| product-owner | Co-Founder; DE/PE/CTO when they own a slice | agentic-scrum-po |
| developer | DE, PE, CTO (Scrum “Developer” = builds the increment) | agentic-scrum-developer |
| tech-lead | CTO, DE, PE — split features and draft sprints | agentic-scrum-tech-lead |

`tech-lead` details: `references/POLICIES/tech-lead.md`.

Defaults if you only bind the team role:

- co-founder → product-owner
- cto → tech-lead
- distinguished-engineer / principal-engineer → tech-lead + developer
- ceo → no hats

Add a hat without removing others: `bind hat product-owner`.

Sidecar (not in git):

- Hermes: `~/.hermes/profiles/<profile>/scrum-bindings.yaml`
- Claude Code: `~/.claude/agentic-scrum-bindings.yaml`

Optional: `$COFOUNDER_ROOT/agent/config/role.txt` for team role only.

What you type:

| You type | Meaning |
|----------|---------|
| `bind co-founder` (or cto, ceo, distinguished-engineer, principal-engineer) | Save team role + default hats |
| `bind hat product-owner` (or developer, tech-lead) | Add a hat; keep existing |
| `session tech-lead` | This chat only |
| `stop` | Do not run the skill |

---

## 4. Scenarios

### 1 — First time, Co-Founder on Hermes, no role.txt

1. `./start.sh --profile tinto`
2. `Load agentic-scrum-po. Refresh the backlog.`
3. No sidecar. Skill asks you to bind.
4. You type `bind co-founder` → sidecar hats: `product-owner` only.
5. Persona still comes from `agent/SOUL.md`. Next session: no prompt.

### 2 — Co-Founder must not implement (mismatch)

1. `tinto` is co-founder / product-owner.
2. Load `agentic-scrum-developer`.
3. Hat `developer` is missing. Skill asks `bind hat developer`, `session developer`, or `stop`.
4. You type `stop`. Title stays Co-Founder. Clone unchanged.

### 3 — Principal Engineer also acts as PO

1. Claude Code PE agent: first load → `bind principal-engineer` (hats: tech-lead, developer).
2. Later: `Load agentic-scrum-po`.
3. Missing hat product-owner → you type `bind hat product-owner`.
4. Sidecar now has developer + tech-lead + product-owner. PE title unchanged. Both PO and implementer skills match.

### 4 — Same clone, new Hermes profile

Profile `ana` has no sidecar. First skill load asks again. Bindings are per profile, not per git clone.

### 5 — Tech-lead (CTO / DE / PE split work)

1. Agent bound as `principal-engineer` (already has tech-lead).
2. `Load agentic-scrum-tech-lead` to split an epic into stories and draft a sprint.
3. MATCH. They wait for your `sprint yes`. They merge nothing. They implement only if they also have the developer hat (DE/PE do by default; CTO does not — add `bind hat developer` if the CTO should code).

---

## 5. Everyday use

You (Founder) approve on the issue or in chat: `approved`, `proceed`, `handle`, `sprint yes`, `send back`. You merge pull requests. Agents never merge.

Typical loop:

1. Hermes Co-Founder + `agentic-scrum-po` — draft epics (after bind). You say `approved`. Issues are created only when you want GitHub in play.
2. PO + `agentic-scrum-tech-lead` — split into stories. You say `sprint yes`.
3. You comment `/implement` on a story.
4. Developer + `agentic-scrum-developer` — plan comment, you `approved`, then branch, tests, PR `Closes #N`.

Persona always comes from the clone. Process comes from the skill.

---

## 6. GitHub (Issues + one Project)

Do this once (automates former GitHub clicks):

```bash
export REPO=owner/name
export GH_PROJECT="Venture board"
python3 "$AGENTIC_SCRUM_HOME/scripts/setup_github.py" \
  --repo "$REPO" --title "$GH_PROJECT" --clone /path/to/repo
```

Details and leftovers: **GITHUB/ONCE.md**. Then:

```bash
export REPO=owner/name
export GH_PROJECT="Venture board"
python3 "$AGENTIC_SCRUM_HOME/scripts/workitems.py" create Epic "Title" ./body.md
python3 "$AGENTIC_SCRUM_HOME/scripts/workitems.py" create Story "Title" ./body.md --parent 12
```

Same project: Roadmap (epics), Sprint (Iteration), Defects (type Bug). Copy issue templates into the clone with `install_agent_config.py --clone` and commit `.github/` yourself.

Hats stay in scrum-bindings. Assignee = who does the work.

---

## 7. What each skill is

| Skill | Use it for |
|-------|------------|
| agentic-scrum | Index, gates, role check |
| agentic-scrum-po | Product backlog / epics |
| agentic-scrum-tech-lead | Feature split and sprint draft (hat tech-lead; CTO/DE/PE) |
| agentic-scrum-ceo | Strategy only |
| agentic-scrum-developer | One story or bug |
| agentic-scrum-story-implement | Plan/RCA then PR steps |
| agentic-scrum-sprint | Remind that sprint = Project Iteration |
| agentic-scrum-work-items | Create/comment issues (types + sub-issues) |

---

## 8. Where files live

```
$HOME/work/dev/agentic-scrum-development/
  README.md
  SKILL.md
  skills/          one folder per skill
  references/      FLOWS, POLICIES (role-binding.md, tech-lead.md)
  scripts/         install_skills.py, scrum_bindings.py, workitems.py
  GITHUB/          templates (optional)
  TRIGGERS/        comment bot (optional)
```

Sidecars (not in the clone):

- `~/.hermes/profiles/<profile>/scrum-bindings.yaml`
- `~/.claude/agentic-scrum-bindings.yaml`

---

## 9. Uninstall skills (keeps the pack)

```bash
rm -f ~/.hermes/skills/agentic-scrum ~/.hermes/skills/agentic-scrum-*
rm -f ~/.claude/skills/agentic-scrum ~/.claude/skills/agentic-scrum-*
```

Remove a Hermes binding: delete that profile’s `scrum-bindings.yaml`.
