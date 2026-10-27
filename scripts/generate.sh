#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
sdk_dir="$repo_root"
spec_file="$repo_root/openapi.json"
config_file="$repo_root/config.json"
ignore_file="$repo_root/openapi-generator/python-sdk.ignore"
version_file="$sdk_dir/.openapi-generator/VERSION"
package_metadata_file="$sdk_dir/pyproject.toml"

sdk_version="$(awk -F '"' '/^version = "/ { print $2; exit }' "$package_metadata_file")"

if [[ -z "$sdk_version" ]]; then
  printf 'Unable to determine SDK package version from %s\n' "$package_metadata_file" >&2
  exit 1
fi

if [[ ! -f "$version_file" ]]; then
  printf 'Missing generator version file: %s\n' "$version_file" >&2
  exit 1
fi

expected_version="$(tr -d '[:space:]' < "$version_file")"

if command -v uv >/dev/null 2>&1; then
  generator_cmd=(uv run --project "$repo_root" --with "openapi-generator-cli[jdk4py]==${expected_version}" openapi-generator-cli)
elif command -v openapi-generator-cli >/dev/null 2>&1; then
  generator_cmd=(openapi-generator-cli)
else
  printf 'Install uv or openapi-generator-cli before regenerating the Python SDK.\n' >&2
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  postprocess_cmd=(python3)
elif command -v python >/dev/null 2>&1; then
  postprocess_cmd=(python)
elif command -v uv >/dev/null 2>&1; then
  postprocess_cmd=(uv run --project "$repo_root" python)
else
  printf 'Install Python 3 before regenerating the Python SDK.\n' >&2
  exit 1
fi

actual_version="$("${generator_cmd[@]}" version | tr -d '\r\n[:space:]')"
if [[ "$actual_version" != "$expected_version" ]]; then
  printf 'Expected OpenAPI Generator %s, got %s.\n' "$expected_version" "$actual_version" >&2
  exit 1
fi

# Strip internal-only endpoints again before generation, in case openapi.json
# was copied from the backend without filter_spec.py.
filtered_spec="$(mktemp)"
trap 'rm -f "$filtered_spec"' EXIT
"${postprocess_cmd[@]}" "$repo_root/openapi-generator/filter_spec.py" "$spec_file" "$filtered_spec"

# The API labels each request by the client named here (scraper-api#674); the token must
# stay in the API's allowlist (app/shared/client_label.py).
http_user_agent="geonode-python-sdk/${sdk_version}"

"${generator_cmd[@]}" generate \
  -g python \
  -i "$filtered_spec" \
  -c "$config_file" \
  -o "$sdk_dir" \
  --ignore-file-override "$ignore_file" \
  --additional-properties "generateSourceCodeOnly=true,packageVersion=${sdk_version},httpUserAgent=${http_user_agent}" \
  --global-property apiDocs=false,modelDocs=false,apiTests=false,modelTests=false

"${postprocess_cmd[@]}" "$script_dir/postprocess_generated.py"

cp "$ignore_file" "$sdk_dir/.openapi-generator-ignore"
rm -f "$sdk_dir/.openapi-generator/FILES" "$sdk_dir/geonode_scraper_sdk_README.md"
