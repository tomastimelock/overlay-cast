import pytest

from overlay_cast import apply_overlay, list_styles

ALL_SLUGS = list_styles()


@pytest.mark.parametrize("slug", ALL_SLUGS)
def test_style_renders(tiny_video, tmp_path, slug):
    out = str(tmp_path / f"{slug}.mp4")
    apply_overlay(str(tiny_video), slug, output=out)
    import os
    assert os.path.exists(out)
    assert os.path.getsize(out) > 0
