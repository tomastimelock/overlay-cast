from __future__ import annotations

import json
from pathlib import Path

from overlay_cast.exceptions import CatalogLoadError, StyleNotFoundError

_CATALOG_PATH = Path(__file__).parent.parent / "data" / "overlay_styles.json"
_catalog: dict[str, dict] | None = None


def _load() -> dict[str, dict]:
    global _catalog
    if _catalog is not None:
        return _catalog
    data = json.loads(_CATALOG_PATH.read_text(encoding="utf-8"))
    entries = data["transitions"]
    if len(entries) != 25:
        raise CatalogLoadError(f"Expected 25 styles, got {len(entries)}")
    _catalog = {e["slug"]: e for e in entries}
    return _catalog


def list_styles() -> list[str]:
    return sorted(_load().keys())


def get_style(slug: str) -> dict:
    cat = _load()
    if slug not in cat:
        raise StyleNotFoundError(slug)
    return cat[slug]
