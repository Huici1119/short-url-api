# 短網址產生器 - URL Shortener（SQLite）

這是一個以 **Flask + SQLite** 為基礎的短網址服務，支援：

* 使用者輸入原始網址，自動轉換成短網址
* 30 天自動過期
* URL 長度與格式驗證
* 頻率限制（每分鐘 5 次）
* 使用 SQLite 本地資料庫，無需額外安裝 MySQL
* Docker 容器打包，可透過 Docker Compose 一鍵啟動

---

## 專案啟動方式（使用 Docker）

### 1 安裝 Docker 與 Docker Compose

請至 [Docker 官網](https://www.docker.com/products/docker-desktop) 安裝 Docker Desktop，並確認終端機可執行：

```bash
docker --version
docker-compose --version
```

### 2 專案結構確認

```
shorten-url/
├── shortenUrl.py
├── templates/
│   └── index.html
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
```

### 3 啟動服務

```bash
# 建構並啟動 Flask + SQLite
docker-compose up --build
```

啟動成功後，您可透過瀏覽器進入：

```
http://localhost:5550/
```

---

##  API 測試方式

您也可以使用 **postman** 測試 `POST/shorten` API：

### 請求設定：

* **方法**:POST
* **URL**:`http://localhost:5550/shorten`
* **Headers**:
  *`content-type`:`application/json`
* **Body**:選擇`raw`格式並填入JSON，如:

```json
{
  "original_url":"https://www.google.com/search?q=%E8%82%8C%E5%B0%91%E7%97%87&sca_esv=b5b85f1110a5fb0d&rlz=1C1GCEU_zh-twTW1161&sxsrf=AHTn8zr-hW3CtTlLhME6JIK2YpP4k03e_A%3A1746646872570&ei=WLcbaKnNIvWi1e8Pt-KkwQo&oq=%E5%9F%BA%E5%B0%91%E6%94%BF&gs_lp=Egxnd3Mtd2l6LXNlcnAiCeWfuuWwkeaUvyoCCAAyChAAGLADGNYEGEcyChAAGLADGNYEGEcyChAAGLADGNYEGEcyChAAGLADGNYEGEcyChAAGLADGNYEGEcyChAAGLADGNYEGEcyChAAGLADGNYEGEcyChAAGLADGNYEGEcyChAAGLADGNYEGEcyChAAGLADGNYEGEdI7jtQ5QtYijpwCXgBkAEAmAE_oAGIBaoBAjEyuAEByAEA-AEBmAISoALUBagCAMICChAjGIAEGCcYigXCAgUQABiABMICCBAAGIAEGKIEwgILEC4YgAQYsQMYgwHCAgsQABiABBixAxiDAcICDhAuGIAEGLEDGMcBGK8BwgIIEAAYgAQYsQPCAg4QABiABBixAxiDARiKBcICCBAuGIAEGLEDwgILEC4YgAQYsQMY1ALCAhEQLhiABBixAxjRAxiDARjHAcICGhAuGIAEGLEDGIMBGJcFGNwEGN4EGOAE2AEBwgIXEC4YgAQYsQMYlwUY3AQY3gQY4ATYAQHCAgUQLhiABMICDhAuGIAEGMcBGI4FGK8BwgIIEC4YgAQY1ALCAgsQLhiABBjHARivAcICBRAAGO8FwgIIEAAYogQYiQWYAwHxBRhVjfNmK0wBiAYBkAYKugYGCAEQARgUkgcCMTigB5FhsgcCMTK4B74F&sclient=gws-wiz-serp"
}
```

### 預期結果:

```json
{
  "short_url":"http://localhost:5550/1",
  "expiration_date":"2025-05-08T03:43:52",
  "success":true,
  "reason":""
}
```

---

##  停止與清除容器

### 暫時停止（保留資料）

```bash
docker-compose down
```

### 停止並刪除資料（含 SQLite 檔案）

```bash
docker-compose down -v
```

>  SQLite 資料會儲存在容器內部，如需保留請使用 volume 映射或將 `.db` 匯出

---
