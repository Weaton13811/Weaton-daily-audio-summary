"""CLI entry point for daily-audio-summary."""

from daily_audio_summary.audio import text_to_audio
from daily_audio_summary.config import load_config
from daily_audio_summary.summarizer import summarize


def main() -> None:
    config = load_config()
    summary = summarize(config["content"])
    output_path = config.get("output_path", "output/summary.mp3")
    text_to_audio(summary, output_path)
    print(f"Audio summary saved to {output_path}")


if __name__ == "__main__":
    main()
