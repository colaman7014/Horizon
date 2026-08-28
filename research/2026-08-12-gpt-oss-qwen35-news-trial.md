# Horizon `gpt-oss:20b` 與 `qwen3.5:9b` 新聞試跑紀錄

**執行日期**：2026-08-12（資料案例為 2026-08-11 摘要）  
**結果產生時間**：2026-08-12T00:54:48.501095Z  
**目的**：用同一批 Horizon 新聞分析輸入，核對兩個候選 Ollama 模型的 JSON 可解析性、分析延遲與評分差異。

## 1. 測試範圍與固定輸入

固定案例來自 [2026-08-11 Horizon 繁中摘要](../docs/_posts/2026-08-11-summary-zh.md)，共 3 筆：

| ID | 標題 | 原摘要位置 |
| --- | --- | --- |
| `2026-08-11-item-1` | 台積電營收飆升 45% 帶動晶片設備股上漲 | [item-1](../docs/_posts/2026-08-11-summary-zh.md#item-1) |
| `2026-08-11-item-25` | OpenClaw 人工智慧代理程式利用健身房預約 API 授權漏洞 | [item-25](../docs/_posts/2026-08-11-summary-zh.md#item-25) |
| `2026-08-11-item-27` | InclusionAI 發布高效 8B MoE 模型 Ling-3.0-tiny | [item-27](../docs/_posts/2026-08-11-summary-zh.md#item-27) |

`/tmp/horizon-news-cases-2026-08-11.json` 保存了本次固定案例的標題、來源、正文與社群討論欄位。三筆輸入在兩個模型之間完全相同；分析順序為 item-1、item-25、item-27。

本次呼叫的是 Horizon 現有 [ContentAnalyzer](../src/ai/analyzer.py) 與 [新聞分析提示](../src/ai/prompts.py)；沒有另寫一套評分規則。提示要求輸出 `score`、`reason`、`summary`、`tags` 四個 JSON 欄位，但沒有要求輸出繁體中文，因此本次不能用來判定繁中生成品質。

## 2. 執行環境與方法

- 本機 Ollama 模型清單（`ollama list`）：
  - `gpt-oss:20b`，ID `17052f91a42e`，13 GB。
  - `qwen3.5:9b`，ID `6488c96fa5fa`，6.6 GB。
  - 原有 `qwen3.6:35b-a3b-mtp-q4_K_M` 仍在本機，未納入本次比較。
- 兩模型均先以 `ollama run <model> 'Reply with exactly OK.'` 預熱：
  - `gpt-oss:20b`：`real 11.77 s`。
  - `qwen3.5:9b`：`real 16.53 s`。
- 試跑透過 Docker Compose 容器執行；Dockerfile 使用 Python 3.11。容器透過 `http://host.docker.internal:11434` 連本機 Ollama。
- 兩個模型使用相同設定：provider `ollama`、temperature `0.3`、`max_tokens=4096`、`analysis_concurrency=1`。這與現有 [Qwen benchmark 設定](../data/bench-qwen36.json) 的本地 Ollama 單工分析模式一致。
- 每個模型各分析 3 筆；每筆只送出 1 次請求，沒有重試。兩模型在同一個試跑命令中依序執行。

成功試跑命令：

```bash
docker compose run --rm --entrypoint sh \
  -v /tmp/horizon-trial:/tmp/horizon-trial \
  -v /tmp/horizon-news-cases-2026-08-11.json:/tmp/horizon-news-cases-2026-08-11.json:ro \
  horizon -lc \
  'uv run python /tmp/horizon-trial/run.py \
    --cases /tmp/horizon-news-cases-2026-08-11.json \
    --output /tmp/horizon-trial/results.json \
    --models gpt-oss:20b qwen3.5:9b \
    --base-url http://host.docker.internal:11434 \
    --temperature 0.3 \
    --max-tokens 4096'
```

`/tmp/horizon-trial/results.json` 保存了本次 API 原始回應、每筆延遲、API 回報 token usage 與解析結果；永久保存的解析結果與指標見 [試跑 JSON 摘要](2026-08-12-gpt-oss-qwen35-news-trial-results.json)，下表由同一份結果整理。

## 3. 整體結果

| 模型 | 3 筆總分析時間 | 單筆時間（item-1 / item-25 / item-27） | API 回報輸入 token | API 回報輸出 token | JSON 解析 | 平均分數 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `gpt-oss:20b` | 28.975 s | 8.492 / 8.010 / 12.471 s | 3,814 | 412 | 3/3（100%） | 7.00 |
| `qwen3.5:9b` | 234.987 s | 66.368 / 100.935 / 67.681 s | 9,249 | 416 | 3/3（100%） | 7.33 |

可觀察結果：

- 兩模型均在 3/3 筆回傳可解析 JSON，且 `attempts_by_item` 每筆均為 1；本次沒有觸發分析器的三次重試或 fallback。
- 在此固定 fixture 中，`qwen3.5:9b` 總分析時間約為 `gpt-oss:20b` 的 **8.11 倍**（234.987 / 28.975）。這是本次實測差異，不是模型一般效能保證。
- 兩模型 API 回報的輸出 token 幾乎相同（412 vs 416）；輸入 token 差異很大，因為兩個模型 tokenizer 不同，不能直接解讀為內容品質差異。
- 目前 Horizon 的 filtering threshold 是 6.0；三筆案例在兩模型結果中都達到或超過 6.0，因此本 fixture 的通過筆數都是 3/3。

## 4. 逐筆評分與輸出

| 案例 | `gpt-oss:20b` | `qwen3.5:9b` | 絕對分數差 |
| --- | ---: | ---: | ---: |
| 台積電營收 / 晶片設備股 | 8 | 8 | 0 |
| OpenClaw API 授權漏洞 | 6 | 8 | 2 |
| Ling-3.0-tiny | 7 | 6 | 1 |

### item-1：台積電營收

- `gpt-oss:20b`：8 分；重點放在營收年增、資本支出展望、晶片設備股與供應鏈影響。
- `qwen3.5:9b`：8 分；同樣視為重大財報與資本支出訊號。
- 兩者結論一致。

### item-25：OpenClaw API 授權漏洞

- `gpt-oss:20b`：6 分；認為是具體且有技術價值的 AI agent 安全案例，但不是市場重大事件。
- `qwen3.5:9b`：8 分；更重視自主代理與 API 授權設計對工程及企業風險的影響。
- 差異為本次最大（2 分），顯示同一條安全新聞在「工程價值」與「市場/讀者即時重要性」之間仍需人工校準。

### item-27：Ling-3.0-tiny

- `gpt-oss:20b`：7 分；強調 MoE、FP8、邊緣推論效率及對硬體的潛在影響。
- `qwen3.5:9b`：6 分；認為是有實用性的增量模型效率改進，尚不足以視為產業級突破。
- 差異為 1 分；兩者都正確保留了模型效率與 edge deployment 主題。

## 5. 判讀與限制

### [FACT] 本次可直接支持的結論

1. 在相同 3 筆輸入、同一 Horizon `ContentAnalyzer`、同一 Ollama OpenAI-compatible 路徑下，兩模型本次均完成 3/3 JSON 分析。
2. 本次量測中，`gpt-oss:20b` 的分析 wall-clock 明顯低於 `qwen3.5:9b`：28.975 秒對 234.987 秒。
3. 兩模型的評分不是完全一致：3 筆中 1 筆同分，另外 2 筆相差 1–2 分。

### [INFERENCE] 適用性判斷

- 若 Horizon 優先考慮本地日報的 wall-clock 與目前單工 Ollama 架構，`gpt-oss:20b` 是較合理的第一個替代試跑候選；本次實測速度優勢足以抵消其模型名稱較大的直覺疑慮。
- `qwen3.5:9b` 本次沒有展現低參數模型應有的速度優勢，暫不適合作為 Horizon 預設模型；可保留作為品質/評分風格 fallback 或後續調整 thinking 設定後再測。
- `qwen3.5:9b` 對 OpenClaw 安全案例給出較高分，而 `gpt-oss:20b` 對 Ling 模型發布給出較高分；不能只用平均分數決定模型，應再加入人工標註或歷史 fixture。

### 限制

- 只有 3 筆案例、每個模型只有 1 次分析；沒有信賴區間，也不能代表長時間日報平均值。
- 沒有比較繁體中文輸出，因本次分析 prompt 沒有要求 `reason` 與 `summary` 使用中文。
- 沒有測試 enrichment、背景搜尋、去重、翻譯、郵件或完整 `docker compose run --rm horizon --hours 24` 日報流程。
- 預熱時間不計入上表模型分析時間；上表只計算 3 筆 `ContentAnalyzer.analyze_batch` 的請求階段。
- 本次沒有修改 `data/config.json`、生產模型設定或 Python 原始碼。

## 6. 來源與原始證據

- 固定新聞案例：[docs/_posts/2026-08-11-summary-zh.md](../docs/_posts/2026-08-11-summary-zh.md)
- 生產分析流程：[src/ai/analyzer.py](../src/ai/analyzer.py)
- Ollama OpenAI-compatible client：[src/ai/client.py](../src/ai/client.py)
- 生產模型設定範例：[data/bench-qwen36.json](../data/bench-qwen36.json)
- Ollama `gpt-oss` registry：[ollama.com/library/gpt-oss](https://ollama.com/library/gpt-oss)
- Ollama `qwen3.5` registry：[ollama.com/library/qwen3.5](https://ollama.com/library/qwen3.5)
- 永久保存的 JSON 解析結果：[2026-08-12-gpt-oss-qwen35-news-trial-results.json](2026-08-12-gpt-oss-qwen35-news-trial-results.json)
- 本次原始 JSON 結果（暫存）：`/tmp/horizon-trial/results.json`
