import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

from rich.console import Console

from src.models import AIConfig, Config, ContentItem, FilteringConfig, SourceType, SourcesConfig
from src.orchestrator import HorizonOrchestrator


def _item(item_id: str) -> ContentItem:
    return ContentItem(
        id=item_id,
        source_type=SourceType.RSS,
        title=item_id,
        url=f"https://example.com/{item_id}",
        published_at=datetime.now(timezone.utc),
        ai_score=8.0,
        ai_summary=f"summary {item_id}",
    )


def _config() -> Config:
    return Config(
        ai=AIConfig(
            provider="openai",
            model="test",
            api_key_env="TEST_API_KEY",
            languages=[],
        ),
        sources=SourcesConfig(),
        filtering=FilteringConfig(ai_score_threshold=7.0, max_items=10),
    )


def test_run_logs_stage_timing_and_item_counts(tmp_path, monkeypatch):
    storage = SimpleNamespace()
    orchestrator = HorizonOrchestrator(_config(), storage)
    orchestrator.console = Console(record=True)
    items = [_item("a"), _item("b")]

    async def fetch_all_sources(since):
        return items

    async def analyze_content(input_items):
        return input_items

    async def merge_topic_duplicates(input_items):
        return input_items

    async def expand_twitter_discussion(input_items):
        return None

    async def enrich_important_items(input_items):
        return None

    monkeypatch.setattr(orchestrator, "fetch_all_sources", fetch_all_sources)
    monkeypatch.setattr(orchestrator, "_analyze_content", analyze_content)
    monkeypatch.setattr(orchestrator, "merge_topic_duplicates", merge_topic_duplicates)
    monkeypatch.setattr(orchestrator, "_expand_twitter_discussion", expand_twitter_discussion)
    monkeypatch.setattr(orchestrator, "_enrich_important_items", enrich_important_items)
    monkeypatch.chdir(tmp_path)

    asyncio.run(orchestrator.run(force_hours=24))

    output = orchestrator.console.export_text()
    assert "⏱️ Fetch completed in" in output
    assert "⏱️ AI scoring completed in" in output
    assert "⏱️ Enrichment completed in" in output
    assert "LLM scoring candidates: 2" in output
