# GitHub Trending 獨立頁面（Top 10）

## 背景與目標

2026-07-14 實測：新聞量大的日子（76 則過門檻搶 40 名額）repo 會被高分新聞
排擠（當日僅 2/5 入選）——配額是上限不是保留席。使用者決定把 repo 完全移出
每日簡報，改為獨立頁面顯示熱門度前 10 名，描述翻成繁體中文。

## 設計

### 1. 管線分流（`src/orchestrator.py`）

cross-source merge 之後、AI 分析之前，把 `source_type == OSSINSIGHT` 的
item 抽出來：新聞照舊走完整流程（分析→門檻→dedup→配額→enrichment），
repo 不評分、不搶名額，交給 TrendingPageWriter。頁面寫完才進新聞分析，
失敗不得中斷新聞流程（try/except + 警告訊息）。

### 2. TrendingPageWriter（新模組 `src/services/trending_page.py`）

`async write(items, date_str, path="docs/github-trending.md", top_n=10)`：

- 依 `metadata.trending_rank` 取前 10。
- 描述翻譯：10 則打包成**單一** LLM 呼叫（JSON in/out，新 prompt 於
  `prompts.py`）；回應解析失敗或丟例外時，退回英文原文（頁面永遠產得出來）。
- 產出 Jekyll 頁面：front matter（layout/title/permalink `/github-trending/`）
  ＋更新日期＋排名清單（連結、+N⭐、語言、繁中描述）。每日覆寫。

### 3. 設定與清理

- `data/config.json`：ossinsight `max_items: 10`、`min_stars: 0`（保證滿 10
  名）；移除 `category_groups.github`（repo 已不在簡報流程）。
- `.gitignore` 加 `docs/github-trending.md`（產出物，與 `_posts` 同規則）。
- `docs/index.md` 首頁加頁面連結。
- `analyzer._score_trending_repo` 保留：MCP 路徑仍可能分析 ossinsight item，
  該分支仍是正確行為。

## 測試

- writer：假 client 回合法 JSON → 頁面含繁中描述與前 10 排名；回垃圾/丟例外
  → 英文 fallback；不足 10 則 → 有幾則列幾則；0 則 → 不寫檔。
- 頁面內容：permalink、日期、連結格式。

## 風險

- qwen3 對批次翻譯 JSON 的解析失敗率——已有 fallback，最壞情況顯示英文。
- gh-pages 部署兩條路（daily-run 的 cp、deploy-docs workflow）都是
  keep_files/整包覆蓋，生成頁不會被互相清掉。
