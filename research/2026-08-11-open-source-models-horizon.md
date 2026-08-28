# Horizon 適用的近期開放權重模型調查

**調查日期**：2026-08-11；**更新**：2026-08-12  
**調查範圍**：截至 2026-08-11 已有官方模型卡、官方模型庫或官方部署文件可核驗的近期開放權重模型。  
**目標**：判斷哪些模型適合 Horizon 的本地 Ollama／OpenAI-compatible 工作負載；不把「開放權重」直接稱為 OSI 定義的「開源」。

> **先講結論**：目前仍不建議直接替換生產模型。`data/config.json` 已指向 `qwen3.6:35b-a3b-mtp-q4_K_M`，本機 `ollama list` 也觀察到同一個已下載的 22 GB tag；它仍是目前最保守的生產基線。`gpt-oss:20b` 已在 2026-08-12 以隔離 Docker 完整跑完 Horizon 日報流程，實測 wall-clock 為 3,469.52 秒；既有 Qwen3.6 完整日跑為 14,529 秒，但兩次抓取時間不同，尚未構成同輸入品質 A/B。故本報告把 gpt-oss 從「待試跑」更新為「已通過整合煙霧測試、仍待固定 fixture 品質 gate」的 P1 候選；不宣稱它已可直接上線。

## 1. 名詞、證據與判斷邊界

### 1.1 開放權重不等於完整開源

本報告分開記錄三件事：

1. **權重可得性**：是否能從官方 Hugging Face／ModelScope／官方模型庫下載模型權重。
2. **權重或程式授權**：例如 Apache 2.0、MIT，或 NVIDIA 的自訂 Open Model License。OSI 認可的軟體授權不代表訓練資料、完整訓練流程或模型行為都可重現。
3. **訓練資料可得性**：除 NVIDIA Nemotron 明確釋出大量資料集合外，本次候選沒有一個能讓 Horizon 直接重建完整訓練語料；「公開資料集清單」也不等於「完整訓練資料已公開」。

因此本文使用「開放權重」作為總稱；只有在授權本身可核驗時，才說該權重採 Apache 2.0 或 MIT。商用部署仍須閱讀每個模型的 LICENSE、使用政策與第三方資料條款。

### 1.2 本報告的證據等級

- **事實（Fact）**：直接來自官方模型卡、官方 GitHub、官方部落格、官方 Ollama／推理框架文件，並附 URL。
- **[INFERENCE] 判讀**：將事實套到 Horizon 的硬體、請求形狀與營運限制；不是模型提供者的保證。
- **未核驗**：本 repo 沒有下載／執行該模型，或官方資料沒有提供足夠資訊；不以推測填空。

官方 benchmark 只代表發布方所列條件。不同模型的 prompt、reasoning 設定、量化、runtime、評測 scaffold 與 judge 不同，不能直接當成本機 tok/s 或 JSON 成功率的替代證據。

## 2. Horizon 實際工作負載與硬限制

### 2.1 產生哪些 LLM 請求

從 [Horizon AI client](../src/ai/client.py)、[ContentAnalyzer](../src/ai/analyzer.py)、[prompts](../src/ai/prompts.py) 可核對：

- 每個進入分析階段的內容通常發出一次 LLM 請求，要求 `score`、`reason`、`summary`、`tags` JSON。
- 高分項目接著做主題去重、概念搜尋／背景補充與雙語輸出；補充 schema 包含 `*_en` 與 `*_zh` 欄位，以及 `sources` URL 陣列。
- 目前 client 對大部分 OpenAI-compatible provider 固定送出 `response_format={"type":"json_object"}`；模型回應再由 `parse_json_response` 做容錯解析。換模型時，JSON mode 能否真的約束最終內容、是否把 thinking trace 混進 `content`，都必須實測。
- `src/ai/client.py` 的 `complete()` 介面沒有通用的 `enable_thinking` 或 `reasoning_effort` 參數；現有 [no-think benchmark](../src/tools/no_think_benchmark.py) 只是在 user prompt 前加 `/no_think`，而不是已證明適用所有模型的 API 控制。

### 2.2 請求量、並行與硬體

- [本地 LLM 效能要求](../specs/2026-07-15-local-llm-performance-requirements.md) 將每次本地 Ollama chat completion 視為昂貴工作單位，要求以單請求佇列估算；歷史紀錄曾觀察到單次 daily run 約 180–292 個 Ollama chat requests、median 約 35–38 秒，但那是 2026-07-13／14 的歷史 log snapshot，不是候選模型的現況 benchmark。
- [目前設定](../data/config.json) 為 Ollama、`host.docker.internal:11434`、`analysis_concurrency: 1`、`enrichment_concurrency: 1`，並將 scoring 輸出上限設為 4096、enrichment 上限設為 8192；目前 digest `max_items` 為 40、`enrichment_top_n` 為 10。
- [本地 daily runner](../scripts/daily-run-local.sh) 先啟動 OrbStack／Docker，再以 `docker compose run --rm horizon --hours 24` 執行；容器透過 `host.docker.internal` 連到宿主機推理服務。這是生產驗證邊界，不應以 host Python 測試取代。
- 工作站基準是 Apple Silicon M4 Pro、48 GB unified memory；報告中的「可執行」均指短上下文、單請求與已選定量化下的候選，不能推廣成所有 context、batch 或 OS 快取條件都安全。

