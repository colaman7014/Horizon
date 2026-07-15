# Local LLM Performance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce Horizon's Docker-based local Ollama daily-run wall-clock time by reducing LLM work units, not by increasing local LLM concurrency.

**Architecture:** Add measurable run-stage observability first, then add source-aware pre-AI caps before scoring, top-10 enrichment selection before background enrichment, and a Docker-backed `/no_think` benchmark harness. The pipeline remains sequential for local Ollama LLM calls because the local backend has been tested as single-request-at-a-time.

**Tech Stack:** Python 3.11, Pydantic v2, asyncio, pytest, Docker Compose, Ollama OpenAI-compatible `/v1/chat/completions`.

## Global Constraints

- Verification commands for this repo must run in Docker or the same containerized environment used by the daily job.
- Host-level Python commands are not authoritative for this deployment.
- Local Ollama throughput must be modeled as single-request-at-a-time unless a future benchmark proves otherwise.
- Increasing `analysis_concurrency` or `enrichment_concurrency` is not an accepted optimization for the current local deployment.
- Optimizations must preserve the daily digest's usefulness: fewer LLM calls cannot mean blindly dropping all finance or tech sources.
- TDD is required for behavior changes: write the failing test, verify RED in Docker, implement the minimum code, verify GREEN in Docker.

## Docker Test Command

Use this command shape for task-level tests. It mounts the local `tests/` directory into the container and installs the `dev` extra inside the disposable test container:

```bash
docker compose run --rm --build --entrypoint sh \
  -v "$PWD/tests:/app/tests:ro" \
  horizon -lc 'uv sync --frozen --extra openbb --extra dev && uv run pytest tests/test_file.py -q'
```

Replace `tests/test_file.py` with the exact task test file. Do not use host `python3 -m pytest` as proof.

## File Structure

Modify:

- `src/models.py` — add config fields for pre-AI source caps, top-N enrichment, and enrichment `max_tokens`.
- `src/orchestrator.py` — add stage timing, pre-AI cap application, item-count logging, and top-N enrichment routing.
- `src/mcp/service.py` — apply the same top-N enrichment policy for MCP enrichment runs.
- `src/ai/enricher.py` — pass a larger `max_tokens` to the bilingual enrichment call so qwen3 stops truncating JSON.
- `data/config.example.json` — document safe defaults without exposing secrets.
- `data/config.json` — add the local deployment's chosen caps and `enrichment_top_n: 10` if the user wants the repo-local config updated.
- `docs/configuration.md` — update after behavior is working; document Docker verification, pre-AI caps, and enrichment top-N.

Create:

- `src/ai/enrichment_policy.py` — small shared policy function for orchestrator and MCP enrichment paths.
- `src/tools/no_think_benchmark.py` — Docker-runnable benchmark harness; no production behavior change.
- `tests/test_orchestrator_metrics.py` — run-stage observability tests.
- `tests/test_pre_ai_source_limits.py` — source-aware cap tests.
- `tests/test_enrichment_policy.py` — top-N enrichment selection tests.
- `tests/test_enricher_max_tokens.py` — enrichment `max_tokens` config + call-through tests.
- `tests/test_no_think_benchmark.py` — benchmark harness pure-function tests.

---

### Task 1: Docker-backed run-stage observability

**Files:**
- Modify: `src/orchestrator.py`
- Create: `tests/test_orchestrator_metrics.py`

**Interfaces:**
- Consumes: existing `HorizonOrchestrator.run()` control flow.
- Produces: console-visible stage timing and item-count logs. Later tasks rely on these logs for verification evidence.

- [ ] **Step 1: Write the failing test**

Create `tests/test_orchestrator_metrics.py`:

```python
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
```

- [ ] **Step 2: Run RED in Docker**

```bash
docker compose run --rm --build --entrypoint sh \
  -v "$PWD/tests:/app/tests:ro" \
  horizon -lc 'uv sync --frozen --extra openbb --extra dev && uv run pytest tests/test_orchestrator_metrics.py -q'
```

