# OrbStack Daily Schedule Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the local launchd daily run start OrbStack and wait for Docker readiness before running the Horizon compose pipeline.

**Architecture:** Keep the readiness preflight in `scripts/daily-run-local.sh`, directly before `docker compose run`. The preflight opens the OrbStack application, polls the Docker daemon with `docker info`, and exits nonzero on timeout. Test the shell behavior through the existing Python subprocess test and temporary command shims; leave the launchd schedule and upstream runner unchanged.

**Tech Stack:** Bash, macOS `open`, Docker CLI, Python 3.11+, pytest, launchd plist.

## Global Constraints

- Change only the local launchd runner path and its focused tests; do not alter `scripts/daily-run.sh`.
- `docker info` is the authoritative readiness check because the pipeline consumes Docker, not merely the OrbStack application process.
- Default OrbStack application name is `OrbStack`.
- Default readiness timeout is `600` seconds.
- Default readiness retry interval is `5` seconds.
- A readiness timeout must prevent both `docker compose run` and deployment from running.
- Do not execute the scheduler test commands until the currently running daily schedule has completed, per user instruction.
- Preserve unrelated user modifications in the working tree.

---

### Task 1: Add the timeout regression test

**Files:**
- Modify: `tests/test_daily_run_local.py`

**Interfaces:**
- Consumes: `scripts/daily-run-local.sh` through the existing `SCRIPT` path.
- Produces: a deterministic test proving that a permanently unavailable Docker daemon stops the run before compose.

- [ ] **Step 1: Extend the command-shim helper with a permanent-failure mode**

Update `_write_bash_env` so the test can choose whether `docker info` becomes ready. Keep the current default behavior (`docker info` succeeds on the second call) for the existing ordering test. The helper signature and Docker branch should be:

```python
def _write_bash_env(
    path: Path,
    calls: Path,
    tmp_path: Path,
    *,
    docker_ready_after: int | None = 2,
) -> None:
    ready_after = "never" if docker_ready_after is None else str(docker_ready_after)
    path.write_text(
        f"""
open() {{
    printf 'open %s\\n' "$*" >> {calls!s}
    return 0
}}

sleep() {{
    printf 'sleep %s\\n' "$*" >> {calls!s}
    return 0
}}

docker() {{
    printf 'docker %s\\n' "$*" >> {calls!s}
    if [ "$1" = "info" ]; then
        if [ "{ready_after}" = "never" ]; then
            return 1
        fi
        count_file={tmp_path!s}/docker-info-count
        count=$(cat "$count_file" 2>/dev/null || echo 0)
        count=$((count + 1))
        echo "$count" > "$count_file"
        [ "$count" -ge {ready_after} ]
        return $?
    fi
    if [ "$1" = "compose" ] && [ "$2" = "run" ]; then
        return 0
    fi
    return 1
}}

git() {{
    printf 'git %s\\n' "$*" >> {calls!s}
    if [ "$1" = "commit" ]; then
        return 1
    fi
    return 0
}}
"""
    )
```

- [ ] **Step 2: Write the failing timeout test**

Append this test after the existing successful readiness-order test:

```python
def test_daily_run_fails_when_docker_never_becomes_ready(tmp_path):
    bash_env = tmp_path / "bash_env"
    calls = tmp_path / "calls.log"
    _write_bash_env(bash_env, calls, tmp_path, docker_ready_after=None)

    env = os.environ.copy()
    env.update(
        {
            "BASH_ENV": str(bash_env),
            "DOCKER_READY_TIMEOUT_SECONDS": "0",
            "DOCKER_READY_INTERVAL_SECONDS": "0",
        }
    )

    result = subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Docker did not become ready within 0 seconds." in result.stdout
    call_lines = calls.read_text().splitlines()
    assert call_lines[:2] == [
        "open -gj -a OrbStack",
        "docker info",
    ]
    assert not any(line == "docker compose run --rm horizon --hours 24" for line in call_lines)
```

- [ ] **Step 3: Run the new test after the active schedule completes**

Run:

```bash
pytest tests/test_daily_run_local.py::test_daily_run_fails_when_docker_never_becomes_ready -q
```

