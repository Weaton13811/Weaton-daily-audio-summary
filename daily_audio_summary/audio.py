"""Text-to-speech using macOS built-in voices via the `say` command."""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def text_to_audio(text: str, output_path: str, voice: str = "Evan (Premium)") -> Path:
    """Convert text to an audio file using macOS `say`.

    The `say` command outputs AIFF natively. We convert to AAC (m4a) for a
    compact file that plays everywhere, including iMessage previews.
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    aiff_path = out.with_suffix(".aiff")

    # Generate speech with the selected macOS voice
    subprocess.run(
        ["say", "-v", voice, "-o", str(aiff_path), text],
        check=True,
        timeout=300,
    )

    # Convert AIFF -> AAC (.m4a) using afconvert (ships with macOS)
    m4a_path = out.with_suffix(".m4a")
    subprocess.run(
        [
            "afconvert",
            "-f", "m4af",
            "-d", "aac",
            "-b", "128000",
            str(aiff_path),
            str(m4a_path),
        ],
        check=True,
        timeout=120,
    )

    # Clean up intermediate AIFF
    aiff_path.unlink(missing_ok=True)

    logger.info("Audio saved to %s (voice: %s)", m4a_path, voice)
    return m4a_path


def list_voices() -> list[str]:
    """Return available macOS voice names."""
    result = subprocess.run(
        ["say", "-v", "?"],
        capture_output=True,
        text=True,
        check=True,
    )
    voices = []
    for line in result.stdout.splitlines():
        # Format: "Name  lang  # description"
        name = line.split("#")[0].strip().rsplit(None, 1)[0] if "#" in line else ""
        if name:
            voices.append(name)
    return voices
