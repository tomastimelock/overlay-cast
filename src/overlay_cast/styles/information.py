from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw

from overlay_cast.config import OverlayConfig


def _rw(video_path: str):
    from video_fx.frames import read_frames, write_frames
    frames, info = read_frames(video_path)
    return frames, info, write_frames


def map_pin_overlay(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    location = config.data.get("location", "Location")
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        cx, cy = w // 2, h // 3
        r = max(12, min(w, h) // 20)
        # Pin circle
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 50, 50, 220), outline=(255, 255, 255, 200), width=2)
        # Pin tail
        draw.polygon([(cx - r // 2, cy + r - 2), (cx + r // 2, cy + r - 2), (cx, cy + r * 2)],
                     fill=(220, 50, 50, 200))
        # Label
        label_y = cy + r * 2 + 4
        draw.rectangle([cx - 40, label_y, cx + 40, label_y + 18], fill=(0, 0, 0, 180))
        draw.text((cx - 35, label_y + 2), location, fill=(255, 255, 255, 230))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output


def callout_box(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    text = config.data.get("text", "Note")
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        box_w = max(120, w // 4)
        box_h = max(36, h // 8)
        bx = w // 4
        by = h // 4
        draw.rounded_rectangle([bx, by, bx + box_w, by + box_h], radius=6, fill=(255, 255, 255, 220))
        draw.rounded_rectangle([bx, by, bx + box_w, by + box_h], radius=6, outline=(26, 143, 227, 200), width=2)
        # Pointer triangle
        draw.polygon([(bx + 20, by + box_h), (bx + 36, by + box_h), (bx + 28, by + box_h + 14)],
                     fill=(255, 255, 255, 200))
        draw.text((bx + 10, by + 10), text, fill=(40, 40, 40, 240))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output


def redaction_bars(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        arr = frame.copy()
        # Redact center horizontal band
        y1 = int(h * 0.35)
        y2 = int(h * 0.55)
        arr[y1:y2, :, :3] = 0
        arr[y1:y2, :, 3] = 255
        result.append(arr)
    write_frames(result, info, video_path, config.output)
    return config.output


def warning_label(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    msg = config.data.get("message", "WARNING")
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        lw = max(160, w // 3)
        lh = max(40, h // 8)
        lx = (w - lw) // 2
        ly = max(10, h // 20)
        # Yellow warning box with black border
        draw.rectangle([lx, ly, lx + lw, ly + lh], fill=(255, 220, 0, 220), outline=(0, 0, 0, 240), width=2)
        draw.text((lx + 10, ly + 8), f"⚠ {msg}", fill=(0, 0, 0, 240))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output


def poll_overlay(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    question = config.data.get("question", "What do you think?")
    opt_a = config.data.get("option_a", "Option A")
    opt_b = config.data.get("option_b", "Option B")
    pct_a = config.data.get("pct_a", 60)
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        pw = max(200, w // 3)
        ph = max(100, h // 4)
        px = (w - pw) // 2
        py = (h - ph) // 2
        draw.rectangle([px, py, px + pw, py + ph], fill=(20, 20, 20, 200))
        draw.text((px + 8, py + 6), question, fill=(255, 255, 255, 240))
        bar_y = py + 32
        bar_h = max(16, ph // 5)
        bar_total = pw - 16
        # Option A bar
        draw.rectangle([px + 8, bar_y, px + 8 + bar_total, bar_y + bar_h], fill=(60, 60, 60, 180))
        draw.rectangle([px + 8, bar_y, px + 8 + int(bar_total * pct_a / 100), bar_y + bar_h],
                       fill=(26, 143, 227, 220))
        draw.text((px + 12, bar_y + 2), f"{opt_a} {pct_a}%", fill=(255, 255, 255, 230))
        bar_y2 = bar_y + bar_h + 8
        draw.rectangle([px + 8, bar_y2, px + 8 + bar_total, bar_y2 + bar_h], fill=(60, 60, 60, 180))
        draw.rectangle([px + 8, bar_y2, px + 8 + int(bar_total * (100 - pct_a) / 100), bar_y2 + bar_h],
                       fill=(227, 80, 26, 220))
        draw.text((px + 12, bar_y2 + 2), f"{opt_b} {100 - pct_a}%", fill=(255, 255, 255, 230))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output
