"""Tail items (beyond enrichment_top_n) must still get a Chinese translation.

Regression: enrichment_top_n capped the second pass, but only enrichment
produces the *_zh fields. Items past the cap shipped with English titles and
summaries. The lightweight translate_batch pass gives every tail item at least
a Traditional Chinese title and summary.
"""

import asyncio
import json
from datetime import datetime, timezone

from types import SimpleNamespace

from rich.console import Console

from src.ai.enricher import ContentEnricher
from src.models import (
    AIConfig,
    Config,
    ContentItem,
    FilteringConfig,
    SourceType,
    SourcesConfig,
)
from src.orchestrator import HorizonOrchestrator


class TranslatingClient:
    """Fake AI client that returns a fixed translation for every call."""

    def __init__(self, config):
        self.config = config
        self.calls = 0

    async def complete(self, system, user, max_tokens=None):
        self.calls += 1
        return json.dumps({"title_zh": "翻譯標題", "summary_zh": "翻譯後的摘要。"})


def _ai_config(**kwargs):
    return AIConfig(provider="openai", model="test", api_key_env="TEST_API_KEY", **kwargs)


def _item(item_id: str) -> ContentItem:
    return ContentItem(
        id=item_id,
        source_type=SourceType.RSS,
        title="English title",
        url=f"https://example.com/{item_id}",
        published_at=datetime(2026, 7, 16, tzinfo=timezone.utc),
        ai_score=6.5,
        ai_summary="English one-sentence summary.",
    )


def test_translate_batch_populates_zh_fields_for_every_item():
    client = TranslatingClient(_ai_config())
    enricher = ContentEnricher(client)

    items = [_item("a"), _item("b")]
    asyncio.run(enricher.translate_batch(items))

    for item in items:
        assert item.metadata.get("title_zh") == "翻譯標題"
        assert item.metadata.get("detailed_summary_zh") == "翻譯後的摘要。"
    # One lightweight call per item, no web search / concept extraction.
    assert client.calls == 2


def test_enrich_important_items_translates_tail_beyond_top_n(monkeypatch):
    config = Config(
        ai=AIConfig(
            provider="openai",
            model="test",
            api_key_env="TEST_API_KEY",
            enrichment_top_n=2,
        ),
        sources=SourcesConfig(),
        filtering=FilteringConfig(),
    )
    orchestrator = HorizonOrchestrator(config, SimpleNamespace())
    orchestrator.console = Console(record=True)

    enriched: list[str] = []
    translated: list[str] = []

    class FakeEnricher:
        def __init__(self, client):
            pass

        async def enrich_batch(self, items):
            enriched.extend(item.id for item in items)

        async def translate_batch(self, items):
            translated.extend(item.id for item in items)

    monkeypatch.setattr("src.orchestrator.ContentEnricher", FakeEnricher)
    monkeypatch.setattr("src.orchestrator.create_ai_client", lambda cfg: object())

    items = [_item(str(i)) for i in range(5)]
    asyncio.run(orchestrator._enrich_important_items(items))

    # Top 2 get full enrichment; the remaining tail is still translated.
    assert enriched == ["0", "1"]
    assert translated == ["2", "3", "4"]
