#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SDK_DIR = REPO_ROOT


def text(*parts: str) -> str:
    return "".join(parts)


def apply_replacements(path: Path, replacements: list[tuple[str, str]]) -> bool:
    original = path.read_text()
    updated = original

    for old, new in replacements:
        if new in updated:
            continue
        if old not in updated:
            raise RuntimeError(f"Unable to find expected generated snippet in {path}")
        updated = updated.replace(old, new, 1)

    if updated == original:
        return False

    path.write_text(updated)
    return True


def main() -> None:
    changed_files: list[Path] = []

    replacement_map: dict[Path, list[tuple[str, str]]] = {
        SDK_DIR / "geonode_scraper_sdk/models/extract_request.py": [
            (
                text(
                    '    formats: Optional[List[OutputFormat]] = Field(',
                    'default=None, description="Output formats to return")\n',
                ),
                text(
                    '    formats: Optional[List[OutputFormat]] = Field(',
                    'default_factory=lambda: [OutputFormat.HTML], ',
                    'description="Output formats to return")\n',
                ),
            ),
            (
                text(
                    '    processing_mode: Optional[ProcessingMode] = Field(',
                    'default=None, description="Processing mode: sync ',
                    '(block until done) or async (starts job and return ',
                    'job ID)")\n',
                ),
                text(
                    '    processing_mode: Optional[ProcessingMode] = Field(',
                    'default=ProcessingMode.SYNC, description="Processing ',
                    'mode: sync (block until done) or async (starts job ',
                    'and return job ID)")\n',
                ),
            ),
            (
                text(
                    '        _obj = cls.model_validate({\n',
                    '            "formats": obj.get("formats"),\n',
                    '            "headers": obj.get("headers"),\n',
                    '            "processing_mode": obj.get("processing_mode"),\n',
                    '            "proxy": ProxySettings.from_dict(',
                    'obj["proxy"]) if obj.get("proxy") is not None else None,\n',
                    '            "render_js": obj.get("render_js") if ',
                    'obj.get("render_js") is not None else False,\n',
                    '            "timeout": obj.get("timeout"),\n',
                    '            "url": obj.get("url"),\n',
                    '            "wait_config": WaitConfig.from_dict(',
                    'obj["wait_config"]) if obj.get("wait_config") is not None ',
                    'else None\n',
                    '        })\n',
                ),
                text(
                    '        model_data = {"url": obj.get("url")}\n',
                    '        if "formats" in obj:\n',
                    '            model_data["formats"] = obj.get("formats")\n',
                    '        if "headers" in obj:\n',
                    '            model_data["headers"] = obj.get("headers")\n',
                    '        if "processing_mode" in obj:\n',
                    '            model_data["processing_mode"] = obj.get("processing_mode")\n',
                    '        if "proxy" in obj:\n',
                    '            model_data["proxy"] = ProxySettings.from_dict(',
                    'obj["proxy"]) if obj.get("proxy") is not None else None\n',
                    '        if "render_js" in obj:\n',
                    '            model_data["render_js"] = obj.get("render_js")\n',
                    '        if "timeout" in obj:\n',
                    '            model_data["timeout"] = obj.get("timeout")\n',
                    '        if "wait_config" in obj:\n',
                    '            model_data["wait_config"] = WaitConfig.from_dict(',
                    'obj["wait_config"]) if obj.get("wait_config") is not None else None\n',
                    '        _obj = cls.model_validate(model_data)\n',
                ),
            ),
        ],
        SDK_DIR / "geonode_scraper_sdk/models/proxy_settings.py": [
            (
                text(
                    '    type: Optional[ProxyType] = Field(',
                    'default=None, description="Type of proxy to use ',
                    "(datacenter or residential). Defaults to 'residential' "
                    'when omitted.")\n',
                ),
                text(
                    '    type: Optional[ProxyType] = Field(',
                    'default=ProxyType.RESIDENTIAL, description="Type of ',
                    "proxy to use (datacenter or residential). Defaults to "
                    "'residential' when omitted.\")\n",
                ),
            ),
            (
                '        _obj = cls.model_validate({\n'
                '            "country": obj.get("country"),\n'
                '            "type": obj.get("type")\n'
                '        })\n',
                '        model_data = {}\n'
                '        if "country" in obj:\n'
                '            model_data["country"] = obj.get("country")\n'
                '        if "type" in obj:\n'
                '            model_data["type"] = obj.get("type")\n'
                '        _obj = cls.model_validate(model_data)\n',
            ),
        ],
        SDK_DIR / "geonode_scraper_sdk/api/extraction_api.py": [
            (
                'from geonode_scraper_sdk.models.extract_request import ExtractRequest\n'
                'from geonode_scraper_sdk.models.extract_sync_response import ExtractSyncResponse\n',
                'from geonode_scraper_sdk.models.extract_async_response import ExtractAsyncResponse\n'
                'from geonode_scraper_sdk.models.extract_request import ExtractRequest\n'
                'from geonode_scraper_sdk.models.extract_sync_response import ExtractSyncResponse\n',
            ),
            (
                '    ) -> ExtractSyncResponse:\n',
                '    ) -> Union[ExtractSyncResponse, ExtractAsyncResponse]:\n',
            ),
            (
                '    ) -> ApiResponse[ExtractSyncResponse]:\n',
                '    ) -> ApiResponse[Union[ExtractSyncResponse, ExtractAsyncResponse]]:\n',
            ),
        ],
    }

    for path, replacements in replacement_map.items():
        if apply_replacements(path, replacements):
            changed_files.append(path)

    if changed_files:
        print("Postprocessed generated Python SDK files:")
        for path in changed_files:
            print(f"- {path.relative_to(REPO_ROOT)}")
    else:
        print("Generated Python SDK files already normalized.")


if __name__ == "__main__":
    main()
