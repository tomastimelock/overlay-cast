from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw

from overlay_cast.config import OverlayConfig


def _rw(video_path: str):
    from video_fx.frames import read_frames, write_frames
    frames, info = read_frames(video_path)
    return frames, info, write_frames


def progress_bar(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    n = len(frames)
    result = []
    for i, frame in enumerate(frames):
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        bar_h = max(4, h // 60)
        y = h - bar_h - 1
        # Background track
        draw.rectangle([0, y, w, y + bar_h], fill=(100, 100, 100, 160))
        # Progress fill
        progress = i / max(1, n - 1)
        fill_w = int(w * progress)
        color = config.data.get("color", (26, 143, 227))
        if isinstance(color, list):
            color = tuple(color)
        draw.rectangle([0, y, fill_w, y + bar_h], fill=(*color, 230) if len(color) == 3 else color)
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output


def loading_spinner(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    result = []
    for i, frame in enumerate(frames):
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        cx, cy = w // 2, h // 2
        r = min(w, h) // 8
        angle = (i * 12) % 360
        start = angle
        end = start + 270
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=start, end=end,
                 fill=(255, 255, 255, 220), width=max(3, r // 5))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output
