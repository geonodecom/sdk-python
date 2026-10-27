#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  printf 'Usage: %s <check|format> [paths ...]\n' "$0" >&2
  exit 1
fi

mode="$1"
shift

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
config_file="$repo_root/pyproject.toml"

if [[ $# -eq 0 ]]; then
  set -- "$repo_root/tests" "$repo_root/setup.py"
fi

if command -v ruff >/dev/null 2>&1; then
  ruff_cmd=(ruff)
elif command -v uv >/dev/null 2>&1; then
  ruff_cmd=(uv run --project "$repo_root" --with ruff ruff)
else
  printf 'Install ruff or uv before running Python SDK linting.\n' >&2
  exit 1
fi

case "$mode" in
  check)
    "${ruff_cmd[@]}" check --force-exclude --config "$config_file" "$@"
    ;;
  format)
    "${ruff_cmd[@]}" format --force-exclude --config "$config_file" "$@"
    ;;
  *)
    printf 'Unknown mode: %s\n' "$mode" >&2
    exit 1
    ;;
esac
