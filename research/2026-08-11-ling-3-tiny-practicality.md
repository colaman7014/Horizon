# InclusionAI Ling-3.0-tiny 官方材料與實用性核驗報告

**核驗日期**：2026-08-11  
**核驗對象**：InclusionAI 官方發布之 Ling-3.0-tiny 模型卡、架構配置、推理說明與基準報告  
**主要權威來源**：
- Hugging Face Model Card (BF16): [inclusionAI/Ling-3.0-tiny](https://huggingface.co/inclusionAI/Ling-3.0-tiny)
- Hugging Face Model Card (FP8): [inclusionAI/Ling-3.0-tiny-fp8](https://huggingface.co/inclusionAI/Ling-3.0-tiny-fp8)
- Hugging Face Model Card (INT4): [inclusionAI/Ling-3.0-tiny-int4](https://huggingface.co/inclusionAI/Ling-3.0-tiny-int4)
- SGLang Official Cookbook: [SGLang Ling-3.0-tiny Cookbook](https://docs.sglang.io/cookbook/autoregressive/InclusionAI/Ling-3.0-tiny)
- vLLM InclusionAI Official Fork: [inclusionAI/vllm-ling-v3](https://github.com/inclusionAI/vllm-ling-v3)
- Ollama Community PR: [ollama/ollama#17643](https://github.com/ollama/ollama/pull/17643)

---

## 一、 結論摘要 (Executive Summary)

1. **模型基本定位與性質**：
   **InclusionAI**（螞蟻集團 AGI 團隊）於 2026 年 8 月釋出輕量化混合推理 MoE 模型 **Ling-3.0-tiny**，採用 **MIT 授權**。該模型總參數為 **7.9B**，每 Token 僅啟用 **1.3B** 參數（1 個共享專家 + 8 個路由專家），旨在提供兼具輕量計算開銷與 Agent／工具呼叫能力之本地與邊緣端推理方案。

2. **核心技術特徵與官方宣稱核驗結果**：
   - **混合線性注意力 (Hybrid-Linear Architecture)**：採 3:1 之 KDA (Kimi Delta Attention) 與 MLA (Multi-Head Latent Attention) 交替堆疊，共 24 層（18 層 KDA + 6 層 MLA）。
   - **原生雙模式推理 (Native Hybrid Reasoning)**：支援思考模式 (Thinking mode) 與直出模式，可在 request 中透過 `enable_thinking` 參數開關。
   - **上下文長度 (Context Window)**：原生配置 `max_position_embeddings` 為 131,072 (128K)；SGLang / 官方模型卡透過 YaRN scaling (`factor: 2.0`, `rope_theta: 6000000`) 將上下文擴展至 **256K** (262,144 tokens)。
   - **硬體效能官方宣稱**：FP8 量化下，在 NVIDIA DGX Spark 達到 **100–105 tokens/s**，在 Apple Silicon M4 Pro (48GB Unified Memory) 達到 **86–90 tokens/s**，8K 上下文峰值記憶體開銷約 **8.34 GiB**。
   - **第三方評測數字 (Artificial Analysis)**：AA Intelligence Index v4.1.1 為 **25** 分，AA Agentic Index 為 **16** 分，輸出速度超過 **160 tokens/s**。

3. **關鍵差異與官方文件勘誤／缺口**：
   - **BFCL-v4 分數有列出，但重現資訊不足**：官方 benchmark 表格圖片列出 BFCL-v4 (FC) **62.72**；模型卡沒有公開該分數的原始輸出、測試腳本、資料版本或完整 protocol，因此二手文章中的其他數字不可直接採信。
   - **無 MTP / NEXTN 投機解碼（模型卡 README 勘誤）**：`config.json` 明確記載 `num_nextn_predict_layers: 0`。HF 模型卡 README 中的 SGLang 範例指令誤寫了 `--speculative-algorithm NEXTN`；SGLang 官方 Cookbook 已澄清 Ling-3.0-tiny 並無內建 MTP 層，不適用 NEXTN 投機解碼。
   - **推理框架上游成熟度不足**：目前 vLLM 需使用專用 fork (`inclusionAI/vllm-ling-v3`)，Ollama 需手動編譯未合併之 PR `#17643`（僅限 Apple Silicon MLX），SGLang 需使用專屬 dev Docker 影像。

---

## 二、 逐項主張與規格核驗矩陣 (Specification & Verification Matrix)

| 編號 | 評估項目 / 主張內容 | 核驗狀態 (Status) | 權威證據摘錄 (Evidence Extract) | 來源 URL (Source URL) |
| :--- | :--- | :---: | :--- | :--- |
| **V1** | **MoE 總參數與啟用參數**：總參數 7.9B，每 Token 啟用 1.3B 參數。 | **Verified** | Model Card 載明 7.9B total / 1.3B activated；`config.json` 列出 `hidden_size: 1536`, `num_hidden_layers: 24`, `num_experts: 128`, `num_experts_per_tok: 8`, `num_shared_experts: 1`。 | [HF Model Card](https://huggingface.co/inclusionAI/Ling-3.0-tiny), [config.json](https://huggingface.co/inclusionAI/Ling-3.0-tiny/raw/main/config.json) |
| **V2** | **架構設計 (KDA + MLA + Sparse MoE)**：3:1 KDA:MLA 交替堆疊，128 個路由專家。 | **Verified** | Model Card 載明 3:1 alternating stacking of KDA and MLA (3 KDA + 1 MLA in every 4-layer block) 與 128 routed experts (`layer_group_size: 4`)。 | [HF Model Card](https://huggingface.co/inclusionAI/Ling-3.0-tiny), [config.json](https://huggingface.co/inclusionAI/Ling-3.0-tiny/raw/main/config.json) |
| **V3** | **量化權重格式**：提供 BF16, FP8, INT4 三種精度權重。 | **Verified** | HF `inclusionAI` 官方組織發布 `inclusionAI/Ling-3.0-tiny` (BF16, ~15.8GB)、`inclusionAI/Ling-3.0-tiny-fp8` (FP8 blockwise E4M3, ~7.9GB) 與 `inclusionAI/Ling-3.0-tiny-int4`。 | [HF inclusionAI Org](https://huggingface.co/inclusionAI), [SGLang Cookbook](https://docs.sglang.io/cookbook/autoregressive/InclusionAI/Ling-3.0-tiny) |
| **V4** | **上下文長度 (256K Context)**：原生 128K，可經由 YaRN 擴展至 256K。 | **Verified with context caveat** | `config.json` 標示 `max_position_embeddings: 131072` (128K)；SGLang 啟動指令帶入 `rope_type: yarn`, `factor: 2.0`, `rope_theta: 6000000`, `context-length: 262144` (256K)。 | [config.json](https://huggingface.co/inclusionAI/Ling-3.0-tiny/raw/main/config.json), [HF Model Card](https://huggingface.co/inclusionAI/Ling-3.0-tiny) |
| **V5** | **8K 上下文記憶體開銷**：FP8 下 8K context 峰值記憶體開銷約 8.34 GiB。 | **Verified as official claim** | HF Model Card 明確記載 "with approximately 8.34 GiB peak memory usage at an 8K context length"（FP8 條件下）。 | [HF Model Card](https://huggingface.co/inclusionAI/Ling-3.0-tiny) |
| **V6** | **DGX Spark / M4 Pro 推理速度**：DGX Spark FP8 達 100-105 tok/s，M4 Pro 達 86-90 tok/s。 | **Verified as official claim** | Model Card 記載 "reaches around 100-105 tokens/s on DGX Spark and 86-90 tokens/s on an M4 Pro MacBook"。 | [HF Model Card](https://huggingface.co/inclusionAI/Ling-3.0-tiny) |
| **V7** | **Artificial Analysis (AA) 評測分數**：Intelligence Index 25，Agentic Index 16，輸出速度 >160 tok/s。 | **Verified as model card statement** | Model Card 載明 AA Intelligence Index v4.1.1: 25, Agentic Index: 16, output speed >160 tokens/s (500 tok 響應 Latency ~18s)。 | [HF Model Card](https://huggingface.co/inclusionAI/Ling-3.0-tiny) |
| **V8** | **思考模式與工具呼叫 Token 格式**：使用專屬 XML 標籤與 `ling3`/`deepseek-r1`/`glm45` 解析器。 | **Verified** | `tokenizer_config.json` 與 `chat_template.jinja` 包含 `<think>`, `</think>`, `<tool_call>`, `</tool_call>`, `<arg_key>`, `<arg_value>`, `<tool_response>` 特殊標籤。 | [tokenizer_config.json](https://huggingface.co/inclusionAI/Ling-3.0-tiny/raw/main/tokenizer_config.json), [chat_template.jinja](https://huggingface.co/inclusionAI/Ling-3.0-tiny/raw/main/chat_template.jinja) |
| **V9** | **BFCL-v4 (Berkeley Function Calling) 評測分數** | **Verified as model-card table; reproducibility gap** | 官方 benchmark 表格圖片列出 **62.72**；但模型卡、config 與 SGLang Cookbook 未提供原始輸出、資料版本、測試腳本或完整重現 protocol，坊間其他分數不可視為已核實。 | [HF Model Card](https://huggingface.co/inclusionAI/Ling-3.0-tiny) |
| **V10** | **MTP / NEXTN 投機解碼支援**：Model Card 寫有 `--speculative-algorithm NEXTN`。 | **Disproven / Official Typo** | `config.json` 設定 `num_nextn_predict_layers: 0`；SGLang 官方文檔明確指出 Ling-3.0-tiny 未內建 MTP 層，故無法使用 NEXTN 投機解碼（模型卡 README 為誤植）。 | [config.json](https://huggingface.co/inclusionAI/Ling-3.0-tiny/raw/main/config.json), [SGLang Cookbook](https://docs.sglang.io/cookbook/autoregressive/InclusionAI/Ling-3.0-tiny) |

---

## 三、 未核實項目、限制與官方宣稱缺口 (Unverified / Gaps & Limitations)

1. **BFCL-v4 評測可重現性不足**：
   - 官方表格確實列出 BFCL-v4 (FC) **62.72**，但未附原始輸出、資料版本、測試腳本或完整 protocol。這足以支持「有一定工具呼叫能力」的初步判斷，不能單獨支持「生產級 function calling」。
2. **HF README Quickstart 中的 NEXTN 投機解碼屬文件誤植**：
   - 官方 Hugging Face README 的 SGLang 範例中包含 `--speculative-algorithm NEXTN`，但 `config.json` 顯示 `num_nextn_predict_layers` 為 0（無預測層）。SGLang 官方 Cookbook 頁面證實了這一點，並指出 NEXTN 僅適用於包含 MTP 結構的 Ling-3.0-flash。

3. **速度與記憶體開銷為單方面宣稱，缺少標準化環境比較**：
   - 官方記載的 M4 Pro (48GB) 86–90 tok/s、DGX Spark 100–105 tok/s，以及 8K 上下文下 8.34 GiB 記憶體使用，未詳細說明 KV Cache 占用的比例、Prompt 長度與 Batch Size 設定。`[INFERENCE]` 在高並發或長 Prompt 情境下，實際記憶體開銷將顯著高於 8.34 GiB。

4. **主流推理引擎上游整合尚未完成**：
   - **vLLM**：官方主流 `vllm-project/vllm` 尚未合併，需改由 `inclusionAI/vllm-ling-v3` 分支 `ling_3_0` 手動編譯。
   - **Ollama / Llama.cpp**：僅存在於 Pull Request `ollama/ollama#17643`（`bailing-moe-v3`），且受限於 Apple Silicon MLX 架構，官方發行版 binary 尚未內建。
   - **SGLang**：需拉取專用開發鏡像 `lmsysorg/sglang:dev-Ling-3.0-tiny`。

---

## 四、 部署與風險意義 (Deployment & Risk Implications)

1. **本地端 / 邊緣端 Agent 節點可行性**：
   - **優點**：FP8 量化後模型權重約 7.9 GB；模型卡另宣稱 8K context 峰值約 8.34 GiB。`[INFERENCE]` 這使 16GB 級記憶體成為短上下文測試的候選硬體，但官方未驗證 RTX 4060 Ti、RTX 4070 等具體卡型，且 runtime、OS、KV cache 與並發會改變實際需求，不應直接承諾可行。
   - **結構化輸出**：模型原生訓練有 `<think>` 思考鏈與 `<tool_call>` 標籤，可透過 SGLang 的 `deepseek-r1` reasoning parser 與 `glm45` tool call parser 進行高品質 JSON 提取。

2. **維護與營運風險 (Operational Risks)**：
   - **非標準 Runtime 依賴**：因模型採用 BailingMoeV3 (`bailing_hybrid`) 自訂架構與 KDA+MLA 混合層，無法直接套用通用 Llama/Qwen 推理 pipeline。極度依賴 InclusionAI 團隊維持其 SGLang Docker 與 vLLM fork 的更新。

3. **長上下文精度與 RoPE Scaling 效能**：
   - 模型原生 `max_position_embeddings` 為 128K，256K 是經由 YaRN 2.0x 擴展而得。在超長上下文 (128K–256K) 任務中，注意力機制可能面臨 Needle-in-a-Haystack (NIAH) 檢索能力衰減或思考鏈中途斷裂之風險。

4. **安全與 Prompt Injection 防護**：
   - Ling-3.0-tiny 預設啟動思考模式 (`enable_thinking: true`)，在自動化 Agent 工作流中，若將 `reasoning_content` 與系統對話記錄傳遞給 downstream 工具，需防範來自外部網頁或文件的間接提示注入 (Indirect Prompt Injection)。

---

## 五、 完整來源清單 (Primary Sources)

1. **InclusionAI Ling-3.0-tiny Hugging Face 官方模型頁面與 Model Card**
   - **URL**: `https://huggingface.co/inclusionAI/Ling-3.0-tiny`
   - **查核存取日期**: 2026-08-11
   - **關鍵證據**:
     > "Ling-3.0-tiny, a lightweight hybrid reasoning MoE model with 7.9B total parameters and only 1.3B activated parameters per token."
     > "With FP8, Ling-3.0-tiny reaches around 100-105 tokens/s on DGX Spark and 86-90 tokens/s on an M4 Pro MacBook, with approximately 8.34 GiB peak memory usage at an 8K context length."

2. **InclusionAI Ling-3.0-tiny 官方模型設定檔 (config.json)**
   - **URL**: `https://huggingface.co/inclusionAI/Ling-3.0-tiny/raw/main/config.json`
   - **查核存取日期**: 2026-08-11
   - **關鍵證據**:
     > `"model_type": "bailing_hybrid"`, `"num_hidden_layers": 24`, `"hidden_size": 1536`, `"num_experts": 128`, `"num_experts_per_tok": 8`, `"num_shared_experts": 1`, `"max_position_embeddings": 131072`, `"num_nextn_predict_layers": 0`

3. **SGLang 官方部署 Cookbook (Ling-3.0-tiny Cookbook)**
   - **URL**: `https://docs.sglang.io/cookbook/autoregressive/InclusionAI/Ling-3.0-tiny`
   - **查核存取日期**: 2026-08-11
   - **關鍵證據**:
     > "~7.9B total parameters with ~1.2B active... Ling-3.0-tiny ships no built-in MTP draft layer (`num_nextn_predict_layers: 0`), so `--speculative-algorithm NEXTN` is not applicable."
     > "Ling-3.0-tiny uses `--reasoning-parser deepseek-r1` and `--tool-call-parser glm45`"

4. **InclusionAI vLLM 官方 Fork 儲存庫**
   - **URL**: `https://github.com/inclusionAI/vllm-ling-v3`
   - **查核存取日期**: 2026-08-11
   - **關鍵證據**:
     > `git clone -b ling_3_0 https://github.com/inclusionAI/vllm-ling-v3.git` 提供特化 vLLM 分支以支援 Ling-3.0 架構。

5. **Ollama 社群/官方 Pull Request #17643**
   - **URL**: `https://github.com/ollama/ollama/pull/17643`
   - **查核存取日期**: 2026-08-11
   - **關鍵證據**:
     > `git fetch origin refs/pull/17643/head:bailing-moe-v3`，目前僅提供 Apple Silicon MLX 之實驗性支援。


6. **Berkeley Function Calling Leaderboard V4 官方說明**
   - **URL**: `https://gorilla.cs.berkeley.edu/leaderboard.html`
   - **查核存取日期**: 2026-08-11
   - **關鍵證據**：
     > BFCL V4 說明 Overall Accuracy 為各子類別的 unweighted average，並公開評測 commit 與結果重現入口；本報告未在公開結果 archive 中找到 Ling-3.0-tiny 的原始回應資料。

7. **BFCL 官方結果 archive**
   - **URL**: `https://github.com/HuanzhiMao/BFCL-Result`
   - **查核存取日期**: 2026-08-11