#!/usr/bin/env python3
"""Org issue types vs personal labels. Shared by setup_github and workitems."""

from __future__ import annotations

import json
import subprocess
from typing import Literal

Mode = Literal["types", "labels"]
SCRUM_LABELS = (
    ("Epic", "6f42c1", "Product outcome"),
    ("Feature", "0052cc", "Slice of an epic"),
    ("Story", "0e8a16", "Implementable story"),
    ("Bug", "d73a4a", "Defect"),
)


def gh(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        ["gh", *args],
        capture_output=True,
        text=True,
        check=False,
        stdin=subprocess.DEVNULL,
    )


def gql(query: str, variables: dict | None = None) -> dict:
    payload = {"query": query, "variables": variables or {}}
    result = subprocess.run(  # noqa: S603
        ["gh", "api", "graphql", "--input", "-"],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout).strip())
    data = json.loads(result.stdout)
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"]))
    return data["data"]


def owner_kind(repo: str) -> str:
    owner, name = repo.split("/", 1)
    data = gql(
        """
        query($o: String!, $n: String!) {
          repository(owner: $o, name: $n) {
            owner { __typename }
          }
        }
        """,
        {"o": owner, "n": name},
    )
    typename = data["repository"]["owner"]["__typename"]
    return "Organization" if typename == "Organization" else "User"


def org_has_epic_and_story(owner: str) -> bool:
    try:
        data = gql(
            """
            query($o: String!) {
              organization(login: $o) {
                issueTypes(first: 50) { nodes { name } }
              }
            }
            """,
            {"o": owner},
        )
    except RuntimeError:
        return False
    nodes = ((data.get("organization") or {}).get("issueTypes") or {}).get("nodes") or []
    names = {n["name"].lower() for n in nodes}
    return "epic" in names and "story" in names


def scrum_mode(repo: str) -> Mode:
    if owner_kind(repo) != "Organization":
        return "labels"
    owner = repo.split("/", 1)[0]
    return "types" if org_has_epic_and_story(owner) else "labels"


def ensure_scrum_labels(repo: str) -> None:
    for name, color, desc in SCRUM_LABELS:
        result = gh(
            "label",
            "create",
            name,
            "--repo",
            repo,
            "--color",
            color,
            "--description",
            desc,
            "--force",
        )
        print(
            f"label {name}"
            if result.returncode == 0
            else f"label {name} note: {(result.stderr or '').strip()}"
        )


def view_filters(mode: Mode) -> list[tuple[str, str, str]]:
    """(view name, layout, filter)."""
    if mode == "types":
        return [
            ("Roadmap", "ROADMAP_LAYOUT", "type:Epic"),
            ("Sprint", "BOARD_LAYOUT", "-type:Epic"),
            ("Defects", "BOARD_LAYOUT", "type:Bug"),
        ]
    return [
        ("Roadmap", "ROADMAP_LAYOUT", "label:Epic"),
        ("Sprint", "BOARD_LAYOUT", "-label:Epic"),
        ("Defects", "BOARD_LAYOUT", "label:Bug"),
    ]
