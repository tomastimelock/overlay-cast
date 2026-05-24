import os

from overlay_cast import apply_overlay


def test_podcast_waveform(tiny_video, tmp_path):
    out = str(tmp_path / "wave.mp4")
    apply_overlay(str(tiny_video), "podcast_waveform", output=out)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 0


def test_audio_visualizer(tiny_video, tmp_path):
    out = str(tmp_path / "viz.mp4")
    apply_overlay(str(tiny_video), "audio_visualizer", output=out)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 0
