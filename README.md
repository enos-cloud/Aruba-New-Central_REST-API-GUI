# Aruba New Central - REST API GUI Tools

本專案 (Repository) 旨在收錄一系列針對 **Aruba New Central REST API** 開發的 GUI 視覺化桌面小工具。
設計這些工具的初衷，是為了解決網路工程師與維運人員在操作底層設備時，直接編寫與發送 API 請求、以及管理 JSON Payload 所帶來的痛點，讓每一次設定變更都能清晰、安全、直覺。

## 為什麼需要這些 GUI 工具？
1. **降低操作門檻**：不必熟記 REST API 所有的路徑端點、參數屬性或使用諸如 Postman / cURL 等開發者工具，透過點擊按鈕即可完成複雜操作。
2. **標準化與防呆**：內置 JSON 酬載 (Payload) 範本，可防範因為打錯欄位或少括號所造成的 API 報錯情形。
3. **無縫共用憑證**：內建 Oauth 2.0 (Client Credentials) 身分驗證模組，單次取得 Token 後自動跨功能帶入，不需再手動複製貼上落長的 JWT。
4. **易於交接與審計**：所有功能與腳本按資料夾歸類，未來的接手人員或團隊成員只要直接執行對應功能的 `.py` 檔案即可完成任務。

## 目錄結構與功能介紹

目前本專案收錄了以下各類型的自動化 GUI 小工具，詳細使用方式請進入各自的子資料夾查看 `README.md`。

| 工具分類資料夾 | 簡介與主要用途 |
| :--- | :--- |
| **📁 [Hardware Modules](./Hardware%20Modules/)** | 提供針對 AOS-CX (如 8325, 8360, 8400, 10000) 交換器的 `system interface-group` 模組相關設定 (包含創建、查詢、刪除 25G/50G/100G 群組速率分配)，**並支援將配置直接下發指派至設備 (Profile Assignment)**。 |
| *(未來開發功能)* | ...等候擴充中 |

---
## 免責聲明與開發者參考資源
> [!WARNING]  
> **非官方工具聲明 (Unofficial Tool Statement)**  
> 本專案為獨立開發者/社群因應網路維運需求所攥寫之開源輔助工具，**非 HPE Aruba 官方正式發佈的軟體產品**。
> 所有底層 API 拋轉與操作邏輯皆是基於原廠公開的開發者網站內容與 REST API 規範進行開發與封裝。

- Aruba 開發者入口與 API 參考依據：[Aruba Developer Portal - New Central](https://developer.arubanetworks.com/new-central/docs/about)

> [!NOTE]
> **關於 Config Assignment 的底層 API 選用說明**
> 官方 Developer Portal 上提供的 `config-assignments` 端點目前仍為 Alpha/Select Availability，實測時可能尚未在所有 Cluster (如 jp1) 啟用並回傳 `400 Invalid URL`。因此，本專案的「Profile Assignment」功能模組**目前底層改採 Aruba 內部隱藏的正式端點 `POST /network-config/v1alpha1/scope-maps` 進行實作**。當未來 Aruba 正式全面開放新版 endpoint 時，將會發佈更新調整。

使用者在正式營運環境 (Production) 中執行包含 DELETE、POST 等破壞性或修改設定之請求前，請務必先於測試環境 (Lab/Staging) 進行驗證，以確保網路服務不受預期外影響。

---
## 開發維護須知
- 所有 GUI 程式推薦使用 Python 的 `tkinter` 作為輕量級介面。
- 網路連線與 API 請求統一使用 `requests` 函式庫實作。

## 授權說明
MIT License
