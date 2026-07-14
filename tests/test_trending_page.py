"""Tests for the standalone GitHub trending page writer."""

import asyncio
import json
from datetime import datetime, timezone

from src.models import ContentItem, SourceType
from src.services.trending_page import TrendingPageWriter


class FakeClient:
    """Returns valid translations, in order."""

    def __init__(self, translations):
        self.translations = translations
        self.calls = 0
        self.last_user = None
        self.last_max_tokens = None

    async def complete(self, system, user, max_tokens=None):
        self.calls += 1
        self.last_user = user
        self.last_max_tokens = max_tokens
        return json.dumps({"translations": self.translations}, ensure_ascii=False)


class GarbageClient:
    async def complete(self, system, user, max_tokens=None):
        return "抱歉，我沒辦法輸出 JSON"


class BoomClient:
    async def complete(self, system, user, max_tokens=None):
        raise RuntimeError("ollama is down")


def _repo(rank, name="owner/repo", stars=5, lang="Python", desc="An English description"):
    return ContentItem(
        id=f"ossinsight:trending:{rank}",
        source_type=SourceType.OSSINSIGHT,
        title=f"{name} (+{stars}⭐ past_24_hours)",
        url=f"https://github.com/{name}",
        published_at=datetime(2026, 7, 14, tzinfo=timezone.utc),
        metadata={
            "repo": name,
            "trending_rank": rank,
            "stars_gained": stars,
            "primary_language": lang,
            "description": desc,
            "category": "github",
        },
    )


def _write(writer, items, tmp_path, date_str="2026-07-14"):
    path = tmp_path / "github-trending.md"
    return asyncio.run(writer.write(items, date_str, path=str(path), top_n=10)), path


def test_renders_translated_descriptions(tmp_path):
    items = [_repo(1, "a/one", 9, desc="First repo"), _repo(2, "b/two", 5, desc="Second repo")]
    client = FakeClient(["第一個倉庫", "第二個倉庫"])
    result, path = _write(TrendingPageWriter(client), items, tmp_path)

    text = path.read_text(encoding="utf-8")
    assert result is not None
    assert client.calls == 1  # one batched call, not one per repo
    # qwen3 needs thinking disabled and headroom, or it returns empty content
    assert "/no_think" in client.last_user
    assert client.last_max_tokens == 8192
    assert "第一個倉庫" in text and "第二個倉庫" in text
    assert "[a/one](https://github.com/a/one)" in text
    assert "+9" in text and "Python" in text
    assert "2026-07-14" in text
    assert "permalink: /github-trending/" in text


def test_falls_back_to_english_on_unparseable_response(tmp_path):
    items = [_repo(1, desc="Original text")]
    _, path = _write(TrendingPageWriter(GarbageClient()), items, tmp_path)
    assert "Original text" in path.read_text(encoding="utf-8")


def test_falls_back_to_english_on_client_error(tmp_path):
    items = [_repo(1, desc="Original text")]
    _, path = _write(TrendingPageWriter(BoomClient()), items, tmp_path)
    assert "Original text" in path.read_text(encoding="utf-8")


def test_falls_back_when_translation_count_mismatch(tmp_path):
    items = [_repo(1, desc="One"), _repo(2, desc="Two")]
    _, path = _write(TrendingPageWriter(FakeClient(["只有一個"])), items, tmp_path)
    text = path.read_text(encoding="utf-8")
    assert "One" in text and "Two" in text


def test_caps_at_top_n_by_rank(tmp_path):
    items = [_repo(r, name=f"o/r{r}") for r in range(12, 0, -1)]  # unsorted input
    _, path = _write(TrendingPageWriter(FakeClient([f"翻{i}" for i in range(10)])), items, tmp_path)
    text = path.read_text(encoding="utf-8")
    assert "o/r1]" in text and "o/r10]" in text
    assert "o/r11]" not in text and "o/r12]" not in text


def test_no_items_writes_nothing(tmp_path):
    result, path = _write(TrendingPageWriter(FakeClient([])), [], tmp_path)
    assert result is None
    assert not path.exists()


def test_without_client_keeps_english(tmp_path):
    items = [_repo(1, desc="Plain English")]
    _, path = _write(TrendingPageWriter(None), items, tmp_path)
    assert "Plain English" in path.read_text(encoding="utf-8")
