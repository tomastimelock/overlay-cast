from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw

from overlay_cast.config import OverlayConfig


def _rw(video_path: str):
    from video_fx.frames import read_frames, write_frames
    frames, info = read_frames(video_path)
    return frames, info, write_frames


def social_media_frame(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        bw = max(8, w // 30)
        draw.rectangle([0, 0, w - 1, h - 1], outline=(255, 255, 255, 220), width=bw)
        draw.rectangle([bw, bw, w - 1 - bw, h - 1 - bw], outline=(200, 200, 200, 120), width=2)
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output


def phone_screen_overlay(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        # Draw phone bezel
        bw = max(6, w // 20)
        draw.rectangle([0, 0, w - 1, h - 1], outline=(30, 30, 30, 240), width=bw)
        # Home indicator bar at bottom
        bar_h = max(4, h // 40)
        bar_w = w // 3
        bar_x = (w - bar_w) // 2
        draw.rectangle([bar_x, h - bw - bar_h, bar_x + bar_w, h - bw], fill=(255, 255, 255, 180))
        # Notch at top
        notch_w = w // 4
        notch_h = max(6, h // 30)
        notch_x = (w - notch_w) // 2
        draw.rectangle([notch_x, 0, notch_x + notch_w, notch_h], fill=(30, 30, 30, 240))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output
