# Contributing to the Geonode Python SDK

Open pull requests against `main`. Keep changes focused, describe the behavior and add an entry under `[Unreleased]` in `CHANGELOG.md`. Do not change package names or versions as part of routine fixes.

## Local checks

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]' build twine
bash scripts/ruff.sh check
bash scripts/test.sh
python -m build
python -m twine check dist/*
```

The tests use local fixtures and mocks; they do not require an API key. Never include credentials, customer data or account-specific output in a pull request.

## Generated code

The runtime client is generated from `openapi.json`. Update the contract and generation/postprocessing scripts when changing generated behavior, and add a focused regression test. See [source provenance](docs/source-provenance.md) for generator requirements and the release-migration boundary.

## Reports and releases

For bugs, include the package version, runtime version, a minimal reproduction and expected behavior. Security reports belong in [SECURITY.md](SECURITY.md), not a public issue. Publishing still runs from the original monorepo; these standalone repositories have no release workflow yet.
