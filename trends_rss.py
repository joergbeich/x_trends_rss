import requests
from bs4 import BeautifulSoup
from datetime import datetime
import html

def fetch_trends():
    url = "https://trends24.in/"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # trends24 packt die Trends in <ol><li>
    trend_lists = soup.select("ol.trend-card__list li a")
    trends = [t.get_text(strip=True) for t in trend_lists]
    return trends[:50]  # Top 50

def build_rss(trends):
    now = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

    rss_items = ""
    for i, trend in enumerate(trends, 1):
        query = requests.utils.quote(trend)
        rss_items += f"""
    <item>
      <title>{html.escape(trend)}</title>
      <link>https://x.com/search?q={query}</link>
      <description>Trend (Worldwide) — position #{i}</description>
      <pubDate>{now}</pubDate>
      <guid isPermaLink="false">trends24-{now}-{i}</guid>
    </item>"""

    rss_feed = f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
  <channel>
    <title>X (Twitter) — Worldwide Trending Topics</title>
    <link>https://trends24.in/</link>
    <description>Worldwide trending topics on X. Source: trends24.</description>
    <language>en-us</language>
    <pubDate>{now}</pubDate>
    <ttl>5</ttl>
    {rss_items}
  </channel>
</rss>
"""
    return rss_feed

if __name__ == "__main__":
    trends = fetch_trends()
    rss = build_rss(trends)
    with open("x-trending-worldwide.rss", "w", encoding="utf-8") as f:
        f.write(rss)
    print("✅ RSS feed erstellt: x-trending-worldwide.rss")
