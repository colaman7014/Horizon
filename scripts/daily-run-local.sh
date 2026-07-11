#!/usr/bin/env bash
# Horizon daily run (local Ollama + Docker) + deploy to GitHub Pages.
# Scheduled via launchd: com.colalin.horizon-daily (see scripts/com.colalin.horizon-daily.plist)
# Unlike upstream daily-run.sh this does NOT git pull: updates from
# upstream are reviewed and merged manually.

set -euo pipefail
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_PREFIX="[$(date '+%Y-%m-%d %H:%M:%S')]"

cd "$PROJECT_DIR"
echo "$LOG_PREFIX Starting Horizon daily run..."

# 1. Run the pipeline; data/ and docs/ are volume-mounted so outputs land on the host
docker compose run --rm horizon --hours 24

# 2. Deploy docs (including today's post) to gh-pages
echo "$LOG_PREFIX Deploying to gh-pages..."
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
    echo "$LOG_PREFIX Published to gh-pages."
else
    echo "$LOG_PREFIX Nothing to commit."
fi

echo "$LOG_PREFIX Done."
