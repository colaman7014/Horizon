import asyncio
from types import SimpleNamespace

from src.ai.prompts import CONTENT_ANALYSIS_SYSTEM, CONTENT_ANALYSIS_USER
from src.tools.no_think_benchmark import build_prompt_variants, run_benchmark, summarize_result


class FakeClient:
    def __init__(self):
        self.calls = []

    async def complete(self, *, system, user, temperature=None, max_tokens=None):
        self.calls.append(
            {
                "system": system,
                "user": user,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
        )
        return '{"score": 8, "reason": "ok", "summary": "summary", "tags": ["ai"]}'


def test_build_prompt_variants_preserves_baseline_and_adds_no_think():
    variants = build_prompt_variants(CONTENT_ANALYSIS_SYSTEM, CONTENT_ANALYSIS_USER)

    assert list(variants) == ["baseline", "no_think"]
    assert variants["baseline"] == (CONTENT_ANALYSIS_SYSTEM, CONTENT_ANALYSIS_USER)
    assert variants["no_think"][0] == CONTENT_ANALYSIS_SYSTEM
    assert variants["no_think"][1].startswith("/no_think\n")
    assert variants["no_think"][1].endswith(CONTENT_ANALYSIS_USER)


def test_summarize_result_reports_parse_success_and_token_counts():
    usage_before = {"input_tokens": 10, "output_tokens": 3, "total_tokens": 13}
    usage_after = {"input_tokens": 15, "output_tokens": 6, "total_tokens": 21}

    result = summarize_result(
        variant="baseline",
        elapsed_sec=1.25,
        response=' {"score": 8, "reason": "ok", "summary": "s", "tags": []} ',
        usage_before=usage_before,
        usage_after=usage_after,
    )

    assert result == {
        "variant": "baseline",
        "elapsed_sec": 1.25,
        "parse_success": True,
        "score": 8,
        "input_tokens": 5,
        "output_tokens": 3,
        "total_tokens": 8,
        "response_chars": 58,
    }

def test_run_benchmark_calls_each_variant_without_changing_prompts():
    client = FakeClient()
    usage = iter(
        [
            {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
            {"input_tokens": 4, "output_tokens": 2, "total_tokens": 6},
            {"input_tokens": 4, "output_tokens": 2, "total_tokens": 6},
            {"input_tokens": 9, "output_tokens": 3, "total_tokens": 12},
        ]
    )

    results = asyncio.run(
        run_benchmark(
            client,
            usage_snapshot=lambda: next(usage),
            system="system",
            user="user",
        )
    )

    assert [result["variant"] for result in results] == ["baseline", "no_think"]
    assert client.calls[0]["user"] == "user"
    assert client.calls[1]["user"] == "/no_think\nuser"
    assert all(result["parse_success"] for result in results)
    assert results[0]["total_tokens"] == 6
    assert results[1]["total_tokens"] == 6
