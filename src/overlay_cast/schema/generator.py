from __future__ import annotations

import json

from overlay_cast.config import OverlayConfig


def generate_schema() -> dict:
    return OverlayConfig.model_json_schema()


def generate_schema_json() -> str:
    return json.dumps(generate_schema(), indent=2)
