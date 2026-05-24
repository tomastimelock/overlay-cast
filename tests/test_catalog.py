from overlay_cast import list_styles

EXPECTED_SLUGS = {
    "social_media_frame", "phone_screen_overlay", "notification_popups", "chat_messages",
    "live_stream_overlay", "like_hearts", "subscribe_button", "comment_storm",
    "progress_bar", "loading_spinner", "lower_third", "news_ticker", "scorebug",
    "breaking_news_frame", "map_pin_overlay", "callout_box", "redaction_bars",
    "warning_label", "poll_overlay", "watermark", "picture_in_picture",
    "split_screen_grid", "vertical_reels_layout", "podcast_waveform", "audio_visualizer",
}


def test_catalog_loads_25():
    styles = list_styles()
    assert len(styles) == 25


def test_all_expected_slugs_present():
    styles = set(list_styles())
    assert styles == EXPECTED_SLUGS
