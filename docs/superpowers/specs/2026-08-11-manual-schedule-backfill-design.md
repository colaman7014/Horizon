# 手動補排程設計

日期：2026-08-11

## 目標

立即補跑 Horizon 今日的本機日常流程，處理最近 24 小時資料，並將產出的文件發布到 `gh-pages`。本次操作不修改程式碼、launchd 設定或資料設定。

## 現況與既有流程

- `scripts/com.colalin.horizon-daily.plist` 以 launchd 每日 01:00 啟動本機流程。
- plist 透過 `caffeinate` 執行 `scripts/daily-run-local.sh`。
- `scripts/daily-run-local.sh` 會：
  1. 啟動 OrbStack（若尚未執行）。
  2. 等待 `docker info` 成功，預設最多 600 秒。
  3. 執行 `docker compose run --rm horizon --hours 24`。
  4. 建立暫存 `gh-pages` worktree，複製 `docs/`，提交並推送變更。

## 採用方案

從 repository 根目錄直接執行既有完整腳本：

```bash
bash scripts/daily-run-local.sh
```

此方案沿用排程真正使用的腳本，避免只產生報告但漏掉發布，亦避免依賴 launchd job 當前是否已載入。執行前確認沒有另一個相同腳本正在執行，避免同時寫入 `data/`、`docs/` 或操作 `gh-pages` worktree。

## 範圍

包含：

- 一次性補跑最近 24 小時的 Horizon pipeline。
- 使用現有本機 Docker、環境變數與設定。
- 依既有腳本發布產出至 `gh-pages`。
- 以實際終端輸出、程序 exit status 與發布結果驗證。

不包含：

- 修改或重新安裝 launchd 排程。
- 多日歷史資料回補或自訂日期切片。
- 變更來源、AI、資料庫、部署或報告格式。
- 新增鎖、重試、CLI 參數或其他永久性功能。

## 錯誤處理與副作用

腳本使用 `set -euo pipefail`；Docker 無法在逾時內就緒或 pipeline 失敗時，流程停止，不進入發布步驟。若報告內容沒有變更，發布階段會記錄 `Nothing to commit.`，這是成功的無變更結果，不視為錯誤。

此操作可能：

- 呼叫外部資料來源與本機 AI/Docker 服務。
- 修改 repository 工作目錄中的 `data/`、`docs/`。
- 使用現有 Git 認證推送 `gh-pages`。

不執行任何 destructive Git 操作，不會 `reset` 或 `clean`；pipeline 仍可能依正常流程更新 `data/` 與 `docs/`，因此執行前需確認現有未提交變更可接受。

## 驗證

執行後確認：

1. 腳本以 exit status 0 結束。
2. 輸出顯示 Docker ready、pipeline 完成，以及 `Published to gh-pages.` 或 `Nothing to commit.`。
3. 若有新報告，確認其存在於 `docs/`，且發布步驟完成。
4. 若失敗，保留完整錯誤輸出，停止宣稱補排程成功，不自動重跑。

## 完成條件

一次完整的 `daily-run-local.sh` 執行成功，且發布階段明確成功或明確確認沒有需要提交的變更。