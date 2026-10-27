# Standalone preparation validation

Checked locally on 2026-10-21.

98 tests passed; Ruff passed; wheel and sdist build passed; twine check passed; clean virtual-environment wheel install/import/model smoke passed. The sdist contains the complete guide, banner and regeneration inputs.

Generated SDK runtime files are unchanged from the subtree split. Package name and version remain unchanged. The complete original consumer README is retained byte-for-byte in `docs/guide.md`. Shell scripts pass `bash -n`; Python maintainer scripts parse; the included OpenAPI contract has no `/v1/internal/` paths.

A high-confidence pattern scan of all preserved-history blobs (363) and working source files found no private-key, GitHub-token, AWS-access-ID, npm-token, PyPI-token or Slack-token patterns. This is a bounded pattern scan, not a comprehensive secrets audit.

No live authenticated API requests, package publication, remote repository changes or trusted-publisher changes were performed. Full regeneration was not executed because the OpenAPI generator toolchain was not installed in this preparation environment. Before enabling releases, run generation in a disposable checkout, review the diff and complete the migration described in [source-provenance.md](source-provenance.md).
