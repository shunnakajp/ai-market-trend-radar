# AI Market Trend Radar

**AI Market Trend Radar** generates a daily Markdown report that helps individual researchers and builders triage attention around US AI/tech market themes.

It scans public RSS/Atom sources across news, Reddit/public social feeds, and GitHub repository momentum, then uses OpenAI to produce concise bilingual summaries.

> This project is for research triage only. It is **not investment advice** and does not recommend buying, selling, or holding any security.

日本語版: [README.ja.md](README.ja.md)

## Why this exists

AI/tech market narratives move quickly across news, social discussion, and open-source developer activity. Individual investors and builders often see only fragments: a semiconductor headline, a Reddit thread, a GitHub repo suddenly getting attention.

This project turns those noisy signals into a transparent daily report:

- top 10 AI/tech themes
- bilingual English/Japanese summaries
- why the theme is getting attention now
- related keywords and reference tickers/themes
- risk notes and source links

## Features

- Daily GitHub Actions report at **07:00 JST** (`0 22 * * *` UTC)
- Markdown-only output under `reports/YYYY-MM-DD.md`
- Public RSS/Atom sources; no paid market data API required
- OpenAI-powered bilingual summarization
- Theme-first design; tickers are references only
- MIT licensed

## Example report structure

```md
# AI Market Trend Radar — 2026-06-03

## Top 10 Trends / トップ10トレンド

### 1. AI Infrastructure — score 18.4

EN: ...
JA: ...
Why now: ...
Keywords: `gpu`, `data center`, `inference`
Reference tickers/themes: `NVDA`, `AMD`, `TSM`
Risks:
- Signal is based on attention and narrative momentum, not price prediction.
```

## Quick start

```bash
git clone https://github.com/shunnakajp/ai-market-trend-radar.git
cd ai-market-trend-radar
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
export OPENAI_API_KEY="your_api_key"
trend-radar
```

The report will be written to:

```text
reports/YYYY-MM-DD.md
```

If `OPENAI_API_KEY` is not set, the tool still creates a basic non-AI report so contributors can test the pipeline.

## GitHub Actions setup

1. Fork or create this repository.
2. Go to **Settings → Secrets and variables → Actions**.
3. Add `OPENAI_API_KEY` as a repository secret.
4. Enable GitHub Actions.
5. Run **Daily AI Market Trend Radar** manually once, or wait for the daily schedule.

## Data sources

The default configuration uses:

- Google News RSS search feeds for AI infrastructure, semiconductors, cloud AI, and macro tech
- Reddit public RSS feeds for AI/tech investing discussions
- GitHub Search Atom feeds for LLM, AI agents, and RAG repository momentum

You can edit sources in [`src/trend_radar/config.py`](src/trend_radar/config.py).

## Methodology

1. Fetch public RSS/Atom items.
2. Deduplicate titles.
3. Score theme momentum using keyword hits, feed category, and source weights.
4. Ask OpenAI to create concise bilingual summaries and risk notes.
5. Save the output as Markdown for transparent review in git history.

This is intentionally simple and auditable. It is a radar, not an oracle.

## Roadmap

- [ ] Add configurable feed files (`feeds.yml`)
- [ ] Add optional JSON output
- [ ] Add GitHub Pages report index
- [ ] Add optional price/volume context from free market data APIs
- [ ] Add Telegram/Slack notification integrations
- [ ] Add backtesting-style narrative tracking without trading recommendations

## Contributing

Contributions are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## Disclaimer

This software and its reports are for informational and research triage purposes only. They are not financial, investment, tax, or legal advice. Always do your own research and consult qualified professionals before making financial decisions.
