# GitBook Docker 部署說明

本專案提供了 Docker 容器化部署方案，支援生產環境和開發環境兩種部署模式。

## 快速開始

### 前置需求

- Docker
- Docker Compose

### 生產環境部署

1. **構建並啟動容器**
```bash
docker-compose up -d
```

2. **訪問應用**
```
http://localhost:8080
```

### 開發環境部署

1. **啟動開發環境**
```bash
docker-compose --profile dev up -d gitbook-dev
```

2. **訪問開發環境**
```
http://localhost:4000
```

開發環境支援即時重載，修改檔案後會自動重新構建。

## 詳細配置說明

### 檔案結構

```
├── Dockerfile              # 生產環境 Docker 檔案（精簡版）
├── Dockerfile.full         # 生產環境 Docker 檔案（完整版，含 canvas）
├── Dockerfile.dev          # 開發環境 Docker 檔案
├── docker-compose.yml      # Docker Compose 配置
├── nginx.conf              # Nginx 配置檔案
├── package.docker.json     # 精簡版依賴清單（不含 canvas）
└── .dockerignore           # Docker 忽略檔案清單
```

### 兼容性問題解決方案

#### Node.js 版本兼容性
- 使用 **Node.js 12** 而非較新版本，因為 GitBook 3.2.3 與 Node.js 16+ 不相容
- 自動修復 `graceful-fs` 兼容性問題
- 確保所有 GitBook 插件正常運行

#### Canvas 依賴問題解決方案
由於 `canvas` 套件在 Alpine Linux 中需要大量系統依賴和編譯工具，我們提供了兩個版本：

1. **精簡版** (`Dockerfile`): 移除了 canvas 依賴，構建速度快，映像體積小
2. **完整版** (`Dockerfile.full`): 包含所有依賴，支援 canvas 功能

#### 如何選擇版本

- 如果您的 GitBook 不需要 canvas 功能（大多數情況），建議使用精簡版
- 如果您的插件或自定義功能需要 canvas，請使用完整版

#### 使用精簡版（推薦）
```bash
docker-compose up -d gitbook
```
訪問 `http://localhost:8080`

#### 使用完整版
```bash
docker-compose --profile full up -d gitbook-full
```
訪問 `http://localhost:8081`

### 生產環境架構

- **多階段構建**: 使用 Node.js 構建 GitBook，然後使用 Nginx 提供靜態檔案
- **效能優化**: 啟用 gzip 壓縮和檔案快取
- **安全性**: 設定了基本的安全標頭

### 開發環境特性

- **即時重載**: 支援檔案變更的即時預覽
- **熱重載**: GitBook serve 模式，修改檔案自動重新構建
- **容量掛載**: 本地檔案直接掛載到容器，無需重新構建映像

## 常用指令

### 基本操作

```bash
# 啟動生產環境
docker-compose up -d

# 啟動開發環境
docker-compose --profile dev up -d gitbook-dev

# 停止所有服務
docker-compose down

# 查看日誌
docker-compose logs gitbook

# 重新構建映像
docker-compose build
```

### 維護指令

```bash
# 清理未使用的映像
docker image prune -f

# 清理未使用的容器
docker container prune -f

# 重新構建並啟動
docker-compose up -d --build
```

## 環境變數配置

可以透過 `.env` 檔案設定環境變數：

```bash
# .env 檔案範例
GITBOOK_PORT=8080
NGINX_HOST=localhost
NODE_ENV=production
```

## 故障排除

### 常見問題

1. **容器無法啟動**
   ```bash
   # 檢查容器狀態
   docker-compose ps
   
   # 查看詳細日誌
   docker-compose logs gitbook
   ```

2. **端口被佔用**
   ```bash
   # 修改 docker-compose.yml 中的端口映射
   ports:
     - "8081:80"  # 改為其他可用端口
   ```

3. **GitBook 插件安裝失敗**
   ```bash
   # 進入容器手動安裝
   docker-compose exec gitbook sh
   gitbook install
   ```

### 效能調優

1. **記憶體限制**
   ```yaml
   services:
     gitbook:
       deploy:
         resources:
           limits:
             memory: 512M
   ```

2. **CPU 限制**
   ```yaml
   services:
     gitbook:
       deploy:
         resources:
           limits:
             cpus: '0.5'
   ```

## 部署到其他環境

### Docker Swarm

```bash
# 初始化 Swarm
docker swarm init

# 部署服務堆疊
docker stack deploy -c docker-compose.yml gitbook
```

### Kubernetes

請參考 `kubernetes/` 目錄下的 YAML 配置檔案。

## 安全性考量

1. **更新基礎映像**: 定期更新 Node.js 和 Nginx 基礎映像
2. **掃描漏洞**: 使用 `docker scan` 或其他工具掃描映像漏洞
3. **非 root 用戶**: 在生產環境中考慮使用非 root 用戶運行容器

## 支援與貢獻

如有問題或建議，請提交 Issue 或 Pull Request。

## 授權

本專案採用 MIT 授權條款，詳見 LICENSE 檔案。
