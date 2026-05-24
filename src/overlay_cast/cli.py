from __future__ import annotations

import json

import typer

from overlay_cast.api import add_lower_third, apply_overlay, list_styles, render_split_screen
from overlay_cast.schema.generator import generate_schema_json

app = typer.Typer(name="overlay-cast", help="Social UI and broadcast overlays for video.")


@app.command()
def apply(
    video: str = typer.Option(..., "--video", "-v", help="Input video path"),
    style: str = typer.Option(..., "--style", "-s", help="Style slug"),
    out: str = typer.Option("out.mp4", "--out", "-o", help="Output path"),
) -> None:
    result = apply_overlay(video, style, output=out)
    typer.echo(result)


@app.command("lower-third")
def lower_third_cmd(
    video: str = typer.Option(..., "--video", "-v"),
    name: str = typer.Option("Speaker", "--name", "-n"),
    title: str = typer.Option("", "--title", "-t"),
    out: str = typer.Option("out.mp4", "--out", "-o"),
) -> None:
    result = add_lower_third(video, name=name, title=title, output=out)
    typer.echo(result)


@app.command()
def phone(
    inner: str = typer.Option(..., "--inner", "-i"),
    out: str = typer.Option("mocked.mp4", "--out", "-o"),
) -> None:
    result = apply_overlay(inner, "phone_screen_overlay", output=out)
    typer.echo(result)


@app.command()
def split(
    videos: list[str] = typer.Option(..., "--videos"),
    layout: str = typer.Option("horizontal", "--layout", "-l"),
    out: str = typer.Option("split.mp4", "--out", "-o"),
) -> None:
    result = render_split_screen(list(videos), layout=layout, output=out)
    typer.echo(result)


@app.command()
def waveform(
    video: str = typer.Option(..., "--video", "-v"),
    audio: str = typer.Option(None, "--audio", "-a"),
    out: str = typer.Option("wave.mp4", "--out", "-o"),
) -> None:
    result = apply_overlay(video, "podcast_waveform", output=out)
    typer.echo(result)


@app.command("list")
def list_cmd() -> None:
    for slug in list_styles():
        typer.echo(slug)


@app.command()
def info(slug: str = typer.Argument(..., help="Style slug")) -> None:
    from overlay_cast.api import get_style_info
    entry = get_style_info(slug)
    typer.echo(json.dumps(entry, indent=2))


@app.command()
def preview(
    style: str = typer.Option(..., "--style", "-s"),
    out: str = typer.Option("preview.mp4", "--out", "-o"),
) -> None:
    import subprocess
    tmp = "preview_src.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=gray:s=320x240:d=4",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", tmp
    ], check=True, capture_output=True)
    result = apply_overlay(tmp, style, output=out)
    typer.echo(result)


@app.command()
def schema() -> None:
    typer.echo(generate_schema_json())


def main() -> None:
    app()


if __name__ == "__main__":
    main()