### 2.3 評估準則

排序優先級為：

1. **JSON 與雙語穩定性**：能否穩定填滿 Horizon schema，繁體中文是否符合 `TAIWAN_GLOSSARY`。
2. **單請求延遲／記憶體**：本地模型不是靠提高 concurrency 取勝，而是降低每個 request 的時間與失敗重試。
3. **Ollama 或 OpenAI-compatible 可部署性**：最好能以現有 `provider: ollama`、`base_url` 和 `model` 設定切換；否則需 vLLM／SGLang 額外維運。
4. **思考模式控制**：scoring 與 translation 需要短 JSON；reasoning trace 不應無限放大單項成本。
5. **授權與語言覆蓋**：Apache 2.0／MIT 不是唯一條件，但 custom license、未列繁中支援或模型政策不明會降級。

## 3. 候選比較矩陣（更新至 2026-08-12）
| 候選 | 官方可核驗規格 | JSON／工具／思考控制 | 自架與 Horizon 適配 | 授權、資料與主要風險 | 建議級別 |
|---|---|---|---|---|---|
| **Qwen3.6-35B-A3B** | 35B total／3B active sparse MoE；官方 agent scaffold 範例使用 131,072 context；原生 multimodal。官方模型卡 metadata 標示 Apache 2.0。([Qwen 官方發布文][S1]、[HF model card][S2]) | 官方 chat template／API 有 `enable_thinking`、`preserve_thinking`，工具訊息格式已定義；JSON mode 由 Ollama／server 提供，模型卡未等同保證 Horizon schema 100% 成功。([S1][S2]、[S7][S8]) | 官方列出 Transformers、llama.cpp、MLX、SGLang、vLLM；Ollama registry 有 Qwen3.6 tags。Horizon 本機已有自訂 `qwen3.6:35b-a3b-mtp-q4_K_M`，是本表唯一已有本機下載證據的模型。([Qwen GitHub][S3]、[Ollama Qwen3.6][S9]) | Apache 2.0 權重；完整訓練資料與可重建訓練流程未在本次來源中核驗。官方 benchmark 是發布方條件，不能轉成 M4 Pro 保證值。 | **P0 保持現況**；先做 fixture regression，不要因新聞發布自動換版。 |
| **OpenAI gpt-oss-20b** | 21B total／3.6B active；官方 repo 指出 MXFP4 後可在 16 GB memory 內運行；120B 才要求單張 80 GB GPU。([gpt-oss 官方 repo][S4]) | 原生 configurable reasoning effort（low／medium／high）、function calling、Structured Outputs；必須使用 Harmony response format。Ollama 官方提供 `gpt-oss:20b` 與 OpenAI-compatible endpoint，並列出 JSON mode、tools、`reasoning_effort`。([S4]、[Ollama gpt-oss][S5]、[Ollama docs][S7][S8]) | 20B 是最合理的替代候選；官方提供 Ollama 路徑，官方 repo 也有 Apple Silicon Metal reference implementation，但明確說 reference Metal 尚非 production-ready。48 GB M4 Pro [INFERENCE] 有足夠記憶體餘裕；本機已於 2026-08-12 以 Docker／Ollama 完成一次完整日報流程，細節見 [S18]。 | Apache 2.0，另有官方 `USAGE_POLICY`，部署前需一併審閱；Harmony、thinking trace、`response_format` 與 Horizon 只讀 `message.content` 的交界是主要整合風險。訓練資料未完整開放。 | **P1 條件式替代候選**；整合 smoke test 已成功，但仍須用固定輸入驗證 JSON、繁中與 `reasoning_effort=none/low` 的實際內容。 |
| **Qwen3.5-9B** | 9.65B BF16 metadata；multimodal，官方模型卡 chat template 支援 `enable_thinking` 與工具訊息；Qwen 官方 repo 列 2026-03-02 釋出 9B。([HF model card][S10]、[Qwen GitHub][S3]) | chat template 可用 `enable_thinking=False`；工具呼叫格式明確存在。JSON mode 仍取決於 Ollama／server 與模型實測，不把 template 等同 schema validator。([S10]、[S8]) | 小於 35B 的 dense fallback，較適合低 RAM 或希望降低單請求成本的 profile；官方 Ollama library 有 `qwen3.5:9b` tag。需用與目前模型相同的 Docker fixture 比較品質。([Ollama Qwen3.5][S11]) | Apache 2.0；Qwen3.5 README 宣稱全球語言覆蓋，但 Qwen3.5-9B 個別模型卡未在本次摘錄中提供繁體中文品質保證；必須跑 Taiwan glossary fixture。完整訓練語料未完全公開。 | **P1 低記憶體 fallback**；若 JSON／繁中通過，可能是日常 scoring 的速度選項。 |
| **InclusionAI Ling-3.0-tiny** | 7.9B total／約 1.3B active；128 experts；config 原生 131,072 context，官方部署文件以 YaRN 可啟至 262,144；官方模型卡宣稱 FP8 在 M4 Pro 約 86–90 tok/s、8K 約 8.34 GiB peak memory。([Ling 核驗報告][S12]) | 原生 `<think>`／`<tool_call>`；SGLang cookbook 使用 reasoning／tool-call parser。這是 XML／parser 路徑，不等於 Horizon 現有 `json_object` 已驗證。`enable_thinking` 可在 template 控制。([S12]) | 理論上最適合追求單執行緒速度；但 vLLM 需 InclusionAI fork，SGLang 需專用 dev image，Ollama 仍是未合併 PR 的 Apple Silicon MLX 實驗支援。([S12]) | MIT；完整訓練資料未公開。主要風險是 custom `bailing_hybrid` 架構與 runtime 維護，不是權重大小。官方 speed／memory 是單方面宣稱，沒有本 repo fixture 重現。 | **P2 速度導向試跑**；只有在接受額外 runtime 維運時才值得做。 |
| **NVIDIA Nemotron 3.5 Lightning 30B-A3B** | 30B total／3B active；hybrid Mamba-2 + MoE + Attention；最高 1M context；官方 Ollama 提供 `30b` 與 Apple Silicon `30b-mlx` tag。([Ollama 官方公告][S19]、[NVIDIA HF model card][S20]) | 官方模型卡與 Ollama metadata 顯示 tools／thinking；Ollama OpenAI-compatible API 支援 `response_format`、`reasoning_effort`。本機預設 reasoning 的 `message.content` 曾為空且 `finish_reason=length`；注入 `reasoning_effort="none"` 後 JSON 可解析。Horizon 現有 client 尚未傳該欄位。([S7]、[S19]、[S20]) | 本機已下載 `nemotron-3.5-lightning:30b-mlx`（22 GB），Docker→`host.docker.internal` 完成固定三案例與真實搜尋隔離評測；但正式 client 仍需 reasoning 控制，且尚未完成 full daily run。固定評測顯示速度潛力，不代表 production 可用。 | OpenMDW-1.1／NVIDIA 本機 tag metadata 顯示 NVIDIA Open Model Agreement；官方 HF 語言標籤為 en、es、fr、de、it、ja，沒有 zh-TW 獨立保證。NVIDIA 宣稱的 throughput 依特定 NVIDIA runtime／硬體，不能轉成 M4 Pro 保證。 | **P2 受控實驗候選**；固定 fixture 已有證據，但引用完整度、禁用詞與 reasoning 控制仍需 gate。 |
| **Mistral Small 3.1 24B Instruct** | 24B dense；官方模型卡列 128K context、vision、多語（含 `zh`），並宣稱量化後可在單張 RTX 4090 或 32 GB MacBook 執行。([Mistral 官方 model card][S13]) | 官方列 native function calling 與 JSON output；官方建議低 temperature，production server 路徑以 vLLM 的 `mistral` tool-call parser 為主。([S13]) | 繁中與 Apache 2.0 是優點；本次官方來源未核對 exact 3.1 Ollama tag，模型卡主推 vLLM，需先驗證是否可沿用現有 Ollama path，否則需維護另一個 OpenAI-compatible server。24B dense 也不會像 3B-active MoE 那樣省單請求計算。 | Apache 2.0；訓練資料未完整公開。模型卡的量化／硬體敘述是部署目標，不是長 context 加上 Docker、KV cache 後的保證。 | **P2 中文品質／vLLM 備選**；不作第一個替代。 |
### 3.1 兩個容易混淆的結論

