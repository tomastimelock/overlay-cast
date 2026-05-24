from __future__ import annotations

import cv2
import numpy as np

from overlay_cast.config import OverlayConfig


def _rw(video_path: str):
    from video_fx.frames import read_frames, write_frames
    frames, info = read_frames(video_path)
    return frames, info, write_frames


def picture_in_picture(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        pip_w = w // 3
        pip_h = h // 3
        margin = max(8, min(w, h) // 30)
        pip_x = w - pip_w - margin
        pip_y = h - pip_h - margin
        small = cv2.resize(frame[:, :, :3], (pip_w, pip_h), interpolation=cv2.INTER_LINEAR)
        out = frame.copy()
        # Draw border
        out[pip_y - 2:pip_y + pip_h + 2, pip_x - 2:pip_x + pip_w + 2, :3] = 255
        out[pip_y - 2:pip_y + pip_h + 2, pip_x - 2:pip_x + pip_w + 2, 3] = 255
        out[pip_y:pip_y + pip_h, pip_x:pip_x + pip_w, :3] = small
        out[pip_y:pip_y + pip_h, pip_x:pip_x + pip_w, 3] = 255
        result.append(out)
    write_frames(result, info, video_path, config.output)
    return config.output


def split_screen_grid(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    result = []
    for frame in frames:
        h, w = frame.shape[:2]
        hw, hh = w // 2, h // 2
        small = cv2.resize(frame[:, :, :3], (hw, hh), interpolation=cv2.INTER_LINEAR)
        grid = np.zeros((h, w, 4), np.uint8)
        grid[:, :, 3] = 255
        # 2x2 grid of the same frame
        for gy in range(2):
            for gx in range(2):
                grid[gy * hh:(gy + 1) * hh, gx * hw:(gx + 1) * hw, :3] = small
        # Grid lines
        grid[:, hw - 1:hw + 1, :3] = 0
        grid[hh - 1:hh + 1, :, :3] = 0
        result.append(grid)
    write_frames(result, info, video_path, config.output)
    return config.output


def vertical_reels_layout(video_path: str, config: OverlayConfig) -> str:
    frames, info, write_frames = _rw(video_path)
    if not frames:
        write_frames(frames, info, video_path, config.output)
        return config.output

    src_h, src_w = frames[0].shape[:2]
    out_w, out_h = 360, 640  # 9:16 scaled down for speed

    target_h = int(out_h * 0.60)
    scale = target_h / src_h
    target_w = int(src_w * scale)
    if target_w > out_w:
        target_w = out_w
        target_h = int(src_h * out_w / src_w)

    result = []
    for frame in frames:
        rgb = frame[:, :, :3]
        # Blurred background
        bg = cv2.resize(rgb, (out_w, out_h), interpolation=cv2.INTER_LINEAR)
        bg = cv2.GaussianBlur(bg, (51, 51), 0)
        bg = np.clip(bg.astype(np.float32) * 0.6, 0, 255).astype(np.uint8)
        # Foreground
        fg = cv2.resize(rgb, (target_w, target_h), interpolation=cv2.INTER_LINEAR)
        y_off = (out_h - target_h) // 2
        x_off = (out_w - target_w) // 2
        out_frame = np.zeros((out_h, out_w, 4), np.uint8)
        out_frame[:, :, :3] = bg
        out_frame[:, :, 3] = 255
        out_frame[y_off:y_off + target_h, x_off:x_off + target_w, :3] = fg
        out_frame[y_off:y_off + target_h, x_off:x_off + target_w, 3] = 255
        result.append(out_frame)

    modified_info = dict(info)
    write_frames(result, modified_info, video_path, config.output)
    return config.output
