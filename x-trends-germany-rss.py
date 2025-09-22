import requests
from bs4 import BeautifulSoup
from datetime import datetime
import html
import urllib.parse

def fetch_trends_germany():
    url = "https://trends24.in/germany/"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # Trends24 strukturiert: die Liste der Trends in Deutschland sind in ol.trend-card__list li a
    # (oder ein ähnliches Element, falls Struktur etwas anders)
    els = soup.select("ol.trend-card__list li a")
    trends = [e.get_text(strip=True) for e in els]
    return trends[:50]

def build_rss_germany(trends):
    now = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

    rss_items = []
    for i, trend in enumerate(trends, start=1):
        escaped = html.escape(trend)
        query = urllib.parse.quote(trend)
        item = f"""<item>
      <title>{escaped}</title>
      <link>https://x.com/search?q={query}</link>
      <description>Trend (Germany) — position #{i}</description>
      <pubDate>{now}</pubDate>
      <guid isPermaLink="false">germany-{now}-{i}</guid>
    </item>"""
        rss_items.append(item)

    rss_body = "\n".join(rss_items)
    rss_feed = f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
  <channel>
    <title>X (Twitter) — Deutschland Trending Topics</title>
    <link>https://trends24.in/germany/</link>
    <description>Trending topics in Germany on X. Quelle: trends24 / Deutschland.</description>
    <language>de-de</language>
    <pubDate>{now}</pubDate>
    <ttl>5</ttl>
{rss_body}
  </channel>
</rss>
"""
    return rss_feed

if __name__ == "__main__":
    trends = fetch_trends_germany()
    rss = build_rss_germany(trends)
    with open("x-trending-germany.rss", "w", encoding="utf-8") as f:
        f.write(rss)
    print("✅ Deutschland-RSS Feed erstellt: x-trending-germany.rss")