Expected: FAIL because `HorizonOrchestrator.run()` does not yet emit the `⏱️ ...` lines or `LLM scoring candidates` line.

- [ ] **Step 3: Implement minimal stage timing**

In `src/orchestrator.py`, add the import:

```python
from time import perf_counter
```

Add this helper method inside `HorizonOrchestrator`:

```python
    def _log_elapsed(self, label: str, started_at: float) -> None:
        elapsed = perf_counter() - started_at
        self.console.print(f"⏱️ {label} completed in {elapsed:.1f}s")
```

Update `run()` around fetch, AI scoring, and enrichment:

```python
            fetch_started = perf_counter()
            all_items = await self.fetch_all_sources(since)
            self._log_elapsed("Fetch", fetch_started)
            self.console.print(f"📥 Fetched {len(all_items)} items from all sources\n")
```

```python
            self.console.print(f"LLM scoring candidates: {len(merged_items)}")
            scoring_started = perf_counter()
            analyzed_items = await self._analyze_content(merged_items)
            self._log_elapsed("AI scoring", scoring_started)
            self.console.print(f"🤖 Analyzed {len(analyzed_items)} items with AI\n")
```

```python
            enrichment_started = perf_counter()
            await self._enrich_important_items(important_items)
            self._log_elapsed("Enrichment", enrichment_started)
```

Do not change pipeline ordering in this task.

- [ ] **Step 4: Run GREEN in Docker**

```bash
docker compose run --rm --build --entrypoint sh \
  -v "$PWD/tests:/app/tests:ro" \
  horizon -lc 'uv sync --frozen --extra openbb --extra dev && uv run pytest tests/test_orchestrator_metrics.py -q'
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/orchestrator.py tests/test_orchestrator_metrics.py
git commit -m "perf: log local llm pipeline stage timings"
```

---

### Task 2: Balanced pre-AI source caps

**Files:**
- Modify: `src/models.py`
- Modify: `src/orchestrator.py`
- Create: `tests/test_pre_ai_source_limits.py`

**Interfaces:**
- Consumes: `FilteringConfig` and `HorizonOrchestrator._sub_source_label()`.
- Produces: `FilteringConfig.pre_ai_source_limits: Dict[str, int]` and `HorizonOrchestrator.apply_pre_ai_source_limits(items)`.
- Key format: exact source key `"<source_type>/<sub_source>"` wins over source-type key `"<source_type>"`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_pre_ai_source_limits.py`:

```python
from datetime import datetime, timezone
from types import SimpleNamespace

from pydantic import ValidationError
import pytest
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
```

- [ ] **Step 2: Run RED in Docker**

```bash
docker compose run --rm --build --entrypoint sh \
  -v "$PWD/tests:/app/tests:ro" \
  horizon -lc 'uv sync --frozen --extra openbb --extra dev && uv run pytest tests/test_pre_ai_source_limits.py -q'
```

Expected: FAIL because `FilteringConfig.pre_ai_source_limits` and `apply_pre_ai_source_limits()` do not exist.

- [ ] **Step 3: Add config field**

In `src/models.py`, keep the existing `pydantic` import style. `field_validator` is already imported in this file, so only add missing names if the file has changed by execution time.

Update `FilteringConfig`:

```python
class FilteringConfig(BaseModel):
    """Content filtering configuration."""

    ai_score_threshold: float = 7.0
    time_window_hours: int = 24
    max_items: Optional[int] = Field(default=None, gt=0)
    category_groups: Dict[str, CategoryGroupConfig] = Field(default_factory=dict)
    default_group: str = "other"
    default_group_limit: Optional[int] = Field(default=None, gt=0)
    pre_ai_source_limits: Dict[str, int] = Field(default_factory=dict)

    @field_validator("pre_ai_source_limits")
    @classmethod
    def validate_pre_ai_source_limits(cls, value: Dict[str, int]) -> Dict[str, int]:
        for key, limit in value.items():
            if not key or not key.strip():
                raise ValueError("filtering.pre_ai_source_limits keys must be non-empty")
            if limit <= 0:
                raise ValueError("filtering.pre_ai_source_limits values must be positive")
        return value
