"""Content summarization module."""

from __future__ import annotations


def summarize(content: str, max_sentences: int = 5) -> str:
    """Summarize text content into a concise brief.

    Splits content into sentences and returns the first `max_sentences`.
    """
    if not content:
        return ""

    sentences = [s.strip() for s in content.split(".") if s.strip()]
    selected = sentences[:max_sentences]
    return ". ".join(selected) + "." if selected else ""
