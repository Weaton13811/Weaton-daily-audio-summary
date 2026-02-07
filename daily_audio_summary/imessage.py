"""Send audio files via iMessage using macOS AppleScript."""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def _escape_applescript(s: str) -> str:
    """Escape a string for safe interpolation into AppleScript."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def send_imessage(file_path: str | Path, recipient: str, text: str = "") -> None:
    """Send a file (and optional text) via iMessage using AppleScript.

    Args:
        file_path: Path to the audio file to attach.
        recipient: Phone number or email of the iMessage recipient.
        text: Optional text message to accompany the file.
    """
    file_path = Path(file_path).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    if not recipient:
        raise ValueError(
            "No iMessage recipient configured. "
            "Set 'imessage_to' in config or DAS_IMESSAGE_TO env var."
        )

    safe_recipient = _escape_applescript(recipient)
    safe_path = _escape_applescript(str(file_path))

    if text:
        safe_text = _escape_applescript(text)
        script = (
            'tell application "Messages"\n'
            "    set targetService to 1st account"
            " whose service type = iMessage\n"
            f'    set targetBuddy to participant "{safe_recipient}"'
            " of targetService\n"
            f'    send "{safe_text}" to targetBuddy\n'
            f'    send POSIX file "{safe_path}" to targetBuddy\n'
            "end tell"
        )
    else:
        script = (
            'tell application "Messages"\n'
            "    set targetService to 1st account"
            " whose service type = iMessage\n"
            f'    set targetBuddy to participant "{safe_recipient}"'
            " of targetService\n"
            f'    send POSIX file "{safe_path}" to targetBuddy\n'
            "end tell"
        )

    logger.info("Sending iMessage to %s with file %s", recipient, file_path)
    subprocess.run(
        ["osascript", "-e", script],
        check=True,
        timeout=60,
    )
    logger.info("iMessage sent successfully")
