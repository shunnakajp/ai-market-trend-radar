# Contributing

Thanks for your interest in AI Market Trend Radar.

Good first contributions include:

- improving feed sources
- improving Japanese/English wording
- adding tests for scoring logic
- adding safer risk/disclaimer wording
- documenting setup steps

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest
```

## Principles

- Keep the project transparent and auditable.
- Do not add trading recommendations.
- Prefer public, low-friction data sources.
- Make OpenAI usage useful but not mandatory for local testing.