```

Use the existing `field_validator` import already present in `src/models.py`.

- [ ] **Step 4: Add the cap helper and call it before scoring**

In `src/orchestrator.py`, add this method inside `HorizonOrchestrator` near `apply_balanced_digest()`:

```python
    def apply_pre_ai_source_limits(self, items: List[ContentItem]) -> List[ContentItem]:
        """Apply source-aware caps before expensive per-item AI scoring."""
        limits = self.config.filtering.pre_ai_source_limits
        if not limits:
            return items

        kept: List[ContentItem] = []
        counts: Dict[str, int] = defaultdict(int)
        removed = 0

        for item in items:
            sub_source_key = f"{item.source_type.value}/{self._sub_source_label(item)}"
            source_key = item.source_type.value
            limit = limits.get(sub_source_key, limits.get(source_key))
            if limit is None:
                kept.append(item)
                continue

            counts[sub_source_key if sub_source_key in limits else source_key] += 1
            if counts[sub_source_key if sub_source_key in limits else source_key] <= limit:
                kept.append(item)
            else:
                removed += 1

        if removed:
            self.console.print(
                f"⚖️ Pre-AI caps removed {removed} items "
                f"→ {len(kept)} scoring candidates\n"
            )
        return kept
```

In `run()`, call it after OSS Insight trending removal and before `_analyze_content()`:

```python
            merged_items = self.apply_pre_ai_source_limits(merged_items)
```

The resulting line order must be:

1. merge URL duplicates
2. remove/write GitHub trending page
3. apply pre-AI caps
4. log `LLM scoring candidates`
5. analyze content

- [ ] **Step 5: Run GREEN in Docker**

```bash
docker compose run --rm --build --entrypoint sh \
  -v "$PWD/tests:/app/tests:ro" \
  horizon -lc 'uv sync --frozen --extra openbb --extra dev && uv run pytest tests/test_pre_ai_source_limits.py tests/test_balanced_digest.py -q'
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/models.py src/orchestrator.py tests/test_pre_ai_source_limits.py
git commit -m "perf: cap noisy sources before ai scoring"
```

---

### Task 3: Top-10 enrichment policy shared by orchestrator and MCP

**Files:**
- Modify: `src/models.py`
- Create: `src/ai/enrichment_policy.py`
- Modify: `src/orchestrator.py`
- Modify: `src/mcp/service.py`
- Create: `tests/test_enrichment_policy.py`

**Interfaces:**
- Produces: `AIConfig.enrichment_top_n: Optional[int] = 10`.
- Produces: `select_items_for_enrichment(items: Sequence[ContentItem], top_n: Optional[int]) -> list[ContentItem]`.
- Consumed by: `HorizonOrchestrator._enrich_important_items()` and `HorizonMcpService.enrich_items()`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_enrichment_policy.py`:

```python
from datetime import datetime, timezone

from pydantic import ValidationError
import pytest

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
```

- [ ] **Step 2: Run RED in Docker**

```bash
docker compose run --rm --build --entrypoint sh \
  -v "$PWD/tests:/app/tests:ro" \
  horizon -lc 'uv sync --frozen --extra openbb --extra dev && uv run pytest tests/test_enrichment_policy.py -q'
```

Expected: FAIL because `src.ai.enrichment_policy` and `AIConfig.enrichment_top_n` do not exist.

- [ ] **Step 3: Add the config field**

In `src/models.py`, update `AIConfig`:

