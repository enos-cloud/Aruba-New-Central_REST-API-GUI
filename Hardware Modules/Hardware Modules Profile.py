import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import webbrowser

class ArubaNewCentralAPIConfigurator:
    def __init__(self, root):
        self.root = root
        self.root.title("Aruba New Central -- API Configurator")
        self.root.geometry("800x700")
        self.root.configure(bg="#f4f4f9")
        
        # 樣式設定 (設定基本的 UI 主題、字體與背景顏色)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f4f4f9')
        style.configure('TLabel', background='#f4f4f9', font=('Helvetica', 10, 'bold'))
        style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=6)
        
        # 全域變數宣告 (用於跨分頁共享 Token)
        self.token_var = tk.StringVar(value="")
        
        # 主框架設定 (包含整個視窗的所有元件)
        main_frame = ttk.Frame(root, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 大標題
        title_label = ttk.Label(main_frame, text="Aruba New Central -- API Configurator", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # 建立分頁管理器 (Notebook 讓使用者可以切換不同功能頁面)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 建立兩個分頁框架
        self.tab_auth = ttk.Frame(self.notebook)
        self.tab_hw = ttk.Frame(self.notebook)
        
        # 將分頁框架加入 Notebook 中並命名
        self.notebook.add(self.tab_auth, text='1. Authentication (身分驗證)')
        self.notebook.add(self.tab_hw, text='2. Hardware Module Profile (硬體模組設定)')
        
        # 呼叫設定方法來初始化兩個分頁的內容
        self.setup_auth_tab()
        self.setup_hw_tab()

    def setup_auth_tab(self):
        # ---------------- AUTHENTICATION TAB (身分驗證分頁設計) ----------------
        frame = ttk.Frame(self.tab_auth, padding="20 20 20 20")
        frame.pack(fill=tk.BOTH, expand=True)

        # 提示資訊區塊 (放在最上方，引導使用者如何獲取憑證)
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 說明文字
        info_text = "💡 如何獲取 Client ID 與 Secret？\n"
        ttk.Label(info_frame, text=info_text, foreground="#555555", justify=tk.LEFT).pack(anchor=tk.W)
        
        # 官方文件超連結 (綁定點擊事件，可以直接開啟瀏覽器)
        link_lbl = ttk.Label(info_frame, text="🔗 取得步驟教學", foreground="blue", cursor="hand2", font=('Helvetica', 10, 'underline'))
        link_lbl.pack(anchor=tk.W, pady=(5, 0))
        link_lbl.bind("<Button-1>", lambda e: webbrowser.open_new("https://developer.arubanetworks.com/new-central/docs/generating-and-managing-access-tokens"))

        # Client ID 輸入欄位
        ttk.Label(frame, text="Client ID:").pack(anchor=tk.W, pady=(10, 2))
        self.client_id_var = tk.StringVar(value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        ttk.Entry(frame, textvariable=self.client_id_var, width=80).pack(fill=tk.X, pady=2)

        # Client Secret 輸入欄位 (show="*" 可將輸入內容隱藏為米字號)
        ttk.Label(frame, text="Client Secret:").pack(anchor=tk.W, pady=(10, 2))
        self.client_secret_var = tk.StringVar(value="f9bfc0e8bfa743f09xxxxxxxxxxxxx")
        ttk.Entry(frame, textvariable=self.client_secret_var, show="*", width=80).pack(fill=tk.X, pady=2)
        
        # 按鈕區塊
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=15)
        # 取得 Token 的觸發按鈕，點擊後會呼叫 fetch_token 函式
        self.get_token_btn = ttk.Button(btn_frame, text="取得 Token (Get Token)", command=self.fetch_token)
        self.get_token_btn.pack(side=tk.LEFT)
        
        # Token 結果顯示欄位
        ttk.Label(frame, text="Bearer Token (JWT):").pack(anchor=tk.W, pady=(10, 2))
        self.token_entry = ttk.Entry(frame, textvariable=self.token_var, width=80)
        self.token_entry.pack(fill=tk.X, pady=2)

        # 驗證狀態顯示區塊 (顯示目前進度或失敗原因)
        auth_status_frame = ttk.Frame(frame)
        auth_status_frame.pack(fill=tk.X, pady=10)
        self.auth_status_var = tk.StringVar(value="等待操作 (Idle)")
        ttk.Label(auth_status_frame, text="狀態 (Status):").pack(side=tk.LEFT)
        self.auth_status_label = ttk.Label(auth_status_frame, textvariable=self.auth_status_var, foreground="blue")
        self.auth_status_label.pack(side=tk.LEFT, padx=5)

    def setup_hw_tab(self):
        # ---------------- HARDWARE MODULE PROFILE TAB (硬體模組設定分頁設計) ----------------
        frame = ttk.Frame(self.tab_hw, padding="20 20 20 20")
        frame.pack(fill=tk.BOTH, expand=True)

        # 顯示當前 Token 區塊 (唯讀)，讓使用者確認目前使用的 Token 是否正確載入
        token_preview_frame = ttk.Frame(frame)
        token_preview_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(token_preview_frame, text="目前使用的 Token:").pack(side=tk.LEFT)
        # state='readonly' 防止使用者在此處修改 Token
        self.hw_token_entry = ttk.Entry(token_preview_frame, textvariable=self.token_var, state='readonly', width=65)
        self.hw_token_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # API 基礎網址設定 (Base URL)
        url_label_frame = ttk.Frame(frame)
        url_label_frame.pack(fill=tk.X)
        ttk.Label(url_label_frame, text="API Base URL (基礎網址):").pack(side=tk.LEFT)
        
        # 提供官方文件連結幫助使用者尋找自己的 Base URL
        url_help = ttk.Label(url_label_frame, text="(🔍 不知道怎麼找 Base URL?)", foreground="blue", cursor="hand2", font=('Helvetica', 9, 'underline'))
        url_help.pack(side=tk.RIGHT, padx=5)
        url_help.bind("<Button-1>", lambda e: webbrowser.open_new("https://developer.arubanetworks.com/new-central/docs/getting-started-with-rest-apis#finding-your-base-url"))
        
        # 網址輸入框 (帶有預設值)
        self.url_var = tk.StringVar(value="https://de1.api.central.arubanetworks.com/")
        ttk.Entry(frame, textvariable=self.url_var, width=80).pack(fill=tk.X, pady=(2, 10))
        
        # 硬體模組設定檔名稱 (用於動態組合 API 路徑)
        ttk.Label(frame, text="硬體模組設定檔名稱 (Hardware Module Profile Name):").pack(anchor=tk.W, pady=(10, 2))
        self.module_var = tk.StringVar(value="enos-new-central-lab-001")
        ttk.Entry(frame, textvariable=self.module_var, width=80).pack(fill=tk.X, pady=2)

        # JSON 請求內容 (Payload 區域)，只有建立/修改時(POST)才會用到這區的資料
        ttk.Label(frame, text="JSON 請求資料 Payload (僅限 CREATE 情境):").pack(anchor=tk.W, pady=(10, 2))
        self.payload_text = tk.Text(frame, height=8, width=80, font=('Courier', 10))
        self.payload_text.pack(fill=tk.BOTH, expand=True, pady=2)
        
        # 自動產生預設的 12 組 25G 介面速度 JSON 資料
        default_payload = {"interface-group-speed-profile": [{"group-id": i + 1, "speed": "INTERFACE_GROUP_25G"} for i in range(12)]}
        self.payload_text.insert("1.0", json.dumps(default_payload, indent=4)) # 將 JSON 轉為格式化字串後寫入文字框
        
        # 執行動作按鈕區塊
        actions_frame = ttk.Frame(frame)
        actions_frame.pack(pady=10)
        
        # lambda 語法用於將參數傳遞給同一個功能函式 execute_request
        ttk.Button(actions_frame, text="查詢 (GET)", command=lambda: self.execute_request("GET")).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="建立 (CREATE - POST)", command=lambda: self.execute_request("POST")).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="刪除 (DELETE)", command=lambda: self.execute_request("DELETE")).pack(side=tk.LEFT, padx=5)
        
        # API 回應結果顯示區塊
        response_frame = ttk.Frame(frame)
        response_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        header_frame = ttk.Frame(response_frame)
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="API 回應結果 (Response):").pack(side=tk.LEFT)
        
        # 即時顯示 HTTP Status Code (狀態碼)
        self.status_var = tk.StringVar(value="尚未執行 (Idle)")
        self.status_label = ttk.Label(header_frame, textvariable=self.status_var, font=('Helvetica', 10, 'bold'), foreground='blue')
        self.status_label.pack(side=tk.RIGHT)
        
        # 顯示 API 回傳的完整內容，使用唯讀模式(DISABLED)避免誤改
        self.response_text = tk.Text(response_frame, height=8, width=80, state=tk.DISABLED, bg="#ffffff", fg="#000000", font=('Courier', 10))
        self.response_text.pack(fill=tk.BOTH, expand=True, pady=2)

    def fetch_token(self):
        """
        向 Aruba SSO 伺服器請求取得 JWT Access Token
        """
        client_id = self.client_id_var.get().strip()
        client_secret = self.client_secret_var.get().strip()

        # 防呆檢查：確保帳密都有輸入
        if not client_id or not client_secret:
            messagebox.showwarning("輸入錯誤 (Input Error)", "請輸入 Client ID 與 Client Secret。")
            return

        url = "https://sso.common.cloud.hpe.com/as/token.oauth2"
        # OAuth 2.0 Client Credentials 認證所需的 Payload
        payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        }

        # 發送請求前，鎖定按鈕並更新 UI 狀態
        self.get_token_btn.state(['disabled'])
        self.auth_status_var.set("正在請求取得 Token...")
        self.auth_status_label.config(foreground="blue")
        self.root.update_idletasks() # 強制刷新 UI
        
        try:
            # 透過 requests 套件發送 POST 請求
            response = requests.post(url, data=payload, headers=headers)
            
            # 若 HTTP 狀態碼為 200 (Success) 則開始解析 Token
            if response.status_code == 200:
                data = response.json()
                access_token = data.get("access_token", "")
                if access_token:
                    # 將取得的 token 寫入共享變數 (分頁 2 也會同步更新)
                    self.token_var.set(access_token)
                    self.auth_status_var.set("Token 產生成功！(你可以前往第二個分頁執行操作了)")
                    self.auth_status_label.config(foreground="green")
                else:
                    self.auth_status_var.set("回應內容中缺少 Token")
                    self.auth_status_label.config(foreground="red")
                    messagebox.showerror("錯誤 (Error)", "伺服器回應中沒有找到 'access_token' 欄位。")
            else:
                self.auth_status_var.set("取得 Token 失敗")
                self.auth_status_label.config(foreground="red")
                messagebox.showerror("錯誤 (Error)", f"無法取得 Token，狀態碼: {response.status_code}\n詳細錯誤: {response.text}")
        except Exception as e:
            # 捕捉網路連線異常等預期外的錯誤
            self.auth_status_var.set("連線至 SSO 伺服器發生異常")
            self.auth_status_label.config(foreground="red")
            messagebox.showerror("例外錯誤 (Exception)", f"發生了未知錯誤:\n{str(e)}")
        finally:
            # 不論成敗，最後都將按鈕解鎖
            self.get_token_btn.state(['!disabled'])

    def execute_request(self, method):
        """
        根據指定的 HTTP Method (GET, POST, DELETE) 對 Aruba API 發送對應的操作請求。
        """
        # 從共享變數中取得當前的 Token，若為空則阻擋操作
        token = self.token_var.get().strip()
        if not token:
            messagebox.showwarning("憑證遺失 (Token Missing)", "缺少 Token！請先回到「1. Authentication」分頁取得 Token。")
            return

        base_url = self.url_var.get().strip()
        
        # 確保網址結尾乾淨，若有斜線則移除，避免 API 路徑組合時產生雙斜線
        if base_url.endswith("/"):
            base_url = base_url[:-1]
            
        # 固定的 Aruba Hardware Modules API 進入點路徑
        api_path = "/network-config/v1alpha1/hardware-modules"

        # 根據不同的請求方法來決定最終網址
        # GET 是查詢所有清單，不需要特定名稱；POST/DELETE 是針對單一裝置，故需要加上 Profile Name
        if method in ["POST", "DELETE"]:
            module_name = self.module_var.get().strip()
            if not module_name:
                messagebox.showwarning("輸入錯誤 (Input Error)", "請在上方輸入硬體模組名稱 (Profile Name)。")
                return
            full_url = f"{base_url}{api_path}/{module_name}" # URL組合: Domain + Path + ProfileName
        else:
            full_url = f"{base_url}{api_path}" # URL組合: Domain + Path
            
        # 設定通用 HTTP 標頭
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {token}"
        }
        
        # 若為建立設定檔 (POST)，需要解析畫面上的 JSON 並加入封包
        payload_obj = None
        if method == "POST":
            headers["content-type"] = "application/json"
            payload_str = self.payload_text.get("1.0", tk.END).strip()
            try:
                # 嘗試將字串轉回 JSON 字典物件，若格式錯誤則報錯並中斷
                payload_obj = json.loads(payload_str)
            except json.JSONDecodeError as e:
                messagebox.showerror("JSON 格式錯誤", f"提供的 JSON Payload 格式有誤:\n{str(e)}")
                return
            
        # 更新 UI 顯示「正在發送」狀態
        self.status_var.set(f"正在發送 {method} 請求...")
        self.status_label.config(foreground="blue")
        self.root.update_idletasks()
        self.set_response_text("執行請求中...\n")
        
        try:
            # 依據傳入的 method 字串呼叫對應的 requests 模組函式
            if method == "GET":
                response = requests.get(full_url, headers=headers)
            elif method == "POST":
                response = requests.post(full_url, json=payload_obj, headers=headers)
            elif method == "DELETE":
                response = requests.delete(full_url, headers=headers)
            
            # 使用我們自訂的邏輯：只有 200 (OK) 時才顯示綠色，其餘一律顯示紅字警告
            if response.status_code == 200:
                self.status_var.set(f"{response.status_code} {response.reason}")
                self.status_label.config(foreground="green")
            else:
                self.status_var.set(f"{response.status_code} {response.reason}")
                self.status_label.config(foreground="red")
            
            # 嘗試優美地格式化(縮排)輸出的 JSON 回應文本
            try:
                # 若有的 API (如 DELETE 成功時) 會回傳空白，直接印出空白會讓畫面看起來像壞掉，所以加上判斷
                if response.text.strip():
                    json_res = response.json()
                    output = json.dumps(json_res, indent=4)
                else:
                    output = "(對方伺服器回傳了空內容)"
            except ValueError:
                # 若對方回傳的不是嚴謹的 JSON，則直接轉換成一般字串顯示
                output = response.text
                
            self.set_response_text(output)
            
        except requests.exceptions.RequestException as e:
            # 捕捉無法連線到伺服器等嚴重網路異常情況
            self.status_var.set("請求失敗 (Request Failed)")
            self.status_label.config(foreground="red")
            self.set_response_text(f"連線至 API 時發生錯誤:\n{str(e)}")

    def set_response_text(self, text):
        """
        處理 Text 區塊唯讀狀態下無法更新的問題，
        更新文字前先打開 (NORMAL)，清空並填入新字串後再鎖上 (DISABLED)。
        """
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert("1.0", text)
        self.response_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    # Tkinter 主視窗啟動點
    root = tk.Tk()
    app = ArubaNewCentralAPIConfigurator(root)
    root.mainloop()
