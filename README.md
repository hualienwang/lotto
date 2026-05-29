# 台灣彩券539開獎系統

一個現代化的台灣彩券539開獎資訊系統，提供開獎結果查詢、號碼預測及數據分析功能。

## 技術架構

### 前端
- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **State Management**: Pinia
- **Router**: Vue Router
- **HTTP Client**: Axios

### 後端
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: SQLite3

## 專案結構

```
lotto539/
├── backend/                 # Python 後端
│   ├── main.py             # FastAPI 主程式
│   ├── models.py           # SQLModel 資料模型
│   ├── database.py         # 資料庫配置
│   ├── requirements.txt    # Python 依賴
│   └── lotto.db            # SQLite 資料庫
│
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── components/    # 共用元件
│   │   ├── views/         # 頁面元件
│   │   ├── stores/        # Pinia 狀態管理
│   │   ├── services/     # API 服務
│   │   ├── router/        # 路由配置
│   │   └── assets/        # 靜態資源
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
└── data/
    └── lotto539_data.json  # 初始資料
```

## 功能特色

### 🔍 最新開獎
- 顯示最新一期開獎結果
- 清晰呈現五個中獎號碼

### 📈 歷次開獎
- 完整開獎歷史記錄
- 支援日期區間篩選
- 表格化呈現

### 🔮 號碼預測
- 根據歷史開獎數據進行大數據分析
- 計算熱門號碼
- 產生預測號碼組合

### 📊 數據分析
- 單數/雙數統計
- 號碼區間分布 (1-10, 11-20, 21-30, 31-39)

### ⚙️ 管理系統
- 新增開獎結果
- 資料管理

## 安裝與執行

### 前置需求
- Python 3.10+
- Node.js 18+

### 後端安裝

```bash
# 進入後端目錄
cd backend

# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 啟動伺服器
python main.py
```

伺服器將在 `http://localhost:8000` 啟動

### 前端安裝

```bash
# 進入前端目錄
cd frontend

# 安裝依賴
npm install

# 啟動開發伺服器
npm run dev
```

前端將在 `http://localhost:5173` 啟動

###  production 建置

```bash
cd frontend
npm run build
```

產生的檔案會在 `dist/` 目錄中

## API 端點

| 端點 | 方法 | 說明 |
|------|------|------|
| `/api/results` | GET | 取得開獎結果列表 |
| `/api/results/latest` | GET | 取得最新開獎結果 |
| `/api/results` | POST | 新增開獎結果 |
| `/api/prediction` | GET | 取得預測號碼 |
| `/api/prediction` | POST | 儲存預測 |
| `/api/statistics` | GET | 取得統計數據 |

## 開發說明

### 後端 API 開發
後端使用 FastAPI 框架，所有路由定義在 `main.py` 中。

### 前端開發
前端使用 Vue 3 Composition API，所有頁面元件在 `views/` 目錄中。

### 資料庫
系統使用 SQLite3 作為資料庫，自動從 `lotto539_data.json` 載入初始資料。

## 授權

MIT License
