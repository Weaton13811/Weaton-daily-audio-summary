"""Configuration handling for daily-audio-summary."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_PATH = "config.json"


def load_config(path: str | None = None) -> dict[str, Any]:
    """Load configuration from a JSON file or environment variables."""
    config_path = path or os.environ.get("DAS_CONFIG", DEFAULT_CONFIG_PATH)

    config: dict[str, Any] = {}
    if Path(config_path).exists():
        with open(config_path) as f:
            config = json.load(f)

    config.setdefault("output_path", "output/summary.mp3")
    config.setdefault("content", "")
    return config
