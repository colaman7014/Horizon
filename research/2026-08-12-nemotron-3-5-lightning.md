# NVIDIA Nemotron 3.5 Lightning 官方資料研析與 Horizon 本地 Ollama 適配評估報告

> **評估日期**：2026-08-12  
> **評估目標**：研析 NVIDIA 於 2026-08-11 發布之 **Nemotron 3.5 Lightning** 官方規格、授權條款與生態系支援，評估其於 Horizon repo（基於 Docker 轉接 Host Ollama、Apple Silicon M4 Pro 48GB、繁體中文結構化 JSON 輸出）之本地工作負載可行性。  
> **結論閘門 (Gate)**：**保留為 P2 實驗候選；已完成最小 Docker smoke，但不進行 Full Run，也不切換主要生產模型。** 預設 reasoning 與 Horizon 現有 `message.content` 介面有實測阻斷風險；只有在正式 client 加入並驗證 `reasoning_effort="none"`（或等價控制）及固定 fixture gate 後，才重新評估。

---

## 1. 執行摘要 (Executive Summary)

NVIDIA 於 2026-08-11 發布了針對 AI Agent 執行層（Execution Layer）優化之**開放權重模型** **Nemotron 3.5 Lightning**。這裡的「開放權重」是本報告的精確用語；不把它直接等同 OSI 認可的完整開源。該模型採用 30B 總參數、3B 啟用參數（30B-A3B）之混合架構（Mamba-2 + MoE + Select Attention），並預載 Multi-Token Prediction (MTP) 技術與 OpenMDW 1.1 授權。這裡的「開放」不等同於 OSI 認可的完整開源；模型權重、授權與訓練資料可得性需分開判讀。

在本地 Ollama 生態中，Ollama 官方已提供包含 `nemotron-3.5-lightning:30b-mlx` 在內之模型標籤。然而，結合 Horizon 現有架構（`response_format={"type": "json_object"}`、`message.content` 解析、繁體中文科技新聞摘要與分析、Apple Silicon M4 Pro 48GB）評估，存在以下關鍵適配風險：
1. **Thinking/Reasoning 標籤污染風險**：模型 chat template 預設啟用推理模式，且官方 vLLM 需特化 `--reasoning-parser nemotron_v3`；若經由 Ollama `/v1/chat/completions` 回傳含有思考標籤或非 JSON 內容，將直接導致 Horizon 的 `message.content` 解析中斷。
2. **繁體中文 (zh-TW) 語意與 Tokenizer 風險**：官方 Hugging Face 標註之主要語言為 `en, es, fr, de, it, ja`；post-training 說明雖包含 Chinese，但並未針對繁體中文語意與台灣用語提供獨立保證，可能造成簡繁混雜或用詞不一致。
3. **推論效能不可直接轉移**：Ollama／NVIDIA 官方宣稱之較高 throughput 與任務加速均有特定硬體、量化、推測解碼與 runtime 條件，**不能視為 Apple Silicon M4 Pro 上的本機表現**。

---

## 2. 官方規格與技術細節 (FACT / 官方公開資料)

本節資料均來自 NVIDIA 官方 Blog、Hugging Face Model Cards、Ollama 官方頁面與 OpenMDW 1.1 授權文件，查閱日期統一為 **2026-08-12**。

