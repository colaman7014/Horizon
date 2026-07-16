"""All Traditional-Chinese-producing prompts must carry the Taiwan glossary.

Ensures a single shared TAIWAN_GLOSSARY (keep company/product names in English,
use Taiwan vocabulary over mainland forms) is wired into every zh output path:
the trending translation, the bilingual enrichment, and the lightweight tail
translation in _translate_item.
"""

import asyncio
from datetime import datetime, timezone

from src.ai.enricher import ContentEnricher
from src.ai.prompts import (
    TAIWAN_GLOSSARY,
    TRENDING_TRANSLATION_SYSTEM,
    CONTENT_ENRICHMENT_SYSTEM,
)
from src.models import AIConfig, ContentItem, SourceType


class SystemRecordingClient:
    """Fake AI client that records the system prompt passed to complete()."""

    def __init__(self, config):
        self.config = config
        self.systems = []

    async def complete(self, system, user, max_tokens=None):
        self.systems.append(system)
        return '{"title_zh": "標題", "summary_zh": "摘要。"}'


def test_trending_translation_prompt_includes_glossary():
    assert TAIWAN_GLOSSARY in TRENDING_TRANSLATION_SYSTEM


def test_enrichment_prompt_includes_glossary():
    assert TAIWAN_GLOSSARY in CONTENT_ENRICHMENT_SYSTEM


def test_glossary_keeps_company_names_in_english_and_lists_tw_vocab():
    # Core intent: brand names stay English, plus at least one vocab mapping.
    assert "英文" in TAIWAN_GLOSSARY
    assert "軟件→軟體" in TAIWAN_GLOSSARY


def test_translate_item_system_prompt_includes_glossary():
    client = SystemRecordingClient(
        AIConfig(provider="openai", model="test", api_key_env="TEST_API_KEY")
    )
    enricher = ContentEnricher(client)
    item = ContentItem(
        id="rss:1",
        source_type=SourceType.RSS,
        title="Nvidia beats AMD",
        url="https://example.com/1",
        published_at=datetime(2026, 7, 17, tzinfo=timezone.utc),
        ai_summary="Some summary.",
    )

    asyncio.run(enricher._translate_item(item))

    assert client.systems, "expected a translation call"
    assert TAIWAN_GLOSSARY in client.systems[0]
