# Horizon `gpt-oss:20b` 繁體中文新聞輸出試跑紀錄

**執行日期**：2026-08-12  
**固定案例日期**：2026-08-11  
**目的**：在不比較已確認過慢的 `qwen3.5:9b` 前提下，使用 Horizon 現有新聞分析流程，驗證 `gpt-oss:20b` 的台灣繁體中文輸出、JSON 可解析性與延遲。

## 1. 測試範圍

本次使用 6 筆來自 [2026-08-11 Horizon 繁中摘要](../docs/_posts/2026-08-11-summary-zh.md) 的新聞：

| ID | 標題 |
| --- | --- |
| `2026-08-11-item-1` | 台積電營收飆升 45% 帶動晶片設備股上漲 |
| `2026-08-11-item-2` | Meta 重返開放 AI 模型並抨擊封閉競爭者 |
| `2026-08-11-item-7` | Rust 探索 GPU SIMD 運算技術 |
| `2026-08-11-item-9` | 利用極長中斷攻擊系統管理模式 |
| `2026-08-11-item-25` | OpenClaw 人工智慧代理程式利用健身房預約 API 授權漏洞 |
| `2026-08-11-item-27` | InclusionAI 發布高效 8B MoE 模型 Ling-3.0-tiny |

固定案例完整保存於 [gpt-oss 繁中試跑案例](2026-08-12-gpt-oss-zh-news-trial-cases.json)。案例包含標題、來源、正文與社群討論；兩模型比較階段使用過的 3 筆案例也保留在其中，因此本次是擴充案例，不是更換既有案例。

## 2. 方法與輸出要求

- 執行模型：`gpt-oss:20b`。
- Provider：Ollama OpenAI-compatible API。
- Docker 容器連線：`http://host.docker.internal:11434`。
- 設定：temperature `0.3`、max tokens `4096`、analysis concurrency `1`。
- 使用 Horizon 現有 `ContentAnalyzer` 與 `CONTENT_ANALYSIS_SYSTEM`。
- 在既有 system prompt 後追加明確要求：
  - `reason`、`summary`、`tags` 全部使用台灣繁體中文。
  - 公司、產品、品牌名保留英文原文。
  - 只輸出有效 JSON，不使用 Markdown code fence。
- 每筆案例只送出一次請求；沒有使用 `qwen3.5:9b`，因前一輪同一類測試中其 3 筆總耗時為 234.987 秒，明顯慢於 `gpt-oss:20b` 的 28.975 秒。

可重現命令：

```bash
docker compose run --rm --entrypoint sh \
  -v /tmp/horizon-trial:/tmp/horizon-trial \
  -v /tmp/horizon-news-cases-2026-08-12-zh.json:/tmp/horizon-news-cases-2026-08-12-zh.json:ro \
  horizon -lc \
  'uv run python /tmp/horizon-trial/run_zh.py \
    --cases /tmp/horizon-news-cases-2026-08-12-zh.json \
    --output /tmp/horizon-trial/results-zh.json \
    --model gpt-oss:20b \
    --base-url http://host.docker.internal:11434 \
    --temperature 0.3 \
    --max-tokens 4096'
```

永久保存：

- [繁中固定案例 JSON](2026-08-12-gpt-oss-zh-news-trial-cases.json)
- [繁中試跑結果 JSON](2026-08-12-gpt-oss-zh-news-trial-results.json)

## 3. 結果

| 指標 | 結果 |
| --- | ---: |
| 案例數 | 6 |
| 總 wall-clock | **89.113 秒** |
| 單筆延遲 | 27.332 / 17.730 / 14.486 / 9.628 / 9.036 / 10.897 秒 |
| API 回報輸入 token | 8,657 |
| API 回報輸出 token | 971 |
| JSON 解析成功 | **6/6（100%）** |
| 請求重試 | 0 |
| 分數範圍 | 5–9 |
| 平均分數 | 6.5 |

### 輸出語言核對

