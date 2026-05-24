from __future__ import annotations

from overlay_cast.exceptions import StyleNotFoundError
from overlay_cast.styles.audio_visual import audio_visualizer, podcast_waveform
from overlay_cast.styles.branding import watermark
from overlay_cast.styles.broadcast import breaking_news_frame, lower_third, news_ticker, scorebug
from overlay_cast.styles.information import (
    callout_box,
    map_pin_overlay,
    poll_overlay,
    redaction_bars,
    warning_label,
)
from overlay_cast.styles.layout import picture_in_picture, split_screen_grid, vertical_reels_layout
from overlay_cast.styles.mobile_ui import chat_messages, notification_popups
from overlay_cast.styles.mockups import phone_screen_overlay, social_media_frame
from overlay_cast.styles.progress import loading_spinner, progress_bar
from overlay_cast.styles.streaming import (
    comment_storm,
    like_hearts,
    live_stream_overlay,
    subscribe_button,
)

STYLE_REGISTRY: dict[str, object] = {
    "social_media_frame": social_media_frame,
    "phone_screen_overlay": phone_screen_overlay,
    "notification_popups": notification_popups,
    "chat_messages": chat_messages,
    "live_stream_overlay": live_stream_overlay,
    "like_hearts": like_hearts,
    "subscribe_button": subscribe_button,
    "comment_storm": comment_storm,
    "progress_bar": progress_bar,
    "loading_spinner": loading_spinner,
    "lower_third": lower_third,
    "news_ticker": news_ticker,
    "scorebug": scorebug,
    "breaking_news_frame": breaking_news_frame,
    "map_pin_overlay": map_pin_overlay,
    "callout_box": callout_box,
    "redaction_bars": redaction_bars,
    "warning_label": warning_label,
    "poll_overlay": poll_overlay,
    "watermark": watermark,
    "picture_in_picture": picture_in_picture,
    "split_screen_grid": split_screen_grid,
    "vertical_reels_layout": vertical_reels_layout,
    "podcast_waveform": podcast_waveform,
    "audio_visualizer": audio_visualizer,
}


def get_recipe(slug: str):
    if slug not in STYLE_REGISTRY:
        raise StyleNotFoundError(slug)
    return STYLE_REGISTRY[slug]
