# Aruba New Central - Hardware Modules

這是一個使用 Python 與 Tkinter (GUI) 打造的桌面輔助工具，專門用來操作 Aruba New Central REST API，幫助使用者建立、查詢與刪除 **Hardware Module Profiles (硬體模組設定)**。

此工具主要應用於設定支援的 AOS-CX 交換器的 `system interface-group` 參數，適用的設備型號包含但不限於：
- **AOS-CX 8325**
- **AOS-CX 8360**
- **AOS-CX 8400**
- **AOS-CX 10000**

## 核心功能
- **單一分頁身分驗證**：透過 HPE GreenLake 發行的 Client ID 與 Client Secret，點擊一鍵產生 API 所需的 Bearer Token，並自動跨分頁帶入。
- **介面設定檔管理**：支援將設定檔透過 API 傳送 (POST)、讀取現有清單 (GET)、以及刪除指定的設定檔 (DELETE)。
- **設定檔一鍵下發 (Profile Assignment)**：第三分頁支援獲取 Central 內可用設備清單 (下拉選單支援設備名稱與 Persona 提示)，並將創建的設定檔綁定至指定設備。
- **動態 API 路徑對齊**：使用者只需填寫基礎域名 (Base URL)，程式會自動將請求指向正確的硬體模組 REST 節點 (`/network-config/v1alpha1/hardware-modules`)。
- **JSON 酬載產生器**：內建預設的 JSON 格式框架，方便網路工程師直接編輯 25G/10G/50G/100G 等各個 Interface Group 的速度，並一鍵套用到設備上。

## 執行環境需求
- **Python 3.x**
- 必備 Python 函式庫：`requests`

安裝網路傳輸套件：
```bash
pip install requests
```

## 使用教學
請在終端機或命令提示字元進入該資料夾後執行底下指令啟動視窗介面：
```bash
python "Hardware Modules Profile.py"
```

### 1. 身分驗證 (Authentication)
1. 進入首頁 **1. Authentication** 分頁。
2. 填寫你從 HPE GreenLake 申請的 **Client ID** 與 **Client Secret**。
3. 點擊 **取得 Token (Get Token)** 按鈕，若成功，畫面將亮起綠燈，並自動將授權碼分享進入第二個操作分頁。

### 2. 硬體模組設定 (Hardware Module Profile)
1. 切換至 **2. Hardware Module Profile** 分頁。
2. 在 **API Base URL** 中保留你的 Central 站點位址 (例如 `https://ap1.api.central.arubanetworks.com/`)。
3. 如果你想建立或刪除特定的設定檔，請在 **硬體模組設定檔名稱** 中填寫 (例如 `enos-test-001`)。
4. 若是「建立 (CREATE)」操作，請在下方的文本區塊中撰寫標準的 JSON API Payload。
5. 最後點擊下方的 **查詢 (GET)**、**建立 (POST)** 或 **刪除 (DELETE)** 按鈕，下方會即時反饋 Aruba 伺服器傳回的執行結果。

### 3. 配置指派 (Profile Assignment)
1. 切換至 **3. Profile Assignment** 分頁。
2. 畫面會自動帶入前兩頁所產生的 Token 與預備設定的 Module Profile Name。
3. 點擊 **取得設備清單 (Fetch Devices)**，程式會呼叫 Central 拿取所有的設備 (包含 ID、角色與序號)。
4. 點開下拉選單，選定你想下發設定檔的目標設備。
5. 點擊 **執行綁定 (Assign Profile)**，系統將自動於底層將 ID 進行 Mapping (利用 `scope-maps` API)，成功後設備即立刻套用該介面群組規則。

> [!CAUTION]  
> 注意：目前開發者大會 (Developer Portal) 上的官方 `config-assignments` 端點仍為 Preview 階段，故本程式實行的下發底層 API 是採用官方向後相容的隱藏端點 `POST /network-config/v1alpha1/scope-maps` 進行封裝處理。

## 設備官方設定指南
如果你想進一步了解 AOS-CX 在 `system interface-group` 上相關的速度參數如何分配以及原理，請參閱 Aruba 官方提供的開通說明文件：
- 📖 [AOS-CX Fundamentals Guide - System Interface Group (適用 8400, 8360, 8325, 10000)](https://arubanetworking.hpe.com/techdocs/AOS-CX/10.14/HTML/fundamentals_8400/Content/Chp_IfaceCfg/Iface_cmds/sys-int-grp.htm)

## 授權條款
MIT License
