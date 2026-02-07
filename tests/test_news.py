"""Tests for the news module."""

from daily_audio_summary.news import Article, _clean, fetch_rss_feed, gather_news

SAMPLE_RSS = """\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Feed</title>
    <item>
      <title>Storm warning for Broome County</title>
      <description>A winter storm is expected to bring heavy snow.</description>
    </item>
    <item>
      <title>New restaurant opens downtown</title>
      <description>&lt;p&gt;A new Italian restaurant has opened.&lt;/p&gt;</description>
    </item>
  </channel>
</rss>
"""


def test_article_str():
    a = Article(title="Test", summary="Summary", source="rss")
    assert "[rss] Test: Summary" == str(a)


def test_clean_strips_html():
    assert _clean("<p>Hello <b>world</b></p>") == "Hello world"


def test_clean_empty():
    assert _clean("") == ""


def test_fetch_rss_feed_parses_xml(requests_mock):
    url = "https://example.com/feed.xml"
    requests_mock.get(url, text=SAMPLE_RSS)
    articles = fetch_rss_feed(url)
    assert len(articles) == 2
    assert articles[0].title == "Storm warning for Broome County"
    assert "heavy snow" in articles[0].summary


def test_fetch_rss_feed_handles_failure(requests_mock):
    url = "https://example.com/broken"
    requests_mock.get(url, status_code=500)
    articles = fetch_rss_feed(url)
    assert articles == []


def test_gather_news_deduplicates(requests_mock):
    url1 = "https://feed1.com/rss"
    url2 = "https://feed2.com/rss"
    requests_mock.get(url1, text=SAMPLE_RSS)
    requests_mock.get(url2, text=SAMPLE_RSS)
    config = {"rss_feeds": [url1, url2], "google_news_query": ""}
    articles = gather_news(config)
    # Same articles from two feeds should be deduplicated
    assert len(articles) == 2
