# Horizon 完整日報：`qwen3.6` 與 `gpt-oss:20b` 比較

**執行日期**：2026-08-12  
**目的**：以完整 Horizon 日報流程比較現有 `qwen3.6:35b-a3b-mtp-q4_K_M` 與候選 `gpt-oss:20b` 的整體執行時間與最終繁中內容。  
**重要限制**：兩次執行都是即時抓取來源，不是同一份固定輸入；來源內容在不同時間會變動。因此時間是實際部署觀測，內容是人工比較材料，不應把兩份日報當成嚴格的 same-input A/B 評測。

## 1. 人工比較檔案

以下兩份是完整流程實際產出的最終 Markdown，已複製到 `research/`，不會覆蓋目前 `docs/_posts/` 或 `data/summaries/`：

- [現有模型：qwen3.6 完整摘要](2026-08-12-full-run-qwen36-summary-zh.md)
- [候選模型：gpt-oss:20b 完整摘要](2026-08-12-full-run-gpt-oss-summary-zh.md)
- [qwen3.6 完整執行 log](2026-08-12-full-run-qwen36.log)
- [gpt-oss:20b 完整執行 log](2026-08-12-full-run-gpt-oss.log)

輸出檔案 SHA-256：

| 檔案 | SHA-256 |
| --- | --- |
| qwen3.6 摘要 | `886add1c2100e09ef88686c6157e57170fdf31fdd5416d053f6d2248dad4a367` |
| gpt-oss 摘要 | `899fdcba7f80aa25bb3a7716fd3b157413bb8f23b9f73bc983e9262fa9b087f8` |

## 2. 測試設定

兩次測試均使用 Docker Compose 的完整 `horizon --hours 24` 流程，隔離掛載各自的 `data/`、`docs/` 輸出目錄。設定沿用當時 repo 的 `data/config.json`，只有模型名稱不同：

- provider：`ollama`
- qwen3.6：`qwen3.6:35b-a3b-mtp-q4_K_M`
- gpt-oss：`gpt-oss:20b`
- base URL：`http://host.docker.internal:11434`
- temperature：`0.3`
- max tokens：`4096`
- analysis concurrency：`1`
- enrichment concurrency：`1`
- language：`zh`
- AI score threshold：`6.0`
- digest max items：`40`
- enrichment：兩次均實際處理 40/40 selected items

候選模型命令：

```bash
/usr/bin/time -p docker compose run --rm \
  -v /tmp/horizon-full-test/gptoss/data:/app/data \
  -v /tmp/horizon-full-test/gptoss/docs:/app/docs \
  horizon --hours 24
```

現有模型的基準取自同日 01:00 的既有 daily-run-local Docker 執行，完整原始 log 已保存於上述 qwen3.6 log 檔。這避免再次等待約四小時，但也代表兩次抓取時間不同。

## 3. 整體執行時間

| 指標 | qwen3.6 現有模型 | gpt-oss:20b | gpt-oss 相對結果 |
| --- | ---: | ---: | ---: |
| 完整 daily job wall-clock | **14,529 s**（4:02:09） | **3,469.52 s**（57:49.52） | 約 **4.19 倍快** |
| Fetch | 14.3 s | 14.0 s | 幾乎相同 |
| AI scoring | 6,221.1 s（1:43:41.1） | 1,159.1 s（19:19.1） | 約 5.37 倍快 |
| Enrichment | 7,864.3 s（2:11:04.3） | 2,143.7 s（35:43.7） | 約 3.67 倍快 |
| Stage timing 合計 | 14,099.7 s | 3,316.8 s | — |
| 未分段流程/啟動/整理等 | 約 429.3 s | 約 152.72 s | — |

qwen3.6 的 14,529 秒是 daily log 從 `01:00:05 Starting Horizon daily run` 到 `05:02:14 Done` 的完整時間，包含 Docker readiness 與最後部署步驟；gpt-oss 的 3,469.52 秒是 `/usr/bin/time` 直接量測的 Docker Compose pipeline，沒有執行 gh-pages deploy。部署差異只有數秒，不足以解釋數小時差距，但時間定義仍需保留。

**時間結論（FACT）**：在這兩次實際完整流程中，gpt-oss 完成速度明顯較快，總差距約 **11,059.48 秒（3 小時 4 分 19.48 秒）**。主要差異來自 AI scoring 與 enrichment，而非抓取或 Markdown 寫檔。

## 4. 工作量與 token

