"""JSON export plugin for krizky.

Generates a JSON sidecar file alongside each HTML page that has a ``json:``
section in its page config. The output mirrors the HTML path structure under
a ``jsons/`` subdirectory of the site output.

Config example::

    pages:
      vsechna_mista:
        path: /mista.html
        template: mista.html
        json:
          fields: [slug, nazev, latitude, longitude]
          exclude: [interni_pole]
          pretty: true
"""

import json as _json
from pathlib import Path, PurePosixPath

from krizky.hooks import hookimpl

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _filter_record(record: dict, fields, exclude: list[str]) -> dict:
    if isinstance(fields, list):
        record = {k: v for k, v in record.items() if k in fields}
    if exclude:
        record = {k: v for k, v in record.items() if k not in exclude}
    return record


def _json_out_path(html_path: str, output_dir: Path) -> Path:
    """Return output path for a JSON file mirroring the given HTML path.

    Example: '/mista.html' → <output_dir>/jsons/mista.json
    """
    p = PurePosixPath(html_path.lstrip("/"))
    return output_dir / "jsons" / p.with_suffix(".json")


def _write_json(data: list | dict, html_path: str, output_dir: Path, pretty: bool) -> None:
    out = _json_out_path(html_path, output_dir)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        _json.dumps(data, ensure_ascii=False, indent=2 if pretty else None),
        encoding="utf-8",
    )


def _write_json_list(
    records: list[dict],
    base_html_path: str,
    output_dir: Path,
    json_cfg: dict,
) -> None:
    """Write a flat JSON array to jsons/<base_html_path>.json (pagination ignored)."""
    fields = json_cfg.get("fields", "*")
    exclude: list[str] = json_cfg.get("exclude") or []
    _write_json(
        [_filter_record(dict(r), fields, exclude) for r in records],
        base_html_path,
        output_dir,
        json_cfg.get("pretty", False),
    )


def _write_json_record(
    record: dict,
    html_path: str,
    output_dir: Path,
    json_cfg: dict,
) -> None:
    """Write a single JSON object to jsons/<html_path>.json (detail pages)."""
    fields = json_cfg.get("fields", "*")
    exclude: list[str] = json_cfg.get("exclude") or []
    _write_json(
        _filter_record(dict(record), fields, exclude),
        html_path,
        output_dir,
        json_cfg.get("pretty", False),
    )


# ---------------------------------------------------------------------------
# Plugin
# ---------------------------------------------------------------------------


class JsonExportPlugin:
    """Writes JSON sidecar files for pages that have a 'json:' config section.

    Fires on the ``after_page_written`` hook. Generates:
    - Simple / category pages: ``jsons/<page>.json`` — array of all records.
    - Detail pages: ``jsons/<record-slug>.json`` — single object per record.
    """

    @hookimpl
    def after_page_written(
        self,
        page_cfg: dict,
        html_path: str,
        output_dir: Path,
        records: list[dict],
        config: dict,
    ) -> None:
        json_cfg = page_cfg.get("json")
        if json_cfg is None:
            return
        if page_cfg.get("detail"):
            if records:
                _write_json_record(records[0], html_path, output_dir, json_cfg)
        else:
            _write_json_list(records, html_path, output_dir, json_cfg)


plugin = JsonExportPlugin()
