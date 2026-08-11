#!/usr/bin/env bash
# Horizon daily run (local Ollama + Docker) + deploy to GitHub Pages.
# Scheduled via launchd: com.colalin.horizon-daily (see scripts/com.colalin.horizon-daily.plist)
# Unlike upstream daily-run.sh this does NOT git pull: updates from
# upstream are reviewed and merged manually.

set -euo pipefail
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

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

cd "$PROJECT_DIR"
log "Starting Horizon daily run..."

# 1. Ensure Docker is awake before running the pipeline; data/ and docs/ are volume-mounted so outputs land on the host
ensure_docker_ready
docker compose run --rm horizon --hours 24

# 2. Deploy docs (including today's post) to gh-pages
log "Deploying to gh-pages..."
WT=$(mktemp -d)
cleanup() {
    cd "$PROJECT_DIR"
    git worktree remove --force "$WT" 2>/dev/null || true
    rm -rf "$WT"
}
trap cleanup EXIT

git fetch origin gh-pages:gh-pages 2>/dev/null || true
git worktree add "$WT" gh-pages
cp -R docs/* "$WT/"
cd "$WT"
git add -A
if git commit -m "Daily Summary: $(date '+%Y-%m-%d')"; then
    git push origin gh-pages
    log "Published to gh-pages."
else
    log "Nothing to commit."
fi

log "Done."
