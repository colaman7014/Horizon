"""Tests for chunked topic deduplication in the orchestrator."""

import asyncio
import json
import re
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from src import orchestrator as orchestrator_module
from src.models import (
    AIConfig,
    AIProvider,
    Config,
    ContentItem,
    FilteringConfig,
    SourcesConfig,
    SourceType,
)
from src.orchestrator import HorizonOrchestrator


def _make_item(idx: int, title: str) -> ContentItem:
    return ContentItem(
        id=f"item-{idx}",
        source_type=SourceType.RSS,
        title=title,
        url=f"https://example.com/{idx}",
        published_at=datetime(2026, 7, 11, tzinfo=timezone.utc),
        ai_score=8.0,
        ai_summary=f"Summary of {title}",
        ai_tags=["news"],
    )


def _make_orchestrator() -> HorizonOrchestrator:
    config = Config(
        ai=AIConfig(provider=AIProvider.OLLAMA, model="test", api_key_env=""),
        sources=SourcesConfig(),
        filtering=FilteringConfig(),
    )
    return HorizonOrchestrator(config, SimpleNamespace())


class FakeAIClient:
    """Groups consecutive items that share the same title.

    Mimics what the dedup prompt asks the model to do, deterministically.
    Optionally emits garbage for the first N calls to exercise the retry
    path.
    """

    def __init__(self, garbage_first_n_calls: int = 0):
        self.calls = []
        self._garbage_left = garbage_first_n_calls

    async def complete(self, system, user, temperature=None, max_tokens=None):
        indexed = re.findall(r"^\[(\d+)\] (.+)$", user, flags=re.MULTILINE)
        self.calls.append(len(indexed))
        if self._garbage_left > 0:
            self._garbage_left -= 1
            return "<think>truncated garbage"
        groups = {}
        for idx, title in indexed:
            groups.setdefault(title, []).append(int(idx))
        duplicates = [g for g in groups.values() if len(g) > 1]
        return json.dumps({"duplicates": duplicates})


def test_large_batch_is_chunked_and_duplicates_merged(monkeypatch):
    orch = _make_orchestrator()
    fake = FakeAIClient()
    monkeypatch.setattr(orchestrator_module, "create_ai_client", lambda _cfg: fake)

    # 66 items: three stories duplicated 5x/4x/3x (adjacent, as score-sorted
    # duplicates typically are), the rest unique.
    titles = (
        ["Apple sues OpenAI"] * 5
        + ["SK Hynix lists on Nasdaq"] * 4
        + [f"unique-a-{i}" for i in range(20)]
        + ["Fed holds rates"] * 3
        + [f"unique-b-{i}" for i in range(34)]
    )
    items = [_make_item(i, t) for i, t in enumerate(titles)]
    assert len(items) == 66

    result = asyncio.run(orch.merge_topic_duplicates(items))

    result_titles = [item.title for item in result]
    assert result_titles.count("Apple sues OpenAI") == 1
    assert result_titles.count("SK Hynix lists on Nasdaq") == 1
    assert result_titles.count("Fed holds rates") == 1
    assert len(result) == 66 - 4 - 3 - 2
    # Every AI call must stay within the chunk size
    assert all(n <= HorizonOrchestrator.TOPIC_DEDUP_CHUNK_SIZE for n in fake.calls)
    # Highest-scored (first) duplicate is kept
    assert result[0].id == "item-0"


def test_unparseable_response_is_retried_once(monkeypatch):
    orch = _make_orchestrator()
    fake = FakeAIClient(garbage_first_n_calls=1)
    monkeypatch.setattr(orchestrator_module, "create_ai_client", lambda _cfg: fake)

    items = [_make_item(0, "same story"), _make_item(1, "same story")]
    result = asyncio.run(orch.merge_topic_duplicates(items))

    assert len(result) == 1
    assert len(fake.calls) == 2  # first garbage call + successful retry


def test_persistent_parse_failure_returns_items_unchanged(monkeypatch):
    orch = _make_orchestrator()
    fake = FakeAIClient(garbage_first_n_calls=99)
    monkeypatch.setattr(orchestrator_module, "create_ai_client", lambda _cfg: fake)

    items = [_make_item(0, "same story"), _make_item(1, "same story")]
    result = asyncio.run(orch.merge_topic_duplicates(items))

    assert len(result) == 2
