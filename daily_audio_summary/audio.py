"""Text-to-speech audio conversion."""

from __future__ import annotations

from pathlib import Path


def text_to_audio(text: str, output_path: str) -> Path:
    """Convert text to an audio file using gTTS."""
    from gtts import gTTS

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    tts = gTTS(text=text, lang="en")
    tts.save(str(out))
    return out