### 2.1 模型基本資訊與規格 (FACT)
* **模型名稱**：NVIDIA Nemotron 3.5 Lightning (30B-A3B)
* **發布日期**：2026-08-11
* **參數規模**：總參數 300 億 (30B Total)，單次 Forward Pass 啟用參數 30 億 (3B Active)。
* **模型架構**：Mamba-2 + Mixture-of-Experts (MoE) + Select Attention 混合層，並整合 Multi-Token Prediction (MTP) Heads 用於原生推測解碼（Speculative Decoding）。
* **上下文長度 (Context Window)**：最高支援 **1,000,000 (1M) tokens**（單張 H100 預設部署常設定為 256K）。
* **開放權重與授權**：[OpenMDW License Agreement, version 1.1 (OpenMDW-1.1)](https://openmdw.ai/license/1-1/) (查閱日期: 2026-08-12)。條款授予在遵守條件下處理 Model Materials 的廣泛權利，但它不是 OSI 認可的標準軟體授權；散布時仍須保留授權與來源聲明。
* **官方 Hugging Face Model Cards**：
  * Base 預訓練檔：[nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Base-BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Base-BF16) (查閱日期: 2026-08-12)
  * Post-trained 參考全精度檔：[nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16) (查閱日期: 2026-08-12)
  * NVFP4 量化與部署檔：[nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4) (查閱日期: 2026-08-12)

### 2.2 官方 Ollama 支援與 Tags (FACT)
* **Ollama 公告日期**：2026-08-11 ([Ollama Blog: NVIDIA Nemotron 3.5 Lightning](https://ollama.com/blog/nemotron-3-5-lightning)) (查閱日期: 2026-08-12)
* **Ollama Library 頁面**：[ollama.com/library/nemotron-3.5-lightning](https://ollama.com/library/nemotron-3.5-lightning) (查閱日期: 2026-08-12)
* **官方提供之 Model Tags**：
  * `nemotron-3.5-lightning:latest`
  * `nemotron-3.5-lightning`
  * `nemotron-3.5-lightning:30b`
  * `nemotron-3.5-lightning:30b-mlx`（特別針對 Apple Silicon 效能特化之版本）

### 2.3 訓練數據與語言支援 (FACT)
* **預訓練 (Pre-training) 資料**：
  * 資料總量：超過 20 Trillion (20T) tokens。
  * 數據截止日：2025 年 9 月。
  * 資料集組成：Nemotron-CC-v2/v2.1 (9.1T)、GitHub Code (1.7T)、Nemotron-CC-Math (133B) 及多項科學、法律、合成數據集。
* **後訓練 (Post-training) 資料**：
  * 數據截止日：2026 年 5 月。
  * 採用 GRPO (Group Relative Policy Optimization) 多環境強化學習與 SFT，包含 HelpSteer3、SWE-Gym、WildChat-1M 及 GPT-OSS-120B 蒸餾之 reasoning traces。
* **官方支援語言 (Language Tags)**：
  * Hugging Face Model Card 明確標註之主要語言標籤為：`en` (English), `es` (Spanish), `fr` (French), `de` (German), `it` (Italian), `ja` (Japanese)。
  * 於 Post-training 說明與評估集（Global-MMLU-Lite, MGSM）中包含 Chinese (`zh`)，**但官方規範與標籤中並無繁體中文 (zh-TW) 之獨立特化或聲明**。

### 2.4 Agentic、Reasoning 與 Tool Calling 特性 (FACT)
* **Reasoning 模式控制**：模型支援推理切換，於 chat template 中透過 `enable_thinking=True/False` 控制。
* **vLLM 解析器規範**：官方於 vLLM 部署範例中指定：
  * Reasoning Parser：`--reasoning-parser nemotron_v3`
  * Tool Calling Parser：`--tool-call-parser qwen3_coder`
  * Auto Tool Choice：`--enable-auto-tool-choice`
  * 程式碼 Agent 建議外加：`extra_body={"chat_template_kwargs": {"force_nonempty_content": True}}`

### 2.5 官方硬體與推論 Runtime (FACT)
* **官方原生目標硬體**：NVIDIA Blackwell (GB200, GeForce RTX 5090)、NVIDIA Hopper (H100, H200)、NVIDIA Ampere (A100)、DGX Spark / DGX Station。
* **官方推測解碼 (Speculative Decoding) 方案**：
  * **DSpark**：針對 DGX Spark 與低並行資料中心之 semi-autoregressive 草稿模型。
  * **DFlash**：基於 block-diffusion 之草稿模型。
  * **MTP**：原生 Multi-Token Prediction 頭部。
* **官方推薦推論引擎**：vLLM (`vllm/vllm-openai:v0.27.1`)、TensorRT-LLM、SGLang、Megatron-LM。

---

## 3. Horizon Repo 架構與適配性分析 (FACT vs INFERENCE)

本節將 Horizon 原始碼（`src/ai/client.py`、`src/orchestrator.py` 等）之實作事實，與 Nemotron 3.5 Lightning 之適配性進行明確的 FACT / INFERENCE 分離評估。

### 3.1 Horizon 現行 AI 請求機制 (FACT)
1. **Ollama 連線端點**：`OpenAIClient` 自動將 `base_url` 規範化為 `/v1` 介面（如 `http://localhost:11434/v1` 或 Docker 環境下透過 `HORIZON_OLLAMA_BASE_URL` 指向 `http://host.docker.internal:11434/v1`）。
2. **強制 JSON 結構化輸出**：`_do_request` 中預設帶入 `request_kwargs["response_format"] = {"type": "json_object"}`。
3. **結果擷取方式**：直接讀取 `response.choices[0].message.content`，並交由上層模組進行 `json.loads()` 解析。
4. **並行度與逾時設定**：Orchestrator 工作流採用 `concurrency=1` 依序處理項目；`AsyncOpenAI` client 設定有 `httpx.Timeout(600.0, connect=15.0)`。
5. **任務目標與 Prompt 語言**：針對 Github / HackerNews / OpenBB 等科技新聞資料進行繁體中文 (zh-TW) 摘要、主題分類、繁中實體提取與結構化 JSON 輸出。
6. **本機硬體環境**：Apple Silicon M4 Pro，配置 48GB 統一記憶體 (Unified Memory)。

### 3.2 適配風險與推論分析 (INFERENCE)

| 分析維度 | 現狀與潛在問題 (INFERENCE) | 影響評估 |
| :--- | :--- | :--- |
| **Reasoning 污染與 JSON 解析失敗** | Nemotron 3.5 Lightning 預設開啟 Reasoning 思考模式。在官方 vLLM 環境下需掛載 `--reasoning-parser nemotron_v3` 才能將思考過程過濾或轉移至特殊欄位。但在 Ollama 的通用 `/v1/chat/completions` API 中，若思考文字直接以 `<think>...</think>` 或原生內部標籤前綴輸出於 `message.content` 中，**Horizon 之 `json.loads(content)` 將直接拋出 `JSONDecodeError` 導致任務失敗**。 | **高風險 (High)** |
| **`response_format` 遵循能力未知** | 該模型雖然經過 Tool calling 與 Structured output SFT/GRPO 訓練，但在 MoE 混合 Mamba-2 架構下，配搭 Ollama 後端是否能在不傳遞特定 system prompt 之下完全遵循 `{"type": "json_object"}` 仍具不確定性。 | **中風險 (Medium)** |
| **繁體中文 (zh-TW) 品質與 Token 溢出** | 官方語言標籤未包含繁體中文。儘管強大的英文/多語言模型通常能進行基礎繁體中文理解，但在未特別優化 zh-TW Tokenizer 的情況下，中文生成可能遭遇：(1) Token 壓縮率低造成推論速度變慢；(2) 輸出混雜簡體中文用語（如「信息」、「软件」）；(3) 繁中語法不自然。 | **中高風險 (Medium-High)** |
| **Apple Silicon 48GB 記憶體與推論效能** | Nemotron 3.5 Lightning 總參數為 30B（啟用 3B）。本機 `ollama pull nemotron-3.5-lightning:30b-mlx` 下載進度顯示約 22GB 套件；這是本機 tag 觀察，不是官方 M4 Pro 記憶體保證。NVIDIA 官方宣稱的較高 throughput 建立於 NVFP4 + TensorRT-LLM / vLLM + DSpark/DFlash 等專屬顯卡技術之上。**在 macOS Metal / MLX 架構下不可直接套用 NVIDIA GPU benchmark。** | **中風險 (Medium)** |
---

## 4. 本機實測結果（2026-08-12）

本節為本機觀察，不是 NVIDIA benchmark；測試只使用隔離的臨時 harness，沒有修改 `src/`、`data/config.json` 或生產模型。

### 4.1 已完成的下載與 API 核驗

* 本機先將 Ollama 從 `0.32.1` 升級至 `0.32.9`；舊版拉取模型時回覆 `412: ... requires a newer version of Ollama`。升級並重啟服務後，`ollama pull nemotron-3.5-lightning:30b-mlx` 成功。
* `ollama list` 觀察到 `nemotron-3.5-lightning:30b-mlx`，本機 registry 顯示大小 **22 GB**；`/api/show` 顯示 format `safetensors`、family `nemotron_h`、parameter size `32.9B`、quantization `nvfp4`，capabilities 包含 `completion`、`tools`、`thinking`。這些是本機 tag metadata，不是 48GB 記憶體保證。
* API smoke 以 `http://127.0.0.1:11434/v1/chat/completions` 發送 `response_format={"type":"json_object"}`。預設推理模式下，一次請求回傳 `finish_reason=length`、`message.content` 為空、另有 `message.reasoning`，不能直接供 Horizon 使用。
* 同一請求加入 Ollama OpenAI-compatible 支援的 `reasoning_effort="none"` 後，`finish_reason=stop`，`message.content` 為可 `json.loads()` 的 JSON；無 `<think>` 標籤，並有非空 `message.content`。`src/ai/client.py` 目前沒有送出此控制欄位，因此**直接把 model tag 切換到 Nemotron 會保留這項風險**。

### 4.2 Horizon 隔離 smoke 結果

使用與 Horizon 相同的 `ContentAnalyzer`、`ContentEnricher`、`response_format` 與 Docker→`host.docker.internal:11434` 路徑，並在臨時 harness 中把每次 request 注入 `reasoning_effort="none"`。輸入為 1 筆英文科技新聞；背景搜尋使用固定假資料，只為隔離模型輸出，不代表真實搜尋品質。

| 測試 | 結果 |
|---|---|
| Docker image／host Ollama 路徑 | 成功，`base_url=http://host.docker.internal:11434` |
| Scoring | 1/1 完成，JSON/schema 欄位完整，score `7.0` |
| Concept extraction | 1/1 非空 JSON 回覆 |
| Enrichment | 1/1 非空 JSON 回覆；`title_zh`、`detailed_summary_zh`、`background_zh` 成功；`community_discussion_zh` 與 `sources` 本次未填滿 |
| `<think>` 標籤 | 0/3 request 回應含標籤（使用 `reasoning_effort=none`） |
| 請求數／token | 3 requests；input 2,349、output 675、total 3,024 tokens |
| wall-clock | scoring 2.042 s；enrichment 8.705 s；合計 10.747 s（單次隔離抽樣，非 daily-run 基準） |

原始結果：[Docker smoke JSON](file:///tmp/nemotron-docker-smoke/result.json)（本機暫存，未提交 repo）。由於只測 1 筆、沒有真實 web search，不能宣稱 daily run 速度或品質。

### 4.3 推理開關的實測結論

本機同時觀察到「預設 reasoning」與「`reasoning_effort=none`」兩種明顯不同結果。前者在 Horizon 直接讀取 `message.content` 的介面下是阻斷性風險；後者能讓最小 scoring／enrichment 流程走通。這支持的不是「模型已可生產」，而是：若要繼續評估，必須在 client 層明確加入並驗證 `reasoning_effort="none"`（或官方等價控制），而不能只改 `model` 字串。

### 4.4 仍未完成的驗證

* `[未完成]` 未執行 10 次連續固定 fixture，也未達成「JSON parse 100% 且繁中品質良好」的 production gate。
* `[未完成]` 未執行完整 Horizon daily run；沒有同輸入下與 Qwen3.6／gpt-oss 的 wall-clock、token、digest coverage A/B。
* `[未完成]` 本次未量測獨立 TTFT／穩態 tok/s，也未記錄載入時 unified memory 峰值。
* `[未完成]` 本次只用英文科技 smoke item，不能證明繁體中文金融、社群討論與來源陣列品質。

---

## 5. 結論與執行門檻建議 (Gate Recommendation)

### 5.1 決策門檻 (Gate Decision)
**建議：【保留為 P2 實驗候選，先完成固定 fixture；不做 Full Run，不替換 production model】。** 本機最小 Docker path 已能在明確關閉 reasoning 時走通，但輸入覆蓋與 schema 完整度不足以支持完整日報。

### 5.2 執行建議路線圖 (Actionable Roadmap)
1. **零程式碼修改原則**：不要直接修改 `src/` 或 `data/config.json` 來切換模型。
2. **若要繼續 smoke**：在隔離測試 client 明確傳 `reasoning_effort="none"`；記錄 model tag、Ollama 版本、量化 metadata、Docker image 與固定 fixture checksum。此欄位是 Ollama OpenAI-compatible 文件列出的控制方式；Horizon 正式 client 目前尚未傳送。
3. **Full Run gate**：至少完成 10 次固定 fixture；JSON parse／schema 欄位完整率達 100%；繁中 glossary、來源 URL、摘要忠實度不低於目前基線；並在 `analysis_concurrency=1`、`enrichment_concurrency=1` 下證明穩態成本改善後，才討論 full daily run。
4. **Production gate**：完整 daily run 可重現、沒有不可接受的 fallback／retry，且 client 端 reasoning 控制已正式實作並由測試覆蓋；否則維持 `data/config.json` 現有模型。

---

## 6. 參考文獻與官方來源 (References & Audit Log)

所有外部資料均於 **2026-08-12** 查閱並核對完畢：

1. **Ollama 官方新聞發布** (2026-08-11)：
   * URL: [https://ollama.com/blog/nemotron-3-5-lightning](https://ollama.com/blog/nemotron-3-5-lightning) (查閱日期: 2026-08-12)
2. **Ollama 模型庫專頁**：
   * URL: [https://ollama.com/library/nemotron-3.5-lightning](https://ollama.com/library/nemotron-3.5-lightning) (查閱日期: 2026-08-12)
3. **NVIDIA 官方 Launch Blog** (2026-08-11)：
   * URL: [https://blogs.nvidia.com/blog/nemotron-lightning-switchyard-rtx-dgx/](https://blogs.nvidia.com/blog/nemotron-lightning-switchyard-rtx-dgx/) (查閱日期: 2026-08-12)
   * URL: [https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/](https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/) (查閱日期: 2026-08-12)
4. **Hugging Face Model Cards** (NVIDIA 官方)：
   * Post-trained Instruct (BF16): [https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16) (查閱日期: 2026-08-12)
   * Base Pre-trained (BF16): [https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Base-BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Base-BF16) (查閱日期: 2026-08-12)
   * Quantized NVFP4: [https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4) (查閱日期: 2026-08-12)
5. **OpenMDW 1.1 授權合約**：
   * URL: [https://openmdw.ai/license/1-1/](https://openmdw.ai/license/1-1/) (查閱日期: 2026-08-12)
   * GitHub Raw License: [https://raw.githubusercontent.com/OpenMDW/OpenMDW/refs/heads/main/1.1/LICENSE.OpenMDW-1.1](https://raw.githubusercontent.com/OpenMDW/OpenMDW/refs/heads/main/1.1/LICENSE.OpenMDW-1.1) (查閱日期: 2026-08-12)
6. **Ollama OpenAI-compatible API 與思考控制文件**：
   * [OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility)（查閱日期: 2026-08-12）：列出 `response_format`、`reasoning_effort` 與 `/v1/chat/completions` 欄位支援。
   * [Thinking](https://docs.ollama.com/capabilities/thinking)（查閱日期: 2026-08-12）：說明思考輸出與 final `message.content`／`message.thinking` 的分離，以及思考預設開啟。
7. **本機實測 artifacts**：
   * `ollama --version`: `0.32.9`
   * `ollama list`: `nemotron-3.5-lightning:30b-mlx`，22 GB
   * Docker smoke：1 筆英文 item，3 requests，`reasoning_effort="none"`，JSON/schema scoring 成功；enrichment 主要欄位成功但 `community_discussion_zh`／`sources` 未穩定填滿。
