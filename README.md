# 部署測試專案

這是一個簡單的全端應用程式，用於測試 Docker Compose 部署，包含：
- 前端：Nuxt.js (Vue 3)
- 後端：FastAPI (Python)
- 資料庫：MongoDB

## 功能特色

- 簡易的任務管理系統
- 前後端 API 連接測試
- MongoDB 資料庫交互
- 響應式 UI 設計

## 快速開始

### 1. 設定環境變數

確保 `.env` 檔案中的變數設定正確：

```env
DB_USERNAME=admin
DB_PASSWORD=password123
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
```

### 2. 啟動所有服務

```bash
docker-compose up --build
```

### 3. 訪問應用程式

- 前端：http://localhost:3000
- 後端 API：http://localhost:80
- API 文檔：http://localhost:80/docs
- MongoDB：localhost:27017

## API 端點

### 健康檢查
- `GET /` - 基本狀態檢查
- `GET /health` - 詳細健康檢查

### 任務管理
- `GET /tasks` - 取得所有任務
- `POST /tasks` - 新增任務
- `PUT /tasks/{task_id}` - 更新任務
- `DELETE /tasks/{task_id}` - 刪除任務

## 專案結構

```
deploy_test/
├── docker-compose.yaml    # Docker Compose 配置
├── .env                   # 環境變數
├── frontend/              # Nuxt.js 前端
│   ├── Dockerfile
│   ├── package.json
│   ├── nuxt.config.ts
│   ├── app.vue
│   └── assets/css/main.css
└── backend/               # FastAPI 後端
    ├── Dockerfile
    ├── requirements.txt
    └── main.py
```

## 測試功能

1. **API 連線測試**：點擊「檢查 API 連線」按鈕
2. **新增任務**：填寫表單新增任務到資料庫
3. **任務管理**：標記完成/未完成、刪除任務
4. **資料持久化**：重啟容器後資料仍然存在

## 故障排除

### 如果前端無法連接後端：
1. 確認所有容器都在運行：`docker-compose ps`
2. 檢查後端日誌：`docker-compose logs backend`
3. 確認防火牆設定

### 如果資料庫連接失敗：
1. 檢查 MongoDB 容器狀態：`docker-compose logs mongodb`
2. 確認環境變數設定正確
3. 等待 MongoDB 完全啟動（可能需要幾分鐘）

## 停止服務

```bash
docker-compose down
```

如需清除所有資料（包含資料庫）：

```bash
docker-compose down -v
```
