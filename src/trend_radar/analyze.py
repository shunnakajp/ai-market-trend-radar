from __future__ import annotations

import collections
import json
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Iterable

from openai import OpenAI

from .config import REFERENCE_TICKERS, THEME_KEYWORDS
from .fetch import FeedItem


GENERIC_EMERGING_STOPWORDS = {
    # Common English / headline glue words.
    "about",
    "after",
    "all",
    "also",
    "and",
    "are",
    "but",
    "can",
    "for",
    "from",
    "has",
    "have",
    "how",
    "into",
    "more",
    "new",
    "news",
    "now",
    "over",
    "says",
    "that",
    "the",
    "their",
    "they",
    "this",
    "what",
    "when",
    "why",
    "will",
    "with",
    "you",
    "your",
    # Too broad for a theme-level market radar.
    "ai",
    "data",
    "link",
    "market",
    "markets",
    "stock",
    "stocks",
    "tech",
    "technology",
    "company",
    "companies",
    "business",
    "comments",
    "infrastructure",
    "invest",
    "investing",
    "investment",
    "investor",
    "investors",
    "billion",
    "million",
    "year",
    "years",
    "today",
    "week",
    "could",
    "would",
    "should",
    "just",
    "like",
    "only",
    "submitted",
    "stars",
}


THEME_KEYWORD_TOKENS = {
    token
    for keywords in THEME_KEYWORDS.values()
    for keyword in keywords
    for token in keyword.lower().replace("/", " ").split()
} | {
    token
    for theme in THEME_KEYWORDS
    for token in theme.lower().replace("/", " ").split()
}


@dataclass
class Trend:
    theme: str
    score: float
    why_now: str
    keywords: List[str] = field(default_factory=list)
    references: List[FeedItem] = field(default_factory=list)
    tickers: List[str] = field(default_factory=list)
    risk_notes: List[str] = field(default_factory=list)
    summary_en: str = ""
    summary_ja: str = ""


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z0-9+.-]{2,}", text.lower())


def _is_emerging_candidate(word: str) -> bool:
    if word in GENERIC_EMERGING_STOPWORDS:
        return False
    if word in THEME_KEYWORD_TOKENS or (word.endswith("s") and word[:-1] in THEME_KEYWORD_TOKENS):
        return False
    # Avoid accidental URL fragments, ticker punctuation, and low-information stems.
    if len(word) < 4 or word.startswith(("http", "www")):
        return False
    return True


def score_trends(items: List[FeedItem], top_n: int = 10) -> List[Trend]:
    theme_scores: Dict[str, float] = collections.defaultdict(float)
    theme_refs: dict[str, List[FeedItem]] = collections.defaultdict(list)
    theme_hits: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)

    for item in items:
        text = f"{item.title} {item.summary}".lower()
        for theme, keywords in THEME_KEYWORDS.items():
            hits = [kw for kw in keywords if kw in text]
            if hits:
                score = item.weight * (1.0 + min(len(hits), 5) * 0.35)
                if item.category == "github":
                    score += 0.35
                if item.category == "social":
                    score += 0.2
                theme_scores[theme] += score
                theme_refs[theme].append(item)
                theme_hits[theme].update(hits)

    # Add emergent keyword clusters so the report is not limited to hand-written themes.
    common = collections.Counter()
    for item in items:
        common.update(_tokenize(f"{item.title} {item.summary}"))
    for word, count in common.most_common(50):
        if not _is_emerging_candidate(word) or count < 3:
            continue
        theme = f"Emerging: {word.upper()}"
        refs = [item for item in items if word in f"{item.title} {item.summary}".lower()][:5]
        if len(refs) >= 3:
            theme_scores[theme] = max(theme_scores.get(theme, 0), count * 0.6)
            theme_refs[theme] = refs
            theme_hits[theme].update([word])

    trends = [
        Trend(
            theme=theme,
            score=round(score, 2),
            why_now=f"Detected across {len(theme_refs[theme])} recent news/social/GitHub items.",
            keywords=[kw for kw, _ in theme_hits[theme].most_common(8)],
            references=theme_refs[theme][:5],
            tickers=REFERENCE_TICKERS.get(theme, []),
            risk_notes=[
                "Signal is based on attention and narrative momentum, not price prediction.",
                "Verify fundamentals, valuation, and source quality before making any investment decision.",
            ],
        )
        for theme, score in sorted(theme_scores.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
    ]
    return trends


def enrich_with_openai(trends: List[Trend], model: str = "gpt-4.1-mini") -> List[Trend]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not trends:
        for trend in trends:
            titles = "; ".join(ref.title for ref in trend.references[:3])
            trend.summary_en = f"{trend.theme} is showing elevated attention. Recent signals include: {titles}"
            trend.summary_ja = f"{trend.theme} は注目度が上がっています。主なシグナル: {titles}"
        return trends

    client = OpenAI(api_key=api_key)
    compact = [
        {
            "theme": t.theme,
            "score": t.score,
            "keywords": t.keywords,
            "tickers": t.tickers,
            "references": [{"title": r.title, "source": r.source, "category": r.category} for r in t.references[:4]],
        }
        for t in trends
    ]
    prompt = """
You are writing a practical, non-advisory market trend radar for AI/tech themes.
For each trend, produce concise English and Japanese summaries, why it matters, and risk notes.
Do not recommend buying or selling securities. Emphasize that this is research triage, not investment advice.
Return strict JSON: {"trends":[{"theme":"...","summary_en":"...","summary_ja":"...","why_now":"...","risk_notes":["...","..."]}]}
""".strip()
    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(compact, ensure_ascii=False)},
        ],
    )
    content = response.choices[0].message.content or "{}"
    data = json.loads(content)
    by_theme = {entry.get("theme"): entry for entry in data.get("trends", [])}
    for trend in trends:
        entry = by_theme.get(trend.theme, {})
        trend.summary_en = entry.get("summary_en") or trend.summary_en
        trend.summary_ja = entry.get("summary_ja") or trend.summary_ja
        trend.why_now = entry.get("why_now") or trend.why_now
        trend.risk_notes = entry.get("risk_notes") or trend.risk_notes
    return trends