| 指標 | qwen3.6 | gpt-oss:20b |
| --- | ---: | ---: |
| Fetched items | 263 | 272 |
| Cross-source merge | 未移除跨源重複 | 移除 1 筆，271 unique |
| Pre-AI scoring candidates | 106 | 110 |
| AI analyzed items | 106 | 110 |
| Score ≥ 6 | 44 | 61 |
| Topic dedup 後 | 未顯示移除 | 58（移除 3 筆） |
| Balanced selected | 40 | 40 |
| Enriched | 40/40 | 40/40 |
| Token total | 632,903 | 326,720 |
| Input / output tokens | 579,808 / 53,095 | 287,892 / 38,828 |

gpt-oss 處理了較多 scoring candidates（110 對 106），仍用了較少 token；因此速度差異不能歸因於它只處理較少內容。

## 5. 最終內容概覽

兩份摘要都產生 40 個 item sections，沒有流程錯誤。由於抓取時點不同，兩份只有 **5 個共同 URL**，其餘 35 個 URL 各自不同；以下統計只能作為人工檢查導航，不是內容品質分數：

| 指標 | qwen3.6 | gpt-oss:20b |
| --- | ---: | ---: |
| Markdown bytes | 83,164 | 62,725 |
| Markdown lines | 832 | 862 |
| Score 8 items | 11 | 15 |
| Score 7 items | 27 | 25 |
| Score 6 items | 2 | 0 |
| 繁中 CJK 字元數（粗略） | 17,346 | 10,645 |

共同 URL 的結果：

| URL | qwen3.6 | gpt-oss:20b |
| --- | --- | --- |
| `stolen-thoughts.com` | 8 分；「從專屬 LLM API 擷取與重播推理軌跡」 | 8 分；「LLM API 漏洞：竊取內部推理痕跡」 |
| CoreWeave Yahoo Video | 8 分；AI 基礎設施需求與市場情緒 | 8 分；AI GPU 需求指標 |
| Qwen Reddit image | 7 分；2.4T MoE 即將推出 | 7 分；Qwen 3.8-27B 即將發布 |
| `news.cnyes.com/news/id/6571810` | 7 分；Jingmei Technology EPS | 7 分；景美科技 EPS |
| `news.cnyes.com/news/id/6572003` | 7 分；上櫃公司營收與 AI 半導體 | 7 分；OTC 營收與 AI 半導體 |

人工比對時建議先看：

1. 相同 URL 的標題是否保留原意。
2. 正文是否只使用來源可支持的事實，有無把背景搜尋內容寫成新聞原文事實。
3. 分數 8/7 的排序是否符合 Horizon 對工程師兼美股/台股投資人的 rubric。
4. 繁體中文用詞：台灣用語、品牌英文保留、`AI`/「人工智慧」一致性。
5. 背景段落與參考連結是否有實質幫助，而不只是增加篇幅。

## 6. 初步判讀

### [FACT] 可直接觀察

- gpt-oss:20b 在完整流程中成功完成抓取、評分、topic dedup、balanced digest、40 筆 enrichment 與繁中 Markdown 產出。
- gpt-oss:20b 的完整 pipeline wall-clock 為 3,469.52 秒；既有 qwen3.6 daily job wall-clock 為 14,529 秒。
- gpt-oss 的最終檔案較小，但 item 數相同；這表示它的每項背景/摘要文字較短，需人工判斷是否是精簡或資訊遺失。
- 兩次輸出內容差異很大，主要原因是來源抓取時間不同，不可單純歸因於模型。

### [INFERENCE] 留給人工決策的重點

- 若人工確認 gpt-oss 的共同案例與主要投資/技術新聞沒有明顯幻覺、遺漏或品質下降，**執行時間優勢足以支持進一步考慮替換現有模型**。
- 若 gpt-oss 的較短內容被判定為背景不足、來源錯配或關鍵脈絡遺失，則不應只因 4.19 倍速度提升而直接替換。
- 目前最關鍵的品質風險不是 JSON 或繁中生成失敗，而是「選了哪些新聞」與「enrichment 是否忠實且足夠完整」。

## 7. 未修改與可重現證據

- 沒有覆蓋目前 repo 的 `data/config.json`。
- 沒有覆蓋目前 repo 的 `docs/_posts/2026-08-12-summary-zh.md`。
- 兩次輸出與 log 均保存在本報告列出的 `research/` 檔案。
- Docker-based run 使用的隔離原始目錄仍保留於 `/tmp/horizon-full-test/qwen36/` 與 `/tmp/horizon-full-test/gptoss/`。
