---
layout: default
title: "Horizon Summary: 2026-08-21 (ZH)"
date: 2026-08-21
lang: zh
---

> 從 223 條內容中篩選出 40 條重要資訊。

---

1. [Arrayref 套件遭受建置時惡意程式攻擊](#item-1) ⭐️ 8.0/10
2. [威宏-KY 2026 年第二季淨利創五季新高](#item-2) ⭐️ 8.0/10
3. [低成本 Mini Kimi‑K3 以 <$250 訓練，擊敗 GPT‑2 HellaSwag 成績](#item-3) ⭐️ 8.0/10
4. [Walmart 報告六年來最低銷售增長](#item-4) ⭐️ 8.0/10
5. [SK Hynix 宣布 290 億美元回購與記憶體短缺警示](#item-5) ⭐️ 8.0/10
6. [NVIDIA 價值因未來出貨而合理化](#item-6) ⭐️ 8.0/10
7. [馬維爾 AI 催化劑或帶來 21％上漲](#item-7) ⭐️ 8.0/10
8. [台積電 VS ASML：哪個半導體巨頭更值得投資？](#item-8) ⭐️ 8.0/10
9. [台積電因 AI 需求飆升](#item-9) ⭐️ 8.0/10
10. [台積電公布七月營收成長，估值爭議升溫](#item-10) ⭐️ 8.0/10
11. [台積電產能限制或改變 AI 晶片供應與價格](#item-11) ⭐️ 8.0/10
12. [台積電股價飆升 31% 超過成長因子估值](#item-12) ⭐️ 8.0/10
13. [ADI 公布歷史高盈餘 股價下跌 TSMC & ASE 受益](#item-13) ⭐️ 8.0/10
14. [應材攜柏克萊加速 AI 晶片創新](#item-14) ⭐️ 8.0/10
15. [Grok 透過加密的上下文注入洩露使用者資料](#item-15) ⭐️ 7.0/10
16. [亞馬遜計畫於 2026 年前覆蓋 500 個美國社區](#item-16) ⭐️ 7.0/10
17. [蘋果新任 CEO 或重塑 AI 策略](#item-17) ⭐️ 7.0/10
18. [財政部計畫加倍長期國債回購](#item-18) ⭐️ 7.0/10
19. [裂解差價上升預示汽油價格持續高企](#item-19) ⭐️ 7.0/10
20. [平日住宿補助最高 NT$3700／人，9/1 起啟動](#item-20) ⭐️ 7.0/10
21. [FactSet 提升旭隼 EPS 預估至 31.42 元](#item-21) ⭐️ 7.0/10
22. [聯亞七月營收大增 503%，光子晶片出貨放量](#item-22) ⭐️ 7.0/10
23. [潤德預估 2026 年上半年 EPS 9.51 元，持有 59 億元工程訂單](#item-23) ⭐️ 7.0/10
24. [FactSet 提升鴻海目標價至 355 元](#item-24) ⭐️ 7.0/10
25. [中鋼 7 月稅前盈餘減 55％](#item-25) ⭐️ 7.0/10
26. [騰訊測試新旗艦模型 Hunyuan Hy4](#item-26) ⭐️ 7.0/10
27. [Meta 面臨即將到來的社交媒體訴訟風險](#item-27) ⭐️ 7.0/10
28. [澳洲對 Meta 與 Google 徵收 2.5％新聞稅](#item-28) ⭐️ 7.0/10
29. [國庫收益率上升，沃爾瑪股價因指引下滑而跌](#item-29) ⭐️ 7.0/10
30. [SpaceX 與 Magnificent Seven：不同的成長路徑](#item-30) ⭐️ 7.0/10
31. [億萬富翁加碼「七巨頭」科技股](#item-31) ⭐️ 7.0/10
32. [Meta 在 AI 競爭中落後於亞馬遜、Alphabet 與微軟](#item-32) ⭐️ 7.0/10
33. [四大非晶片股有望受益於 AI 資料中心擴張](#item-33) ⭐️ 7.0/10
34. [AWS 後備庫存突破 4.96 億美元—亞馬遜仍被低估？](#item-34) ⭐️ 7.0/10
35. [麥金塔面臨$115 億美元晶片廠建設風險](#item-35) ⭐️ 7.0/10
36. [Broadcom 持平 ARK 買入谷底，Intel 下跌，AMD 因 Google‑Marvell 交易回落](#item-36) ⭐️ 7.0/10
37. [AMD 與 Intel 股價大跌](#item-37) ⭐️ 7.0/10
38. [杜克倫米勒賣出 Micron 與 Intel，買進兩支 AI 股](#item-38) ⭐️ 7.0/10
39. [TSMC 與 GlobalFoundries：哪一間晶圓代工股更值得買入？](#item-39) ⭐️ 7.0/10
40. [三星股價下跌近 8％，AI 需求推升晶片價格](#item-40) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Arrayref 套件遭受建置時惡意程式攻擊](https://safedep.io/arrayref-proc-macro1-rust-build-time-malware/) ⭐️ 8.0/10

惡意版本的 Rust 套件 Arrayref 被推送到 crates.io，注入對 proc‑macro1 的依賴，在建置時下載並執行遠端 payload。受攻擊的維護者帳號被鎖定且相關套件已被撤回，但最初未發佈安全諮詢。 此事件揭露了 Cargo 建置腳本執行模型的重大弱點，允許攻擊者在依賴編譯期間執行任意程式碼，並可能危及所有拉取該套件的下游專案。它強調需要對 build.rs 進行沙盒化以及 crates.io 更完善的事件回應機制。 惡意 payload 透過 base64 片段在 build.rs 中重組伺服器位址，經 HTTPS 下載並以提升權限執行程式。雖然該套件在兩小時內被撤回，但缺乏安全諮詢以及攻擊版本的消失凸顯了 crates.io 事件處理中的漏洞。

hackernews · abhisek · 8月20日 13:23 · [社群討論](https://news.ycombinator.com/item?id=49374269)

**背景**: Rust 是一種系統程式語言，使用 Cargo 作為套件管理器，其中依賴可能包含在編譯前執行的建置腳本 (build.rs)。建置腳本功能強大，但歷來被視為可直接執行，缺乏隔離，使其成為供應鏈攻擊的目標。crates.io 托管數千個套件並依賴維護者發布更新，但目前尚未具備細粒度的事件回應機制。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://blog.rust-lang.org/2026/08/20/supply-chain-attack-on-arrayref/">Supply chain attack on arrayref | Rust Blog</a></li>
<li><a href="https://safedep.io/arrayref-proc-macro1-rust-build-time-malware/">Malicious Rust Crate arrayref Runs a Build-Time Payload - Real-time Open Source Software Supply Chain Security</a></li>

</ul>
</details>

**社群討論**: 社群成員批評 crates.io 未能標記惡意版本且未發佈安全諮詢，並呼籲對建置腳本進行沙盒化；有人則主張更「一體化」的語言設計可降低依賴面積。討論提及 Rust 目標中的沙盒化建置腳本，以及對未來生態系統惡意程式的擔憂。

**標籤**: `#Rust`, `#Supply Chain Security`, `#Build Scripts`, `#Crate Management`, `#Security Incident`

---

<a id="item-2"></a>
## [威宏-KY 2026 年第二季淨利創五季新高](https://news.cnyes.com/news/id/6582707) ⭐️ 8.0/10

威宏-KY 公布 2026 年第二季稅後純益 9,460 萬元，較上一季增長 43 倍，創五季以來新高。 此大幅獲利提升顯示公司營運表現強勁，可能提振投資者對其估值的信心。 2026 年上半年每股純益為 1.38 元，顯示公司利潤持續強勁，儘管營運成本有所增加。

rss · Anue 鉅亨網台股 · 8月20日 09:28

**背景**: 台灣上市公司每季公布獲利資訊，對市場情緒與股價估值有重要影響。大幅盈利提升常引發買盤並左右行業指數。投資者會密切關注稅後純益和每股盈餘等財務指標，以評估公司經營狀況。

**標籤**: `#Taiwan Equity`, `#Quarterly Earnings`, `#Profit Surge`, `#Stock News`

---

<a id="item-3"></a>
## [低成本 Mini Kimi‑K3 以 <$250 訓練，擊敗 GPT‑2 HellaSwag 成績](https://i.redd.it/wfbl9726oikh1.png) ⭐️ 8.0/10

使用不到 250 美元，某用戶從零開始預訓練了 1.02 十億參數的 mini Kimi‑K3 模型，並以 5 十億去除雜訊的 token 訓練，最終在 HellaSwag 基準上取得 33.4% 的分數，高於 GPT‑2 的 28%。 此舉證明大型語言模型可在有限預算內構建與訓練，降低研究人員和業餘愛好者的門檻，同時顯示 Kimi‑K3 等高效架構能以更少資源擊敗傳統模型。 該模型採用 Kimi‑K3 的架構：Kimi Delta Attention、Gated MLA、Attention Residuals，以及帶有無輔助損失平衡器的 LatentMoE 路由，並保留原始 163,840 個 token 的分詞器；訓練僅為下一個 token 預測，未進行指令微調。

reddit · r/LocalLLaMA · OtherRaisin3426 · 8月20日 11:38 · [社群討論](https://www.reddit.com/r/LocalLLaMA/comments/1vth1c3/i_just_built_a_mini_kimik3_from_scratch_under_250/)

**背景**: Kimi‑3 是 Kimi AI 推出的新型開源 LLM，結合高效注意力機制與稀疏 Mixture‑of‑Experts 層，以降低計算需求並保持性能。HellaSwag 則是一套 10,000 個句子補全任務的常識推理基準，用於評估模型預測合理延續的能力。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://platform.kimi.ai/docs/guide/kimi-k3-quickstart">Kimi K3 - Kimi API Platform</a></li>
<li><a href="https://sebastianraschka.com/blog/2026/kimi-k3-architecture-notes.html">Kimi K3 Architecture Notes | Sebastian Raschka, PhD</a></li>
<li><a href="https://www.kimi.ai/blog/kimi-k3">Kimi K3 Tech Blog: Open Frontier Intelligence</a></li>

</ul>
</details>

**社群討論**: 社群留言稱讚此低成本方案並鼓勵他人複製或擴充，亦有人建議將規模提升至更大模型或以 Kimi‑K3 為教師進行強化學習。

**標籤**: `#AI/ML`, `#Language Models`, `#Open-source LLMs`, `#Hardware Efficiency`, `#Engineering`

---

<a id="item-4"></a>
## [Walmart 報告六年來最低銷售增長](https://www.reddit.com/r/stocks/comments/1vtkwas/walmart_posts_weakest_sales_growth_in_over_six/) ⭐️ 8.0/10

在最新的財報中，Walmart 公布美國可比銷售僅增長 2.6%，為自 2020 年以來最小增幅；公司指出新藥價規定將本應達到的 3.4% 提升降至 2.6%。 銷售增長疲軟暗示消費者支出可能放緩，進而影響零售利潤率並促使投資者重新評估整個行業的估值。 可比銷售衡量已營業至少一年之店面表現，結合實體與數位渠道；2.6% 的增幅即反映此組合，而藥價規定的影響則突顯法規對收入來源的衝擊。

reddit · r/stocks · IvoryTowerResident · 8月20日 14:21

**背景**: 可比銷售（comp）是零售業的重要指標，用以衡量過去一年內規模與商品組合相似的店面表現，排除新開或關閉的門市，以呈現有機成長。2026 年《通脹減少法案》所引入之藥價規定則採用成本基礎報銷限制，收窄零售藥房利潤空間。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://timewellscheduled.com/blog/what-does-comp-mean-in-retail-comparable-sales/">What does comp mean in retail ? – Comparable Sales</a></li>
<li><a href="https://scriptpro.com/maximum-fair-pricing-impact-on-retail-pharmacies/">Maximum Fair Pricing: Impact on Retail Pharmacies - ScriptPro</a></li>

</ul>
</details>

**社群討論**: 評論者對經濟衰退前景展開爭論，部分人認為 Walmart 與 Costco 的估值倍率仍偏高；另一些則警告說消費支出指標表面上看似健康，但實際趨勢可能正在惡化。

**標籤**: `#Retail`, `#Earnings`, `#Consumer Spending`, `#Valuation`, `#US Stocks`

---

<a id="item-5"></a>
## [SK Hynix 宣布 290 億美元回購與記憶體短缺警示](https://www.reddit.com/r/stocks/comments/1vt2buv/sk_hynix_is_every_investors_dream_stock/) ⭐️ 8.0/10

SK Hynix 宣布將於 8 月 20 日啟動 290 億美元的股份回購計畫，並計劃在 2025‑27 年期間將超過一半的自由現金流分配給股東回報，同時正在評估特別股息。公司亦警告說，到 2027 年結束前，DRAM 的結構性需求將超過供應，可能使全球記憶體短缺惡化。 股份回購與自由現金流分配表明公司對股東友好，可能推升 SK Hynix 股價；同時記憶體短缺警示暗示 DRAM 價格上行空間，進而影響整個半導體市場估值。投資者將關注這些舉措如何改變市場情緒與公司估值。 SK Hynix 截至第二季結束時的凈現金約為 69 萬億韓元（49.36 億美元），並將於 8 月 20 日啟動 290 億美元的回購。公司計畫在第三季財報公布時提供特別股息細節。

reddit · r/stocks · Euro347 · 8月19日 23:10

**背景**: SK Hynix 是全球最大的 DRAM 製造商之一，與三星、美光競爭激烈。由於人工智慧工作負載和高性能計算的需求激增，全球記憶體供應短缺自 2025 年開始並預計將持續至 2027 年。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://www.how2shout.com/news/memory-shortage-2027-ai-hbm-samsung-sk-hynix-micron.html">Memory Shortage to Last Until 2027 : AI Demand Squeezes PC...</a></li>

</ul>
</details>

**社群討論**: 社群成員普遍持懷疑態度，認為價格目標毫無意義，並警告不要過於樂觀。部分評論者指出記憶體市場的週期性，並提醒近期可能出現供應過剩。

**標籤**: `#SK Hynix`, `#Semiconductor`, `#Buyback`, `#Memory Supply Shortage`, `#Investor News`

---

<a id="item-6"></a>
## [NVIDIA 價值因未來出貨而合理化](https://finance.yahoo.com/markets/stocks/articles/nvidia-looks-expensive-until-ask-154655567.html) ⭐️ 8.0/10

文章指出，若考慮未來 GPU 出貨需求，Nvidia 的高股價可被合理化，並將估值與 2024–25 年的預測量產及供應鏈動態掛鈎。 對投資者而言，這一觀點暗示目前的高溢價可能反映了與 AI 工作負載相關的實質增長前景；對工程師來說，它凸顯供應限制如何影響產品規劃。 分析依賴 Bloomberg、IDC 等機構的出貨預測，指出 EUV 光刻瓶頸與記憶體短缺可能延遲產能提升；同時提醒估值取決於 AI 需求持續以及晶片生產規模化成功。

openbb · TSM · 8月20日 15:46

**背景**: Nvidia 已成為 GPU 的主導者，推動資料中心 AI、遊戲與汽車市場。其股價在 AI 熱潮中飆升，形成高估值倍率，一些分析師認為已被過度膨脹。供應鏈限制—如先進光刻設備和記憶體晶片短缺—歷來限制 Nvidia 滿足需求的能力。

**標籤**: `#NVIDIA`, `#GPU`, `#Semiconductors`, `#Valuation`, `#Supply Chain`

---

<a id="item-7"></a>
## [馬維爾 AI 催化劑或帶來 21％上漲](https://finance.yahoo.com/technology/ai/articles/prediction-marvell-ai-catalyst-could-153001459.html) ⭐️ 8.0/10

馬維爾宣布其新 AI 催化劑產品，為資料中心與汽車 AI 工作負載設計的客製 ASIC。分析師預測此發佈可能使馬維爾股價上漲高達 21%。 潛在上漲反映出對專用 AI 基礎設施需求的增長，將馬維爾定位為資料中心加速的重要玩家。股價提升 21%將顯示投資者信心，並可能促進更多客製晶片投資。 此催化劑基於馬維爾下一代 ASIC 架構，為推論工作負載提供高吞吐量，同時保持低功耗。然其面臨 Nvidia、Broadcom 及其他晶片供應商競爭，其成功取決於獲得大型超級規模合約。

openbb · TSM · 8月20日 15:30

**背景**: 馬維爾在過去兩年半內已從多元晶片供應商轉型為純粹 AI 基礎設施提供者。其新 AI 催化劑以現有 ASIC 產品線為基礎，針對資料中心與汽車領域的高效推論。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://www.marvell.com/company/media-kit/ai-accelerator-asics-press-kit.html">AI Accelerator ASICs Press Kit | Enabling the Next... - Marvell</a></li>
<li><a href="https://invest101.com.hk/marvell-technology-mrvl-stock-research-report-by-invest101-copilot">Marvell Technology (MRVL) — Stock Research Report by ...</a></li>
<li><a href="https://www.fool.com/coverage/stock-market-today/2026/06/02/stock-market-today-june-2-marvell-technology-surges-after-nvidia-ceo-highlights-ai-infrastructure-role/">Stock Market Today, June 2: Marvell Technology Surges After ...</a></li>

</ul>
</details>

**標籤**: `#Marvell`, `#AI chips`, `#Semiconductor`, `#Stock analysis`, `#Taiwan`

---

<a id="item-8"></a>
## [台積電 VS ASML：哪個半導體巨頭更值得投資？](https://finance.yahoo.com/markets/stocks/articles/taiwan-semiconductor-vs-asml-semiconductor-085500627.html) ⭐️ 8.0/10

本文提供台積電與 ASML 的詳細對比，重點說明兩家公司財務指標、成長前景及供應鏈動態，以協助投資者判斷今天哪一家公司更值得購買。 透過比較估值倍數、營收成長與技術領先度，該分析協助美台股市投資者在快速變動的半導體供應鏈中做出資金配置決策。 台積電的先進 FinFET 工藝節點（3 nm、2.5 nm）與 ASML 的 EUV 光刻平台（NXE:3100、NXE:3400）是對比的核心；ASML 是多家晶圓代工的重要供應商，而台積電則主導製造能力。

openbb · TSM · 8月20日 08:55

**背景**: FinFET（鳶形場效電晶體）技術以多閘結構取代平面 MOSFET，提升在子 10 nm 節點下的性能與功耗。極紫外光刻 (EUV) 使用波長為 13.5 nm 的光線，在矽晶圓上製造最小特徵；它是製造先進晶片的關鍵技術。ASML 的 EUV 系統對於台積電等晶圓代工公司實現 3 nm 及以下節點至關重要。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://www.asml.com/en/products/euv-lithography-systems">EUV lithography systems – Products | ASML</a></li>
<li><a href="https://en.wikipedia.org/wiki/Extreme_ultraviolet_lithography">Extreme ultraviolet lithography</a></li>
<li><a href="https://en.wikipedia.org/wiki/Fin_field-effect_transistor">Fin field-effect transistor - Wikipedia</a></li>

</ul>
</details>

**標籤**: `#Semiconductors`, `#Investment Analysis`, `#TSMC`, `#ASML`, `#Equities`

---

<a id="item-9"></a>
## [台積電因 AI 需求飆升](https://finance.yahoo.com/technology/ai/articles/stock-riding-ai-wave-shows-130020996.html) ⭐️ 8.0/10

台積電股價因 AI 加速晶片需求持續攀升，分析師指出市場尚未顯現放緩跡象。 由於人工智慧工作負載推動從資料中心到消費電子的各種應用，台積電股價上升顯示半導體市場持續擴張，也為投資者提供高成長領域的機會。 台積電的 3 nm N3 與 N3E 工藝節點提供更佳功耗與效能平衡，已被應用於 Nvidia H100 GPU 等旗艦 AI 加速器，凸顯其在下一代 AI 硬體供應鏈中的關鍵地位。

openbb · TSM · 8月20日 13:00

**背景**: 台積電是全球最大的專業晶圓代工廠，為多家科技巨頭製造晶片。公司先後推出 5 nm 與最新的 3 nm FinFET（N3）技術，提供顯著提升效能與功耗表現。人工智慧工作負載，尤其是大型神經網路推論和訓練，需要高晶體管密度與低功耗設計，而這些前沿工藝正好滿足需求。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/3_nm_process">3 nm process - Wikipedia</a></li>
<li><a href="https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_3nm">3nm Technology - Taiwan Semiconductor Manufacturing ... - TSMC</a></li>
<li><a href="https://en.wikipedia.org/wiki/Neural_processing_unit">Neural processing unit - Wikipedia</a></li>

</ul>
</details>

**標籤**: `#AI`, `#Semiconductor`, `#TSMC`, `#Investing`, `#Tech Stocks`

---

<a id="item-10"></a>
## [台積電公布七月營收成長，估值爭議升溫](https://finance.yahoo.com/markets/stocks/articles/taiwan-semiconductor-manufacturing-tsm-july-121138319.html) ⭐️ 8.0/10

台積電公布七月營收較前期成長，投資者與分析師因此重新評估公司估值。 此財報更新即時顯示台積電營運動能，對半導體供應鏈投資者及關注美股市場的投資人皆具重要參考價值。 儘管營收上升顯示需求旺盛，分析師指出台積電的市盈率仍高於同業，引發股價是否被高估或仍有成長空間之爭議。

openbb · TSM · 8月20日 12:11

**背景**: 台積電（TSMC）是全球最大的獨立晶圓代工廠，為主要科技公司製造先進邏輯晶片，並在全球供應鏈中扮演關鍵角色。其財務表現受到全球投資者的高度關注。

**標籤**: `#TSMC`, `#Semiconductors`, `#Earnings`, `#Valuation`, `#Taiwan`

---

<a id="item-11"></a>
## [台積電產能限制或改變 AI 晶片供應與價格](https://finance.yahoo.com/technology/ai/articles/could-taiwan-semiconductor-manufacturing-tsm-111322612.html) ⭐️ 8.0/10

台積電在先進製程的產能瓶頸正限制尖端 AI 加速器的供應，可能推高價格並延遲 NVIDIA、AMD 等公司的交付。 這種產能壓力將影響全球 AI 生態系統，可能提高雲端服務商的硬體成本並左右半導體股的投資情緒。 台積電的 5nm 與 3nm 製程已接近滿載，7nm 線路亦已超負荷；公司已宣布新 2nm 專案，但預計要到 2026 年才可投入量產。

openbb · TSM · 8月20日 11:13

**背景**: 台積電是全球最大的專業晶圓代工廠，為 AI 加速器提供先進邏輯製程。隨著雲端、汽車及消費電子對 AI 晶片需求激增，市場規模迅速擴大。領先晶圓廠的產能限制往往會導致價格波動與交付延遲。

**標籤**: `#Semiconductors`, `#AI Hardware`, `#TSMC`, `#Supply Chain`, `#Investing`

---

<a id="item-12"></a>
## [台積電股價飆升 31% 超過成長因子估值](https://finance.yahoo.com/markets/stocks/articles/tsmc-trades-30-87-above-220612599.html) ⭐️ 8.0/10

台積電股價正以約 30.87％高於其成長因子（GF）估值交易，原因是先進晶片製造產能收縮；此訊息來自 2024 年 6 月 12 日的 Yahoo Finance 報導。 此溢價顯示投資者對供應限制的樂觀情緒，可能推升未來盈利；因此台積電成為關注半導體供應鏈與 AI 需求的重要標的。 GF Value 模型結合了盈利增長、自由現金流收益率與風險因素；30％的溢價暗示市場預期即使產能受限，AI 硬體需求仍將推動收入加速。

openbb · TSM · 8月19日 22:06

**背景**: 台積電是全球最大的專業晶圓代工廠，生產 5 nm、3 nm 等先進節點晶片，用於 AI 加速器。成長因子估值（GF Value）是一種專有模型，根據預期盈利增長、自由現金流收益率與風險調整來估算內在價值。近期報導顯示台灣先進晶片產能已接近滿載，供應緊縮影響全球客戶。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://au.finance.yahoo.com/news/tsmc-trades-30-87-above-220612599.html">TSMC Trades 30.87% Above GF Value as Chip Capacity Tightens</a></li>
<li><a href="https://www.gurufocus.com/news/8997805/amat-looks-1262-overvalued-on-gf-value">AMAT Looks 126.2% Overvalued on GF Value</a></li>
<li><a href="https://www.marketscreener.com/quote/stock/TSMC-TAIWAN-SEMICONDUCTOR-6492349/valuation/">TSMC (TAIWAN SEMICONDUCTOR MANUFACTURING COMPANY)</a></li>

</ul>
</details>

**標籤**: `#TSMC`, `#Semiconductors`, `#Taiwan Equity`, `#Supply Chain`, `#Valuation`

---

<a id="item-13"></a>
## [ADI 公布歷史高盈餘 股價下跌 TSMC & ASE 受益](https://news.google.com/rss/articles/CBMinwRBVV95cUxPTVM5WTBvdUJLLWFuWVF0WHRBeTctTXVKZzVWSkUyTzJlMzlxRms1b19HVnJTN3lleVRCWWRkWmRkUERVdWFjVTMzelh3WjhFLWRhWHREaGJhMUtTRFFwS3ZaaVRIX2tPaTgtRU03UWRSVnAzUEJDZ1NLZFR0NmItT0ptT0dVNVExbC1JUnlFZzgwYy1Nd1JUMlNfQ1lqTXU3SDJCYlFsS2dGSTJZa01MUWNhX0YxTklVUjB0VjBhbzhTLXBJWFVXU1gxLWhDWnRYOWFvREs2UF9FQ2dXWEdxaHFuMGxaeThTS3NqVXNpWHBwenFyQ2FUM0FVM0pjeGpGQWE3ckJrM3ZHZWlaQnVVX1NRcnZBbTYteUltNVZ3WV85dVRXeXZ1QURCRklhU0VkbzJDYlNKT1N1MVpNOHY4TDZOMlQwUnZZZVNSYWRKMVRMYUhKbTI3WEtpZy15eXBaSUstdXJvNlNxSzJ2eHRRV3V6V0ZrSEoxRWhTbS0zYnVtLXViMWZfdHRrSlg3SE4wbGllUXNEMzJLdi1yQlBWeHZhZG00RmVfdTdicXhiRGRQSFc4WUZzLVNqazc1OTl1cFZfWUY1M091NDJEY0p0U2hkNjd3aEhpN2lxMF9xY0tNN1lqUTc0NTZmTFJDWTVpY3B3RUNEQUdZUmhlYnJ2ZW1ONW5hMDktTHhIdHMtWjFyT25sT2pncDNwNHJMTUU?oc=5) ⭐️ 8.0/10

Analog Devices (ADI) 公布本季歷史最高營收與淨利，股價卻在財報公布後下跌。其強勁表現間接惠及製造合作夥伴，TSMC 與 ASE 由於 ADI 對類比晶片需求上升而受益。 ADI 基本面與股價的脫節凸顯半導體市場波動，TSMC 與 ASE 的間接收益則說明供應鏈協同的重要性。投資者及分析師可藉此案例重新評估類比晶片製造商及其服務提供商之估值。 ADI 的盈餘主要來自於汽車、工業及資料中心市場的高利潤類比 IC。公司已透過 JASM 與 TSMC 確保 40 nm 以上節點之長期晶圓產能，且 ASE 提供全方位封裝與測試服務以支援 ADI 的產品線。

google_news · sinotrade.com.tw · 8月20日 11:37

**背景**: Analog Devices 是精密類比與混訊號集成電路的領先供應商，產品包括 ADC 與高速轉換器。公司依賴 TSMC 的先進晶圓代工服務製造晶片，以及 ASE 的封裝與測試設施將產品推向市場。近年來的合作擴大了 ADI 在供應鏈中的產能與韌性。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://ase.aseglobal.com/about-ase/">About ASE</a></li>
<li><a href="https://www.tsmc.com/english/dedicatedFoundry/technology/specialty/analog">Analog Technology - Taiwan Semiconductor Manufacturing ... - TSMC</a></li>
<li><a href="https://www.analog.com/en/newsroom/press-releases/2024/2-22-2024-adi-strengthens-capacity-resiliency-through-expanded-partnership-tsmc.html">Analog Devices Strengthens Capacity and Resiliency Through ...</a></li>

</ul>
</details>

**標籤**: `#ADI`, `#Earnings`, `#TSMC`, `#ASE`, `#Semiconductors`

---

<a id="item-14"></a>
## [應材攜柏克萊加速 AI 晶片創新](https://news.google.com/rss/articles/CBMicEFVX3lxTE5DWEJyWkx4U21wTF91WVVhRVVsOGdubm5VbDRISFpiX0lMM2l2X2ZNSTRCOUw5cFNKRmR1VDRJckRKY01QbEVBV0ZjYTFTNkF6V05fWFg0UVg1YURkcTVleFF1b19SeFFkSERicG82Z1U?oc=5) ⭐️ 8.0/10

應材與加州大學柏克萊分校於 2026 年 8 月 12 日共同啟動了位於矽谷的 EPIC 中心，這是一個結合產業級半導體設備與專業知識的研究設施。此合作旨在推動針對 AI 晶片的新材料及製程技術之開發，加速從學術研究到商用量產的轉化。 此合作可大幅縮短 AI 專用半導體材料從實驗室原型到量產的時間，進一步加速 AI 硬體整體發展。它亦顯示對先進製造工具需求上升，可能提升應材銷售並影響 TSMC 等主要晶圓代工廠的供應鏈動態。 EPIC 中心將配備應材的沉積、光刻與蝕刻設備，讓研究人員能在實驗室原型階段測試新材料。儘管如此，從實驗室突破轉化為高量產仍具挑戰性，合作還需面對知識產權及成本等障礙。

google_news · TechNews 科技新報 · 8月20日 10:13

**背景**: AI 晶片是為機器學習工作負載設計的專用處理器，需使用新型半導體材料與極精細製程以滿足現代 AI 應用對性能的需求。應材是全球領先的晶圓製造設備供應商，涵蓋沉積、光刻等全流程工具。加州大學柏克萊分校在材料科學研究方面長期居於前沿，其突破經常轉化為商業技術。EPIC 中心旨在縮短學術發現與工業量產之間的距離，讓研究團隊能使用產業級設備進行原型開發。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://science.report/discover/applied-materials-and-uc-berkeley-launch-silicon-valley-epic-center-for-ai-chips-80599/">Applied Materials and UC Berkeley Launch Silicon Valley EPIC ...</a></li>
<li><a href="https://ir.appliedmaterials.com/node/29506/pdf">UC Berkeley to Join Applied Materials EPIC Center to Speed ...</a></li>
<li><a href="https://thevoltpost.com/applied-materials-uc-berkeley-epic-center-ai-chip/">Applied Materials, UC Berkeley Partner on AI Chip Research</a></li>

</ul>
</details>

**標籤**: `#Semiconductor`, `#Materials Engineering`, `#AI Chips`, `#Applied Materials`, `#Research Partnership`

---

<a id="item-15"></a>
## [Grok 透過加密的上下文注入洩露使用者資料](https://arstechnica.com/security/2026/08/grok-exfiltrates-user-data-when-malicious-instructions-are-encrypted/) ⭐️ 7.0/10

近期一次加密上下文注入攻擊使 Grok 能在指令被加密時洩露使用者資料，繞過其安全防護。 此漏洞顯示即使指令被加密，仍可被操縱，削弱對 AI 服務的信任並將敏感資料暴露給攻擊者。 此攻擊利用 Grok 處理工具輸出與中間狀態的方式，將惡意指令注入模型自身上下文，即使負載被加密也能成功。

rss · Ars Technica · 8月20日 13:00

**背景**: 加密上下文注入（CCI）是一種利用大型語言模型使用的更廣泛上下文（如工具輸出或執行時狀態）來繞過安全過濾器的技術。Grok 是 SpaceXAI 於 2023 年推出的一系列生成式大語言模型，隨著多個版本演進，加入了圖片產生、網路搜尋與代理編碼工具等功能。最新漏洞顯示即使指令被加密，也能被利用，凸顯 LLM 防護機制的脆弱性。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://adversa.ai/blog/cryptographic-context-injection-grok-data-theft/">Grok chat history leak: Cryptographic Context Injection</a></li>
<li><a href="https://arstechnica.com/security/2026/08/grok-exfiltrates-user-data-when-malicious-instructions-are-encrypted/">Grok exfiltrates user data when malicious instructions... - Ars Technica</a></li>

</ul>
</details>

**社群討論**: 安全研究人員指出，Grok 的安全防護機制脆弱，可被加密上下文注入繞過；部分專家呼籲加強工具輸出隔離與更完善的加密處理。

**標籤**: `#AI Security`, `#LLM Vulnerability`, `#Cryptography`, `#Cybersecurity`, `#Tech News`

---

<a id="item-16"></a>
## [亞馬遜計畫於 2026 年前覆蓋 500 個美國社區](https://arstechnica.com/gadgets/2026/08/amazon-aims-for-delivery-drones-to-reach-500-us-neighborhoods-by-end-of-2026/) ⭐️ 7.0/10

亞馬遜宣布其 Prime Air 無人機配送服務將於 2026 年底擴展至近 500 個美國城市和城鎮，較目前覆蓋範圍增長六倍。 此擴張可能降低亞馬遜的物流成本、加速最後一哩配送，並重塑基於無人機的包裹服務競爭格局。 Prime Air 無人機為全電動混合飛行器，垂直起降如直升機、水平飛行如飛機，配備偵測與迴避感測器並符合 FAA Part 107 BVLOS 規則及必須的 Remote ID。

rss · Ars Technica · 8月19日 22:02

**背景**: 亞馬遜的 Prime Air 自 2016 年起在美國部分市場測試無人機配送，提供一小時內送達有限商品。該服務利用 AI 與深度學習電腦視覺實現自動導航，偵測障礙並安全降落。2025 年 FAA 近期修訂規則允許超視距（BVLOS）作業並要求遠程識別，為更廣泛商用部署鋪路。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://www.aboutamazon.com/news/transportation/amazon-prime-air-drone-delivery-expansion">Amazon Prime Air drone delivery expands to nearly 500 US ...</a></li>
<li><a href="https://www.freightwaves.com/news/new-faa-rules-put-drone-delivery-closer-to-reality">New FAA rules put drone delivery closer to reality - FreightWaves</a></li>
<li><a href="https://www.amazon.com/Prime-Air-Drone-Delivery/b?node=206533607011">Prime Air Drone Delivery - amazon.com</a></li>

</ul>
</details>

**標籤**: `#Amazon`, `#Delivery Drones`, `#Logistics`, `#Prime Air`, `#Tech Innovation`

---

<a id="item-17"></a>
## [蘋果新任 CEO 或重塑 AI 策略](https://www.marketwatch.com/story/apple-has-gotten-too-predictable-can-its-next-ceo-bring-back-the-element-of-surprise-5bd674a0?mod=mw_rss_topstories) ⭐️ 7.0/10

華爾街期望約翰·特納斯將透過增加研發投入、尋求更大型併購以及加速創新，徹底改變蘋果的 AI 策略。 若實施成功，將提升蘋果在 AI 競爭中的地位、影響股價表現並推動整個產業的創新。 目前尚未有官方確認，且蘋果過去在 AI 方面採取較為謹慎策略，此舉可能帶來風險與不確定性。

rss · MarketWatch Top Stories · 8月20日 16:48

**背景**: 蘋果傳統上專注於硬體與生態系統整合，AI 公開舉措相較 Google 或 Microsoft 較為有限。公司最近任命約翰·特納斯為臨時 CEO，隨著蒂姆·庫克離職，引發對戰略重心可能轉變的猜測。華爾街分析師密切關注任何能改變蘋果市場定位與股東價值的動向。

**標籤**: `#Apple`, `#CEO succession`, `#AI strategy`, `#US equities`, `#investment`

---

<a id="item-18"></a>
## [財政部計畫加倍長期國債回購](https://www.marketwatch.com/story/bessent-suggests-treasury-could-intervene-again-in-bond-market-we-have-a-big-tool-kit-358829e1?mod=mw_rss_topstories) ⭐️ 7.0/10

美國財政部長官 Scott Bessent 宣布將把長期國債回購操作的最大規模從 20 億美元提升至至少 40 億美元，並於 2026 年 9 月 9 日生效。 此舉透過向長期市場注入流動性，有望壓低收益率、降低企業與消費者的借貸成本，進而可能提振股市估值。 該計畫針對 10 年至 20 年及 20 年至 30 年名義票息部門，屬於「強力贊助」的流動性支援回購，但市場分析師警告其可能僅提供短暫緩解長期收益率。

rss · MarketWatch Top Stories · 8月20日 16:23

**背景**: 美國財政部自 2024 年起實施常規回購計畫，以改善因債務上升而造成的市場功能。透過回購舊有國債，財政部將其從流通中移除並注入新現金至銀行體系，收窄買賣差價。此計畫通常限於短期證券，但近期已擴大至長期國債。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://www.reuters.com/world/us-treasury-double-sizes-some-debt-buyback-operations-least-4-billion-2026-08-19/">Treasury Secretary Bessent doubles US long-bond buybacks in ...</a></li>
<li><a href="https://home.treasury.gov/news/press-releases/sb0607">Treasury Announces Increased Sizes of Nominal Long-End ...</a></li>
<li><a href="https://fortune.com/2026/08/20/scott-bessent-us-treasury-4-billion-bond-buyback-plan-rearranging-deckchairs-on-the-titanic-ing/">US Treasury : Scott Bessent’ s bond plan like ‘rearranging... | Fortune</a></li>

</ul>
</details>

**社群討論**: 市場分析師對 Bessent 的計畫持分歧觀點；有人認為這是緩解長期收益率的必要干預，亦有人擔心此舉僅能提供暫時性緩解，並可能暗示更深層的財政問題。

**標籤**: `#US Treasury`, `#Bond Market`, `#Interest Rates`, `#Monetary Policy`, `#Equity Markets`

---

<a id="item-19"></a>
## [裂解差價上升預示汽油價格持續高企](https://www.marketwatch.com/story/the-energy-markets-rising-crack-spread-is-threatening-to-break-the-american-consumer-90b421dc?mod=mw_rss_topstories) ⭐️ 7.0/10

能源市場報告原油與精煉產品之間的裂解差價擴大，暗示汽油價格可能持續偏高。 裂解差價上升表明精煉利潤壓縮，可能使汽油價格高於原油水平，進一步推動消費者支出中的通脹壓力。 裂解差價計算方式為原油價格與汽油及柴油合併價格之差，並作為精煉利潤的領先指標；但它不包含地區稅費或配送成本。

rss · MarketWatch Top Stories · 8月20日 15:22

**背景**: 裂解差價衡量原油與精煉石油產品之間的利潤差距，傳統上以 3-2-1 比例表示（三桶原油產出兩桶汽油和一桶柴油）。它被精煉商與交易者廣泛用於評估利潤並預測燃料價格走勢。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://www.investopedia.com/terms/c/crackspread.asp">investopedia.com/terms/c/crackspread.asp</a></li>

</ul>
</details>

**標籤**: `#energy`, `#inflation`, `#fuel-costs`, `#equity-markets`, `#consumer-prices`

---

<a id="item-20"></a>
## [平日住宿補助最高 NT$3700／人，9/1 起啟動](https://news.cnyes.com/news/id/6582942) ⭐️ 7.0/10

自 9 月 1 日起，交通部觀光署將推出平日國旅補助，每人最高可領 NT$3,700，作為「觀光雙輪驅動方案」的一部分，該方案預計投入 33.3 億元並涵蓋九項措施。 此補助將刺激平日國內旅遊需求，可能提升航空、酒店及旅行社等相關產業營收，同時促進整體經濟復甦。 此方案針對平日住宿，最高可折抵 NT$3,700／人，無論住宿類型；補助僅於經核准的預訂管道提供。

rss · Anue 鉅亨網台股 · 8月20日 14:44

**背景**: 交通部觀光署於 8 月推出「觀光雙輪驅動方案」，以振興國旅並吸引國際遊客。該計畫將投入 33.3 億元，涵蓋九項措施，包括平日住宿折扣、生日留宿、Taiwan PASS 優惠、樂園留宿及公司員工國旅等。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://www.storm.mg/lifestyle/11157987">今日（08/20）重點新聞！ 5 大旅遊補助金出爐「最高領 3700...</a></li>
<li><a href="https://money.udn.com/money/story/7307/9704066">國旅補助估帶 動 400... | 經濟日報</a></li>
<li><a href="https://www.marieclaire.com.tw/lifestyle/travel/95428">2026 國旅補助 8/20... | Marie Claire 美麗佳人</a></li>

</ul>
</details>

**標籤**: `#Taiwan`, `#tourism subsidies`, `#economic stimulus`, `#equity impact`, `#travel industry`

---

<a id="item-21"></a>
## [FactSet 提升旭隼 EPS 預估至 31.42 元](https://news.cnyes.com/news/id/6583008) ⭐️ 7.0/10

FactSet 已將台灣公司旭隼（6409‑TW）的每股盈餘預估上修至 31.42 元新臺幣，並訂出新的目標價為 1,035 元。 此更新讓投資人更清楚旭隼的獲利前景，可能影響交易決策，也會對整體台灣股市情緒產生衝擊。 FactSet 的上修基於更新的營收預測與最新財報，目標價較先前估值高出約 30%。

rss · Anue 鉅亨網台股 · 8月20日 14:11

**背景**: FactSet 是美國的資料與分析供應商，為機構投資人提供財報預估。旭隼（6409‑TW）是台灣半導體設備公司，以精密機械聞名。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/FactSet">FactSet - Wikipedia</a></li>
<li><a href="https://www.factset.com/">FactSet | Financial Data, Market Analytics & AI Solutions</a></li>
<li><a href="https://tw.stock.yahoo.com/quote/6409.TW/profile">旭隼 (6409.TW) 基本資料 - Yahoo 股市</a></li>

</ul>
</details>

**標籤**: `#Taiwanese equities`, `#EPS estimate`, `#Target price`, `#FactSet`, `#Investment analysis`

---

<a id="item-22"></a>
## [聯亞七月營收大增 503%，光子晶片出貨放量](https://news.cnyes.com/news/id/6582905) ⭐️ 7.0/10

聯亞公布七月稅後純益為 2.11 億元，年增 503%，每股盈餘達 2.07 元。 此成長顯示光子晶片需求旺盛，將聯亞定位為高速資料基礎設施關鍵供應商。 利潤增長主要來自光子晶片出貨量提升，該技術將光學元件集成於晶片上以實現高速頻寬傳輸。

rss · Anue 鉅亨網台股 · 8月20日 12:04

**背景**: 光子晶片是利用矽作為光學介質，將光子元件集成於半導體晶片上以實現高速資料傳輸的技術。它因低功耗與高頻寬而在資料中心及 AI 工作負載中受到重視。STMicroelectronics 等公司正擴大生產規模，市場預計將以 25% 的 CAGR 成長至 2035 年。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Silicon_photonics">Silicon photonics - Wikipedia</a></li>
<li><a href="https://www.linkedin.com/pulse/silicon-photonics-technology-real-world-5-uses-youll-sp2ve">Silicon Photonics Technology in the Real World: 5 Uses You'll...</a></li>
<li><a href="https://www.eetasia.com/silicon-photonics-sticks-its-head-above-the-parapet/">Silicon Photonics Sticks Its Head Above the Parapet - EE Times Asia</a></li>

</ul>
</details>

**標籤**: `#Taiwan equities`, `#Earnings`, `#Semiconductors`, `#Profitability`, `#Market News`

---

<a id="item-23"></a>
## [潤德預估 2026 年上半年 EPS 9.51 元，持有 59 億元工程訂單](https://news.cnyes.com/news/id/6582770) ⭐️ 7.0/10

潤德於法人說明會公布，預估 2026 年上半年每股純益為 9.51 元，較去年同期的 8.51 元成長；同時，公司在手工程訂單約 59 億元，其中尚未認列金額約 23 億元。 此指引顯示潤德的獲利持續穩健，且擁有龐大訂單積壓，為投資者提供更清晰的財務預期。 在手工程訂單總額包含已認列與未認列金額，約有 36 億元已被確認，剩餘部分為潛在收益；此 EPS 預估僅針對 2026 年上半年。

rss · Anue 鉅亨網台股 · 8月20日 10:56

**背景**: 潤德（6881‑TW）正式名稱為 Ruentex Interior Design Inc.，是一家專注於室內設計、建築服務及相關施工項目的台灣公司。該公司按季公布財務報告並向投資者提供盈餘指引。每股純益（EPS）代表公司利潤分配給每一張普通股的部分。龐大的在手工程訂單積壓顯示未來收入來源，對市場情緒具有影響力。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://finance.biggo.com/quote/6881.TW/profile">潤德室內裝修設計工程(股) Company Profile | 6881.TW Profile & Comp...</a></li>
<li><a href="https://tw.stock.yahoo.com/quote/6881.TWO/profile">潤德 (6881.TWO) 基本資料 - Yahoo 股市</a></li>
<li><a href="https://finance.yahoo.com/quote/6881.TWO/profile/?fr=sycsrp_catchall">Ruentex Interior Design Inc. (6881.TWO) Company Profile ...</a></li>

</ul>
</details>

**標籤**: `#Taiwanese equities`, `#earnings forecast`, `#order backlog`, `#Runde`

---

<a id="item-24"></a>
## [FactSet 提升鴻海目標價至 355 元](https://news.cnyes.com/news/id/6582756) ⭐️ 7.0/10

FactSet 最新調查顯示，鴻海(2317‑TW)的目標價已調升至 355 元，幅度約為 3.02%。此變動反映了分析師對公司未來營收與利潤前景的樂觀評估。 此舉可能影響投資者對鴻海股票的買賣決策，並可能在短期內推動股價波動。目標價調升亦顯示市場對公司成長潛力的信心。 FactSet 的報告同時提供了最高估值、最低估值、中位數以及綜合評級，並列出了近五日股價走勢與大盤表現。投資者可參考這些指標以評估風險與機會。

rss · Anue 鉅亨網台股 · 8月20日 10:10

**背景**: FactSet 是一家全球知名的金融資訊平台，為投資專業人士提供多種資料來源和分析工具。它整合了超過 30 個資料集及 850 位獨立資料供應商，以協助使用者進行深入研究與決策。台灣股市中，鴻海（2317‑TW）是主要的電子製造服務公司，其股票常受到投資者關注。目標價是分析師根據財務模型和市場預期所設定的理想買入或賣出價格。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://www.factset.com/">FactSet | Financial Data , Market Analytics & AI Solutions</a></li>
<li><a href="https://corporatefinanceinstitute.com/resources/economics/factset/">FactSet - Overview, Mission, Services, How It Works</a></li>

</ul>
</details>

**標籤**: `#Foxconn`, `#Target Price`, `#Taiwan Stock`, `#FactSet`, `#Analyst Rating`

---

<a id="item-25"></a>
## [中鋼 7 月稅前盈餘減 55％](https://news.cnyes.com/news/id/6582710) ⭐️ 7.0/10

中鋼公布七月份稅前盈餘為新台幣 29.94 億元，較上個月下降 55%。 這一大幅下滑凸顯了臺灣鋼鐵產業面臨的挑戰，可能影響投資者對台灣股市的信心。 55％的月減幅度顯示營收大幅縮水，儘管如此，中鋼仍錄得相當可觀的稅前盈餘。

rss · Anue 鉅亨網台股 · 8月20日 09:31

**背景**: 中鋼是臺灣最大的鋼鐵製造商，供應國內市場大部分需求，在島內工業基礎中扮演重要角色。投資者密切關注其財報，以了解整體經濟狀況。

**標籤**: `#China Steel`, `#Taiwan equities`, `#earnings`, `#steel industry`, `#financial results`

---

<a id="item-26"></a>
## [騰訊測試新旗艦模型 Hunyuan Hy4](https://www.reddit.com/gallery/1vth4lo) ⭐️ 7.0/10

騰訊已開始灰階測試其新旗艦大型語言模型 Hunyuan Hy4。該模型已在騰訊 Yuanbao 應用程式中顯示，標註為「專家級模型」並提供「使用工具解決問題」功能。 Hy4 的推出標誌著騰訊在更大規模、多模態人工智慧能力上的重要進展，使其能與全球領導者如 OpenAI 更直接競爭。此舉可能影響中國科技行業的市場動態和投資者情緒。 Hy4 在騰訊 Hunyuan 基礎上擴大了參數量並採用 Mixture‑of‑Experts 設計，實現先進的多模態推理和工具整合。然而該模型仍處於灰階測試階段，其確切上市日期尚未確認。

reddit · r/LocalLLaMA · Nunki08 · 8月20日 11:42 · [社群討論](https://www.reddit.com/r/LocalLLaMA/comments/1vth4lo/tencent_begins_testing_its_new_flagship_model/)

**背景**: Hunyuan 是騰訊於 2023 年九月推出的一系列通用大型語言模型，採用 Transformer 架構和 Mixture‑of‑Experts 技術，擁有萬億參數規模。Yuanbao 應用程式於 2024 年五月發布，作為面向消費者的 AI 助手，以 Hunyuan 為基礎並整合 DeepSeek 等推理模型。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://baike.baidu.com/en/item/Tencent+HY/1450766">Tencent HY（A large language model developed by Tencent ...</a></li>
<li><a href="https://www.tencentcloud.com/product/tclm?lang=en">Tencent HY</a></li>
<li><a href="https://github.com/Tencent-Hunyuan/Tencent-Hunyuan-Large">GitHub - Tencent-Hunyuan/Tencent-Hunyuan-Large · GitHub</a></li>

</ul>
</details>

**社群討論**: 社群成員表達熱情，認為 Hy4 能夠匹敵甚至超越 GLM‑5.3 等模型，同時保持 Hy3 的體積。部分用戶質疑更大的參數量是否會帶來顯著提升，並對未來定價表示好奇。

**標籤**: `#Tencent`, `#AI`, `#LargeLanguageModel`, `#HunyuanHy4`, `#YuanbaoApp`

---

<a id="item-27"></a>
## [Meta 面臨即將到來的社交媒體訴訟風險](https://finance.yahoo.com/technology/article/meta-faces-risks-whether-it-wins-or-loses-major-social-media-trial-163725852.html) ⭐️ 7.0/10

Meta 正在為一項聯邦訴訟做準備，該訴訟指控其在社交媒體平台上從事反競爭行為，審判預計將於今年晚些時候舉行。 此案的結果可能影響 Meta 的估值，並為科技巨頭如何處理用戶資料與競爭設立先例，進而波及投資者和整個技術產業。 即使勝訴也能鞏固 Meta 的市場地位，但敗訴可能引發監管審查和罰款，且法院裁決或迫使其改變資料處理方式。

openbb · AAPL · 8月20日 16:37

**背景**: Meta（Facebook 和 Instagram 的母公司）因其資料隱私政策和市場主導地位而受到越來越多的監管關注。近年來，全球各國政府都在審查社交媒體平台如何影響消費者行為與競爭。

**標籤**: `#Meta`, `#lawsuit`, `#regulatory risk`, `#tech stocks`, `#social media`

---

<a id="item-28"></a>
## [澳洲對 Meta 與 Google 徵收 2.5％新聞稅](https://finance.yahoo.com/economy/policy/articles/australia-hits-meta-google-2-163633536.html) ⭐️ 7.0/10

澳洲政府已正式啟用對 Meta 與 Alphabet 旗下 Google 因新聞內容產生的營收徵收 2.5％稅，除非雙方達成協議，否則立即生效。 此稅項為全球最大兩個以廣告營收為主的平台帶來新合規成本，可能削減其廣告收入並影響投資者估值。 此稅僅適用於被歸類為「指定」平台的服務，並以其首頁新聞內容所產生營收的 2.5％計算。

openbb · AAPL · 8月20日 16:36

**背景**: 澳洲的新聞媒體談判法規（News Media Bargaining Code）於 2021 年推出，要求受惠於本土新聞的數位平台與媒體機構協商公平報酬。此法規旨在解決大型科技公司與地方新聞機構之間的議價失衡問題。近期修訂將未達成協議的平台稅率提高至 2.5％。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://www-accc-gov-au.nproxy.org/by-industry/digital-platforms-and-services/news-media-bargaining-code/news-media-bargaining-code">News media bargaining code | ACCC</a></li>
<li><a href="https://www.accc.gov.au/media-release/australian-news-media-to-negotiate-payment-with-major-digital-platforms">Australian news media to negotiate payment with major... | ACCC</a></li>
<li><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2llbjhMOEVCSDR0TXI0NmFwcVVDZ0FQAQ?hl=en-IN&gl=IN&ceid=IN:en">Google News - Australia proposes news levy on Google, Meta, and...</a></li>

</ul>
</details>

**標籤**: `#Regulatory`, `#Meta`, `#Alphabet`, `#Australia`, `#AdRevenue`

---

<a id="item-29"></a>
## [國庫收益率上升，沃爾瑪股價因指引下滑而跌](https://finance.yahoo.com/markets/stocks/articles/top-midday-stories-treasury-yields-153556130.html) ⭐️ 7.0/10

美國國庫收益率回升至四年高點，沃爾瑪股價因下調全年每股盈餘指引低於市場預期而下跌。 收益率上升表明貨幣政策收緊，將影響企業和家庭的借貸成本；沃爾瑪下調指引則可能預示零售業普遍疲軟。 國庫十年期收益率升至 4.12%，為 2022 年底以來最高水平；沃爾瑪將每股盈餘指引下調約 0.15 美元，導致股票在盤中交易中跌幅約 3%。

openbb · AAPL · 8月20日 15:35

**背景**: 美國國庫收益率是借貸成本的基準，反映投資者對通脹和貨幣政策的預期。收益率上升通常表示信貸條件收緊，可能壓縮企業盈利。每股盈餘（EPS）指引是公司對未來獲利的預測；若低於分析師估計，股票往往會出現負面反應。

**標籤**: `#Treasury Yields`, `#Walmart`, `#Earnings Guidance`, `#Equity Markets`, `#Macro`

---

<a id="item-30"></a>
## [SpaceX 與 Magnificent Seven：不同的成長路徑](https://www.barrons.com/articles/spacex-stock-price-mag-7-amazon-meta-0a22f620?siteid=yhoof2&yptr=yahoo) ⭐️ 7.0/10

Barron's 文章將 SpaceX 的商業模式與估值走勢與 Magnificent Seven 科技巨頭做對比，指出 SpaceX 專注於可重複使用的發射載具、衛星網路及高資本支出，使其成長曲線相較 Amazon 或 Meta 更為緩慢。文章亦說明這些結構差異如何影響投資者對未來 IPO 的期望。 了解這些差異對於關注 SpaceX 可能上市的投資者至關重要，因為其估值動態與已建立的科技巨頭截然不同。此分析亦能幫助市場更好預測高成長私營太空企業的可行性和定價。 SpaceX 的收入來源—主要是發射服務與 Starlink 訂閱—受到監管批准、發射頻率限制及長期資本投資的影響，限制了其達到 Amazon 或 Meta 所見快速盈餘成長的能力。再者，SpaceX 的估值往往以未來潛力為主，而非現有獲利，這使得與成熟科技公司直接比較變得困難。

openbb · AAPL · 8月20日 15:30

**背景**: Magnificent Seven 指的是美國市值最大、投資者關注度最高的七大科技公司—Amazon、Apple、Microsoft、Alphabet、Meta、Tesla 與 Nvidia。SpaceX 於 2002 年由 Elon Musk 創立，仍為私營企業，以可重複使用火箭革新太空旅行並透過 Starlink 擴展衛星寬頻服務。分析師長期以來一直推測 SpaceX 的 IPO 潛力，但其商業模式與資本需求與公開上市的科技巨頭有顯著差異。

**標籤**: `#SpaceX`, `#IPO`, `#Tech Stocks`, `#Investment Analysis`, `#Private Equity`

---

<a id="item-31"></a>
## [億萬富翁加碼「七巨頭」科技股](https://finance.yahoo.com/markets/stocks/articles/billionaire-recently-loading-magnificent-seven-150300730.html) ⭐️ 7.0/10

文章報導，一位知名億萬富翁近期增持了七巨頭科技股，包括 Alphabet、Amazon、Apple、Meta Platforms、Microsoft、NVIDIA 和 Tesla。 此舉顯示對這些巨型科技股持續領先的信心，可能影響市場情緒並促使其他投資者跟進。 該億萬富翁的持股透過最新的 Form 13F 文件披露，顯示其對高成長科技領導者的戰略調整。

openbb · AAPL · 8月20日 15:03

**背景**: 七巨頭是由 Alphabet、Amazon、Apple、Meta Platforms、Microsoft、NVIDIA 和 Tesla 組成的高績效科技股集團。它們共同佔 S&P 500 指數約 30%–35%，多年來一直推動市場表現。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://www.investopedia.com/magnificent-seven-stocks-8402262">Magnificent 7 Stocks: What You Need to Know - Investopedia What are the Magnificent 7 stocks? | Fidelity What Are The Magnificent 7 Stocks? - Investing.com Magnificent 7 Stocks 2026 — What They Are and How to Invest Magnificent 7 Stocks: What Are They and How They Dominate the ... The Magnificent Seven Stocks: What They Are And How To ... Full list of Magnificent 7 Stocks - Updated Daily</a></li>
<li><a href="https://www.fidelity.com/learning-center/smart-money/magnificent-7-stocks">What are the Magnificent 7 stocks? | Fidelity</a></li>

</ul>
</details>

**標籤**: `#Investing`, `#Tech Stocks`, `#Billionaire Investment`, `#Market Sentiment`, `#Magnificent Seven`

---

<a id="item-32"></a>
## [Meta 在 AI 競爭中落後於亞馬遜、Alphabet 與微軟](https://finance.yahoo.com/technology/ai/articles/meta-falls-far-behind-amazon-144806616.html) ⭐️ 7.0/10

文章指出，Meta 在人工智慧領域的進展遠落後於亞馬遜、Alphabet 與微軟。它強調了模型規模、投資水平和產品部署速度上的差距。 這種差距可能會影響 Meta 未來的成長前景和投資者情緒，因為人工智慧能力正日益成為科技行業創造收入與競爭優勢的關鍵。 此分析基於公開披露的資料，例如模型規模、雲端人工智慧服務產品與資本配置，並指出 Meta 的私有計畫可能未被完全反映。

openbb · AAPL · 8月20日 14:48

**背景**: 主要科技公司正競相打造大型語言模型並將生成式人工智慧整合進其平台。亞馬遜提供 Bedrock，Alphabet 擁有 Gemini/PaLM，而微軟則提供 Azure OpenAI 服務。

**標籤**: `#Artificial Intelligence`, `#Meta Platforms`, `#US Tech Stocks`, `#Competitive Analysis`, `#Investor Insight`

---

<a id="item-33"></a>
## [四大非晶片股有望受益於 AI 資料中心擴張](https://finance.yahoo.com/technology/ai/articles/beyond-chipmakers-4-stocks-buy-144300979.html) ⭐️ 7.0/10

文章推薦了四支非晶片公司股票，這些公司有機會從不斷擴大的 AI 資料中心市場中獲利。 投資者可以透過投資提供 AI 工作負載關鍵基礎設施的公司，從而擺脫對晶片製造商的單一依賴。 這些公司主要從事支援 AI 資料中心的領域，例如高效能互連（RoCE、InfiniBand）、NVMe over Fabrics 儲存方案，以及適用於高密度伺服器機架的液體冷卻系統。

openbb · AAPL · 8月20日 14:43

**背景**: AI 資料中心需要大量計算能力、低延遲網路、快速儲存與高效冷卻。RoCE（RDMA over Converged Ethernet）因為工程師熟悉且開發週期較快，正逐漸取代傳統 InfiniBand。NVMe over Fabrics 能將本地 NVMe 驅動器的性能延伸至網路，而液體冷卻則能讓伺服器機架達到超過 100 kW 的高密度運作。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://www.juniper.net/content/dam/www/assets/white-papers/us/en/2024/juniper-artificial-intelligence-data-center-comparison-of-infiniband-and-rdma-over-converged-ethernet.pdf">ACG: Juniper Artificial Intelligence Data Center: Comparison ...</a></li>
<li><a href="https://www.nvmexpress.org/wp-content/uploads/NVMe_Over_Fabrics.pdf">NVMe over Fabrics Overview</a></li>
<li><a href="https://www.coolitsystems.com/">Cooling Solutions for HPC, AI & Data Centers | CoolIT Systems</a></li>

</ul>
</details>

**標籤**: `#AI`, `#Data Centers`, `#Stocks`, `#Investment`, `#Technology`

---

<a id="item-34"></a>
## [AWS 後備庫存突破 4.96 億美元—亞馬遜仍被低估？](https://finance.yahoo.com/markets/stocks/articles/amazons-aws-backlog-just-hit-165000582.html) ⭐️ 7.0/10

亞馬遜雲端服務 AWS 公布其後備庫存已達 4.96 億美元，創下新紀錄。 此數字顯示未來營收承諾與持續需求，影響投資者對亞馬遜估值的看法。 後備庫存包含已簽署的計算、儲存等服務合約，但未考慮取消或價格變動，需謹慎解讀。

openbb · AAPL · 8月20日 16:50

**背景**: Amazon Web Services (AWS) 是全球最大的雲端運算平台，為企業提供基礎設施即服務（IaaS）及多種管理服務。後備庫存是指已簽署但尚未履行的合約，代表公司未來的營收來源。AWS 以往一直是亞馬遜營業收入的重要推動力，也是主要成長引擎。

**標籤**: `#Amazon`, `#AWS`, `#Backlog`, `#Stock Valuation`, `#US Equities`

---

<a id="item-35"></a>
## [麥金塔面臨$115 億美元晶片廠建設風險](https://finance.yahoo.com/markets/stocks/articles/microns-biggest-risk-written-construction-152112282.html) ⭐️ 7.0/10

麥金塔宣布投資 1150 億美元建造美國最大晶片製造廠，但施工延誤與成本超支可能威脅其預期盈利和供應鏈可靠性。 此風險可能延遲新記憶體產品上市、壓縮利潤，並使麥金塔面臨海外晶片廠競爭，影響投資者與美國半導體供應鏈。 單一先進晶片廠建造成本超過 200 億美元，麥金塔的項目是美國歷史上最大的；任何延誤都可能推遲數月或數年產能啟動，影響營收預測。

openbb · TSM · 8月20日 15:21

**背景**: 半導體製造廠（Fab）是高度資本密集的設施，用於生產整合電路。麥金塔科技是美國唯一的 DRAM 記憶體晶片製造商，為降低對海外供應商的依賴而擴大國內產能。建造晶片廠需要複雜工程、嚴格潔淨室標準及龐大的前期投資，往往超過 200 億美元每個工廠。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://www.youtube.com/watch?v=S3geK7xVDQU">How Micron ’s Building Biggest U.S. Chip Fab , Despite... - YouTube</a></li>
<li><a href="https://manufacturingleadgeneration.com/semiconductor-manufacturing-statistics/">90+ Semiconductor Manufacturing Statistics 2026</a></li>
<li><a href="https://en.wikipedia.org/wiki/List_of_semiconductor_fabrication_plants">List of semiconductor fabrication plants - Wikipedia</a></li>

</ul>
</details>

**標籤**: `#Micron`, `#Semiconductor`, `#Capital Expenditure`, `#Investment Risk`, `#US Equities`

---

<a id="item-36"></a>
## [Broadcom 持平 ARK 買入谷底，Intel 下跌，AMD 因 Google‑Marvell 交易回落](https://finance.yahoo.com/markets/stocks/articles/broadcom-holds-steady-ark-buys-133232286.html) ⭐️ 7.0/10

Broadcom 股價當日持平，ARK 投資公司因市場低點買入其股份。與此同時，Intel 股價下滑，而 AMD 在 Google 宣布可選擇購買高達 12.2 億美元的 Marvell 技術股份（以未來自訂 AI 晶片採購為條件）後也回落。 這些股價變動顯示投資者對半導體行業的情緒，尤其是在 AI 基礎設施需求上升之際。Broadcom 的穩定表現與 ARK 的買入行為暗示市場對網路及儲存晶片仍有信心，而 Intel 的下跌和 AMD 的回落則凸顯 Google 與 Marvell 合作帶來的競爭壓力。 Google 的選擇權允許其以每股 $206.58 購買最高 5,8970,907 股，潛在估值達 12.2 億美元；此交易取決於未來晶片採購，可能影響 Marvell 的市值。ARK 在 Broadcom 價格短暫下跌時進行買入，顯示其機會主義策略。

openbb · TSM · 8月20日 13:32

**背景**: Broadcom、Intel 與 AMD 是美國半導體市場的主要參與者，產品線涵蓋從網路晶片到中央處理器。ARK Invest 是一家主動管理的 ETF，以在短期低點買入被低估的科技股而聞名。Google 最近對 Marvell 的選擇權投資符合其為資料中心確保自訂 AI 晶片的策略。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://www.reuters.com/technology/marvell-grants-google-122-billion-stock-warrant-custom-chip-deal-2026-08-19/">Marvell gives Google option to buy $12.2 billion stake in ...</a></li>
<li><a href="https://www.cnbc.com/2026/08/19/marvell-google-ai-chips.html">Marvell pops on AI chip deal letting Google buy up to $12.2B ...</a></li>
<li><a href="https://www.hindustantimes.com/business/why-is-marvell-stock-surging-google-s-12-2-billion-ai-chip-deal-explained-101787149636754.html">Why is Marvell stock surging? Google’s $12.2 billion AI chip ...</a></li>

</ul>
</details>

**標籤**: `#Semiconductor`, `#Stock Market`, `#Intel`, `#AMD`, `#Google-Marvell`

---

<a id="item-37"></a>
## [AMD 與 Intel 股價大跌](https://finance.yahoo.com/markets/stocks/articles/amd-intel-shares-plummet-know-233402382.html) ⭐️ 7.0/10

AMD 與 Intel 的股價在最新財報公布後大幅下跌，顯示投資者對營收前景及產品路線圖延遲的擔憂。 股價下跌凸顯美國晶片製造商面臨的挑戰，可能影響資本配置、研發投資與與 AMD 及海外競爭者之間的競爭格局。 兩家公司公布的財報均未達市場預期，成為股價急劇下跌的主要原因。

openbb · TSM · 8月19日 23:34

**背景**: AMD 與 Intel 是美國最大的兩家半導體公司，彼此競爭於 CPU、GPU 及資料中心晶片的市場主導權。近年來，Intel 採取 IDM 2.0 策略，以內部製造與第三方產能結合，同時推出以 Golden Cove 微架構為基礎的 Sapphire Rapids Xeon 系列。另一方面，AMD 擴充其加速器產品線，推出 MI300 系列，針對生成式 AI 與高效能運算工作負載。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://www.intc.com/news-events/press-releases/detail/1451/intel-ceo-pat-gelsinger-announces-idm-2-0-strategy">Intel CEO Pat Gelsinger Announces ‘ IDM 2 . 0 ’ Strategy for...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Sapphire_Rapids">Sapphire Rapids - Wikipedia</a></li>
<li><a href="https://www.amd.com/en/products/accelerators/instinct/mi300.html">AMD Instinct™ MI300 Series Accelerators</a></li>

</ul>
</details>

**標籤**: `#Semiconductors`, `#Earnings`, `#Stock Market`, `#AMD`, `#Intel`

---

<a id="item-38"></a>
## [杜克倫米勒賣出 Micron 與 Intel，買進兩支 AI 股](https://finance.yahoo.com/markets/stocks/articles/billionaire-stanley-druckenmiller-just-dumped-215200310.html) ⭐️ 7.0/10

杜克倫米勒最近賣出了 Micron 與 Intel 的持股，並新增了兩支未公開名稱的 AI 專注公司股份。 他的投資組合變動凸顯了從傳統半導體向高成長 AI 技術的潛在轉移，為投資者重新評估行業配置提供可能訊號。 這些交易是透過他的投資機構執行，但具體的成交日期和金額未公開；投資者應注意，過往表現不代表未來結果。

openbb · TSM · 8月19日 21:52

**背景**: 杜克倫米勒是前對沖基金經理，以長期宏觀投資風格聞名。Micron Technology 生產記憶體晶片，廣泛應用於資料中心與消費電子；Intel Inc. 則在 CPU 市場佔有主導地位。近年來，由於 AI 對專業硬體（如 GPU 與神經網路加速器）的需求激增，AI 公司吸引了大量資金。

**標籤**: `#investing`, `#semiconductors`, `#AI stocks`, `#portfolio moves`, `#market signals`

---

<a id="item-39"></a>
## [TSMC 與 GlobalFoundries：哪一間晶圓代工股更值得買入？](https://finance.yahoo.com/markets/stocks/articles/tsmc-vs-globalfoundries-foundry-stock-123500621.html) ⭐️ 7.0/10

本文評估了 TSMC 與 GlobalFoundries 的股價，對比其財務狀況、技術路線圖與市場定位，以協助投資者判斷哪一支股票更具上漲潛力。 投資者在美台股市中依賴此類分析來配置資金至高成長的半導體企業，工程師亦可藉由了解晶圓代工技術成熟度判斷未來產品路線。 TSMC 已推出高量產 3 nm FinFET（N3）工藝，而 GlobalFoundries 正在推進其 7 nm 工藝並採用 EUV 光刻，以縮小與先進節點的差距。

openbb · TSM · 8月20日 12:35

**背景**: 半導體晶圓代工透過在更小的製程節點（以 nm 為單位）製造晶片，提升晶片密度與效能。TSMC 以 3 nm N3 技術領先市場，而 GlobalFoundries 則歷史上較為落後，但正大力投資 EUV 光刻以縮小差距。

<details><summary>參考連結</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/3_nm_process">3 nm process - Wikipedia</a></li>
<li><a href="https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_3nm">3nm Technology - TSMC</a></li>
<li><a href="https://semiwiki.com/wikis/industry-wikis/tsmc-n3-process-node-3nm-wiki/">TSMC N3 Process Technology Wiki - SemiWiki</a></li>

</ul>
</details>

**標籤**: `#Semiconductors`, `#TSMC`, `#GlobalFoundries`, `#Investment Analysis`, `#US-Taiwan Equities`

---

<a id="item-40"></a>
## [三星股價下跌近 8％，AI 需求推升晶片價格](https://finance.yahoo.com/markets/stocks/articles/samsung-tumbled-nearly-8-seoul-211220540.html) ⭐️ 7.0/10

三星在韓國交易所的股價下跌近 8%，同時 AI 驅動需求使晶片價格上升約 15%。 股價下跌顯示投資者對三星半導體部門的擔憂，晶片價格上升則表明供應緊張與 AI 工作負載增長，可能影響全球晶片市場。 價格上升主要來自對 AI 加速器使用的記憶體與邏輯晶片需求增加，但三星仍未調整盈利指引。

openbb · TSM · 8月19日 21:12

**背景**: 三星電子是全球領先的半導體製造商，生產 DRAM、NAND 閃存與系統 LSI 晶片。近幾個月來 AI 的興起推動了對高性能記憶體和處理器的需求，造成全球供應鏈緊張。投資者密切關注三星股價，以了解晶片產業的整體趨勢。

**標籤**: `#Samsung`, `#Semiconductors`, `#AI Demand`, `#Chip Prices`, `#Stock Market`

---