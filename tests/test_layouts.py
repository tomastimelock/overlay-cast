import os

import cv2

from overlay_cast import apply_overlay, render_vertical_reels_layout


def test_vertical_reels_produces_portrait(tiny_video, tmp_path):
    out = str(tmp_path / "reels.mp4")
    render_vertical_reels_layout(str(tiny_video), output=out)
    assert os.path.exists(out)
    cap = cv2.VideoCapture(out)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    # Output should be taller than wide (portrait/9:16)
    assert h > w


def test_picture_in_picture(tiny_video, tmp_path):
    out = str(tmp_path / "pip.mp4")
    apply_overlay(str(tiny_video), "picture_in_picture", output=out)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 0


def test_split_screen_grid(tiny_video, tmp_path):
    out = str(tmp_path / "grid.mp4")
    apply_overlay(str(tiny_video), "split_screen_grid", output=out)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 0
