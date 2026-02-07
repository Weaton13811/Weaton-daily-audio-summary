"""Tests for the summarizer module."""

from daily_audio_summary.summarizer import summarize


def test_summarize_empty_string():
    assert summarize("") == ""


def test_summarize_single_sentence():
    result = summarize("Hello world.")
    assert result == "Hello world."


def test_summarize_respects_max_sentences():
    content = "First. Second. Third. Fourth. Fifth. Sixth. Seventh."
    result = summarize(content, max_sentences=3)
    assert result == "First. Second. Third."


def test_summarize_default_max():
    content = "One. Two. Three. Four. Five. Six. Seven."
    result = summarize(content)
    sentences = [s.strip() for s in result.rstrip(".").split(".") if s.strip()]
    assert len(sentences) <= 5
