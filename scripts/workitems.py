#!/usr/bin/env python3
"""GitHub work-item adapter v0. Stdlib + gh CLI. Never shell=True."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from github_mode import scrum_mode  # noqa: E402


def repo() -> str:
    value = os.environ.get("REPO", "").strip()
    if not value:
        sys.exit("Set REPO=owner/name")
    return value


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    cmd = ["gh", *args]
    result = subprocess.run(  # noqa: S603
        cmd,
        capture_output=True,
        text=True,
        check=False,
        stdin=subprocess.DEVNULL,
    )
    if check and result.returncode != 0:
        err = (result.stderr or result.stdout or "").strip()
        sys.exit(err or f"gh failed: {' '.join(cmd)}")
    return result


def cmd_bootstrap_labels(_ns: argparse.Namespace) -> None:
    print(
        "Happy path does not use type:/status:/sprint: labels.\n"
        "See GITHUB/ONCE.md: Issue types + one Project (Roadmap / Sprint / Defects).\n"
        "Optional exception label only:",
        file=sys.stderr,
    )
    r = repo()
    gh(
        "label",
        "create",
        "blocked",
        "--repo",
        r,
        "--color",
        "b60205",
        "--description",
        "Blocked (optional; prefer Project Status)",
        "--force",
        check=False,
    )
    print("label blocked (optional)")


def cmd_get(ns: argparse.Namespace) -> None:
    result = gh("issue", "view", str(ns.number), "--repo", repo(), "--comments")
    sys.stdout.write(result.stdout)


def cmd_create(ns: argparse.Namespace) -> None:
    body = Path(ns.body)
    r = repo()
    mode = os.environ.get("GH_SCRUM_MODE", "").strip() or scrum_mode(r)
    itype = ns.issue_type
    label = itype[:1].upper() + itype[1:].lower() if itype else itype
    if itype.lower() == "bug":
        label = "Bug"
    elif itype.lower() == "epic":
        label = "Epic"
    elif itype.lower() == "story":
        label = "Story"
    elif itype.lower() == "feature":
        label = "Feature"
    args = [
        "issue",
        "create",
        "--repo",
        r,
        "--title",
        ns.title,
        "--body-file",
        str(body),
    ]
    if mode == "types":
        args.extend(["--type", itype])
    else:
        args.extend(["--label", label])
    project = ns.project or os.environ.get("GH_PROJECT", "").strip()
    if project:
        args.extend(["--project", project])
    if ns.parent:
        args.extend(["--parent", str(ns.parent)])
    result = gh(*args, check=False)
    if result.returncode != 0 and mode == "types":
        fallback = {"story": "Task", "epic": "Feature"}.get(itype.lower())
        if fallback:
            idx = args.index("--type") + 1
            args[idx] = fallback
            result = gh(*args, check=False)
            if result.returncode == 0:
                print(
                    f"used issue type {fallback} (org has no {itype} type)",
                    file=sys.stderr,
                )
    if result.returncode != 0:
        sys.exit((result.stderr or result.stdout or "gh issue create failed").strip())
    sys.stdout.write(result.stdout)


def cmd_comment(ns: argparse.Namespace) -> None:
    result = gh(
        "issue",
        "comment",
        str(ns.number),
        "--repo",
        repo(),
        "--body-file",
        ns.body,
    )
    sys.stdout.write(result.stdout)


def cmd_label(ns: argparse.Namespace) -> None:
    joined = ",".join(ns.labels)
    gh("issue", "edit", str(ns.number), "--repo", repo(), "--add-label", joined)
    print(f"#{ns.number} + {joined}")


def cmd_ready(ns: argparse.Namespace) -> None:
    print(
        f"#{ns.number}: set Project Status to Ready / In progress in the Sprint view "
        "(not a GitHub label)."
    )


def cmd_sprint(ns: argparse.Namespace) -> None:
    print(
        "Sprint is the Project Iteration field, not a label.\n"
        f"Put issues {', '.join(str(n) for n in ns.numbers)} on the current Iteration "
        f"(requested name {ns.name}) in the GitHub Project UI or API."
    )


def cmd_setup_project(ns: argparse.Namespace) -> None:
    owner = ns.owner or os.environ.get("GH_OWNER") or repo().split("/")[0]
    title = ns.title or os.environ.get("GH_PROJECT") or "Venture board"
    result = gh(
        "project",
        "create",
        "--owner",
        owner,
        "--title",
        title,
        "--format",
        "json",
    )
    sys.stdout.write(result.stdout)
    number = None
    try:
        number = json.loads(result.stdout).get("number")
    except json.JSONDecodeError:
        number = None
    if number:
        gh(
            "project",
            "link",
            str(number),
            "--owner",
            owner,
            "--repo",
            repo(),
            check=False,
        )
        print(f"linked project {number} to {repo()}")
    print("Create Roadmap / Sprint / Defects views in the UI. See GITHUB/ONCE.md")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="workitems")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("bootstrap-labels")
    p.set_defaults(func=cmd_bootstrap_labels)

    p = sub.add_parser("get")
    p.add_argument("number", type=int)
    p.set_defaults(func=cmd_get)

    p = sub.add_parser("create")
    p.add_argument("issue_type", help="Epic, Feature, Story, Bug, or Task")
    p.add_argument("title")
    p.add_argument("body")
    p.add_argument("--parent", type=int, default=0)
    p.add_argument("--project", default="")
    p.set_defaults(func=cmd_create)

    p = sub.add_parser("comment")
    p.add_argument("number", type=int)
    p.add_argument("body")
    p.set_defaults(func=cmd_comment)

    p = sub.add_parser("label")
    p.add_argument("number", type=int)
    p.add_argument("labels", nargs="+")
    p.set_defaults(func=cmd_label)

    p = sub.add_parser("ready")
    p.add_argument("number", type=int)
    p.set_defaults(func=cmd_ready)

    p = sub.add_parser("sprint")
    p.add_argument("name", help="Iteration name reminder")
    p.add_argument("numbers", nargs="+", type=int)
    p.set_defaults(func=cmd_sprint)

    p = sub.add_parser("setup-project")
    p.add_argument("--owner", default="")
    p.add_argument("--title", default="")
    p.set_defaults(func=cmd_setup_project)
    return parser


def main(argv: list[str] | None = None) -> int:
    ns = build_parser().parse_args(argv)
    ns.func(ns)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
