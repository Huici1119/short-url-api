#  Short URL API 規格說明

此 API 提供短網址產生與轉址功能(使用Python)，其中包含兩個主要端點：

1. 建立短網址（POST /shorten）
2. 透過短網址自動轉址（GET /\<short\_id>）

---

##  API 1：GetShortURL（建立短網址）

此 API 用於產生短網址。

---

##  請求資訊

| 序號 | 名稱            | 說明  | 資料型別   | 備註 |
| -- | ------------- | --- | ------ | -- |
| 1  | original\_url | 長網址 | String | 必填 |

---

##  回應資訊

| 序號 | 名稱               | 說明   | 資料型別     | 備註                                     |
| -- | ---------------- | ---- | -------- | -------------------------------------- |
| 1  | short_url       | 短網址  | String   | 自動產生的短網址                               |
| 2  | expiration_date | 存活天數 | DateTime | 預設為產生日起算 30 天                          |
| 3  | success          | 是否成功 | Boolean  | 成功：`true`，失敗：`false`                   |
| 4  | reason           | 錯誤描述 | String   | 當 `success=false` 時，提供失敗原因（如格式錯誤、缺欄位等） |

---


###  說明

* `expiration_date` 預設為建立時間後 30 天
* Rate limit：每個 IP 每分鐘最多 5 次使用(預防濫用)

---

##  舉例

### 請求資訊

```json
{
  "original_url": "https://ithelp.ithome.com.tw/articles/10276184"
}

```

###  回應資訊(成功)

```json
{
  "short_url": "http://localhost:5550/1",
  "expiration_date": "2025-06-07T13:00:00",
  "success": true,
  "reason": ""
}

```

###  回應資訊(失敗)

* 缺少 original_url：

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

##  失敗原因

| 序號 | 原因            | 說明 | 狀態碼 |
| -- | ---------------- | ------------------------ | ---- |
| 1  | 無輸入值      | Missing 'original_url'  | 400 |
| 2  | 格式非Url | Invalid URL format | 400 |
| 3  | 長度超過2048          | URL too long | 400 |

---

##  API 2：Redirect Short URL（使用短網址轉址）

此 API 用於使用生成之短網址轉載至原網址。

---

##  請求資訊

| 序號 | 名稱        | 說明     | 資料型別 | 備註                    |
| -- | --------- | ------ | ---- | --------------------- |
| 1  | short_id | 短網址 ID | Path | 必填，於網址路徑中提供 `/1` 這種格式 |

---

##  回應行為與資訊

| 狀態碼 | 說明     | 回應內容                               |
| --- | ------ | ---------------------------------- |
| 302 | 成功轉址   | HTTP 重導向，無回傳 JSON                  |
| 404 | 短網址不存在 | `{ "error": "Invalid short URL" }` |
| 410 | 短網址已過期 | `{ "error": "Short URL expired" }` |

---

###  說明

* 短網址超過30天即過期
* 每個 IP 每分鐘最多 5 次使用，超過會回應"處理請求時發生錯誤，請稍後再試。"

---

##  舉例

### 錯誤回應

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

##  狀態碼一覽

| 狀態碼 | 說明          |
| --- | ----------- |
| 201 | 成功建立短網址     |
| 400 | 請求格式錯誤／缺少欄位 |
| 404 | 找不到對應的短網址   |
| 410 | 短網址已過期      |



