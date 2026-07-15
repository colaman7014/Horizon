# Local LLM Performance Requirements

## Context

Horizon's current local production run executes inside Docker, not the host Python environment.

The configured AI backend is a local Ollama endpoint from inside Docker:

```json
{
  "provider": "ollama",
  "model": "qwen3:30b-a3b",
  "base_url": "http://host.docker.internal:11434",
  "analysis_concurrency": 1,
  "enrichment_concurrency": 1
}
```

The local LLM backend has already been tested and only provides useful throughput as a single-threaded / single-request-at-a-time runner. Horizon-level concurrency is therefore not the primary optimization path for this deployment.

## Problem Statement

Daily runs spend most wall-clock time waiting on local Ollama chat completions. The repository still has performance-improvement space, but the expected wins come from reducing LLM work rather than parallelizing LLM calls.

The system should treat each local Ollama chat completion as the expensive unit of work.

## Evidence Snapshot

Observed from local logs:

- `~/Library/Logs/horizon-daily.log` records Docker-based daily runs through `scripts/daily-run-local.sh`.
- `/opt/homebrew/var/log/ollama.log` records `/v1/chat/completions` timings.
- A completed run on 2026-07-13 made 180 parsed Ollama chat requests with median request duration around 35 seconds.
- A completed run on 2026-07-14 made 292 parsed Ollama chat requests before Horizon finished, with median request duration around 38 seconds.
- `scripts/watch-progress.sh` exists because the analysis phase is otherwise silent in the daily log; it counts Ollama chat completions as progress.

## Constraints

1. Verification commands for this repo must run in Docker or the same containerized environment used by the daily job.
2. Host-level Python commands are not authoritative for this deployment.
3. Local Ollama throughput must be modeled as single-request-at-a-time unless a future benchmark proves otherwise.
4. Increasing `analysis_concurrency` or `enrichment_concurrency` is not an accepted optimization for the current local deployment.
5. Optimizations must preserve the daily digest's usefulness: fewer LLM calls cannot mean blindly dropping all finance or tech sources.

## Current LLM Work Units

The main LLM work units are:

1. **Scoring** — one AI analysis call per content item that reaches `ContentAnalyzer.analyze_batch()`.
2. **Topic deduplication** — AI batch calls over high-scoring items.
3. **Enrichment concept extraction** — one AI call per selected item.
4. **Enrichment writing** — one AI call per selected item.
5. **Fallback translation** — one extra AI call when enrichment parsing fails.
6. **GitHub trending translation** — batched into one AI call for top repositories.

The final Markdown summary generation is not an LLM call.

## Optimization Direction

### Primary: reduce items before AI scoring

The highest leverage path is to prevent low-value items from reaching per-item AI scoring.

Candidate controls:

- Per-source or per-feed pre-AI caps.
- Enforce OpenBB watchlist-level caps after provider fan-out.
- Tighter Google News max results.
- RSS source-specific caps for noisy feeds.
- Rule-based bypasses for deterministic sources, following the existing OSS Insight rule-scoring pattern.

Accepted policy: use balanced pre-AI caps. Each important source class should retain baseline coverage, while noisy sources receive explicit caps before scoring. The optimization must reduce LLM calls without starving an entire domain such as finance or technology.

Initial cap targets should focus on:

- OpenBB watchlist results after provider fan-out.
- High-volume RSS feeds such as Anue.
- Google News result count.

The cap policy should be source-aware rather than a single global top-N list.

### Secondary: reduce enrichment calls

The next highest leverage path is to reduce the two-call enrichment pattern.

Candidate controls:

- Enrich only top N selected items.
- Disable enrichment for low-context routine finance items.
- Replace AI concept extraction with deterministic keyword extraction.
- Make enrichment optional per deployment profile.

Accepted policy: use top-N enrichment. All selected items keep the scoring summary so they can still appear in the digest, but only the highest-ranked selected items receive the full concept-search-plus-background enrichment pass.

Default N: 10. With the current default selected digest size of 40 items, this changes enrichment from roughly 80 local LLM calls to roughly 20 local LLM calls while still preserving full scoring summaries for every selected item.

### Tertiary: reduce model output waste

For Qwen thinking models, prompts may need explicit no-thinking instructions when the output must be compact JSON.

Candidate controls:

- Benchmark `/no_think` on scoring, topic deduplication, concept extraction, and enrichment prompts.
- Compare latency, parse success, token usage, and summary quality before adopting.

Accepted policy: benchmark first. `/no_think` must not become default behavior for scoring, enrichment, or deduplication until a Docker-backed fixture shows lower latency or token usage without unacceptable parse failures or summary-quality regression.

## Non-Goals

- Do not optimize by increasing LLM concurrency for the current local Ollama deployment.
- Do not treat host Python test failures as deployment failures when Docker is the authoritative environment.
- Do not micro-optimize Markdown generation, file writes, or deploy steps before reducing LLM work units.

## Acceptance Criteria

A performance change is accepted only if Docker-based verification shows at least one of:

1. Fewer Ollama `/v1/chat/completions` requests for the same source configuration class.
2. Lower median or total Ollama request time for a fixed fixture.
3. Lower daily run wall-clock time without reducing digest quality below the agreed source coverage policy.
4. Better progress observability during long LLM phases.

## Required Verification Shape

Use Docker-backed commands or the daily-run container path.

Minimum evidence for a performance PR:

- Run command used.
- Number of fetched items.
- Number of items sent to scoring.
- Number of selected items sent to enrichment.
- Count of Ollama chat completions.
- Wall-clock time by stage when available.
- Token usage summary when available.

