from __future__ import annotations

import logging

from overlay_cast.config import OverlayConfig
from overlay_cast.styles.loader import get_style
from overlay_cast.styles.loader import list_styles as _list_styles
from overlay_cast.styles.recipes import get_recipe

logger = logging.getLogger(__name__)


def apply_overlay(
    video: str,
    style: str,
    output: str = "out.mp4",
    config: OverlayConfig | None = None,
    **kwargs,
) -> str:
    if config is None:
        config = OverlayConfig(style=style, output=output, **kwargs)
    else:
        object.__setattr__(config, "output", output)
    recipe = get_recipe(style)
    logger.info("Applying style %r to %r -> %r", style, video, output)
    return recipe(video, config)


def add_lower_third(
    video: str,
    name: str = "Speaker Name",
    title: str = "",
    style: str = "lower_third",
    output: str = "out.mp4",
    **kwargs,
) -> str:
    data = kwargs.pop("data", {})
    data.setdefault("name", name)
    data.setdefault("title", title)
    return apply_overlay(video, style, output=output, data=data, **kwargs)


def render_phone_mockup(
    inner_video: str,
    output: str = "mocked.mp4",
    style: str = "phone_screen_overlay",
    **kwargs,
) -> str:
    return apply_overlay(inner_video, style, output=output, **kwargs)


def render_split_screen(
    videos: list[str],
    layout: str = "horizontal",
    output: str = "split.mp4",
    **kwargs,
) -> str:
    src = videos[0] if videos else ""
    return apply_overlay(src, "split_screen_grid", output=output, **kwargs)


def render_vertical_reels_layout(
    video: str,
    output: str = "reels.mp4",
    **kwargs,
) -> str:
    return apply_overlay(video, "vertical_reels_layout", output=output, **kwargs)


def render_waveform(
    video: str,
    audio: str | None = None,
    style: str = "podcast_waveform",
    output: str = "wave.mp4",
    **kwargs,
) -> str:
    return apply_overlay(video, style, output=output, **kwargs)


def list_styles() -> list[str]:
    return _list_styles()


def get_style_info(slug: str) -> dict:
    return get_style(slug)