- **「3B active」不等於「只佔 3B 記憶體」**：Qwen3.6-35B-A3B 仍有約 35B total weights；active parameters 主要影響每 token 計算量，不會消除權重、KV cache、runtime 與量化的記憶體成本。
- **「官方支援 JSON」不等於 Horizon schema 已通過**：Horizon 需要數值 score、tag 陣列、雙語欄位、來源 URL 與 parse/retry 行為一起正確。任何候選都必須跑固定 fixture；沒有實測的推薦只是一個優先級，不是上線批准。

### 3.2 已完成的 `gpt-oss:20b` 完整 Docker 試跑

本節是本機實測，不是官方 benchmark。完整命令、原始 log、兩份摘要與限制記錄在[雙模型比較報告](2026-08-12-full-run-model-comparison.md)。

| 指標 | 現有 Qwen3.6 基準 | `gpt-oss:20b` |
|---|---:|---:|
| 完整流程 wall-clock | 14,529 s（4:02:09） | 3,469.52 s（57:49.52） |
| Fetch | 14.3 s | 14.0 s |
| AI scoring | 6,221.1 s | 1,159.1 s |
| Enrichment | 7,864.3 s | 2,143.7 s |
| AI scoring candidates | 106 | 110 |
| 最終選取／背景補充 | 40／40 | 40／40 |
| Token total | 632,903 | 326,720 |

