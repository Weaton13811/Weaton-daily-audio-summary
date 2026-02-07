"""AI-powered news summarization using the Anthropic Claude API."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

import anthropic

if TYPE_CHECKING:
    from daily_audio_summary.news import Article

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are a friendly, professional morning news anchor for the Binghamton, NY area.
Your job is to write a script for a daily audio briefing that will be read aloud
by a text-to-speech voice.

Guidelines:
- Open with a warm greeting and today's date
- Cover the most important local stories first
- Keep each story to 2-3 sentences
- Use a conversational, radio-anchor tone
- Transition smoothly between stories
- Close with a brief sign-off wishing the listener a great day
- Keep the total script to about 2 minutes of speaking time (~300 words)
- Do NOT include any markup, headers, or stage directions
"""


def summarize(articles: list[Article], config: dict[str, Any]) -> str:
    """Use Claude to turn raw articles into a polished morning briefing script."""
    if not articles:
        today = datetime.now().strftime("%A, %B %d")
        return (
            f"Good morning! It's {today}. "
            "There are no local news stories to report this morning. "
            "Have a wonderful day!"
        )

    headlines_block = "\n".join(
        f"- {a.title}: {a.summary}" for a in articles[:20]
    )

    today = datetime.now().strftime("%A, %B %d, %Y")
    user_prompt = (
        f"Today is {today}. Here are the latest local news headlines and "
        f"summaries for {config.get('location', 'Binghamton, NY')}:\n\n"
        f"{headlines_block}\n\n"
        "Please write the morning audio briefing script."
    )

    client = anthropic.Anthropic(api_key=config.get("anthropic_api_key"))
    response = client.messages.create(
        model=config.get("claude_model", "claude-sonnet-4-5-20250929"),
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    script = response.content[0].text
    logger.info("Generated briefing script (%d chars)", len(script))
    return script.strip()
