from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw

from overlay_cast.config import OverlayConfig


def _rw(video_path: str):
    from video_fx.frames import read_frames, write_frames
    frames, info = read_frames(video_path)
    return frames, info, write_frames


def watermark(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    text = config.data.get("text", "© Trollfabriken")
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        margin = max(8, min(w, h) // 30)
        draw.text((w - 120 - margin, h - 20 - margin), text, fill=(255, 255, 255, 100))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output
