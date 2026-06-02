from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from .analyze import enrich_with_openai, score_trends
from .config import DEFAULT_FEEDS, GITHUB_SEARCH_QUERIES
from .fetch import fetch_feeds, fetch_github_search
from .report import render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a daily AI/tech market trend radar report.")
    parser.add_argument("--output", "-o", default=None, help="Output Markdown path. Defaults to reports/YYYY-MM-DD.md")
    parser.add_argument("--top", type=int, default=10, help="Number of trends to include.")
    parser.add_argument("--per-feed-limit", type=int, default=20, help="Maximum items to read from each feed.")
    parser.add_argument("--model", default="gpt-4.1-mini", help="OpenAI model for summaries.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    today = date.today()
    output = Path(args.output or f"reports/{today.isoformat()}.md")

    items, warnings = fetch_feeds(DEFAULT_FEEDS, per_feed_limit=args.per_feed_limit)
    github_items, github_warnings = fetch_github_search(GITHUB_SEARCH_QUERIES, per_query_limit=args.per_feed_limit)
    items.extend(github_items)
    warnings.extend(github_warnings)
    trends = score_trends(items, top_n=args.top)
    trends = enrich_with_openai(trends, model=args.model)
    markdown = render_markdown(trends, items, warnings, report_date=today)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    print(f"Wrote {output} with {len(trends)} trends from {len(items)} items")


if __name__ == "__main__":
    main()
