import importlib.util
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "postprocess_generated.py"


@pytest.fixture(scope="module")
def pp():
    spec = importlib.util.spec_from_file_location("postprocess_generated", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    yield module
    sys.modules.pop(spec.name, None)


@pytest.fixture
def bare_tree(pp, tmp_path, monkeypatch):
    # One edited file is generated but no longer matches; the other two are not generated at all.
    path = tmp_path / "geonode_scraper_sdk/models/extract_request.py"
    path.parent.mkdir(parents=True)
    path.write_text("class ExtractRequest:\n    pass\n")
    monkeypatch.setattr(pp, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(pp, "SDK_DIR", tmp_path)
    return tmp_path


def test_without_sync_notes_a_problem_is_an_error(pp, bare_tree, monkeypatch):
    monkeypatch.setattr(pp, "SYNC_NOTES", None)

    with pytest.raises(RuntimeError, match="extract_request.py`: Unable to find expected generated snippet"):
        pp.main()


def test_with_sync_notes_problems_become_notes(pp, bare_tree, monkeypatch):
    notes = bare_tree / "notes.md"
    monkeypatch.setattr(pp, "SYNC_NOTES", str(notes))

    pp.main()

    text = notes.read_text()
    assert "`geonode_scraper_sdk/models/extract_request.py`: Unable to find expected generated snippet" in text
    assert "`geonode_scraper_sdk/models/proxy_settings.py` is no longer generated" in text
    assert "`geonode_scraper_sdk/api/extraction_api.py` is no longer generated" in text
    assert (bare_tree / "geonode_scraper_sdk/models/extract_request.py").read_text() == (
        "class ExtractRequest:\n    pass\n"
    )
