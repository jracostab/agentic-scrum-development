#!/usr/bin/env python3
"""Team role vs Scrum hats. Sidecar only. Never writes SOUL.md."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

TEAM_ROLES = (
    "co-founder",
    "ceo",
    "cto",
    "distinguished-engineer",
    "principal-engineer",
)
HATS = ("product-owner", "developer", "tech-lead")
DEFAULT_HATS: dict[str, list[str]] = {
    "co-founder": ["product-owner"],
    "ceo": [],
    "cto": ["tech-lead"],
    "distinguished-engineer": ["tech-lead", "developer"],
    "principal-engineer": ["tech-lead", "developer"],
}
# Skill → required Scrum hat (None = any hat). CEO skill checks team role.
SKILL_HAT: dict[str, str | None] = {
    "agentic-scrum-po": "product-owner",
    "agentic-scrum-tech-lead": "tech-lead",
    "agentic-scrum-developer": "developer",
    "agentic-scrum-ceo": None,
    "agentic-scrum-work-items": None,
    "agentic-scrum-sprint": None,
    "agentic-scrum-story-implement": None,
    "agentic-scrum": None,
}
SKILL_TEAM: dict[str, str | None] = {
    "agentic-scrum-ceo": "ceo",
}
LEGACY_ROLE = {
    "co-founder": ("co-founder", ["product-owner"]),
    "cto": ("cto", ["tech-lead"]),
    "developer": ("principal-engineer", ["developer"]),
    "ceo": ("ceo", []),
    "product-owner": ("co-founder", ["product-owner"]),
    "tech-lead": ("cto", ["tech-lead"]),
}


def hermes_home() -> Path:
    return Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))


def profile_name() -> str:
    return (
        os.environ.get("COFOUNDER_PROFILE")
        or os.environ.get("HERMES_PROFILE")
        or os.environ.get("AGENTIC_SCRUM_PROFILE")
        or ""
    ).strip()


def claude_agent() -> str:
    return (
        os.environ.get("CLAUDE_AGENT_NAME")
        or os.environ.get("AGENTIC_SCRUM_AGENT")
        or "default"
    ).strip()


def runtime() -> str:
    if profile_name() or os.environ.get("HERMES_HOME"):
        return "hermes"
    if os.environ.get("CLAUDE_AGENT_NAME") or os.environ.get("CLAUDECODE"):
        return "claude"
    return "hermes" if (hermes_home() / "profiles").is_dir() else "claude"


def binding_path() -> Path:
    if runtime() == "hermes":
        return hermes_home() / "profiles" / (profile_name() or "default") / "scrum-bindings.yaml"
    return Path.home() / ".claude" / "agentic-scrum-bindings.yaml"


def clone_team_role() -> str:
    root = os.environ.get("COFOUNDER_ROOT", "").strip()
    if not root:
        return ""
    path = Path(root) / "agent" / "config" / "role.txt"
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8").strip().splitlines()[0].strip()


def parse_lists(text: str) -> dict[str, object]:
    team_role = ""
    legacy = ""
    hats: list[str] = []
    skills: list[str] = []
    mode = ""
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("team_role:"):
            team_role = line.split(":", 1)[1].strip()
            mode = ""
        elif line.startswith("role:"):
            legacy = line.split(":", 1)[1].strip()
            mode = ""
        elif line == "hats:":
            mode = "hats"
        elif line == "skills:":
            mode = "skills"
        elif line.startswith("- ") and mode == "hats":
            hats.append(line[2:].strip())
        elif line.startswith("- ") and mode == "skills":
            skills.append(line[2:].strip())
    if not team_role and legacy in LEGACY_ROLE:
        team_role, hats = LEGACY_ROLE[legacy][0], list(LEGACY_ROLE[legacy][1])
    elif not team_role and legacy:
        team_role = legacy
    return {"team_role": team_role, "hats": hats, "skills": skills}


def load_binding() -> dict[str, object]:
    path = binding_path()
    if not path.is_file():
        return {"team_role": "", "hats": [], "skills": []}
    return parse_lists(path.read_text(encoding="utf-8"))


def dump(team_role: str, hats: list[str], skills: list[str]) -> str:
    lines = [
        f"team_role: {team_role}",
        f"profile: {profile_name() or claude_agent()}",
        "hats:",
    ]
    for hat in hats:
        lines.append(f"  - {hat}")
    lines.append("skills:")
    for skill in skills:
        lines.append(f"  - {skill}")
    return "\n".join(lines) + "\n"


def unique(items: list[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        if item and item not in out:
            out.append(item)
    return out


def declared() -> tuple[str, list[str], str]:
    clone = clone_team_role()
    data = load_binding()
    hats = [str(h) for h in (data.get("hats") or [])]
    team = clone or str(data.get("team_role") or "")
    source = str(binding_path())
    if clone:
        source = str(
            Path(os.environ["COFOUNDER_ROOT"]) / "agent" / "config" / "role.txt"
        )
    return team, hats, source


def cmd_check(ns: argparse.Namespace) -> int:
    skill = ns.skill
    if skill not in SKILL_HAT and skill not in SKILL_TEAM:
        print("STATUS=UNKNOWN_SKILL")
        return 1
    team, hats, source = declared()
    need_hat = SKILL_HAT.get(skill)
    need_team = SKILL_TEAM.get(skill)
    if need_team:
        status = "MATCH" if team == need_team else ("UNSET" if not team else "MISMATCH")
        required = f"team:{need_team}"
    elif not team and not hats:
        status = "UNSET"
        required = need_hat or "any-hat"
    elif need_hat is None:
        status = "MATCH" if (team or hats) else "UNSET"
        required = "any-hat"
    elif need_hat in hats:
        status = "MATCH"
        required = f"hat:{need_hat}"
    else:
        status = "MISMATCH"
        required = f"hat:{need_hat}"
    print(f"STATUS={status}")
    print(f"TEAM_ROLE={team}")
    print(f"HATS={','.join(hats)}")
    print(f"REQUIRED={required}")
    print(f"SKILL={skill}")
    print(f"RUNTIME={runtime()}")
    print(f"PROFILE={profile_name() or claude_agent()}")
    print(f"BINDING={source}")
    if status == "MATCH":
        print("ACTION=continue")
        return 0
    if status == "UNSET":
        print(
            "ACTION=ask No Scrum binding yet. "
            "Type `bind <team-role>` (co-founder|ceo|cto|distinguished-engineer|principal-engineer) "
            "or `bind hat <product-owner|developer|tech-lead>`. Never writes SOUL.md. Or `stop`."
        )
        return 2
    print(
        "ACTION=ask "
        f"Team role `{team}` hats [{', '.join(hats) or 'none'}]. Skill {skill} needs `{required}`. "
        f"Type `bind hat {need_hat or need_team}` (add, keep existing hats), "
        f"`session {need_hat or need_team}` (this chat only), or `stop`."
    )
    return 3


def cmd_bind(ns: argparse.Namespace) -> int:
    data = load_binding()
    team = str(data.get("team_role") or "")
    hats = [str(h) for h in (data.get("hats") or [])]
    skills = [str(s) for s in (data.get("skills") or [])]
    if ns.team_role:
        if ns.team_role not in TEAM_ROLES:
            sys.exit(f"team-role must be one of {', '.join(TEAM_ROLES)}")
        team = ns.team_role
        if not ns.hats:
            hats = unique(hats + DEFAULT_HATS[team])
    for hat in ns.hats or []:
        if hat not in HATS:
            sys.exit(f"hat must be one of {', '.join(HATS)}")
        hats = unique(hats + [hat])
    if ns.skill and ns.skill not in skills:
        skills.append(ns.skill)
    if not team and not hats:
        sys.exit("provide --team-role and/or --hat")
    path = binding_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump(team, hats, skills), encoding="utf-8")
    print(f"wrote {path}")
    return 0


def cmd_show(_ns: argparse.Namespace) -> int:
    team, hats, source = declared()
    print(f"team_role={team}")
    print(f"hats={','.join(hats)}")
    print(f"source={source}")
    data = load_binding()
    skills = data.get("skills") or []
    print(f"skills={','.join(str(s) for s in skills)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="scrum_bindings")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("check")
    p.add_argument("--skill", required=True)
    p.set_defaults(func=cmd_check)
    p = sub.add_parser("bind")
    p.add_argument("--team-role", dest="team_role", default="")
    p.add_argument("--hat", dest="hats", action="append", default=[])
    p.add_argument("--skill", default="")
    p.set_defaults(func=cmd_bind)
    p = sub.add_parser("show")
    p.set_defaults(func=cmd_show)
    ns = parser.parse_args()
    return int(ns.func(ns))


if __name__ == "__main__":
    raise SystemExit(main())
