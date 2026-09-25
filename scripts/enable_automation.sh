#!/usr/bin/env bash
# Enable GitHub labels/templates AND/OR install skills into Hermes + Claude Code.
set -euo pipefail
PACK="$(cd "$(dirname "$0")/.." && pwd)"
REPO="${REPO:-}"
CLONE=""
PROFILE=""
PYTHON="${PYTHON:-python3}"

usage() {
  cat <<EOF
usage: $0 [options]

  --clone DIR       Write .github issue templates + workflow into a git clone
  --profile NAME    Also link skills into ~/.hermes/profiles/NAME/skills
  --skip-github     Do not run GitHub project/type setup
  --skip-skills     Do not install Hermes/Claude skills

Examples:
  export REPO=jracostab/ai-co-founder-workspace
  $0 --clone \$HOME/work/dev/ai-co-founder-workspace
EOF
}

DO_GITHUB=1
DO_SKILLS=1
CLONE=""
PROFILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --clone) CLONE="${2:?}"; shift 2 ;;
    --profile) PROFILE="${2:?}"; shift 2 ;;
    --skip-github|--skip-labels) DO_GITHUB=0; shift ;;
    --skip-skills) DO_SKILLS=0; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage; exit 2 ;;
  esac
done

if [[ "$DO_GITHUB" == 1 ]]; then
  if [[ -z "$REPO" ]]; then
    echo "Set REPO=owner/name (or pass --skip-github)" >&2
    exit 2
  fi
  command -v gh >/dev/null || { echo "gh is required"; exit 1; }
  echo "==> GitHub project + issue types"
  gh_args=(--repo "$REPO" --title "${GH_PROJECT:-Venture board}")
  if [[ -n "$CLONE" ]]; then
    gh_args+=(--clone "$CLONE")
  fi
  "$PYTHON" "$PACK/scripts/setup_github.py" "${gh_args[@]}"
elif [[ -n "$CLONE" ]]; then
  echo "==> .github templates only"
  "$PYTHON" "$PACK/scripts/install_agent_config.py" --clone "$CLONE"
fi

if [[ "$DO_SKILLS" == 1 ]]; then
  echo "==> Hermes + Claude Code skills"
  skill_args=(--hermes --claude)
  if [[ -n "$PROFILE" ]]; then
    skill_args+=(--profile "$PROFILE")
  fi
  if [[ -n "$CLONE" ]]; then
    skill_args+=(--project "$CLONE")
  fi
  "$PYTHON" "$PACK/scripts/install_skills.py" "${skill_args[@]}"
fi

echo
echo "Pack: $PACK"
echo "Read: $PACK/README.md"