Expected on a baseline runner without the preflight: `FAIL`, with a zero return code or a compose invocation. If the test passes immediately because the existing uncommitted `ensure_docker_ready` implementation is already present, retain the test and record that the pre-existing implementation satisfies this contract; do not weaken the assertion.

---

### Task 2: Reconcile the local runner with the approved preflight

**Files:**
- Modify: `scripts/daily-run-local.sh`

**Interfaces:**
- Consumes: `ORBSTACK_APP_NAME`, `DOCKER_READY_TIMEOUT_SECONDS`, and `DOCKER_READY_INTERVAL_SECONDS` when set by launchd or a local invocation.
- Produces: `ensure_docker_ready`, which returns only after `docker info` succeeds or exits the script with status 1 after timeout.

- [ ] **Step 1: Verify the preflight is immediately before compose**

The runner must contain this function before `cd "$PROJECT_DIR"` and must invoke it immediately before the pipeline:

```bash
ensure_docker_ready() {
    local app_name="${ORBSTACK_APP_NAME:-OrbStack}"
    local timeout="${DOCKER_READY_TIMEOUT_SECONDS:-600}"
    local interval="${DOCKER_READY_INTERVAL_SECONDS:-5}"
    local deadline=$((SECONDS + timeout))

    log "Ensuring OrbStack/Docker is ready..."
    open -gj -a "$app_name" || true

    until docker info >/dev/null 2>&1; do
        if ((SECONDS >= deadline)); then
            log "Docker did not become ready within ${timeout} seconds."
            exit 1
        fi
        sleep "$interval"
    done

    log "Docker is ready."
}
```

The execution order must remain:

```bash
ensure_docker_ready
docker compose run --rm horizon --hours 24
```

If this exact behavior is already present in the user’s uncommitted runner changes, preserve it rather than rewriting unrelated lines. If any part is absent, add only the missing function or call.

- [ ] **Step 2: Run the success-order regression test after the active schedule completes**

Run:

```bash
pytest tests/test_daily_run_local.py::test_daily_run_starts_orbstack_and_waits_for_docker_before_pipeline -q
```

Expected: `1 passed`. The recorded calls must remain:

```text
open -gj -a OrbStack
docker info
sleep 0
docker info
docker compose run --rm horizon --hours 24
```

- [ ] **Step 3: Run the timeout regression test again**

Run:

```bash
pytest tests/test_daily_run_local.py::test_daily_run_fails_when_docker_never_becomes_ready -q
```

Expected: `1 passed`, with no compose invocation in the call log.

---

### Task 3: Verify the complete scheduler contract

**Files:**
- Test: `tests/test_daily_run_local.py`
- Test: `tests/test_local_scheduler_config.py`
- Verify: `scripts/daily-run-local.sh`
- Verify: `scripts/com.colalin.horizon-daily.plist`

**Interfaces:**
- Consumes: the local runner and launchd plist.
- Produces: evidence that the daily schedule remains at 01:00 and the runner gates the compose pipeline on Docker readiness.

- [ ] **Step 1: Check shell syntax without launching the real scheduler**

Run:

```bash
bash -n scripts/daily-run-local.sh
```

Expected: exit status 0 and no output.

- [ ] **Step 2: Run the focused scheduler test module**

Run:

```bash
pytest tests/test_daily_run_local.py tests/test_local_scheduler_config.py -q
```

Expected: all tests pass, including both readiness scenarios and the existing 01:00 launchd assertion.

- [ ] **Step 3: Inspect the final call-order assertions**

Run:

```bash
pytest tests/test_daily_run_local.py -q
```

Expected: all local-runner tests pass; no real `open`, Docker, GitHub, or deployment service is contacted because the test supplies command shims through `BASH_ENV`.

- [ ] **Step 4: Commit only the implementation artifacts**

After the checks pass, review the changed paths and commit the runner/test changes without staging unrelated user files:

```bash
git add scripts/daily-run-local.sh tests/test_daily_run_local.py
git commit -m "fix(scripts): wait for OrbStack before daily run"
```

The launchd plist remains unchanged by this feature unless a test demonstrates that its existing schedule or runner path is incorrect.
