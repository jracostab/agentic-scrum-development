#!/usr/bin/env python3
"""Copy issue templates, workflow, and Hermes/Claude agent files. Stdlib only."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parent.parent


def copy_tree(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dest, dirs_exist_ok=True)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    print(f"copied {src} -> {dest}")


def install_github_repo(clone: Path) -> None:
    templates = PACK / "GITHUB" / "ISSUE_TEMPLATE"
    dest = clone / ".github" / "ISSUE_TEMPLATE"
    dest.mkdir(parents=True, exist_ok=True)
    for path in templates.glob("*.yml"):
        shutil.copy2(path, dest / path.name)
        print(f"copied {path.name} -> {dest}")
    wf_src = PACK / "TRIGGERS" / "scrum-commands.yml"
    wf_dest = clone / ".github" / "workflows" / "scrum-commands.yml"
    wf_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(wf_src, wf_dest)
    print(f"copied workflow -> {wf_dest}")


def install_hermes_profile(profile: str) -> None:
    home = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
    dest = home / "profiles" / profile / "skills"
    copy_tree(PACK / "skills" / "work-items", dest / "work-items")
    copy_tree(PACK / "skills" / "sprint", dest / "sprint")
    copy_tree(PACK / "skills" / "story-implement", dest / "story-implement")
    copy_tree(PACK / "skills" / "product-owner", dest / "product-owner")
    include = home / "profiles" / profile / "SCRUM.md"
    include.write_text(
        "Load skill agentic-scrum (product-owner). "
        "Pack: $HOME/workspace/agentic-scrum-development\n",
        encoding="utf-8",
    )
    print(f"wrote {include}")


def install_claude_dir(target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for role in ("ceo", "tech-lead", "developer", "product-owner"):
        src = PACK / "skills" / role
        if src.is_dir():
            copy_tree(src, target / role)
    (target / "README.md").write_text(
        "Point each Claude Code agent at the matching role folder.\n"
        "Developer: also POLICIES/coding-policy.md and SKILLS/story-implement.\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clone", type=Path, help="git clone to receive .github templates")
    parser.add_argument("--profile", help="Hermes profile name to receive skills")
    parser.add_argument(
        "--claude-dir",
        type=Path,
        default=PACK / "install" / "claude-agents",
        help="Where to copy CEO/CTO/Developer agent files",
    )
    ns = parser.parse_args()
    if ns.clone:
        if not ns.clone.is_dir():
            sys.exit(f"clone not a directory: {ns.clone}")
        install_github_repo(ns.clone)
    if ns.profile:
        install_hermes_profile(ns.profile)
    install_claude_dir(ns.claude_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