```python
class AIConfig(BaseModel):
    """AI client configuration."""

    provider: AIProvider
    provider_chain: Optional[str] = None
    model: str
    base_url: Optional[str] = None
    api_key_env: str
    temperature: float = 0.3
    max_tokens: int = 4096
    throttle_sec: float = 0.0
    analysis_concurrency: int = 1
    enrichment_concurrency: int = 1
    enrichment_top_n: Optional[int] = Field(default=10, gt=0)
    languages: List[str] = Field(default_factory=lambda: ["en"])
    azure_endpoint_env: Optional[str] = None
    api_version: Optional[str] = None
```

`None` means enrich all selected items. The default `10` implements the confirmed local deployment policy.

- [ ] **Step 4: Add the shared policy module**

Create `src/ai/enrichment_policy.py`:

```python
"""Selection policy for expensive second-pass enrichment."""

from collections.abc import Sequence
from typing import Optional

from ..models import ContentItem


def select_items_for_enrichment(
    items: Sequence[ContentItem],
    top_n: Optional[int],
) -> list[ContentItem]:
    """Return the selected prefix for full enrichment.

    Items are already score-sorted by the orchestrator/filter stage. `None`
    preserves legacy behavior by enriching every selected item.
    """
    if top_n is None:
        return list(items)
    return list(items[:top_n])
```

- [ ] **Step 5: Route orchestrator enrichment through the policy**

In `src/orchestrator.py`, add import:

```python
from .ai.enrichment_policy import select_items_for_enrichment
```

Update `_enrich_important_items()`:

```python
        self.console.print("📚 Enriching with background knowledge...")
        ai_client = create_ai_client(self.config.ai)
        enricher = ContentEnricher(ai_client)
        items_to_enrich = select_items_for_enrichment(
            items,
            self.config.ai.enrichment_top_n,
        )
        await enricher.enrich_batch(items_to_enrich)
        self.console.print(
            f"   Enriched {len(items_to_enrich)}/{len(items)} items\n"
        )
```

Do not remove non-enriched items from `important_items`; they must still appear in summaries using `item.ai_summary`.

- [ ] **Step 6: Route MCP enrichment through the same policy**

In `src/mcp/service.py`, add the relative import near the existing `..dates` import:

```python
from ..ai.enrichment_policy import select_items_for_enrichment
```

Update `enrich_items()`:

```python
        ai_client = ctx.runtime.create_ai_client(ctx.config.ai)
        enricher = ctx.runtime.ContentEnricher(ai_client)
        items_to_enrich = select_items_for_enrichment(
            items,
            ctx.config.ai.enrichment_top_n,
        )
        await enricher.enrich_batch(items_to_enrich)
```

Update metadata:

```python
                "enriched_count": len(items_to_enrich),
                "enrichment_input_count": len(items),
```

- [ ] **Step 7: Run GREEN in Docker**

```bash
docker compose run --rm --build --entrypoint sh \
  -v "$PWD/tests:/app/tests:ro" \
  horizon -lc 'uv sync --frozen --extra openbb --extra dev && uv run pytest tests/test_enrichment_policy.py tests/test_balanced_digest.py -q'
```

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add src/models.py src/ai/enrichment_policy.py src/orchestrator.py src/mcp/service.py tests/test_enrichment_policy.py
git commit -m "perf: limit full enrichment to top selected items"
```

---

### Task 4: Raise enrichment `max_tokens` so qwen3 stops truncating JSON

Observed 2026-07-15: qwen3 returned unparseable JSON on the bilingual enrichment call for 2/40 selected items, falling back to plain translation (`Warning: could not parse enrichment response ...`). Root cause is the default `max_tokens` (4096): with thinking enabled, qwen3 spends part of the budget reasoning and truncates the large bilingual JSON. Unlike the trending-page translation, enrichment **must keep thinking on** (it synthesizes web-search context into analysis), so the fix is a larger token budget, not `/no_think`.

This task complements Task 3: once only the top 10 items are enriched, a parse failure on one of just 10 is proportionally more visible, so per-call reliability matters more, not less.

**Files:**
- Modify: `src/models.py`
- Modify: `src/ai/enricher.py`
- Create: `tests/test_enricher_max_tokens.py`

**Interfaces:**
- Produces: `AIConfig.enrichment_max_tokens: int = 8192` (independent of the 4096 scoring budget; safe for cloud providers, which already run higher caps).
- Produces: `ContentEnricher._enrichment_max_tokens()` reading the value from the client config with a safe fallback.
- Consumed by: the enrichment `complete()` call in `ContentEnricher._enrich_item()`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_enricher_max_tokens.py`:

