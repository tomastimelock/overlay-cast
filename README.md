# overlay-cast

25 social UI and broadcast overlay styles for video — lower thirds, news tickers, phone mockups, live stream HUDs, split screen, vertical Reels layout, and podcast waveforms.

```python
from overlay_cast import apply_overlay, add_lower_third, OverlayConfig

# Add a lower third
add_lower_third("interview.mp4", name="Dr. Chen", title="Researcher", output="captioned.mp4")

# Live stream overlay
apply_overlay("raw.mp4", style="live_stream_overlay", output="streamed.mp4")

# Convert landscape to vertical Reels format
apply_overlay("landscape.mp4", style="vertical_reels_layout", output="reels.mp4")
```

Part of the Trollfabriken video-effects family: `video-fx` · `watch-cast` · `overlay-cast` · `scene-fx`.

Built at Trollfabriken AITrix AB · PyPI: `opusmorale` · GitHub: `tomastimelock`
