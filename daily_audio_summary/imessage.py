"""Send audio files via iMessage using macOS AppleScript."""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


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

    # AppleScript to send a file via Messages.app
    script = f"""\
tell application "Messages"
    set targetService to 1st account whose service type = iMessage
    set targetBuddy to participant "{recipient}" of targetService
    send POSIX file "{file_path}" to targetBuddy
end tell
"""

    if text:
        script = f"""\
tell application "Messages"
    set targetService to 1st account whose service type = iMessage
    set targetBuddy to participant "{recipient}" of targetService
    send "{text}" to targetBuddy
    send POSIX file "{file_path}" to targetBuddy
end tell
"""

    logger.info("Sending iMessage to %s with file %s", recipient, file_path)
    subprocess.run(
        ["osascript", "-e", script],
        check=True,
    )
    logger.info("iMessage sent successfully")
