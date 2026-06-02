from __future__ import annotations

from datetime import date
from typing import List, Optional

from .analyze import Trend
from .fetch import FeedItem

DISCLAIMER_EN = "This report is for research triage only and is not investment advice. It does not recommend buying, selling, or holding any security."
DISCLAIMER_JA = "このレポートは調査の入口を作るためのものであり、投資助言ではありません。いかなる証券の売買・保有も推奨しません。"


def render_markdown(trends: List[Trend], items: List[FeedItem], warnings: List[str], report_date: Optional[date] = None) -> str:
    report_date = report_date or date.today()
    lines: List[str] = []
    lines.append(f"# AI Market Trend Radar — {report_date.isoformat()}")
    lines.append("")
    lines.append("日本語名: **AI投資トレンドレーダー**")
    lines.append("")
    lines.append(f"> {DISCLAIMER_EN}")
    lines.append(f"> {DISCLAIMER_JA}")
    lines.append("")
    lines.append("## Executive Summary / 概要")
    lines.append("")
    lines.append(f"- Sources scanned: **{len(items)}** recent items from news, Reddit/public social RSS, and GitHub search feeds.")
    lines.append(f"- Top trends: **{len(trends)}**")
    lines.append("- Focus: US AI/tech themes; tickers are references only, not recommendations.")
    lines.append("")

    if warnings:
        lines.append("## Source Warnings")
        lines.append("")
        for warning in warnings:
            lines.append(f"- {warning}")
        lines.append("")

    lines.append("## Top 10 Trends / トップ10トレンド")
    lines.append("")
    for idx, trend in enumerate(trends, 1):
        lines.append(f"### {idx}. {trend.theme} — score {trend.score}")
        lines.append("")
        lines.append(f"**EN:** {trend.summary_en}")
        lines.append("")
        lines.append(f"**JA:** {trend.summary_ja}")
        lines.append("")
        lines.append(f"**Why now:** {trend.why_now}")
        lines.append("")
        if trend.keywords:
            lines.append("**Keywords:** " + ", ".join(f"`{kw}`" for kw in trend.keywords))
            lines.append("")
        if trend.tickers:
            lines.append("**Reference tickers/themes:** " + ", ".join(f"`{ticker}`" for ticker in trend.tickers))
            lines.append("")
        lines.append("**Risks / 注意点:**")
        for note in trend.risk_notes:
            lines.append(f"- {note}")
        lines.append("")
        lines.append("**Sample signals:**")
        for ref in trend.references[:3]:
            link = f" — {ref.link}" if ref.link else ""
            lines.append(f"- [{ref.category}] {ref.title} ({ref.source}){link}")
        lines.append("")

    lines.append("## Method")
    lines.append("")
    lines.append("1. Fetch public RSS/Atom feeds for AI, semiconductors, cloud, macro tech, Reddit discussions, and GitHub repository momentum.")
    lines.append("2. Deduplicate items and score themes by keyword hits, source category, and feed weight.")
    lines.append("3. Use OpenAI to produce concise bilingual summaries when `OPENAI_API_KEY` is configured.")
    lines.append("4. Save the report as Markdown for transparent review in GitHub history.")
    lines.append("")
    lines.append("## Disclaimer")
    lines.append("")
    lines.append(DISCLAIMER_EN)
    lines.append(DISCLAIMER_JA)
    lines.append("")
    return "\n".join(lines)
