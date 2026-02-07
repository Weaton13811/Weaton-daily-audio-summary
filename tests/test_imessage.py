"""Tests for the iMessage module."""

import pytest

from daily_audio_summary.imessage import send_imessage


def test_send_imessage_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError, match="Audio file not found"):
        send_imessage(tmp_path / "nonexistent.m4a", "+15551234567")


def test_send_imessage_no_recipient(tmp_path):
    audio = tmp_path / "test.m4a"
    audio.write_bytes(b"fake audio")
    with pytest.raises(ValueError, match="No iMessage recipient"):
        send_imessage(audio, "")
