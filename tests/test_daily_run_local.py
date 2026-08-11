import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "daily-run-local.sh"


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


def test_daily_run_starts_orbstack_and_waits_for_docker_before_pipeline(tmp_path):
    bash_env = tmp_path / "bash_env"
    calls = tmp_path / "calls.log"
    _write_bash_env(bash_env, calls, tmp_path)

    env = os.environ.copy()
    env.update(
        {
            "BASH_ENV": str(bash_env),
            "DOCKER_READY_TIMEOUT_SECONDS": "5",
            "DOCKER_READY_INTERVAL_SECONDS": "0",
        }
    )

    subprocess.run(["bash", str(SCRIPT)], cwd=ROOT, env=env, check=True)

    call_lines = calls.read_text().splitlines()
    assert call_lines[:5] == [
        "open -gj -a OrbStack",
        "docker info",
        "sleep 0",
        "docker info",
        "docker compose run --rm horizon --hours 24",
    ]

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
