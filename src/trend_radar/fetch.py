from __future__ import annotations

import html
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from email.utils import parsedate_to_datetime
from typing import Optional, List, Iterable

from .config import FeedSource


@dataclass
class FeedItem:
    title: str
    link: str
    summary: str
    source: str
    category: str
    published: Optional[str] = None
    weight: float = 1.0


_TAG_RE = re.compile(r"<[^>]+>")
_SPACE_RE = re.compile(r"\s+")


def clean_text(value: Optional[str]) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    value = _TAG_RE.sub(" ", value)
    return _SPACE_RE.sub(" ", value).strip()


def fetch_url(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ai-market-trend-radar/0.1 (+https://github.com/shunnakajp/ai-market-trend-radar)",
            "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:  # noqa: S310 - controlled feed URLs
        return response.read()


def _first_text(element: ET.Element, names: Iterable[str]) -> str:
    for name in names:
        found = element.find(name)
        if found is not None and found.text:
            return found.text
    return ""


def _first_link(element: ET.Element) -> str:
    # RSS link text
    link = _first_text(element, ["link"])
    if link:
        return link
    # Atom link href
    for child in element.findall("{http://www.w3.org/2005/Atom}link") + element.findall("link"):
        href = child.attrib.get("href")
        if href:
            return href
    return ""


def parse_feed(raw: bytes, source: FeedSource, limit: int = 20) -> List[FeedItem]:
    root = ET.fromstring(raw)
    items: list[ET.Element]

    if root.tag.endswith("feed"):
        ns = "{http://www.w3.org/2005/Atom}"
        items = root.findall(f"{ns}entry")
        title_names = [f"{ns}title", "title"]
        summary_names = [f"{ns}summary", f"{ns}content", "summary", "content"]
        date_names = [f"{ns}updated", f"{ns}published", "updated", "published"]
    else:
        channel = root.find("channel")
        items = channel.findall("item") if channel is not None else root.findall("item")
        title_names = ["title"]
        summary_names = ["description", "summary"]
        date_names = ["pubDate", "published", "updated"]

    parsed: List[FeedItem] = []
    for item in items[:limit]:
        title = clean_text(_first_text(item, title_names))
        link = clean_text(_first_link(item))
        summary = clean_text(_first_text(item, summary_names))
        published = clean_text(_first_text(item, date_names)) or None
        if title:
            parsed.append(FeedItem(title, link, summary, source.name, source.category, published, source.weight))
    return parsed


def fetch_feeds(sources: List[FeedSource], per_feed_limit: int = 20, polite_delay: float = 0.2) -> tuple[List[FeedItem], List[str]]:
    items: List[FeedItem] = []
    warnings: List[str] = []
    for source in sources:
        try:
            raw = fetch_url(source.url)
            items.extend(parse_feed(raw, source, limit=per_feed_limit))
        except Exception as exc:  # network feeds should not kill the whole report
            warnings.append(f"Could not fetch {source.name}: {exc}")
        time.sleep(polite_delay)
    return dedupe_items(items), warnings


def dedupe_items(items: List[FeedItem]) -> List[FeedItem]:
    seen: set[str] = set()
    result: List[FeedItem] = []
    for item in items:
        key = re.sub(r"\W+", "", item.title.lower())[:90]
        if key and key not in seen:
            seen.add(key)
            result.append(item)
    return result



def fetch_github_search(queries: List[str], per_query_limit: int = 10) -> tuple[List[FeedItem], List[str]]:
    """Fetch repository momentum from GitHub's public Search API.

    This intentionally avoids credentials for the default OSS workflow. GitHub may
    rate-limit anonymous requests; failures are reported as warnings rather than
    stopping the report.
    """
    items: List[FeedItem] = []
    warnings: List[str] = []
    for query in queries:
        url = "https://api.github.com/search/repositories?q=" + urllib.parse.quote(query) + "&sort=updated&order=desc&per_page=" + str(per_query_limit)
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "ai-market-trend-radar/0.1 (+https://github.com/shunnakajp/ai-market-trend-radar)",
                    "Accept": "application/vnd.github+json",
                },
            )
            with urllib.request.urlopen(req, timeout=20) as response:  # noqa: S310 - controlled GitHub API URL
                data = json.loads(response.read().decode("utf-8"))
            for repo in data.get("items", [])[:per_query_limit]:
                name = repo.get("full_name") or repo.get("name") or "GitHub repository"
                description = repo.get("description") or ""
                stars = repo.get("stargazers_count", 0)
                language = repo.get("language") or "unknown"
                items.append(
                    FeedItem(
                        title=f"{name} ({stars} stars, {language})",
                        link=repo.get("html_url") or "",
                        summary=description,
                        source=f"GitHub Search: {query}",
                        category="github",
                        published=repo.get("updated_at"),
                        weight=1.1,
                    )
                )
        except Exception as exc:
            warnings.append(f"Could not fetch GitHub Search query '{query}': {exc}")
        time.sleep(0.2)
    return dedupe_items(items), warnings
