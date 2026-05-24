from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class OverlayConfig(BaseModel):
    style: str = ""
    output: str = "out.mp4"
    position: Literal["top", "center", "bottom", "lower_third", "custom"] = "lower_third"
    position_custom: tuple[int, int] | None = None
    safe_area: Literal["minimal", "standard", "max", "broadcast"] = "standard"
    font_family: str | None = None
    font_size: int | None = None
    color: str | None = None
    background_color: str | None = None
    background_opacity: float = 0.7
    start_time: float = 0.0
    duration: float | None = None
    in_animation: str | None = None
    out_animation: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)
    model_config = ConfigDict(extra="forbid")
