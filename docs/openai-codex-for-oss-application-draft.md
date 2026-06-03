# OpenAI Codex for OSS Application Draft

## Repository

https://github.com/shunnakajp/ai-market-trend-radar

## Project summary

AI Market Trend Radar is an open-source GitHub Actions tool that generates daily bilingual Markdown reports for US AI/tech market themes. It scans public RSS/Atom sources across news, Reddit/public social feeds, and GitHub repository momentum, then uses OpenAI to summarize why themes are gaining attention and what risks researchers should check.

The project is designed as research triage, not investment advice. It helps individual builders and investors understand noisy AI/tech narratives transparently through source-linked reports.

## Current implementation status

- Daily GitHub Actions workflow is implemented, including manual dispatch.
- `OPENAI_API_KEY` is supported through GitHub Actions repository secrets.
- A generated sample report exists under `reports/2026-06-03.md`.
- The scoring pipeline includes tests for core theme detection and emerging-trend noise filtering.

## Why this project is eligible / important

AI and technology market narratives increasingly emerge from a mix of news, social discussion, and open-source developer activity. Many individual researchers, especially Japanese readers, struggle to follow fast-moving English-language signals. This project provides an auditable OSS workflow that converts public sources into bilingual trend reports, making the research process more accessible and transparent.

## Maintainer role

Shun Nakajima is the creator and primary maintainer of the project, responsible for roadmap, source selection, prompt design, report quality, documentation, and community contributions.

## How OpenAI API credits will be used

OpenAI API credits will be used to generate concise English/Japanese summaries, explain why each theme is currently receiving attention, identify risk notes, and improve report readability. The credits will also support future OSS work such as issue triage, documentation improvements, and contributor onboarding for feed/source improvements.

## Safety / non-advisory stance

The project does not provide trading recommendations or price predictions. Reports clearly state that they are for research triage only and are not financial advice. Tickers are included only as references to related themes.
