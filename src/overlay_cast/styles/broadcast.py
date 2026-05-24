from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw

from overlay_cast.config import OverlayConfig


def _rw(video_path: str):
    from video_fx.frames import read_frames, write_frames
    frames, info = read_frames(video_path)
    return frames, info, write_frames


def lower_third(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    name = config.data.get("name", "Speaker Name")
    title = config.data.get("title", "Title / Organization")
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        bar_h = max(48, h // 7)
        y = h - bar_h - max(16, h // 20)
        # Main bar
        draw.rectangle([0, y, w * 2 // 3, y + bar_h], fill=(20, 20, 120, 210))
        # Accent line
        accent_h = max(4, bar_h // 10)
        draw.rectangle([0, y, w * 2 // 3, y + accent_h], fill=(26, 143, 227, 240))
        # Text
        draw.text((12, y + 6), name, fill=(255, 255, 255, 240))
        draw.text((12, y + bar_h // 2 + 2), title, fill=(200, 220, 255, 220))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output


def news_ticker(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    ticker_text = config.data.get("text", "BREAKING: Latest news headline scrolling here — Stay tuned for updates")
    result = []
    for i, frame in enumerate(frames):
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        bar_h = max(24, h // 14)
        y = h - bar_h
        # Red ticker background
        draw.rectangle([0, y, w, h], fill=(200, 0, 0, 220))
        # Scrolling text (static for simplicity)
        offset = (i * 3) % (w + len(ticker_text) * 8)
        draw.text((w - offset, y + 4), ticker_text, fill=(255, 255, 255, 240))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output


def scorebug(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    home = config.data.get("home", "HME")
    away = config.data.get("away", "AWY")
    home_score = config.data.get("home_score", 0)
    away_score = config.data.get("away_score", 0)
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        box_w = max(120, w // 5)
        box_h = max(36, h // 10)
        margin = max(8, w // 60)
        # Score box
        draw.rectangle([margin, margin, margin + box_w, margin + box_h], fill=(20, 20, 20, 210))
        draw.text((margin + 6, margin + 4), f"{home}  {home_score}", fill=(255, 255, 255, 240))
        draw.text((margin + 6, margin + box_h // 2 + 2), f"{away}  {away_score}", fill=(200, 200, 255, 240))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output


def breaking_news_frame(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    headline = config.data.get("headline", "BREAKING NEWS")
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        img = Image.fromarray(frame, "RGBA")
        draw = ImageDraw.Draw(img)
        banner_h = max(40, h // 9)
        # Top red banner
        draw.rectangle([0, 0, w, banner_h], fill=(200, 10, 10, 220))
        draw.text((12, 8), "BREAKING", fill=(255, 255, 255, 255))
        # Bottom info bar
        bot_h = max(32, h // 12)
        draw.rectangle([0, h - bot_h, w, h], fill=(20, 20, 20, 210))
        draw.text((12, h - bot_h + 6), headline, fill=(255, 255, 200, 240))
        result.append(np.array(img))
    write_frames(result, info, video_path, config.output)
    return config.output
