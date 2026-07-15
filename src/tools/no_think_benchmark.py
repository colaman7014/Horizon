"""Benchmark Qwen /no_think prompting without changing production behavior."""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from time import perf_counter
from typing import Any, Callable

from src.ai.client import create_ai_client
from src.ai.prompts import CONTENT_ANALYSIS_SYSTEM, CONTENT_ANALYSIS_USER
from src.ai.tokens import get_usage_snapshot
from src.ai.utils import parse_json_response
from src.models import Config, ContentItem, SourceType


def build_prompt_variants(system: str, user: str) -> dict[str, tuple[str, str]]:
    """Return the baseline prompt and the candidate /no_think prompt."""
    return {
        "baseline": (system, user),
        "no_think": (system, f"/no_think\n{user}"),
    }


def _usage_delta(before: dict[str, int], after: dict[str, int], key: str) -> int:
    return int(after.get(key, 0)) - int(before.get(key, 0))


def summarize_result(
    *,
    variant: str,
    elapsed_sec: float,
    response: str,
    usage_before: dict[str, int],
    usage_after: dict[str, int],
) -> dict[str, Any]:
    """Summarize latency, parse success, score, token use, and response size."""
    parsed = parse_json_response(response)
    return {
        "variant": variant,
        "elapsed_sec": round(elapsed_sec, 2),
        "parse_success": parsed is not None,
        "score": parsed.get("score") if parsed else None,
        "input_tokens": _usage_delta(usage_before, usage_after, "input_tokens"),
        "output_tokens": _usage_delta(usage_before, usage_after, "output_tokens"),
        "total_tokens": _usage_delta(usage_before, usage_after, "total_tokens"),
        "response_chars": len(response),
    }


async def run_benchmark(
    client: Any,
    *,
    usage_snapshot: Callable[[], dict[str, int]] = get_usage_snapshot,
    system: str = CONTENT_ANALYSIS_SYSTEM,
    user: str,
) -> list[dict[str, Any]]:
    """Run the benchmark variants sequentially against one client."""
    results: list[dict[str, Any]] = []
    for variant, (variant_system, variant_user) in build_prompt_variants(system, user).items():
        usage_before = usage_snapshot()
        started = perf_counter()
        response = await client.complete(system=variant_system, user=variant_user)
        elapsed = perf_counter() - started
        usage_after = usage_snapshot()
        results.append(
            summarize_result(
                variant=variant,
                elapsed_sec=elapsed,
                response=response,
                usage_before=usage_before,
                usage_after=usage_after,
            )
        )
    return results


def _sample_item() -> ContentItem:
    return ContentItem(
        id="benchmark:sample",
        source_type=SourceType.RSS,
        title="Open-source local LLM tool improves structured JSON generation",
        url="https://example.com/local-llm-json",
        content=(
            "A new open-source inference tool claims faster structured JSON output "
            "for local language models while preserving schema adherence. Early users "
            "report lower latency on consumer GPUs, but benchmarks vary by prompt style."
        ),
        author="Benchmark Fixture",
        published_at="2026-07-15T00:00:00Z",
        metadata={"score": 120, "discussion_url": "https://example.com/discussion"},
    )


def _analysis_user_prompt(item: ContentItem) -> str:
    return CONTENT_ANALYSIS_USER.format(
        title=item.title,
        source=item.source_type.value,
        author=item.author or "Unknown",
        url=str(item.url),
        content_section=f"Content: {item.content[:1000] if item.content else ''}",
        discussion_section="Engagement: score: 120\nDiscussion: https://example.com/discussion",
    )


async def _amain(config_path: str) -> int:
    config = Config(**json.loads(Path(config_path).read_text(encoding="utf-8")))
    client = create_ai_client(config.ai)
    results = await run_benchmark(client, user=_analysis_user_prompt(_sample_item()))
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark baseline vs Qwen /no_think prompting.")
    parser.add_argument("--config", default="data/config.json", help="Path to Horizon config JSON")
    args = parser.parse_args()
    raise SystemExit(asyncio.run(_amain(args.config)))


if __name__ == "__main__":
    main()
