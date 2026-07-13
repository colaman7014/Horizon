"""Rule-based popularity scoring for OSS Insight trending repos."""

import asyncio
from datetime import datetime, timezone

import httpx
import pytest

from src.ai.analyzer import ContentAnalyzer
from src.models import ContentItem, OSSInsightConfig, SourceType
from src.scrapers.ossinsight import OSSInsightScraper


class ExplodingClient:
    """AI client that fails the test if the analyzer calls the LLM."""

    async def complete(self, **kwargs):
        raise AssertionError("LLM must not be called for OSSINSIGHT items")


def _repo_item(rank=None, stars=5, description="A cool repo", language="Python"):
    metadata = {
        "stars_gained": stars,
        "primary_language": language,
        "description": description,
        "period": "past_24_hours",
    }
    if rank is not None:
        metadata["trending_rank"] = rank
    return ContentItem(
        id=f"ossinsight:trending:{rank or 'x'}",
        source_type=SourceType.OSSINSIGHT,
        title="owner/repo (+5⭐ past_24_hours)",
        url="https://github.com/owner/repo",
        published_at=datetime(2026, 7, 13, tzinfo=timezone.utc),
        metadata=metadata,
    )


@pytest.mark.parametrize(
    "rank,expected",
    [(1, 8.0), (2, 7.5), (5, 6.0), (6, 5.5), (15, 3.0)],
)
def test_score_follows_rank(rank, expected):
    analyzer = ContentAnalyzer(ExplodingClient())
    item = _repo_item(rank=rank)
    asyncio.run(analyzer._analyze_item(item))
    assert item.ai_score == expected


def test_missing_rank_scores_below_threshold():
    analyzer = ContentAnalyzer(ExplodingClient())
    item = _repo_item(rank=None)
    asyncio.run(analyzer._analyze_item(item))
    assert item.ai_score == 5.0


def test_summary_reason_and_tags_from_metadata():
    analyzer = ContentAnalyzer(ExplodingClient())
    item = _repo_item(rank=3, stars=6)
    asyncio.run(analyzer._analyze_item(item))
    assert item.ai_summary == "A cool repo"
    assert "#3" in item.ai_reason and "+6" in item.ai_reason
    assert item.ai_tags == ["Python", "github", "trending"]


def test_summary_falls_back_to_title_without_description():
    analyzer = ContentAnalyzer(ExplodingClient())
    item = _repo_item(rank=1, description="")
    asyncio.run(analyzer._analyze_item(item))
    assert item.ai_summary == item.title


def _fake_rows():
    return [
        {"repo_id": 1, "repo_name": "a/low", "stars": "3", "description": "low"},
        {"repo_id": 2, "repo_name": "b/high", "stars": "9", "description": "high"},
        {"repo_id": 3, "repo_name": "c/mid", "stars": "5", "description": "mid"},
    ]


def test_scraper_sets_rank_and_category(monkeypatch):
    cfg = OSSInsightConfig(
        enabled=True,
        period="past_24_hours",
        languages=["All"],
        keywords=[],
        min_stars=0,
        max_items=15,
    )

    async def main():
        async with httpx.AsyncClient() as client:
            scraper = OSSInsightScraper(cfg, client)

            async def fake_fetch_period(period, language):
                return _fake_rows()

            monkeypatch.setattr(scraper, "_fetch_period", fake_fetch_period)
            return await scraper.fetch(datetime.now(timezone.utc))

    items = asyncio.run(main())

    assert [i.metadata["repo"] for i in items] == ["b/high", "c/mid", "a/low"]
    assert [i.metadata["trending_rank"] for i in items] == [1, 2, 3]
    assert all(i.metadata["category"] == "github" for i in items)
