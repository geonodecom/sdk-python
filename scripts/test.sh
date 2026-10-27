#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
sdk_dir="$(cd "$script_dir/.." && pwd)"
repo_root="$sdk_dir"

if command -v pytest >/dev/null 2>&1; then
  cd "$sdk_dir"
  pytest tests "$@"
elif command -v uv >/dev/null 2>&1; then
  cd "$sdk_dir"
  uv run --project "$repo_root" --with-editable "$sdk_dir" --with pytest --with pytest-cov pytest tests "$@"
else
  printf 'Install pytest or uv before running the Python SDK test suite.\n' >&2
  exit 1
fi
