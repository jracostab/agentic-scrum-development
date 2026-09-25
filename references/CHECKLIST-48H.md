# 48-hour start

Repo default: set `REPO` in your shell.

## Hour 0–2 — GitHub

```bash
export REPO=jracostab/ai-co-founder-workspace
export PACK="$HOME/work/dev/agentic-scrum-development"
chmod +x "$PACK/scripts/"*.sh
"$PACK/scripts/enable_automation.sh"
# optional: write .github into a clone and skills onto a Hermes profile
"$PACK/scripts/enable_automation.sh" \
  --clone "$HOME/work/dev/ai-co-founder-workspace" \
  --profile tinto
```

Exact `gh` commands: GITHUB/commands.md

Confirm projects exist: Co-Founder Task Board, Co-Founder Open Defects.

## Hour 2–4 — Co-Founder (Hermes)

In the co-founder clone:

- Append POLICIES/sdlc-policy.md and POLICIES/approval-policy.md into `agent/AGENTS.md` (or copy AGENTS/co-founder/AGENTS.md over and keep venture-cli section).
- Copy SKILLS/work-items into `agent/skills/work-items/` (or `~/.hermes/profiles/$PROFILE/skills/work-items/`).
- Restart: `./start.sh` then chat: `Take the PO role. Load work-items skill. List open type:epic issues.`

## Hour 4–8 — CEO, CTO, Developer (Claude Code today)

Each Claude Code agent / CLAUDE.md:

- Paste the matching `AGENTS/<role>/SOUL.md` + `AGENTS.md`.
- Developer also gets POLICIES/coding-policy.md + SKILLS/story-implement/SKILL.md.
- CTO gets SKILLS/sprint/SKILL.md.

## Hour 8–12 — First product slice (with you)

In Hermes co-founder chat:

```
Draft 3 epics for this venture. Use EXAMPLES format. Do not create GitHub issues until I say approved.
```

You: edit, then `approved`. PO creates issues with `type:epic`.

Then:

```
With CTO: split epic #N into features, then one feature into stories. Wait for my sprint yes.
```

## Hour 12–16 — First story through the loop

1. Label a story `role:developer` `status:ready-for-dev`.
2. You comment: `/implement`
3. In Developer (Claude Code): `Take GitHub issue #N. Follow story-implement skill. Plan on the issue. Stop.`
4. You comment `approved`.
5. Developer implements, PR, you merge.

## Day 2 — Make it habitual

- Use `/plan` `/approve` `/implement` `/rca` only (TRIGGERS/comment-commands.md).
- One bug through Flow 5 if you have one.
- Do not build a custom orchestrator yet.

Done when: one epic, one feature, one story, one PR merged with you as G3+G4.
