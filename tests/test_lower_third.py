import os

from overlay_cast import add_lower_third


def test_lower_third_name_title(tiny_video, tmp_path):
    out = str(tmp_path / "lt.mp4")
    add_lower_third(str(tiny_video), name="Dr. Chen", title="Researcher", output=out)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 0


def test_lower_third_defaults(tiny_video, tmp_path):
    out = str(tmp_path / "lt2.mp4")
    add_lower_third(str(tiny_video), output=out)
    assert os.path.exists(out)
