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
| **📁 [Hardware Modules](./Hardware%20Modules/)** | 提供針對 AOS-CX (如 8325, 8360, 8400, 10000) 交換器的 `system interface-group` 模組相關設定 (包含創建、查詢、刪除 25G/50G/100G 群組速率分配)。 |
| *(未來開發功能)* | ...等候擴充中 |

---
## 開發維護須知
- 所有 GUI 程式推薦使用 Python 的 `tkinter` 作為輕量級介面。
- 網路連線與 API 請求統一使用 `requests` 函式庫實作。

## 授權說明
MIT License
