from trend_radar.analyze import score_trends
from trend_radar.fetch import FeedItem


def test_score_trends_detects_ai_infrastructure():
    items = [
        FeedItem(
            title="NVIDIA GPUs and data center capex dominate AI infrastructure discussion",
            link="https://example.com",
            summary="Cloud providers increase GPU clusters for inference and training.",
            source="test",
            category="news",
            weight=1.0,
        )
    ]
    trends = score_trends(items, top_n=3)
    assert trends
    assert trends[0].theme == "AI Infrastructure"
    assert "gpu" in trends[0].keywords
