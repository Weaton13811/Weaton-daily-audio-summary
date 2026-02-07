"""Fetch local news headlines and summaries for the Binghamton NY area."""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote_plus

import requests

logger = logging.getLogger(__name__)

GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"


@dataclass
class Article:
    title: str
    summary: str
    source: str

    def __str__(self) -> str:
        return f"[{self.source}] {self.title}: {self.summary}"


def fetch_rss_feed(url: str, max_items: int = 10) -> list[Article]:
    """Parse an RSS feed and return articles."""
    articles: list[Article] = []
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        root = ET.fromstring(resp.text)

        # Handle both RSS 2.0 (<item>) and Atom (<entry>) feeds
        items = root.findall(".//item") or root.findall(
            ".//{http://www.w3.org/2005/Atom}entry"
        )
        for item in items[:max_items]:
            title = _text(item, "title") or _text(
                item, "{http://www.w3.org/2005/Atom}title"
            )
            description = (
                _text(item, "description")
                or _text(item, "{http://www.w3.org/2005/Atom}summary")
                or ""
            )
            if title:
                articles.append(
                    Article(
                        title=title,
                        summary=_clean(description),
                        source=url,
                    )
                )
    except Exception:
        logger.warning("Failed to fetch RSS feed: %s", url, exc_info=True)
    return articles


def fetch_google_news(query: str, max_items: int = 10) -> list[Article]:
    """Fetch news from Google News RSS for a search query."""
    url = GOOGLE_NEWS_RSS.format(query=quote_plus(query))
    return fetch_rss_feed(url, max_items=max_items)


def gather_news(config: dict[str, Any]) -> list[Article]:
    """Gather news from all configured sources."""
    articles: list[Article] = []

    for feed_url in config.get("rss_feeds", []):
        articles.extend(fetch_rss_feed(feed_url))

    if query := config.get("google_news_query"):
        articles.extend(fetch_google_news(query))

    # Deduplicate by title (case-insensitive)
    seen: set[str] = set()
    unique: list[Article] = []
    for article in articles:
        key = article.title.lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(article)

    logger.info("Gathered %d unique articles from %d total", len(unique), len(articles))
    return unique


def _text(element: ET.Element, tag: str) -> str | None:
    child = element.find(tag)
    return child.text.strip() if child is not None and child.text else None


def _clean(html: str) -> str:
    """Strip basic HTML tags from a description string."""
    import re

    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text).strip()
