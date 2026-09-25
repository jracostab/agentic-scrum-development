#!/usr/bin/env python3
"""Install this pack as skills for Hermes and/or Claude Code. Stdlib only."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parent.parent
MODULAR = [
    ("work-items", "agentic-scrum-work-items"),
    ("sprint", "agentic-scrum-sprint"),
    ("story-implement", "agentic-scrum-story-implement"),
    ("product-owner", "agentic-scrum-po"),
    ("tech-lead", "agentic-scrum-tech-lead"),
    ("developer", "agentic-scrum-developer"),
    ("ceo", "agentic-scrum-ceo"),
]


def replace_link(src: Path, dest: Path, *, copy: bool = False) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_symlink() or dest.is_file():
        dest.unlink()
    elif dest.is_dir():
        shutil.rmtree(dest)
    if copy:
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        print(f"copied {src} -> {dest}")
        return
    try:
        dest.symlink_to(src, target_is_directory=src.is_dir())
        print(f"symlink {dest} -> {src}")
    except OSError:
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        print(f"copied {src} -> {dest}")


def write_home_pointer() -> None:
    cfg = Path.home() / ".config" / "agentic-scrum"
    cfg.mkdir(parents=True, exist_ok=True)
    (cfg / "home").write_text(str(PACK) + "\n", encoding="utf-8")
    print(f"AGENTIC_SCRUM_HOME -> {PACK} ({cfg / 'home'})")


def hermes_skills_root() -> Path:
    home = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
    return home / "skills"


def install_hermes(profile: str | None) -> None:
    root = hermes_skills_root()
    replace_link(PACK, root / "agentic-scrum")
    for folder, skill_name in MODULAR:
        replace_link(PACK / "skills" / folder, root / skill_name)
    if profile:
        dest = (
            Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
            / "profiles"
            / profile
            / "skills"
        )
        replace_link(PACK, dest / "agentic-scrum")
        for folder, skill_name in MODULAR:
            replace_link(PACK / "skills" / folder, dest / skill_name)


def install_claude(project: Path | None, *, copy: bool) -> None:
    dests = [Path.home() / ".claude" / "skills"]
    if project:
        dests.append(project / ".claude" / "skills")
    for root in dests:
        replace_link(PACK, root / "agentic-scrum", copy=copy)
        for folder, skill_name in MODULAR:
            replace_link(PACK / "skills" / folder, root / skill_name, copy=copy)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install agentic-scrum skills")
    parser.add_argument("--hermes", action="store_true")
    parser.add_argument("--claude", action="store_true")
    parser.add_argument("--profile", help="Also link into this Hermes profile")
    parser.add_argument("--project", type=Path, help="Also link into clone/.claude/skills")
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy files instead of symlinks (Claude Code Skills tab prefers copies)",
    )
    ns = parser.parse_args()
    if not ns.hermes and not ns.claude:
        ns.hermes = True
        ns.claude = True
    write_home_pointer()
    if ns.hermes:
        install_hermes(ns.profile)
    if ns.claude:
        install_claude(ns.project, copy=True)
    print("Done. Restart Hermes / Claude Code so they rescan skills.")
    print("Hermes: Skills hub or `hermes skills list` (enabled local).")
    print("Claude Code: new chat → Skills; user dir ~/.claude/skills/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
