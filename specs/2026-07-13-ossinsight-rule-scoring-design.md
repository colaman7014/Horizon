# OSS Insight repo：熱門度規則評分＋每日配額

## 目標

GitHub trending repo（OSS Insight 來源）不使用金融導向的 LLM 評分標準，
改用「純熱門度」的規則直接算分；每日簡報固定最多 5 則 repo，
與金融/科技新聞互不排擠。金融新聞評分標準完全不動。

## 設計

### 1. Scraper 標注排名與類別（`src/scrapers/ossinsight.py`）

`fetch()` 依 stars_gained 排序、截斷 max_items 之後，對每個 item 寫入：

- `metadata["trending_rank"]`：1-based 排名（排序鍵＝當期星數增量，降冪）
- `metadata["category"] = "github"`：供 balanced digest 配額分組

### 2. Analyzer 規則評分分支（`src/ai/analyzer.py`）

`_analyze_item()` 開頭：`source_type == SourceType.OSSINSIGHT` 時走
`_score_trending_repo(item)` 並直接 return，**不呼叫 LLM**：

- `ai_score = max(3.0, 8.0 - 0.5 * (rank - 1))`
  - 第 1 名 8.0、第 2 名 7.5 … 第 5 名 6.0（剛好過 6.0 門檻）、
    第 6 名 5.5 起低於門檻自然出局——門檻與配額雙重保證每日最多 5 則
  - `trending_rank` 缺失時 fallback 5.0（低於門檻，安全側）
- `ai_summary`：repo description（缺 description 時用 title）
- `ai_reason`：`GitHub trending #N: +X stars (past_24_hours)`（英文，
  與其他來源的 reason 一致；繁中化由後段 enrichment 處理）
- `ai_tags`：`[primary_language, "github", "trending"]`

### 3. 配額（`data/config.json`，gitignored、直接修改）

```json
"category_groups": {
  "github": { "name": "GitHub Trending", "limit": 5, "categories": ["github"] }
}
```

新聞類 item 沒有 github category，留在 `other`（無上限），不受影響。

### 4. 不變動

enrichment（繁中翻譯/背景）、summarizer、topic dedup 照現有流程處理
repo item；`github: []` 來源（指定 repo events/releases）不在本次範圍。

## 測試

- scraper：假 API rows → 驗證 `trending_rank` 排序正確、`category="github"`。
- analyzer：OSSINSIGHT item 不得呼叫 AI client（fake client 若被呼叫即 fail）；
  rank 1→8.0、5→6.0、6→5.5、缺 rank→5.0；summary/tags 內容正確。

## 風險與取捨

- 與其他來源處理路徑不一致（多一個規則分支）——換取每天省 12-15 次
  Ollama 呼叫與穩定可預測的入選結果，已在方案討論中確認接受。
- OSS Insight API 掛掉時當日簡報無 repo，維持現狀行為。
