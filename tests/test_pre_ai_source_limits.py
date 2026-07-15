from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from pydantic import ValidationError
from rich.console import Console

from src.models import ContentItem, FilteringConfig, SourceType
from src.orchestrator import HorizonOrchestrator


def _item(item_id: str, source_type: SourceType, metadata: dict) -> ContentItem:
    return ContentItem(
        id=item_id,
        source_type=source_type,
        title=item_id,
        url=f"https://example.com/{item_id}",
        published_at=datetime.now(timezone.utc),
        metadata=metadata,
    )


def _orchestrator(limits: dict[str, int]) -> HorizonOrchestrator:
    orchestrator = HorizonOrchestrator.__new__(HorizonOrchestrator)
    orchestrator.config = SimpleNamespace(
        filtering=FilteringConfig(pre_ai_source_limits=limits)
    )
    orchestrator.console = Console(record=True)
    return orchestrator


def test_pre_ai_source_limits_apply_exact_sub_source_before_scoring():
    orchestrator = _orchestrator({"openbb/megacaps": 2})
    items = [
        _item("openbb-1", SourceType.OPENBB, {"watchlist": "megacaps"}),
        _item("openbb-2", SourceType.OPENBB, {"watchlist": "megacaps"}),
        _item("openbb-3", SourceType.OPENBB, {"watchlist": "megacaps"}),
        _item("rss-1", SourceType.RSS, {"feed_name": "Anue"}),
    ]

    result = orchestrator.apply_pre_ai_source_limits(items)

    assert [item.id for item in result] == ["openbb-1", "openbb-2", "rss-1"]
    assert "Pre-AI caps removed 1 items" in orchestrator.console.export_text()


def test_pre_ai_source_limits_support_source_type_fallback():
    orchestrator = _orchestrator({"google_news": 1})
    items = [
        _item("g1", SourceType.GOOGLE_NEWS, {"source_name": "A"}),
        _item("g2", SourceType.GOOGLE_NEWS, {"source_name": "B"}),
        _item("r1", SourceType.RSS, {"feed_name": "Anue"}),
    ]

    result = orchestrator.apply_pre_ai_source_limits(items)

    assert [item.id for item in result] == ["g1", "r1"]


def test_pre_ai_source_limits_reject_non_positive_limits():
    with pytest.raises(ValidationError):
        FilteringConfig(pre_ai_source_limits={"rss/Anue": 0})