**[FACT]** `gpt-oss:20b` 在本 repo 的 Docker／Ollama／OpenAI-compatible 路徑中完成 scoring、去重、balanced digest、40 筆 enrichment、繁中 Markdown 輸出；log 結尾為 `✅ Horizon completed successfully!`。相對於這次 Qwen3.6 基準，完整 wall-clock 約快 4.19 倍，且處理的 scoring candidates 較多（110 對 106）。

**比較限制**：兩次執行是不同時間的即時抓取，qwen3.6 日跑包含 daily runner 的部署步驟，gpt-oss 測試則以 `/usr/bin/time` 量測 Docker pipeline；兩份摘要只有 5 個共同 URL。因此這是整合與耗時證據，不是同輸入的內容品質優勝證明。兩份完整輸出可直接人工比對：[Qwen3.6 摘要](2026-08-12-full-run-qwen36-summary-zh.md)、[gpt-oss 摘要](2026-08-12-full-run-gpt-oss-summary-zh.md)。

**[INFERENCE]** 若固定 fixture 的 JSON schema、繁中 glossary、來源忠實度與 digest 覆蓋率不低於 Qwen3.6，這個速度差距足以讓 gpt-oss 成為實際替代方案；在該 gate 完成前，不應修改 production model。
### 3.3 固定三案例 fixture：Qwen3.6 與 Nemotron 3.5 Lightning

以下是 2026-08-12 使用相同三筆固定案例（台積電財務、OpenClaw API 授權、Ling 模型發布）的隔離評測。評測腳本、原始 JSON 與摘要保存在本機 `/tmp/horizon-full-eval/`，不屬於 repo 產物；本節只記錄可重算的摘要數據。兩模型均使用 Ollama OpenAI-compatible、`temperature=0.3`、`analysis_concurrency=1`、`enrichment_concurrency=1`、9 次請求，且 `parse_success=9/9`、`error=0`。

| 評測模式 | 模型 | 總耗時 | input/output/total tokens | schema 完整度 | 來源／錨點／禁用詞 |
|---|---|---:|---:|---|---|
| 固定搜尋（合成背景） | Qwen3.6 | 840.198 s | 33,902 / 2,965 / 36,867 | `title_zh`、`detailed_summary_zh`、`background_zh` 3/3；`community_discussion_zh` 2/3 | sources 1 筆；錨點 8/9；禁用詞 0 |
| 固定搜尋（合成背景） | Nemotron 3.5 `30b-mlx`，`reasoning_effort=none` | 83.669 s | 10,687 / 3,134 / 13,821 | `title_zh`、`detailed_summary_zh`、`background_zh` 3/3；`community_discussion_zh` 2/3 | sources 0 筆；錨點 9/9；禁用詞 2 |
| 真實 DuckDuckGo 搜尋 | Qwen3.6 | 782.002 s | 32,641 / 3,117 / 35,758 | 四個繁中欄位：3/3、3/3、3/3、2/3 | sources 2/3 項、共 5 筆；錨點 6/9；禁用詞 4 |
| 真實 DuckDuckGo 搜尋 | Nemotron 3.5 `30b-mlx`，`reasoning_effort=none` | 95.087 s | 12,318 / 2,984 / 15,302 | 四個繁中欄位：3/3、3/3、3/3、3/3 | sources 1/3 項、共 2 筆；錨點 9/9；禁用詞 2 |

**[FACT]** 在這組三案例、單執行緒與本機 Ollama 條件下，Nemotron 的固定搜尋總耗時約為 Qwen3.6 的 1/10；真實搜尋總耗時約為 1/8.2。它的 total tokens 分別少 62.5% 與 57.2%，但 output tokens 並未少（固定 3,134 對 2,965；真實 2,984 對 3,117）。兩模型 18/18 JSON 回應均可解析，沒有錯誤。

**[FACT]** 品質面不是單向勝負：Nemotron 在固定與真實搜尋均填滿 3/3 `background_zh`、真實搜尋的 `community_discussion_zh` 為 3/3，且固定案例錨點為 9/9；Qwen3.6 的真實搜尋來源數較高（5 對 2），但固定／真實搜尋分別有 2/3、2/3 community 欄位，且真實搜尋錨點為 6/9。評測工具把 `數據`、`激活` 等 2026-08-12 禁用詞列入計數；Nemotron 共 2 次、Qwen3.6 真實搜尋共 4 次。這些是機械指標，不是人工事實性評分。

