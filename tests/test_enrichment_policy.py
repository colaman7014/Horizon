from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.ai.enrichment_policy import select_items_for_enrichment
from src.models import AIConfig, ContentItem, SourceType


def _item(item_id: str) -> ContentItem:
    return ContentItem(
        id=item_id,
        source_type=SourceType.RSS,
        title=item_id,
        url=f"https://example.com/{item_id}",
        published_at=datetime.now(timezone.utc),
    )


def test_ai_config_defaults_enrichment_top_n_to_10():
    config = AIConfig(provider="openai", model="test", api_key_env="TEST_API_KEY")
    assert config.enrichment_top_n == 10


def test_enrichment_top_n_can_be_disabled_with_null():
    config = AIConfig(
        provider="openai",
        model="test",
        api_key_env="TEST_API_KEY",
        enrichment_top_n=None,
    )
    assert config.enrichment_top_n is None


def test_enrichment_top_n_rejects_zero():
    with pytest.raises(ValidationError):
        AIConfig(
            provider="openai",
            model="test",
            api_key_env="TEST_API_KEY",
            enrichment_top_n=0,
        )


def test_select_items_for_enrichment_returns_top_n_in_order():
    items = [_item(str(i)) for i in range(12)]
    selected = select_items_for_enrichment(items, 10)
    assert [item.id for item in selected] == [str(i) for i in range(10)]


def test_select_items_for_enrichment_none_means_all_items():
    items = [_item(str(i)) for i in range(3)]
    selected = select_items_for_enrichment(items, None)
    assert selected == items