```python
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
```

- [ ] **Step 2: Run RED in Docker**

```bash
docker compose run --rm --build --entrypoint sh \
  -v "$PWD/tests:/app/tests:ro" \
  horizon -lc 'uv sync --frozen --extra openbb --extra dev && uv run pytest tests/test_enricher_max_tokens.py -q'
```

Expected: FAIL because `AIConfig.enrichment_max_tokens` and `ContentEnricher._enrichment_max_tokens()` do not exist, and the enrichment call does not pass `max_tokens`.

- [ ] **Step 3: Add the config field**

In `src/models.py`, add to `AIConfig` (next to `max_tokens`):

```python
    enrichment_max_tokens: int = Field(default=8192, gt=0)
```

- [ ] **Step 4: Pass the budget from the enricher**

In `src/ai/enricher.py`, add a helper on `ContentEnricher` (mirrors the analyzer's `getattr(self.client, "config", None)` pattern):

```python
    def _enrichment_max_tokens(self) -> Optional[int]:
        """Token budget for the bilingual enrichment call.

        qwen3 with thinking on truncates the large enrichment JSON at the
        default 4096 budget; a larger budget keeps the response parseable.
        """
        config = getattr(self.client, "config", None)
        return getattr(config, "enrichment_max_tokens", None)
```

Update the enrichment call in `_enrich_item()` (the `CONTENT_ENRICHMENT_SYSTEM` call, currently near line 188) to pass it — and keep thinking enabled (do **not** append `/no_think`):

```python
        response = await self.client.complete(
            system=CONTENT_ENRICHMENT_SYSTEM,
            user=user_prompt,
            max_tokens=self._enrichment_max_tokens(),
        )
```

Apply the same `max_tokens=self._enrichment_max_tokens()` to the translation-fallback call in `_translate_item()` (also bilingual, currently near line 243), so a fallback triggered by truncation is not itself truncated. `Optional` is already imported in this file.

- [ ] **Step 5: Run GREEN in Docker**

```bash
docker compose run --rm --build --entrypoint sh \
  -v "$PWD/tests:/app/tests:ro" \
  horizon -lc 'uv sync --frozen --extra openbb --extra dev && uv run pytest tests/test_enricher_max_tokens.py tests/test_enrichment_policy.py -q'
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/models.py src/ai/enricher.py tests/test_enricher_max_tokens.py
git commit -m "fix(ai): give enrichment a larger max_tokens so qwen3 stops truncating json"
```

`ai.enrichment_max_tokens` is documented in Task 6 alongside the other performance controls.

---

### Task 5: Docker-backed `/no_think` benchmark harness

**Files:**
- Create: `src/tools/no_think_benchmark.py`
- Create: `src/tools/__init__.py`
- Create: `tests/test_no_think_benchmark.py`

**Interfaces:**
- Produces: `build_prompt_variants(system: str, user: str) -> dict[str, tuple[str, str]]`.
- Produces: Docker-runnable module command `python -m src.tools.no_think_benchmark`.
- Does not change production prompt behavior.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_no_think_benchmark.py`:

```python
from src.tools.no_think_benchmark import build_prompt_variants, summarize_result


def test_build_prompt_variants_keeps_baseline_unchanged():
    variants = build_prompt_variants("system", "user")
    assert variants["baseline"] == ("system", "user")


def test_build_prompt_variants_appends_no_think_to_user_prompt():
    variants = build_prompt_variants("system", "user")
    assert variants["no_think"] == ("system", "user\n/no_think")


def test_summarize_result_includes_parse_and_token_fields():
    summary = summarize_result(
        variant="baseline",
        elapsed_sec=1.25,
        parsed=True,
        input_tokens=100,
        output_tokens=25,
    )
    assert summary == {
        "variant": "baseline",
        "elapsed_sec": 1.25,
        "parsed": True,
        "input_tokens": 100,
        "output_tokens": 25,
    }
```

- [ ] **Step 2: Run RED in Docker**

```bash
docker compose run --rm --build --entrypoint sh \
  -v "$PWD/tests:/app/tests:ro" \
  horizon -lc 'uv sync --frozen --extra openbb --extra dev && uv run pytest tests/test_no_think_benchmark.py -q'
```

Expected: FAIL because the benchmark module does not exist.

- [ ] **Step 3: Add the tools package**

Create `src/tools/__init__.py`:

```python
"""Operational tooling modules for Horizon."""
```

Create `src/tools/no_think_benchmark.py`:

```python
"""Benchmark `/no_think` prompt variants against the configured local LLM.

This module is intentionally outside production pipeline behavior. It is used
only to decide whether `/no_think` should be adopted after Docker-backed
measurement.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from time import perf_counter
from typing import Any

from src.ai.client import create_ai_client
from src.ai.prompts import CONTENT_ANALYSIS_SYSTEM, CONTENT_ANALYSIS_USER
from src.ai.utils import parse_json_response
from src.models import Config, ContentItem, SourceType


def build_prompt_variants(system: str, user: str) -> dict[str, tuple[str, str]]:
    return {
        "baseline": (system, user),
        "no_think": (system, f"{user}\n/no_think"),
    }


def summarize_result(
    *,
    variant: str,
    elapsed_sec: float,
    parsed: bool,
    input_tokens: int,
    output_tokens: int,
) -> dict[str, Any]:
    return {
        "variant": variant,
        "elapsed_sec": round(elapsed_sec, 2),
        "parsed": parsed,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }


def _sample_item() -> ContentItem:
    return ContentItem(
        id="benchmark:sample",
        source_type=SourceType.RSS,
        title="Benchmark item: local LLM JSON scoring",
        url="https://example.com/benchmark",
        content="A concise technology news item used to compare baseline JSON output against /no_think.",
    )


def _analysis_user_prompt(item: ContentItem) -> str:
    return CONTENT_ANALYSIS_USER.format(
        title=item.title,
        source=item.source_type.value,
        author=item.author or "Unknown",
        url=str(item.url),
        content_section=f"Content: {(item.content or '')[:1000]}",
        discussion_section="",
    )


async def run_benchmark(config_path: str = "data/config.json") -> list[dict[str, Any]]:
    config = Config(**json.loads(Path(config_path).read_text(encoding="utf-8")))
    client = create_ai_client(config.ai)
    item = _sample_item()
    variants = build_prompt_variants(CONTENT_ANALYSIS_SYSTEM, _analysis_user_prompt(item))
    results: list[dict[str, Any]] = []

    for variant, (system, user) in variants.items():
        started = perf_counter()
        response = await client.complete(system=system, user=user)
        elapsed = perf_counter() - started
        parsed = parse_json_response(response) is not None
        results.append(
            summarize_result(
                variant=variant,
                elapsed_sec=elapsed,
                parsed=parsed,
                input_tokens=0,
                output_tokens=0,
            )
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark /no_think prompt variants.")
    parser.add_argument("--config", default="data/config.json")
    args = parser.parse_args()
    results = asyncio.run(run_benchmark(args.config))
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

Keep token fields at `0` until a later implementation wires per-request usage into the benchmark. The acceptance criterion for this task is that the harness exists and records elapsed time plus parse success without changing production behavior.

- [ ] **Step 4: Run GREEN in Docker**

```bash
docker compose run --rm --build --entrypoint sh \
  -v "$PWD/tests:/app/tests:ro" \
  horizon -lc 'uv sync --frozen --extra openbb --extra dev && uv run pytest tests/test_no_think_benchmark.py -q'
```

Expected: PASS.

- [ ] **Step 5: Smoke-run the benchmark in Docker only when Ollama is available**

```bash
docker compose run --rm --build --entrypoint uv horizon run python -m src.tools.no_think_benchmark --config data/config.json
```

Expected when Ollama is reachable: JSON array with `baseline` and `no_think` rows. If Ollama is not reachable, record the connection failure and do not claim benchmark success.

- [ ] **Step 6: Commit**

```bash
git add src/tools/__init__.py src/tools/no_think_benchmark.py tests/test_no_think_benchmark.py
git commit -m "chore: add qwen no-think benchmark harness"
```

---

### Task 6: Configuration and documentation cleanup

**Files:**
- Modify: `data/config.example.json`
- Modify: `docs/configuration.md`
- Optionally modify: `data/config.json`

**Interfaces:**
- Consumes: fields implemented in Tasks 2 and 3.
- Produces: documented config for Docker/local-Ollama deployments.

- [ ] **Step 1: Update example config after tests are green**

In `data/config.example.json`, add:

```json
{
  "ai": {
    "enrichment_top_n": 10,
    "enrichment_max_tokens": 8192
  },
  "filtering": {
    "pre_ai_source_limits": {
      "openbb/tech-megacaps": 15,
      "openbb/semiconductors": 15,
      "rss/Anue 鉅亨網台股": 20,
      "google_news": 15
    }
  }
}
```

Merge this into the existing JSON structure; do not replace unrelated config.

- [ ] **Step 2: Update local config only if this repository's `data/config.json` is the intended deployment config**

If updating `data/config.json`, add:

```json
"enrichment_top_n": 10,
"enrichment_max_tokens": 8192
```

inside `ai`, and add:

```json
"pre_ai_source_limits": {
  "openbb/tech-megacaps": 15,
  "openbb/semiconductors": 15,
  "rss/Anue 鉅亨網台股": 20,
  "google_news": 15
}
```

inside `filtering`.

- [ ] **Step 3: Update `docs/configuration.md`**

Add a section near AI concurrency:

```markdown
### Local Ollama throughput

For local Ollama deployments that can only process one useful chat request at a time, do not rely on Horizon concurrency settings for speed. Keep `analysis_concurrency` and `enrichment_concurrency` at `1`, then reduce LLM work with pre-AI source caps and `enrichment_top_n`.
```

Add a section near filtering:

```markdown
### Pre-AI source limits

`filtering.pre_ai_source_limits` caps noisy sources before per-item AI scoring. Keys use either the source type, such as `google_news`, or the source/sub-source label shown in run logs, such as `openbb/tech-megacaps` or `rss/Anue 鉅亨網台股`.

```json
{
  "filtering": {
    "pre_ai_source_limits": {
      "openbb/tech-megacaps": 15,
      "openbb/semiconductors": 15,
      "rss/Anue 鉅亨網台股": 20,
      "google_news": 15
    }
  }
}
```
```

Add a section near enrichment:

```markdown
### Top-N enrichment

`ai.enrichment_top_n` limits the expensive second-pass enrichment stage. All selected items remain in the digest with their scoring summaries, but only the first N selected items receive full background enrichment. Set it to `null` to enrich every selected item.
```

Add a section on the enrichment token budget:

```markdown
### Enrichment token budget

`ai.enrichment_max_tokens` (default `8192`) is the token budget for the bilingual background-enrichment call, separate from the `max_tokens` used for scoring. Local reasoning models such as qwen3 spend part of the budget thinking; the default 4096 can truncate the large bilingual JSON and force a fallback to plain translation. Keep this at 8192 or higher for local thinking models. Do not disable thinking for enrichment — it needs reasoning to synthesize web-search context (that trick is only for mechanical tasks like the trending-page translation).
```

- [ ] **Step 4: Run focused Docker tests**

```bash
docker compose run --rm --build --entrypoint sh \
  -v "$PWD/tests:/app/tests:ro" \
  horizon -lc 'uv sync --frozen --extra openbb --extra dev && uv run pytest tests/test_orchestrator_metrics.py tests/test_pre_ai_source_limits.py tests/test_enrichment_policy.py tests/test_enricher_max_tokens.py tests/test_no_think_benchmark.py tests/test_balanced_digest.py tests/test_google_news.py tests/test_openbb_scraper.py tests/test_rss.py -q'
```

Expected: PASS.

- [ ] **Step 5: Smoke-check config parsing in Docker**

```bash
docker compose run --rm --build --entrypoint uv horizon run python -c 'from src.storage.manager import StorageManager; c=StorageManager("data").load_config(); print(c.ai.enrichment_top_n); print(c.filtering.pre_ai_source_limits)'
```

Expected: prints `10` and the configured source-limit mapping, or `{}` if local `data/config.json` was intentionally left unchanged.

- [ ] **Step 6: Commit**

```bash
git add data/config.example.json docs/configuration.md data/config.json
git commit -m "docs: document local ollama performance controls"
```

If `data/config.json` is intentionally not changed, omit it from `git add`.

---

## Final Verification

After all tasks are implemented, run:

```bash
docker compose run --rm --build --entrypoint sh \
  -v "$PWD/tests:/app/tests:ro" \
  horizon -lc 'uv sync --frozen --extra openbb --extra dev && uv run pytest tests/test_orchestrator_metrics.py tests/test_pre_ai_source_limits.py tests/test_enrichment_policy.py tests/test_enricher_max_tokens.py tests/test_no_think_benchmark.py tests/test_balanced_digest.py tests/test_google_news.py tests/test_openbb_scraper.py tests/test_rss.py -q'
```

Then run a non-publishing smoke command against the daily container path only if the environment has reachable Ollama and source credentials:

```bash
docker compose run --rm --build horizon --hours 24
```

Record:

- Number of fetched items.
- Number of LLM scoring candidates.
- Number of selected items.
- Number of enriched items versus selected items.
- Ollama `/v1/chat/completions` count from `/opt/homebrew/var/log/ollama.log` or `scripts/watch-progress.sh`.
- Stage timings printed by Horizon.
- Token usage summary printed by Horizon.

## Self-Review

Spec coverage:

- Docker-only verification: covered by Global Constraints, Docker Test Command, and every test command.
- Local LLM single-thread constraint: covered by Architecture and Non-Goal of not increasing concurrency.
- Balanced pre-AI caps: Task 2.
- Top-10 enrichment: Task 3.
- Enrichment reliability (raise `max_tokens`, keep thinking on): Task 4.
- `/no_think` benchmark first: Task 5.
- Config and docs cleanup: Task 6.
- Observability: Task 1 and Final Verification.

Placeholder scan:

- No `TBD`, `TODO`, or unspecified test commands remain.
- Every code-changing task includes RED and GREEN Docker commands.

Type consistency:

- `FilteringConfig.pre_ai_source_limits` is used by `HorizonOrchestrator.apply_pre_ai_source_limits()`.
- `AIConfig.enrichment_top_n` is used by `select_items_for_enrichment()` callers in orchestrator and MCP service.
- `select_items_for_enrichment()` returns `list[ContentItem]` for both production call sites.
- `AIConfig.enrichment_max_tokens` is read by `ContentEnricher._enrichment_max_tokens()` and passed to the enrichment and translation-fallback `complete()` calls.