**[INFERENCE]** Nemotron 的速度優勢值得保留，但不能直接升格為生產替換：本次只涵蓋三筆案例，來源搜尋非固定結果，且 `sources` 引用完整度與繁中詞彙仍未達可接受的明確優勢。更重要的是，所有 Nemotron 結果都注入了 Ollama 文件所列的 `reasoning_effort="none"`；正式 `src/ai/client.py` 尚未傳該欄位。報告中因此把 Nemotron 從「尚未有固定 fixture 證據」更新為「已有固定 fixture 與真實搜尋證據、但仍未通過 production gate」。

原始評測證據（本機暫存）：

- [Qwen3.6 固定搜尋 JSON](file:///tmp/horizon-full-eval/qwen36.json)、[摘要](file:///tmp/horizon-full-eval/qwen36-summary-zh.md)
- [Nemotron 固定搜尋 JSON](file:///tmp/horizon-full-eval/nemotron.json)、[摘要](file:///tmp/horizon-full-eval/nemotron-summary-zh.md)
- [Qwen3.6 真實搜尋 JSON](file:///tmp/horizon-full-eval/qwen36-real.json)、[摘要](file:///tmp/horizon-full-eval/qwen36-real-summary-zh.md)
- [Nemotron 真實搜尋 JSON](file:///tmp/horizon-full-eval/nemotron-real.json)、[摘要](file:///tmp/horizon-full-eval/nemotron-real-summary-zh.md)


## 4. 推薦分級與決策

### P0：保持 Qwen3.6-35B-A3B，先不換

這不是「最新新聞中最強」的宣稱，而是最保守的 repo 決策：

1. `data/config.json` 已指向一個本機已下載的 Qwen3.6 35B-A3B 量化 tag。
2. Qwen 官方提供同系列的 Ollama／Transformers／llama.cpp／MLX／vLLM／SGLang 路徑；Apache 2.0 的權重授權也符合本 repo 的 permissive 偏好。
3. 本 repo 已有 Qwen thinking／`/no_think` 探索工具與歷史執行限制；改用另一個模型不能假設 prompt 行為相同。

**不應做的事**：不要只把 `model` 改成 `gpt-oss:20b` 或 `qwen3.5:9b` 就稱為完成。即使 gpt-oss 已通過一次完整 Docker smoke test，仍要保留目前 config，建立候選 config，使用相同 fixture 比較 parse success、繁中 glossary、每階段 request 數、p50/p95 latency、output tokens 與 daily digest 差異。

### P1：優先評估 `gpt-oss:20b`（已完成一次完整試跑）

**理由**：官方提供 Ollama 指令、OpenAI-compatible client、structured outputs、function calling 與 reasoning effort；官方聲稱 MXFP4 後可在 16 GB memory 運行。這與 M4 Pro 48 GB、Horizon 的 Ollama endpoint 和 JSON request 形狀相容；本機完整試跑也證明現有 pipeline 可走通，且在本次不同輸入的比較中顯著較快。

**目前結果與阻塞條件**：一次完整 run 已確認 Harmony／Ollama／`message.content` 交界沒有阻止 Horizon 完成輸出，但它沒有回答同輸入下的品質與 reasoning 成本問題。仍必須確認 `response_format={"type":"json_object"}`、final channel／thinking trace、`reasoning_effort=none/low` 與繁體中文輸出在固定 fixture 上的行為。

### P1：Qwen3.5-9B 作為速度／記憶體 fallback

若 P0 的 35B tag 在長時間 daily run 仍是瓶頸，9B 是比更換到 24–30B dense 模型更直接的成本實驗。官方 template 有 `enable_thinking=False`，可針對短 JSON scoring 做明確比較；代價是可能降低去重、金融語境與雙語 enrichment 品質，必須用 fixture 和 digest review gate 擋住回歸。

### P2：Nemotron 3.5 Lightning 僅作受控實驗候選

本次固定三案例與真實搜尋評測顯示它有顯著速度潛力，但尚未滿足 production gate：正式 client 尚未傳 `reasoning_effort="none"`；來源引用數低於 Qwen3.6（真實搜尋共 2 對 5）；且禁用詞機械計數仍為 2 次。若要繼續，先在隔離 client 加入 reasoning 控制，再擴大固定 fixture 與人工事實性／繁中審查；不直接修改 `data/config.json`。

### P2：Ling tiny 只在「速度優先且能維護專用 runtime」時導入

官方硬體數字很吸引人，但它不是現成 Ollama 版本替換：SGLang dev image、vLLM fork、Ollama 未合併 PR 都會增加供應鏈、升級與故障排查面。若目標是把 M4 Pro daily run 壓到更短，應先用官方 FP8／SGLang 路徑做可重現試跑，而不是在生產機手動編譯後直接切換。

### P2：Mistral Small 3.1 作為繁中／vLLM 備選

它有明確的 `zh` 語言標示、native JSON/function calling 與 Apache 2.0；若未來本 repo 決定把 Ollama 換成 vLLM，這是合理的 dense baseline。現階段它沒有勝過已下載 Qwen tag 的「整合成本」優勢。

### P3：不適合本機 Horizon 的候選

- **Nemotron Nano**：即使 active 參數少，官方支援重心是 NVIDIA GPU／Linux，官方語言清單沒有中文，且 license 是 custom。
- **DeepSeek-V4-Flash**：官方 Ollama 尺寸 130.4–155.4 GB，與 48 GB unified memory 及本 repo 單請求低延遲目標不相容。

## 5. 驗證門檻（固定三案例已完成；尚未形成 production gate）

對尚未完成固定 fixture 或仍有介面阻塞的候選，應使用**獨立 config**，不要污染目前 `data/config.json`。所有測量在 Docker daily-run 容器路徑完成；模型下載與 warm-up 時間另行記錄，不混入穩態 request latency。

### 5.1 固定測試內容

1. 取一組涵蓋英文技術、繁體中文金融、混合中英產品名、長 RSS、含社群留言與可能 prompt injection 的固定 fixture。
2. 跑 scoring、topic dedup、concept extraction、enrichment、translation fallback 的實際 prompt；不要只測一個 hello world。
3. 每個模型至少記錄：JSON parse success、schema 欄位完整率、`score` 型別、tags 數量、`sources` URL 是否來自輸入、`*_zh` 是否為繁體中文、reasoning／output token 數、p50/p95 request latency、重試數與錯誤類型。
4. 以相同 source snapshot 比較 digest：不能因速度改善而讓 finance 或 tech 類別被無聲丟棄。

### 5.2 模型特定測試

- **Qwen3.6／Qwen3.5**：比較正常 thinking、官方 template 的 `enable_thinking=False`（若 server 暴露該欄位）與 repo 現有 `/no_think` fixture；不要先把 `/no_think` 設為 production default。
- **gpt-oss**：比較 `reasoning_effort=none/low`，確認 Ollama 的 Harmony rendering、JSON mode 與 `message.content` 的 final answer 形狀；確認沒有把完整 reasoning trace 寫入 digest 或 log。
- **Ling**：在官方 SGLang／vLLM 路徑確認 parser、`<think>`／`<tool_call>` 邊界與 OpenAI-compatible JSON；不要以 Ollama PR 狀態推論主線 binary 已支援。
- **Mistral**：用官方 vLLM parser／tokenizer 形狀跑工具與 JSON fixture；確認 Chinese output 與 Horizon 的 `response_format` 行為。

### 5.3 建議採用 gate

只有同時滿足以下條件才可改 production config：

- 固定 fixture 沒有不可接受的 parse／schema 回歸；
- 繁中 glossary 與雙語欄位抽樣品質不低於目前 Qwen3.6 baseline；
- 在 `analysis_concurrency=1`、`enrichment_concurrency=1` 下穩態 latency 或 token cost 確實改善；
- 完整 daily run 的來源覆蓋與 max-items／top-N 政策沒有改變；
- Docker container path 可重現，且 model tag、runtime 版本、量化檔 checksum 已記錄；
- license、USAGE_POLICY、模型卡與第三方資料條款已由部署者審閱。

## 6. 風險與維運

1. **間接提示注入**：RSS、Hacker News、Reddit、Telegram、Google News 內容是不受信任輸入。模型支援 tool calling 不表示 Horizon 應把工具權限交給它；維持目前「內容是資料，不是指令」的 system prompt，並對 URL、sources 與輸出做驗證。
2. **thinking 成本**：reasoning trace 可能讓每項 scoring 的 output tokens 與 retry 數急升；需以 token／latency 實測，不用模型名稱推論速度。
3. **量化與上下文**：官方權重大小或 8K memory 宣稱不包含 Horizon 所有 prompt、KV cache、Docker、OS 與可能的 runtime buffer。長 context 只有在實際輸入需要時才值得付成本。
4. **自訂 runtime 供應鏈**：Ling 的 fork／dev image 與 gpt-oss 的 Harmony／Metal reference 都需要鎖定版本、來源與 checksum；不要把社群 PR、未合併分支或 reference implementation 誤當 production support。
5. **資料與授權邊界**：本地推論降低把新聞內容送到外部 API 的需要，但不會自動解決模型 license、訓練資料 provenance 或 output 的事實性問題。

## 7. 來源清單（官方來源於 2026-08-11 查閱；本地實測於 2026-08-12）

### Horizon 本地來源

- [Horizon AI client](../src/ai/client.py)：OpenAI-compatible client、Ollama base URL normalization、`response_format`、timeout／retry。
- [Horizon analyzer](../src/ai/analyzer.py)：每項內容的 scoring 呼叫與 JSON fallback。
- [Horizon prompts](../src/ai/prompts.py)：scoring、dedup、enrichment、繁中 glossary 與雙語 schema。
- [Horizon config](../data/config.json)：目前 Ollama model tag、單請求 concurrency、max items 與 enrichment top-N。
- [Local LLM performance requirements](../specs/2026-07-15-local-llm-performance-requirements.md)：歷史 request 數、單請求限制與 Docker 驗證規範。
- [Local daily runner](../scripts/daily-run-local.sh)：Docker／OrbStack／`host.docker.internal` 執行入口。
- [No-think benchmark](../src/tools/no_think_benchmark.py)：目前只把 `/no_think` 作為 prompt variant 的研究工具。

### 本地完整試跑證據（2026-08-12）

**[S18] 雙模型完整流程**：見[比較報告](2026-08-12-full-run-model-comparison.md)，收錄 qwen3.6／gpt-oss log、wall-clock、token 與內容比較限制；完整摘要與 log 亦保存在 `research/`。

**[S22] 固定三案例評測**：本機暫存 `/tmp/horizon-full-eval/qwen36.json`、`nemotron.json`、`qwen36-real.json`、`nemotron-real.json` 及對應摘要。評測腳本為 `/tmp/horizon_full_eval.py`；檔案不在 repo，須以本次報告的摘要數據與執行設定解讀。

**本機 Nemotron gate 判定（更新）**：Nemotron 3.5 Lightning 已完成三筆固定 fixture 的合成背景與真實 DuckDuckGo 搜尋兩組隔離評測；9/9 請求均成功解析、沒有錯誤，並顯示明顯速度優勢。但兩組評測都在 harness 注入 `reasoning_effort="none"`，且只涵蓋三筆案例；真實搜尋的 `sources` 為 2/3 項、共 2 筆，尚不足以取代 production gate。因此維持「P2 受控實驗候選，不切換生產」。
- **已觀察**：repo 現在用 Ollama OpenAI-compatible path；本機已有 Qwen3.6 自訂 35B-A3B Q4 tag、`gpt-oss:20b` 與 `nemotron-3.5-lightning:30b-mlx`。Nemotron tag 在 Ollama 0.32.9 下可載入，大小 22 GB。
- **已核驗**：Qwen3.6、gpt-oss、Qwen3.5-9B、Ling tiny、Mistral Small 3.1、Muse Glimmer、Nemotron Nano、DeepSeek V4 Flash 與 Nemotron 3.5 Lightning 的官方規格、授權／語言／部署差異如上。
- **本機 Nemotron 固定 fixture**：固定合成背景總耗時 83.669 秒、真實搜尋總耗時 95.087 秒；兩者均 9/9 JSON parse 成功、0 error。`reasoning_effort="none"` 下固定案例 `community_discussion_zh` 為 2/3、sources 0，真實搜尋為 3/3、sources 2；禁用詞機械計數分別 2 次。這些數據不能推廣到完整 daily run。
- **尚未聲稱**：Nemotron 已在完整 Horizon daily run、同輸入 wall-clock、繁中人工事實性或引用忠實度上勝過目前模型；正式 client 尚未加入 reasoning control。
### 官方模型與部署來源

- **[S19] Ollama Nemotron 3.5 Lightning 官方公告**：<https://ollama.com/blog/nemotron-3-5-lightning> — 30B total／3B active、Apple Silicon `30b-mlx` tag、1M context 與官方宣稱的 agent 定位。
- **[S20] NVIDIA Nemotron 3.5 Lightning 官方 Hugging Face model card**：<https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4> — OpenMDW-1.1 metadata、官方語言標籤、30B／3B active、硬體與 runtime 限制。
- **[S21] Ollama thinking 控制文件**：<https://docs.ollama.com/capabilities/thinking> — `thinking`／`content` 分離、API 預設 thinking 與關閉方式。
- **[S2] Qwen3.6-35B-A3B 官方 Hugging Face model card**：<https://huggingface.co/Qwen/Qwen3.6-35B-A3B> — Apache 2.0 metadata、chat template、模型檔與架構 metadata。
- **[S3] Qwen3.6 官方 GitHub**：<https://github.com/QwenLM/Qwen3.6> — Apache 2.0 repo、Qwen3.6／3.5 release timeline、Transformers／llama.cpp／MLX／SGLang／vLLM 部署說明。
- **[S4] OpenAI gpt-oss 官方 GitHub**：<https://github.com/openai/gpt-oss> — 20B／120B total and active parameters、Apache 2.0、MXFP4 memory claim、Harmony requirement、structured outputs、Ollama／Metal 路徑與 `USAGE_POLICY`。
- **[S5] Ollama gpt-oss 官方模型頁**：<https://ollama.com/library/gpt-oss> — `gpt-oss:20b`／`gpt-oss:120b` 官方 Ollama tags 與模型定位。
- **[S7] Ollama OpenAI compatibility**：<https://docs.ollama.com/api/openai-compatibility> — `/v1/chat/completions` 支援項目與 `response_format`／`reasoning_effort` 欄位。
- **[S8] Ollama Structured Outputs**：<https://docs.ollama.com/capabilities/structured-outputs> — JSON mode、JSON Schema `format` 與 OpenAI-compatible structured output 說明。
- **[S9] Ollama Qwen3.6 官方模型頁**：<https://ollama.com/library/qwen3.6> — 官方可用 tags 與 Qwen3.6 本地模型入口。
- **[S10] Qwen3.5-9B 官方 Hugging Face model card**：<https://huggingface.co/Qwen/Qwen3.5-9B> — Apache 2.0、9B metadata、multimodal chat template、`enable_thinking`／tool-call template。
- **[S11] Ollama Qwen3.5 官方模型頁**：<https://ollama.com/library/qwen3.5> — 官方 `qwen3.5:9b` tag 入口。
- **[S12] Ling-3.0-tiny 已完成的官方材料核驗報告**：[`research/2026-08-11-ling-3-tiny-practicality.md`](2026-08-11-ling-3-tiny-practicality.md) — 內含官方 HF model cards、config、SGLang cookbook、vLLM fork 與 Ollama PR 的逐項證據。
 
### 7.1 本機評測來源

- **[S22] 固定評測 JSON 與摘要（本機暫存）**：`file:///tmp/horizon-full-eval/qwen36.json`、`file:///tmp/horizon-full-eval/nemotron.json`、`file:///tmp/horizon-full-eval/qwen36-real.json`、`file:///tmp/horizon-full-eval/nemotron-real.json` 及同名 `*-summary-zh.md`；評測腳本為 `file:///tmp/horizon_full_eval.py`。這些檔案不在 repo，資料只代表 2026-08-12 本機執行。

## 8. 本次調查的可驗證結論

**本機 Nemotron gate 判定（更新）**：Nemotron 3.5 Lightning 已完成三筆固定 fixture 的合成背景與真實 DuckDuckGo 搜尋兩組隔離評測；9/9 請求均成功解析、沒有錯誤，並顯示明顯速度優勢。但兩組評測都在 harness 注入 `reasoning_effort="none"`，且只涵蓋三筆案例；真實搜尋的 `sources` 為 2/3 項、共 2 筆，尚不足以取代 production gate。因此維持「P2 受控實驗候選，不切換生產」。
- **已觀察**：repo 現在用 Ollama OpenAI-compatible path；本機已有 Qwen3.6 自訂 35B-A3B Q4 tag、`gpt-oss:20b` 與 `nemotron-3.5-lightning:30b-mlx`。Nemotron tag 在 Ollama 0.32.9 下可載入，大小 22 GB。
- **已核驗**：Qwen3.6、gpt-oss、Qwen3.5-9B、Ling tiny、Mistral Small 3.1、Muse Glimmer、Nemotron Nano、DeepSeek V4 Flash 與 Nemotron 3.5 Lightning 的官方規格、授權／語言／部署差異如上。
- **本機 Nemotron 固定 fixture**：固定合成背景總耗時 83.669 秒、真實搜尋總耗時 95.087 秒；兩者均 9/9 JSON parse 成功、0 error。`reasoning_effort="none"` 下固定案例 `community_discussion_zh` 為 2/3、sources 0，真實搜尋為 3/3、sources 2；禁用詞機械計數分別 2 次。這些數據不能推廣到完整 daily run。
- **尚未聲稱**：Nemotron 已在完整 Horizon daily run、同輸入 wall-clock、繁中人工事實性或引用忠實度上勝過目前模型；正式 client 尚未加入 reasoning control。

[S1]: https://qwen.ai/blog?id=qwen3.6-35b-a3b
[S2]: https://huggingface.co/Qwen/Qwen3.6-35B-A3B
[S3]: https://github.com/QwenLM/Qwen3.6
[S4]: https://github.com/openai/gpt-oss
[S5]: https://ollama.com/library/gpt-oss
[S7]: https://docs.ollama.com/api/openai-compatibility
[S8]: https://docs.ollama.com/capabilities/structured-outputs
[S9]: https://ollama.com/library/qwen3.6
[S10]: https://huggingface.co/Qwen/Qwen3.5-9B
[S11]: https://ollama.com/library/qwen3.5
[S12]: 2026-08-11-ling-3-tiny-practicality.md
[S13]: https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503
[S14]: 2026-08-10-meta-muse-glimmer-verification.md
[S15]: https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-FP8
[S16]: https://ollama.com/library/nemotron-3-nano
[S17]: https://ollama.com/library/deepseek-v4-flash
[S18]: 2026-08-12-full-run-model-comparison.md
[S19]: https://ollama.com/blog/nemotron-3-5-lightning
[S20]: https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4
[S21]: https://docs.ollama.com/capabilities/thinking
