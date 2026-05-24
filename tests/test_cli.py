from typer.testing import CliRunner

from overlay_cast.cli import app

runner = CliRunner()


def test_cli_list():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    lines = [l for l in result.output.strip().splitlines() if l.strip()]
    assert len(lines) == 25


def test_cli_schema():
    result = runner.invoke(app, ["schema"])
    assert result.exit_code == 0
    assert "OverlayConfig" in result.output or "style" in result.output


def test_cli_apply(tiny_video, tmp_path):
    out = str(tmp_path / "cli_out.mp4")
    result = runner.invoke(app, ["apply", "--video", str(tiny_video), "--style", "watermark", "--out", out])
    assert result.exit_code == 0
    import os
    assert os.path.exists(out)


def test_cli_lower_third(tiny_video, tmp_path):
    out = str(tmp_path / "lt.mp4")
    result = runner.invoke(app, [
        "lower-third", "--video", str(tiny_video),
        "--name", "Test Name", "--title", "Test Title", "--out", out
    ])
    assert result.exit_code == 0
