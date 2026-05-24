import subprocess

import pytest


@pytest.fixture(scope="session")
def tiny_video(tmp_path_factory):
    out = tmp_path_factory.mktemp("clips") / "test.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "color=darkblue:s=320x240:d=4",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=4",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest",
            str(out),
        ],
        check=True,
        capture_output=True,
    )
    return out
