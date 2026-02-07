"""CLI entry point for daily-audio-summary."""

from __future__ import annotations

import argparse
import logging
from datetime import datetime
from pathlib import Path

from daily_audio_summary.audio import text_to_audio
from daily_audio_summary.config import load_config
from daily_audio_summary.imessage import send_imessage
from daily_audio_summary.news import gather_news
from daily_audio_summary.summarizer import summarize

logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a daily audio news briefing")
    parser.add_argument("--config", help="Path to config.json")
    parser.add_argument("--no-send", action="store_true", help="Skip iMessage delivery")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    config = load_config(args.config)

    # 1. Gather local news
    logger.info("Gathering news for %s...", config["location"])
    articles = gather_news(config)
    logger.info("Found %d articles", len(articles))

    # 2. Summarize into a morning briefing script via Claude
    logger.info("Generating briefing script with Claude...")
    script = summarize(articles, config)
    logger.info("Script ready (%d chars)", len(script))

    # 3. Convert to audio
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path(config["output_dir"])
    output_path = str(output_dir / f"briefing-{today}.m4a")
    logger.info("Converting to audio with voice '%s'...", config["tts_voice"])
    audio_file = text_to_audio(script, output_path, voice=config["tts_voice"])
    logger.info("Audio saved: %s", audio_file)

    # 4. Send via iMessage
    if not args.no_send and config.get("imessage_to"):
        logger.info("Sending via iMessage to %s...", config["imessage_to"])
        send_imessage(
            audio_file,
            config["imessage_to"],
            text=f"Good morning! Here's your Binghamton news briefing for {today}.",
        )
        logger.info("Delivered!")
    elif not config.get("imessage_to"):
        logger.warning("No iMessage recipient configured — skipping delivery")

    print(f"Done! Audio briefing: {audio_file}")


if __name__ == "__main__":
    main()
