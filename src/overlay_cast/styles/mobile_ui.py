from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw

from overlay_cast.config import OverlayConfig


def _rw(video_path: str):
    from video_fx.frames import read_frames, write_frames
    frames, info = read_frames(video_path)
    return frames, info, write_frames


def notification_popups(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        card_h = max(40, h // 8)
        card_w = w * 3 // 4
        card_x = (w - card_w) // 2
        margin = max(8, h // 40)
        # Draw notification card
        draw.rounded_rectangle(
            [card_x, margin, card_x + card_w, margin + card_h],
            radius=8, fill=(255, 255, 255, 220), outline=(200, 200, 200, 180), width=1
        )
        app_name = config.data.get("app_name", "Notification")
        msg = config.data.get("message", "You have a new message")
        draw.text((card_x + 12, margin + 6), app_name, fill=(80, 80, 80, 240))
        draw.text((card_x + 12, margin + card_h // 2), msg, fill=(40, 40, 40, 240))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output


def chat_messages(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        bubble_h = max(32, h // 10)
        bubble_w = w // 2
        margin = max(8, h // 40)
        # Left bubble
        draw.rounded_rectangle(
            [margin, h - 2 * bubble_h - 2 * margin, margin + bubble_w, h - bubble_h - 2 * margin],
            radius=12, fill=(240, 240, 240, 220)
        )
        draw.text((margin + 10, h - 2 * bubble_h - 2 * margin + 8),
                  config.data.get("left_msg", "Hello!"), fill=(40, 40, 40, 240))
        # Right bubble
        right_x = w - margin - bubble_w
        draw.rounded_rectangle(
            [right_x, h - bubble_h - margin, right_x + bubble_w, h - margin],
            radius=12, fill=(0, 132, 255, 220)
        )
        draw.text((right_x + 10, h - bubble_h - margin + 8),
                  config.data.get("right_msg", "Hey there!"), fill=(255, 255, 255, 240))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output
