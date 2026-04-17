import feedparser
import httpx
from datetime import datetime, timezone, timedelta
from typing import Optional
from config import RSS_FEEDS, ARTICLES_PER_FEED, MAX_ARTICLES_TOTAL


def _parse_date(entry) -> datetime:
    for field in ("published_parsed", "updated_parsed"):
        val = getattr(entry, field, None)
        if val:
            try:
                return datetime(*val[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return datetime.now(timezone.utc)


def _fetch_feed(url: str, topic: str, max_age_days: int = 7) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    articles = []
    try:
        # feedparser doesn't support async; use httpx to get raw content then parse
        response = httpx.get(url, timeout=15, follow_redirects=True,
                             headers={"User-Agent": "Mozilla/5.0 (newsletter-bot/1.0)"})
        response.raise_for_status()
        feed = feedparser.parse(response.text)

        for entry in feed.entries[:ARTICLES_PER_FEED]:
            pub_date = _parse_date(entry)
            if pub_date < cutoff:
                continue

            summary = getattr(entry, "summary", "") or ""
            # Strip HTML tags roughly
            import re
            summary = re.sub(r"<[^>]+>", "", summary).strip()
            summary = summary[:500] + "..." if len(summary) > 500 else summary

            articles.append({
                "title": getattr(entry, "title", "Sin título").strip(),
                "url": getattr(entry, "link", ""),
                "summary": summary,
                "published": pub_date.strftime("%d/%m/%Y"),
                "topic": topic,
                "source": feed.feed.get("title", url),
            })
    except Exception as e:
        print(f"[rss_fetcher] Error fetching {url}: {e}")

    return articles


def fetch_all_articles() -> list[dict]:
    all_articles = []
    for topic, urls in RSS_FEEDS.items():
        for url in urls:
            articles = _fetch_feed(url, topic)
            all_articles.extend(articles)
            print(f"[rss_fetcher] {topic} | {url} -> {len(articles)} articles")

    # Sort by date descending, cap total
    all_articles.sort(key=lambda a: a["published"], reverse=True)
    return all_articles[:MAX_ARTICLES_TOTAL]
