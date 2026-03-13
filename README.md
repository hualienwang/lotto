# 台灣彩券539開獎系統 (Lotto 539 System)

[![Node.js](https://img.shields.io/badge/Node.js-18.x-green.svg)](https://nodejs.org/)
[![Express](https://img.shields.io/badge/Express-4.18.x-blue.svg)](https://expressjs.com/)
[![SQLite3](https://img.shields.io/badge/SQLite-3-yellow.svg)](https://www.sqlite.org/)

一個基於 Node.js 和 Express 建構的台灣彩券539開獎號碼管理系統，提供開獎結果查詢、號碼預測及統計分析功能。

## 功能特色

- 📊 **開獎結果管理** - 查詢、新增台灣彩券539開獎號碼
- 🔮 **號碼預測** - 根據歷史開獎資料分析熱門號碼
- 📈 **統計分析** - 號碼出現頻率、奇偶比、區間分佈
- 🌐 **RESTful API** - 完整的 API 介面供前端呼叫
- 💾 **SQLite 資料庫** - 輕量級本地資料儲存

## 技術棧

| 技術 | 版本 | 說明 |
|------|------|------|
| Node.js | 18.x+ | JavaScript 執行環境 |
| Express | ^4.18.2 | Web 框架 |
| SQLite3 | ^5.1.6 | 嵌入式資料庫 |
| CORS | ^2.8.5 | 跨域資源共享 |

## 專案結構

```
lotto/
├── public/
│   └── index.html      # 前端網頁介面
├── server.js           # 主伺服器檔案
├── lotto.db            # SQLite 資料庫檔案
├── package.json        # 專案配置
└── README.md           # 使用說明文件
```

## 安裝與執行

### 前置需求

- Node.js 18.x 或更高版本
- npm 或 yarn

### 安裝步驟

```bash
# 1. 安裝相依套件
npm install

# 2. 啟動伺服器
npm start
```

伺服器將於 `http://localhost:3000` 啟動。

### 開發模式

```bash
npm run dev
```

## API 文件

### 1. 取得所有開獎結果

```http
GET /api/results
```

**回應範例：**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "period": "1150312",
      "numbers": "05, 12, 18, 25, 33",
      "draw_date": "2026-03-12",
      "created_at": "2026-03-12 10:00:00"
    }
  ]
}
```

### 2. 取得最新開獎結果

```http
GET /api/results/latest
```

### 3. 新增開獎結果

```http
POST /api/results
Content-Type: application/json

{
  "period": "1150313",
  "numbers": "03, 07, 14, 22, 38",
  "draw_date": "2026-03-13"
}
```

### 4. 取得號碼預測

```http
GET /api/prediction
```

**回應範例：**
```json
{
  "success": true,
  "data": {
    "numbers": "05, 12, 18, 25, 33",
    "analysis": {
      "hot_numbers": [5, 12, 18, 25, 33, ...],
      "frequency": { "5": 15, "12": 12, ... }
    }
  }
}
```

### 5. 儲存預測

```http
POST /api/prediction
Content-Type: application/json

{
  "period": "1150313",
  "numbers": "05, 12, 18, 25, 33"
}
```

### 6. 取得統計資料

```http
GET /api/statistics
```

**回應範例：**
```json
{
  "success": true,
  "data": {
    "frequency": { "1": 15, "2": 12, ... },
    "oddEven": { "odd": 250, "even": 200 },
    "ranges": { "1-10": 120, "11-20": 110, "21-30": 130, "31-39": 90 }
  }
}
```

## 資料庫架構

### lottery_results 資料表

| 欄位 | 類型 | 說明 |
|------|------|------|
| id | INTEGER | 主鍵 ID |
| period | TEXT | 開獎期別 (民國年+月日) |
| numbers | TEXT | 開獎號碼 (5個號碼逗號分隔) |
| draw_date | TEXT | 開獎日期 |
| created_at | TEXT | 資料建立時間 |

### predictions 資料表

| 欄位 | 類型 | 說明 |
|------|------|------|
| id | INTEGER | 主鍵 ID |
| period | TEXT | 預測期別 |
| numbers | TEXT | 預測號碼 |
| created_at | TEXT | 資料建立時間 |

## 開獎規則 (台灣彩券539)

- 每期開獎 5 個號碼（範圍 1-39）
- 號碼不重複
- 週日不開獎

## 環境變數

目前無需額外環境變數配置。如需自訂連接埠，可修改 [`server.js`](server.js:7) 中的 `PORT` 常數：

```javascript
const PORT = 3000; // 可自訂連接埠
```

## 授權

MIT License

---

如有問題或建議，歡迎提交 Issue 或 Pull Request。
