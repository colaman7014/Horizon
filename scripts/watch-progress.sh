#!/usr/bin/env bash
# 觀察 Horizon 手動/排程執行進度。
# 分析階段每則內容 = 一次 Ollama chat 請求，daily log 在此階段是靜默的，
# 所以用 Ollama server log 計數當作即時進度。
# 用法：bash scripts/watch-progress.sh [執行的 stdout log 路徑]
set -euo pipefail

RUN_LOG="${1:-$HOME/Library/Logs/horizon-daily.log}"
OLLAMA_LOG="/opt/homebrew/var/log/ollama.log"

echo "現在時間：$(date '+%Y-%m-%d %H:%M:%S')"

# 1. 進程是否還活著
if pgrep -f 'compose run --rm horizon' >/dev/null 2>&1; then
    echo "狀態：● 執行中"
else
    echo "狀態：○ 沒有偵測到執行中的容器（可能已結束或尚未開始）"
fi

# 2. 目前階段 = daily log 最後一行非空的 emoji 進度訊息
if [ -f "$RUN_LOG" ]; then
    phase=$(grep -aE '^(📅|🔍|📥|🔗|📈|🤖|⭐️|🧹|⚖️|📚|💾|📄|📧|✅|Deploying|Published|\[)' "$RUN_LOG" 2>/dev/null | tail -1)
    echo "目前階段：${phase:-（尚無輸出）}"
    total=$(grep -aoE '→ [0-9]+ unique items' "$RUN_LOG" 2>/dev/null | tail -1 | grep -oE '[0-9]+' || true)
    [ -z "${total:-}" ] && total=$(grep -aoE 'Fetched [0-9]+ items' "$RUN_LOG" 2>/dev/null | tail -1 | grep -oE '[0-9]+' || true)
else
    echo "找不到執行 log：$RUN_LOG"
    total=""
fi

# 3. Ollama 目前是否在推論
active=$(curl -s --max-time 5 http://localhost:11434/api/ps 2>/dev/null | grep -oE '"name":"[^"]+"' | head -1 || true)
[ -n "$active" ] && echo "Ollama：忙碌中（${active#*:}）" || echo "Ollama：閒置"

# 4. 今天完成的 chat 請求數（分析+enrich 都算），近一小時內的當作本輪
today=$(date '+%Y/%m/%d')
done_cnt=$(grep -aE "$today.*chat/completions\"" "$OLLAMA_LOG" 2>/dev/null | tail -400 \
    | awk -v now="$(date +%s)" '
        { split($4,a,":"); # 只看最近 4 小時內完成的
          # 粗略：全部列入，讓使用者對照 total
          c++ }
        END{ print c+0 }')
last_ts=$(grep -aE "chat/completions\"" "$OLLAMA_LOG" 2>/dev/null | tail -1 | awk '{print $4}')
echo "Ollama 今日累計完成 chat 請求：${done_cnt} 筆（最新一筆 ${last_ts:-—}）"
[ -n "${total:-}" ] && echo "本輪待處理內容數：約 ${total} 則（分析階段每則約 40-60 秒）"
