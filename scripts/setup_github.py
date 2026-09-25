#!/usr/bin/env python3
"""Automate GitHub Issue types + one Project (Roadmap / Sprint / Defects). Stdlib + gh."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

PACK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PACK / "scripts"))
from github_mode import ensure_scrum_labels, scrum_mode, view_filters  # noqa: E402


def gh_json(args: list[str]) -> dict:
    result = subprocess.run(  # noqa: S603
        ["gh", *args],
        capture_output=True,
        text=True,
        check=False,
        stdin=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "gh failed").strip())
    return json.loads(result.stdout) if result.stdout.strip() else {}


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


def leftover(msg: str, items: list[str]) -> None:
    print(f"\n==> {msg}")
    if not items:
        print("    (nothing left)")
        return
    for item in items:
        print(f"    - {item}")


def repo_ids(repo: str) -> tuple[str, str, str, str]:
    owner, name = repo.split("/", 1)
    data = gql(
        """
        query($o: String!, $n: String!) {
          repository(owner: $o, name: $n) {
            id
            owner {
              __typename
              ... on Organization { id login }
              ... on User { id login }
            }
          }
        }
        """,
        {"o": owner, "n": name},
    )
    repo_node = data["repository"]
    own = repo_node["owner"]
    kind = "Organization" if own["__typename"] == "Organization" else "User"
    return repo_node["id"], own["id"], kind, own["login"]


def ensure_issue_types(owner_id: str, kind: str) -> None:
    if kind != "Organization":
        print("issue types: skipped (personal account → labels mode)")
        return
    existing = gql(
        """
        query($id: ID!) {
          node(id: $id) {
            ... on Organization {
              issueTypes(first: 50) { nodes { name } }
            }
          }
        }
        """,
        {"id": owner_id},
    )
    names = {
        n["name"].lower()
        for n in ((existing.get("node") or {}).get("issueTypes") or {}).get("nodes") or []
    }
    wanted = [
        ("Epic", "Product outcome; parent of features and stories", "PURPLE"),
        ("Story", "Implementable user story", "GREEN"),
    ]
    for name, desc, color in wanted:
        if name.lower() in names:
            print(f"issue type exists: {name}")
            continue
        try:
            gql(
                """
                mutation($ownerId: ID!, $name: String!, $description: String, $color: IssueTypeColor) {
                  createIssueType(input: {
                    ownerId: $ownerId, isEnabled: true, name: $name,
                    description: $description, color: $color
                  }) { issueType { name } }
                }
                """,
                {
                    "ownerId": owner_id,
                    "name": name,
                    "description": desc,
                    "color": color,
                },
            )
            print(f"created issue type: {name}")
        except RuntimeError as exc:
            print(f"issue type {name} skipped ({exc}); will use labels if needed")


def find_project(owner: str, kind: str, title: str) -> tuple[str, int] | None:
    if kind == "Organization":
        data = gql(
            """
            query($o: String!) {
              organization(login: $o) {
                projectsV2(first: 50) { nodes { id number title } }
              }
            }
            """,
            {"o": owner},
        )
        nodes = ((data.get("organization") or {}).get("projectsV2") or {}).get("nodes") or []
    else:
        data = gql(
            """
            query($o: String!) {
              user(login: $o) {
                projectsV2(first: 50) { nodes { id number title } }
              }
            }
            """,
            {"o": owner},
        )
        nodes = ((data.get("user") or {}).get("projectsV2") or {}).get("nodes") or []
    for node in nodes:
        if node.get("title") == title:
            return node["id"], node["number"]
    return None


def create_project(owner_id: str, title: str, repo_id: str) -> tuple[str, int | None]:
    data = gql(
        """
        mutation($ownerId: ID!, $title: String!, $repositoryId: ID) {
          createProjectV2(input: {ownerId: $ownerId, title: $title, repositoryId: $repositoryId}) {
            projectV2 { id number url title }
          }
        }
        """,
        {"ownerId": owner_id, "title": title, "repositoryId": repo_id},
    )
    proj = data["createProjectV2"]["projectV2"]
    print(f"project {proj['number']} {proj['url']}")
    try:
        gql(
            """
            mutation($projectId: ID!, $repositoryId: ID!) {
              linkProjectV2ToRepository(input: {projectId: $projectId, repositoryId: $repositoryId}) {
                repository { name }
              }
            }
            """,
            {"projectId": proj["id"], "repositoryId": repo_id},
        )
        print("linked project to repository")
    except RuntimeError as exc:
        print(f"link note: {exc}")
    return proj["id"], proj.get("number")


def ensure_iteration_field(project_id: str) -> list[str]:
    fields = gql(
        """
        query($id: ID!) {
          node(id: $id) {
            ... on ProjectV2 {
              fields(first: 50) {
                nodes {
                  ... on ProjectV2Field { name }
                  ... on ProjectV2IterationField { name }
                  ... on ProjectV2SingleSelectField { name }
                }
              }
            }
          }
        }
        """,
        {"id": project_id},
    )
    names = [
        n.get("name", "")
        for n in ((fields.get("node") or {}).get("fields") or {}).get("nodes") or []
    ]
    if any(n.lower() == "iteration" for n in names):
        print("iteration field exists")
        return []
    start = date.today().isoformat()
    try:
        gql(
            """
            mutation($projectId: ID!, $start: Date!) {
              createProjectV2Field(input: {
                projectId: $projectId
                dataType: ITERATION
                name: "Iteration"
                iterationConfiguration: {
                  startDate: $start
                  duration: 14
                  iterations: []
                }
              }) { projectV2Field { ... on ProjectV2IterationField { name } } }
            }
            """,
            {"projectId": project_id, "start": start},
        )
        print("created Iteration field (14-day)")
        return []
    except RuntimeError as exc:
        return [f"Add Iteration field in the Project UI (API: {exc})"]


def ensure_views(project_id: str, mode: str) -> list[str]:
    left: list[str] = []
    existing = gql(
        """
        query($id: ID!) {
          node(id: $id) {
            ... on ProjectV2 { views(first: 20) { nodes { id name } } }
          }
        }
        """,
        {"id": project_id},
    )
    nodes = ((existing.get("node") or {}).get("views") or {}).get("nodes") or []
    have = {n.get("name"): n.get("id") for n in nodes}
    wanted = view_filters(mode)
    for name, layout, filt in wanted:
        view_id = have.get(name)
        if view_id:
            print(f"view exists: {name}")
            if filt:
                try:
                    gql(
                        """
                        mutation($viewId: ID!, $filter: String!) {
                          updateProjectV2View(input: {viewId: $viewId, filter: $filter}) {
                            projectV2View { name }
                          }
                        }
                        """,
                        {"viewId": view_id, "filter": filt},
                    )
                    print(f"updated {name} filter: {filt}")
                except RuntimeError as exc:
                    left.append(f"Set {name} view filter to {filt} in the UI ({exc})")
            continue
        try:
            data = gql(
                """
                mutation($projectId: ID!, $name: String!, $layout: ProjectV2ViewLayout!) {
                  createProjectV2View(input: {projectId: $projectId, name: $name, layout: $layout}) {
                    projectV2View { id name }
                  }
                }
                """,
                {"projectId": project_id, "name": name, "layout": layout},
            )
            view_id = data["createProjectV2View"]["projectV2View"]["id"]
            if filt:
                gql(
                    """
                    mutation($viewId: ID!, $filter: String!) {
                      updateProjectV2View(input: {viewId: $viewId, filter: $filter}) {
                        projectV2View { name }
                      }
                    }
                    """,
                    {"viewId": view_id, "filter": filt},
                )
            print(f"view {name} ({layout}) filter={filt or 'none'}")
        except RuntimeError as exc:
            left.append(f"Create view {name} in the UI ({exc})")
    return left


def maybe_template(project_id: str, kind: str) -> None:
    if kind != "Organization":
        print("project template: skipped (org-owned projects only)")
        return
    try:
        gql(
            """
            mutation($projectId: ID!) {
              markProjectV2AsTemplate(input: {projectId: $projectId}) { projectV2 { id } }
            }
            """,
            {"projectId": project_id},
        )
        print("marked project as template")
    except RuntimeError as exc:
        print(f"project template skipped ({exc})")


def copy_templates(clone: Path) -> None:
    import shutil

    src = PACK / "GITHUB" / "ISSUE_TEMPLATE"
    dest = clone / ".github" / "ISSUE_TEMPLATE"
    dest.mkdir(parents=True, exist_ok=True)
    for path in src.glob("*.yml"):
        shutil.copy2(path, dest / path.name)
        print(f"copied {path.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description="GitHub one-time setup with least friction")
    parser.add_argument("--repo", default=os.environ.get("REPO", ""))
    parser.add_argument("--title", default=os.environ.get("GH_PROJECT", "Venture board"))
    parser.add_argument("--clone", type=Path, default=None)
    parser.add_argument("--skip-project", action="store_true")
    ns = parser.parse_args()
    if not ns.repo:
        sys.exit("Set --repo owner/name or REPO=")
    left: list[str] = []
    repo_id, owner_id, kind, owner = repo_ids(ns.repo)
    print(f"owner={owner} ({kind}) repo={ns.repo}")
    ensure_issue_types(owner_id, kind)
    mode = scrum_mode(ns.repo)
    print(f"scrum mode={mode}")
    if mode == "labels":
        ensure_scrum_labels(ns.repo)
    if not ns.skip_project:
        found = find_project(owner, kind, ns.title)
        if found:
            project_id, number = found
            print(f"reusing project {number} {ns.title!r}")
        else:
            project_id, number = create_project(owner_id, ns.title, repo_id)
        left.extend(ensure_iteration_field(project_id))
        left.extend(ensure_views(project_id, mode))
        maybe_template(project_id, kind)
        print(f"\nexport GH_PROJECT={ns.title!r}")
        print(f"export REPO={ns.repo}")
        print(f"export GH_SCRUM_MODE={mode}")
    if ns.clone:
        copy_templates(ns.clone)
        left.append(f"Commit {ns.clone}/.github/ISSUE_TEMPLATE yourself (script does not push).")
    leftover("Still manual (if any)", left)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
