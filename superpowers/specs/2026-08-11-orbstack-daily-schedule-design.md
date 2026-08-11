# OrbStack Readiness Check for Daily Schedule

## Problem

The local daily schedule runs through launchd and invokes `scripts/daily-run-local.sh`. The pipeline requires Docker, but OrbStack may not be running when launchd starts the job. Starting the compose pipeline before Docker is ready causes the daily run to fail or produce no result.

## Goal

Before the daily pipeline starts, automatically open OrbStack when necessary and wait until Docker is ready. The pipeline must not run until the readiness check succeeds.

## Scope

- Change the local launchd runner path only: `scripts/daily-run-local.sh`.
- Keep the existing launchd schedule and downstream deployment flow unchanged.
- Add regression coverage for command ordering, readiness waiting, and timeout failure.
- Do not change the upstream `scripts/daily-run.sh` runner, which does not use the local OrbStack/Docker setup.

## Design

### Readiness preflight

Add an `ensure_docker_ready` shell function and invoke it immediately before `docker compose run`.

The function will:

1. Resolve the OrbStack application name from `ORBSTACK_APP_NAME`, defaulting to `OrbStack`.
2. Resolve the maximum wait from `DOCKER_READY_TIMEOUT_SECONDS`, defaulting to `600` seconds.
3. Resolve the retry interval from `DOCKER_READY_INTERVAL_SECONDS`, defaulting to `5` seconds.
4. Run `open -gj -a "$app_name"` to start or bring up OrbStack without opening a foreground window. An `open` failure is not treated as readiness; the Docker check remains authoritative.
5. Poll `docker info` until it succeeds.
6. Sleep between failed checks while the timeout has not elapsed.
7. Log a clear timeout message and exit nonzero if Docker never becomes ready.
8. Log readiness success before returning to the pipeline.

The compose command and deployment steps remain after the preflight, so a timeout cannot start a partial pipeline.

### Configuration

The following environment variables are optional and intended for launchd or local troubleshooting:

| Variable | Default | Purpose |
| --- | --- | --- |
| `ORBSTACK_APP_NAME` | `OrbStack` | Application name passed to `open` |
| `DOCKER_READY_TIMEOUT_SECONDS` | `600` | Maximum readiness wait |
| `DOCKER_READY_INTERVAL_SECONDS` | `5` | Delay between readiness checks |

The script already defines a predictable `PATH` for launchd and will continue to use it.

## Error handling

- An already-running OrbStack instance is safe: `open` is idempotent and `docker info` succeeds without waiting.
- A still-starting OrbStack instance is safe: failed `docker info` checks cause retries.
- A missing application, unavailable Docker daemon, or other permanent startup problem causes a timeout and nonzero exit. The compose pipeline and deployment do not run.
- Existing `set -euo pipefail` behavior remains in force for downstream failures.

## Testing

Use the existing subprocess-based shell test pattern with temporary command shims:

- Assert `open -gj -a OrbStack` is called before the first Docker readiness check.
- Simulate an initial failed `docker info`, assert the configured sleep occurs, then simulate success.
- Assert `docker compose run --rm horizon --hours 24` occurs only after Docker readiness succeeds.
- Add a timeout scenario that keeps `docker info` failing and asserts the script exits nonzero without invoking compose.

Tests must exercise observable command order and failure behavior rather than inspect shell source text.

## Alternatives considered

### launchd `KeepAlive`

Rejected. Keeping a process or application alive does not prove that the Docker daemon is ready when the schedule fires.

### OrbStack-specific CLI status

Rejected. It introduces unnecessary coupling to OrbStack CLI commands and versions. `docker info` checks the service that the pipeline actually consumes.
