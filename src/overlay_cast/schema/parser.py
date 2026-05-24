from __future__ import annotations

import json

from pydantic import ValidationError

from overlay_cast.config import OverlayConfig
from overlay_cast.exceptions import ConfigError


def parse_config(data: dict | str) -> OverlayConfig:
    if isinstance(data, str):
        data = json.loads(data)
    try:
        return OverlayConfig(**data)
    except (ValidationError, TypeError) as exc:
        raise ConfigError(str(exc)) from exc
