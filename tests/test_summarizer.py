"""Tests for the summarizer module."""

from unittest.mock import MagicMock, patch

from daily_audio_summary.news import Article
from daily_audio_summary.summarizer import summarize


def test_summarize_no_articles():
    result = summarize([], {})
    assert "Good morning" in result
    assert "no local news" in result


@patch("daily_audio_summary.summarizer.anthropic")
def test_summarize_calls_claude(mock_anthropic):
    mock_client = MagicMock()
    mock_anthropic.Anthropic.return_value = mock_client
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Good morning Binghamton!")]
    mock_client.messages.create.return_value = mock_response

    articles = [
        Article(title="Test headline", summary="Test summary", source="test"),
    ]
    config = {"anthropic_api_key": "test-key", "location": "Binghamton, NY"}
    result = summarize(articles, config)

    assert result == "Good morning Binghamton!"
    mock_client.messages.create.assert_called_once()
    call_kwargs = mock_client.messages.create.call_args.kwargs
    assert call_kwargs["system"]
    assert "Test headline" in call_kwargs["messages"][0]["content"]
