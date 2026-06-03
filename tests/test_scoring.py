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


def test_emerging_trends_skip_generic_noise_words():
    items = [
        FeedItem(
            title="You can use this data link for market stocks",
            link="https://example.com/1",
            summary="You can use this data link for market stocks but this is generic.",
            source="test",
            category="news",
            weight=1.0,
        )
        for _ in range(6)
    ]
    trends = score_trends(items, top_n=10)
    themes = {trend.theme for trend in trends}
    assert "Emerging: YOU" not in themes
    assert "Emerging: DATA" not in themes
    assert "Emerging: LINK" not in themes
    assert "Emerging: BUT" not in themes


def test_emerging_trends_keep_specific_new_terms():
    items = [
        FeedItem(
            title=f"Enterprise copilots adopt vectorstore routing pattern {idx}",
            link=f"https://example.com/{idx}",
            summary="Vectorstore retrieval keeps appearing in developer workflows.",
            source="test",
            category="github",
            weight=1.0,
        )
        for idx in range(4)
    ]
    trends = score_trends(items, top_n=10)
    assert any(trend.theme == "Emerging: VECTORSTORE" for trend in trends)
