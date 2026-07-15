import asyncio
import json
from datetime import datetime, timezone

from pydantic import ValidationError
import pytest

from src.ai.enricher import ContentEnricher
from src.models import AIConfig, ContentItem, SourceType


class RecordingClient:
    """Fake AI client that records the max_tokens passed to complete()."""

    def __init__(self, config, response):
        self.config = config
        self.response = response
        self.max_tokens_calls = []

    async def complete(self, system, user, max_tokens=None):
        self.max_tokens_calls.append(max_tokens)
        return self.response


def _ai_config(**kwargs):
    return AIConfig(provider="openai", model="test", api_key_env="TEST_API_KEY", **kwargs)


def _item():
    return ContentItem(
        id="rss:enrich:1",
        source_type=SourceType.RSS,
        title="Sample",
        url="https://example.com/1",
        published_at=datetime(2026, 7, 15, tzinfo=timezone.utc),
        ai_score=8.0,
        ai_summary="sample summary",
        content="Some article body.",
    )


_VALID_ENRICHMENT = json.dumps(
    {
        "title_en": "T", "title_zh": "標題",
        "whats_new_en": "a", "whats_new_zh": "甲",
        "why_it_matters_en": "b", "why_it_matters_zh": "乙",
        "key_details_en": "c", "key_details_zh": "丙",
        "background_en": "", "background_zh": "",
        "community_discussion_en": "", "community_discussion_zh": "",
        "sources": [],
    }
)


def test_ai_config_defaults_enrichment_max_tokens_to_8192():
    assert _ai_config().enrichment_max_tokens == 8192


def test_enrichment_max_tokens_rejects_zero():
    with pytest.raises(ValidationError):
        _ai_config(enrichment_max_tokens=0)


def test_enrichment_call_uses_configured_max_tokens(monkeypatch):
    client = RecordingClient(_ai_config(enrichment_max_tokens=8192), _VALID_ENRICHMENT)
    enricher = ContentEnricher(client)

    async def no_concepts(item, content_text):
        return []

    monkeypatch.setattr(enricher, "_extract_concepts", no_concepts)

    item = _item()
    asyncio.run(enricher._enrich_item(item))

    # The large bilingual enrichment call must request the raised budget so
    # qwen3 has room for thinking + full JSON (default 4096 truncates it).
    assert 8192 in client.max_tokens_calls
    # Valid response → no fallback → enrichment fields populated
    assert item.metadata.get("detailed_summary_en") == "a b c"
