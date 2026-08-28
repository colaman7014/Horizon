"""Regression tests for Traditional-Chinese and citation validation retries."""

import asyncio
import json
from datetime import datetime, timezone

from src.ai.enricher import ContentEnricher
from src.models import AIConfig, ContentItem, SourceType


class QueueClient:
    """Return deterministic enrichment responses and record each request."""

    def __init__(self, responses):
        self.config = AIConfig(
            provider="ollama",
            model="nemotron-3.5-lightning:30b-mlx",
            api_key_env="",
            enrichment_max_tokens=8192,
        )
        self.responses = list(responses)
        self.calls = []

    async def complete(self, system, user, max_tokens=None):
        self.calls.append({"system": system, "user": user, "max_tokens": max_tokens})
        return self.responses.pop(0)


def _item() -> ContentItem:
    return ContentItem(
        id="rss:validation:1",
        source_type=SourceType.RSS,
        title="Example announcement",
        url="https://example.com/item",
        published_at=datetime(2026, 8, 12, tzinfo=timezone.utc),
        content="Example article body.",
        ai_score=8.0,
        ai_summary="Example summary.",
    )


def _enrichment_response(*, zh_term="", sources=None) -> str:
    term_suffix = f" {zh_term}" if zh_term else ""
    return json.dumps(
        {
            "title_en": "Example announcement",
            "title_zh": "範例公告",
            "whats_new_en": "New details.",
            "whats_new_zh": f"新內容。{term_suffix}".strip(),
            "why_it_matters_en": "It matters.",
            "why_it_matters_zh": "這很重要。",
            "key_details_en": "Key detail.",
            "key_details_zh": "關鍵細節。",
            "background_en": "Background.",
            "background_zh": "背景說明。",
            "community_discussion_en": "",
            "community_discussion_zh": "",
            "sources": sources if sources is not None else [],
        },
        ensure_ascii=False,
    )


def _configure_search(monkeypatch, enricher, results):
    async def concepts(item, content_text):
        return ["example concept"]

    async def search(query):
        return results

    monkeypatch.setattr(enricher, "_extract_concepts", concepts)
    monkeypatch.setattr(enricher, "_web_search", search)


def test_invalid_taiwan_terms_trigger_one_corrective_retry(monkeypatch):
    client = QueueClient(
        [
            _enrichment_response(zh_term="激活"),
            _enrichment_response(),
        ]
    )
    enricher = ContentEnricher(client)
    _configure_search(monkeypatch, enricher, [])

    item = _item()
    asyncio.run(enricher._enrich_item(item))

    assert len(client.calls) == 2
    assert "VALIDATION FAILURE" in client.calls[1]["user"]
    assert "激活" in client.calls[1]["user"]
    assert item.metadata["detailed_summary_zh"] == "新內容。 這很重要。 關鍵細節。"
    assert "激活" not in item.metadata["detailed_summary_zh"]


def test_missing_or_external_sources_trigger_retry_and_only_real_urls_are_kept(
    monkeypatch,
):
    allowed_url = "https://source.example/context"
    client = QueueClient(
        [
            _enrichment_response(sources=["https://not-a-search-result.example/fake"]),
            _enrichment_response(
                sources=[allowed_url, "https://not-a-search-result.example/also-fake"]
            ),
        ]
    )
    enricher = ContentEnricher(client)
    _configure_search(
        monkeypatch,
        enricher,
        [{"title": "Source result", "url": allowed_url, "body": "Context."}],
    )

    item = _item()
    asyncio.run(enricher._enrich_item(item))

    assert len(client.calls) == 2
    assert "sources must contain at least one exact URL" in client.calls[1]["user"]
    assert item.metadata["sources"] == [{"url": allowed_url, "title": "Source result"}]