- `reason` 與 `summary`：12/12 欄位含繁體中文，沒有欄位完全以英文輸出。
- 30 個 tags 中，14 個含中文，16 個保留英文技術名詞或產品/概念名；這符合「品牌、產品、技術名可保留英文」的輸出要求，但不代表所有標籤都必須中文化。
- 以本次檢查的常見簡體字集合比對，沒有發現殘留：`为`、`国`、`发`、`现`、`与`、`开`、`过`、`对`、`权`、`关`、`产`、`业`、`时`。
- JSON 結構、`score`、`reason`、`summary`、`tags` 欄位均存在；每筆 tags 至少 3 個。

### 逐筆結果

| ID | 分數 | 繁中輸出摘要 |
| --- | ---: | --- |
| item-1 | 9 | 台積電七月營收年增 45% 推升晶片設備股，並將資本支出預測上調至 600–640 億美元。 |
| item-2 | 8 | Meta 公布將再次發布開放權重 AI 模型，可能改變 AI 產業競爭格局。 |
| item-7 | 5 | Rust nightly 版 SIMD 函式庫應用於 GPU 運算，仍面臨效能與可攜性挑戰。 |
| item-9 | 5 | 極長 CPU 中斷可能繞過系統管理模式防護，但需要 root 權限，實際風險有限。 |
| item-25 | 7 | OpenClaw 利用健身房預約平台 API 授權漏洞，凸顯自主代理系統的安全風險。 |
| item-27 | 5 | Ling-3.0-tiny 是可在邊緣裝置高效推理的 8B MoE 模型，具低記憶體需求。 |

## 4. 判讀

### [FACT] 本次直接觀察

1. `gpt-oss:20b` 在 6 筆新聞中均產生可解析 JSON。
2. `reason` 與 `summary` 均含繁體中文；英文保留主要出現在 `Meta`、`TSMC`、`Rust`、`GPU`、`SMM`、`OpenClaw`、`AI Security` 等品牌或技術標籤。
3. 本次 6 筆連續單工分析總耗時為 89.113 秒，沒有重試或分析錯誤。
4. 目前 Horizon threshold 為 6.0；本次 item-1、item-2、item-25 通過，item-7、item-9、item-27 低於 threshold。

### [INFERENCE] 適用性判斷

- `gpt-oss:20b` 已通過本次有限的「繁體中文 + JSON」煙霧測試，可進入較大案例集或完整日報流程的下一階段驗證。
- 本次輸出仍有幾項可改善處：部分 tags 為英文、`AI晶片` 缺少空格、`AI`/`人工智慧` 混用，以及 `root` 未轉為「根」；這些屬於風格一致性問題，不是 JSON 或繁中可用性失敗。
- 不建議只依這 6 筆結果直接替換生產模型；尚未測試 enrichment、翻譯、去重、完整日報與長時間資源使用。

## 5. 限制與未測試項目

- 只有 6 筆案例、每筆 1 次請求；沒有信賴區間或重複試驗。
- 本次未再執行 `qwen3.5:9b`，遵循「太慢就不比較」的決定。
- 只測 ContentAnalyzer 的分析階段，未測 enrichment、背景搜尋、去重、翻譯、郵件、Webhook 或完整 `docker compose run --rm horizon --hours 24`。
- 本次試跑未修改 `data/config.json`、生產模型設定或 Python 原始碼；繁中要求只存在於試跑入口的 prompt variant。

## 6. 來源與原始證據

- 固定新聞來源：[docs/_posts/2026-08-11-summary-zh.md](../docs/_posts/2026-08-11-summary-zh.md)
- 生產分析流程：[src/ai/analyzer.py](../src/ai/analyzer.py)
- 生產提示：[src/ai/prompts.py](../src/ai/prompts.py)
- Ollama client：[src/ai/client.py](../src/ai/client.py)
- `gpt-oss` registry：[ollama.com/library/gpt-oss](https://ollama.com/library/gpt-oss)
- 原始暫存結果：`/tmp/horizon-trial/results-zh.json`
