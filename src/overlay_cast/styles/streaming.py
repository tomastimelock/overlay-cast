from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw

from overlay_cast.config import OverlayConfig


def _rw(video_path: str):
    from video_fx.frames import read_frames, write_frames
    frames, info = read_frames(video_path)
    return frames, info, write_frames


def live_stream_overlay(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        margin = max(8, w // 40)
        badge_h = max(20, h // 16)
        # LIVE badge
        draw.rectangle([margin, margin, margin + badge_h * 2, margin + badge_h],
                       fill=(255, 0, 0, 230))
        draw.text((margin + 4, margin + 2), "LIVE", fill=(255, 255, 255, 255))
        # Viewer count
        viewers = config.data.get("viewers", "1.2K")
        draw.text((margin, margin + badge_h + 4), f"👁 {viewers}", fill=(255, 255, 255, 220))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output


def like_hearts(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    rng = np.random.default_rng(42)
    result = []
    for i, frame in enumerate(frames):
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        n_hearts = config.data.get("count", 5)
        for j in range(n_hearts):
            x = int(rng.uniform(w * 0.7, w * 0.95))
            y = int(rng.uniform(h * 0.2, h * 0.8))
            alpha = int(rng.uniform(150, 230))
            draw.text((x, y), "♥", fill=(255, 80, 120, alpha))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output


def subscribe_button(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        btn_h = max(28, h // 12)
        btn_w = max(100, w // 4)
        x = (w - btn_w) // 2
        y = h - btn_h - max(20, h // 15)
        draw.rounded_rectangle([x, y, x + btn_w, y + btn_h], radius=4,
                               fill=(255, 0, 0, 230))
        draw.text((x + btn_w // 2 - 35, y + 6), "SUBSCRIBE", fill=(255, 255, 255, 255))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output


def comment_storm(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    rng = np.random.default_rng(42)
    comments = config.data.get("comments", ["Great video!", "Love it!", "🔥🔥🔥", "Amazing!"])
    result = []
    for i, frame in enumerate(frames):
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        n = min(len(comments), 4)
        for j in range(n):
            x = int(rng.uniform(5, w * 0.5))
            y = int(h * 0.3 + j * (h * 0.12))
            alpha = max(100, 220 - i * 2)
            draw.rectangle([x - 2, y - 2, x + len(comments[j]) * 7 + 4, y + 16],
                           fill=(0, 0, 0, min(alpha, 160)))
            draw.text((x, y), comments[j % len(comments)], fill=(255, 255, 255, min(alpha, 240)))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output
