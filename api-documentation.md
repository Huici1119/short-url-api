#  Short URL API 文件說明

此 API 提供短網址產生與轉址功能(使用Python)，其中包含兩個主要端點：

1. 建立短網址（POST /shorten）
2. 透過短網址自動轉址（GET /\<short\_id>）

---

##  API 1：建立短網址

###  Endpoint

```
POST /shorten
```

###  請求格式（JSON）

```json
{
  "original_url": "https://example.com"
}
```

###  回應格式（成功）

```json
{
  "short_url": "http://localhost:5550/1",
  "expiration_date": "2025-06-07T13:00:00",
  "success": true,
  "reason": ""
}
```

###  回應格式（失敗）

* 缺少 `original_url`：

```json
{
  "short_url": "",
  "expiration_date": "",
  "success": false,
  "reason": "Missing 'original_url'"
}
```

* URL 格式不正確：

```json
{
  "short_url": "",
  "expiration_date": "",
  "success": false,
  "reason": "Invalid URL format"
}
```

* URL 長度超過限制：

```json
{
  "short_url": "",
  "expiration_date": "",
  "success": false,
  "reason": "URL too long"
}
```

###  說明

* `expiration_date` 預設為建立時間後 30 天
* Rate limit：每個 IP 每分鐘最多 5 次使用(預防濫用)

---

##  API 2：使用短網址轉址（Redirect Short URL）

###  Endpoint

```
GET /<short_id>
```

###  行為說明

* 若 `short_id` 有效且未過期，將自動轉址到對應 `original_url`
* 若 `short_id` 不存在，回傳 404
* 若網址已過期，回傳 410

###  錯誤回應

* 無效短網址：

```json
{
  "error": "Invalid short URL"
}
```

* 已過期：

```json
{
  "error": "Short URL expired"
}
```

---

##  測試建議

###  建立短網址

```bash
curl -X POST http://localhost:5550/shorten \
     -H "Content-Type: application/json" \
     -d '{"original_url": "https://example.com"}'
```

###  點擊短網址測試轉址

```
http://localhost:5550/1
```

---

##  狀態碼一覽

| 狀態碼 | 說明          |
| --- | ----------- |
| 201 | 成功建立短網址     |
| 400 | 請求格式錯誤／缺少欄位 |
| 404 | 找不到對應的短網址   |
| 410 | 短網址已過期      |

