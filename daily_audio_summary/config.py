"""Configuration handling for daily-audio-summary."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_PATH = "config.json"

DEFAULTS: dict[str, Any] = {
    "location": "Binghamton, NY",
    "output_dir": "output",
    "claude_model": "claude-sonnet-4-5-20250929",
    "tts_voice": "Evan (Premium)",
    "imessage_to": "",
    "rss_feeds": [
        "https://www.wbng.com/news/local/feed/",
        "https://spectrumlocalnews.com/nys/binghamton.rss",
        "https://www.pressconnects.com/rss/news/",
    ],
    "google_news_query": "Binghamton NY local news",
}


def load_config(path: str | None = None) -> dict[str, Any]:
    """Load configuration from a JSON file, with env-var overrides."""
    config_path = path or os.environ.get("DAS_CONFIG", DEFAULT_CONFIG_PATH)

    config: dict[str, Any] = {}
    if Path(config_path).exists():
        with open(config_path) as f:
            config = json.load(f)

    for key, default in DEFAULTS.items():
        config.setdefault(key, default)

    # Allow env-var overrides for secrets and key settings
    if api_key := os.environ.get("ANTHROPIC_API_KEY"):
        config["anthropic_api_key"] = api_key
    if imessage_to := os.environ.get("DAS_IMESSAGE_TO"):
        config["imessage_to"] = imessage_to

    return config
