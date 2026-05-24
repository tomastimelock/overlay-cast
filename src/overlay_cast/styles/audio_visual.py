from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from overlay_cast.config import OverlayConfig


def _rw(video_path: str):
    from video_fx.frames import read_frames, write_frames
    frames, info = read_frames(video_path)
    return frames, info, write_frames


def podcast_waveform(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    n_bars = 40
    result = []
    for i, frame in enumerate(frames):
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        zone_h = h // 4
        zone_y = h - zone_h - max(4, h // 40)
        # Semi-transparent background strip
        draw.rectangle([0, zone_y - 4, w, h - max(4, h // 40)], fill=(0, 0, 0, 120))
        bar_w = max(2, (w - 20) // n_bars - 1)
        for j in range(n_bars):
            amplitude = 0.3 + 0.7 * abs(math.sin(j * 0.4 + i * 0.1))
            bar_h = int(zone_h * amplitude)
            bx = 10 + j * (bar_w + 1)
            by = zone_y + (zone_h - bar_h) // 2
            draw.rectangle([bx, by, bx + bar_w, by + bar_h], fill=(26, 143, 227, 200))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output


def audio_visualizer(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    n_bars = 32
    result = []
    for i, frame in enumerate(frames):
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        zone_h = h // 3
        zone_y = h - zone_h
        draw.rectangle([0, zone_y, w, h], fill=(0, 0, 0, 140))
        bar_w = max(2, (w - 10) // n_bars - 2)
        for j in range(n_bars):
            freq = j / n_bars
            amplitude = max(0.05, abs(math.sin(freq * math.pi * 3 + i * 0.15)))
            bar_h = int(zone_h * amplitude * 0.9)
            bx = 5 + j * (bar_w + 2)
            by = h - bar_h - 2
            # Color gradient from blue to purple
            r = int(100 * freq)
            g = int(20 + 50 * (1 - freq))
            b = int(220 - 80 * freq)
            draw.rectangle([bx, by, bx + bar_w, h - 2], fill=(r, g, b, 220))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output
