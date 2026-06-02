from __future__ import annotations

from typing import Dict, List

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FeedSource:
    name: str
    url: str
    category: str
    weight: float = 1.0


DEFAULT_FEEDS: List[FeedSource] = [
    # News: Google News RSS query feeds keep the project API-key-light.
    FeedSource("Google News: AI infrastructure", "https://news.google.com/rss/search?q=AI%20infrastructure%20OR%20data%20center%20OR%20GPU%20when:2d&hl=en-US&gl=US&ceid=US:en", "news", 1.2),
    FeedSource("Google News: semiconductors", "https://news.google.com/rss/search?q=semiconductor%20OR%20NVIDIA%20OR%20AMD%20OR%20TSMC%20when:2d&hl=en-US&gl=US&ceid=US:en", "news", 1.2),
    FeedSource("Google News: cloud AI", "https://news.google.com/rss/search?q=cloud%20AI%20OR%20Microsoft%20Azure%20OR%20AWS%20OR%20Google%20Cloud%20when:2d&hl=en-US&gl=US&ceid=US:en", "news", 1.1),
    FeedSource("Google News: macro tech", "https://news.google.com/rss/search?q=interest%20rates%20technology%20stocks%20OR%20Nasdaq%20AI%20when:2d&hl=en-US&gl=US&ceid=US:en", "news", 0.9),
    # Reddit public RSS feeds; no Reddit API credentials required.
    FeedSource("Reddit: stocks", "https://www.reddit.com/r/stocks/search.rss?q=AI%20OR%20semiconductor%20OR%20cloud&restrict_sr=1&sort=new&t=week", "social", 1.0),
    FeedSource("Reddit: investing", "https://www.reddit.com/r/investing/search.rss?q=AI%20OR%20semiconductor%20OR%20cloud&restrict_sr=1&sort=new&t=week", "social", 1.0),
    FeedSource("Reddit: artificial", "https://www.reddit.com/r/artificial/.rss", "social", 0.8),
    # GitHub/OSS momentum is fetched via the public GitHub Search API in fetch_github_search().
]


THEME_KEYWORDS: Dict[str, List[str]] = {
    "AI Infrastructure": ["gpu", "accelerator", "data center", "datacenter", "inference", "training", "nvidia", "amd", "tsmc", "hbm"],
    "Semiconductors": ["semiconductor", "chip", "foundry", "wafer", "asml", "tsmc", "arm", "memory"],
    "Cloud AI": ["azure", "aws", "google cloud", "cloud", "capex", "server", "oracle"],
    "LLM Applications": ["llm", "chatbot", "copilot", "agent", "rag", "workflow", "automation"],
    "AI Safety / Regulation": ["regulation", "safety", "copyright", "lawsuit", "policy", "governance"],
    "Robotics / Edge AI": ["robot", "robotics", "edge ai", "autonomous", "humanoid"],
    "Market Macro": ["fed", "rates", "inflation", "nasdaq", "treasury", "earnings", "guidance"],
}


REFERENCE_TICKERS: Dict[str, List[str]] = {
    "AI Infrastructure": ["NVDA", "AMD", "TSM", "AVGO", "SMCI"],
    "Semiconductors": ["NVDA", "AMD", "TSM", "ASML", "ARM", "MU"],
    "Cloud AI": ["MSFT", "AMZN", "GOOGL", "ORCL"],
    "LLM Applications": ["MSFT", "GOOGL", "META", "CRM", "ADBE"],
    "Robotics / Edge AI": ["TSLA", "NVDA", "ISRG", "TER"],
    "Market Macro": ["QQQ", "SPY"],
}

# GitHub Search API queries. These are public and do not require a token for small daily runs.
GITHUB_SEARCH_QUERIES: List[str] = [
    "LLM stars:>100",
    "AI agent stars:>100",
    "RAG stars:>100",
]
