# 路由設計文件 (ROUTES)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁 / 儀表板** | GET | `/` | `index.html` | 顯示閱讀統計（總量、平均評分）與最近筆記 |
| **書單列表** | GET | `/books` | `books/list.html` | 顯示所有書目，支援分類與評分篩選 |
| **新增書籍頁面** | GET | `/books/create` | `books/create.html` | 顯示新增書籍的表單 |
| **建立書籍** | POST | `/books/create` | — | 接收表單、驗證並存入資料庫後重導向至書單 |
| **書籍詳情** | GET | `/books/<id>` | `books/detail.html` | 顯示單一書籍的詳細資訊、評分與相關心得 |
| **編輯書籍頁面** | GET | `/books/<id>/edit` | `books/edit.html` | 顯示書籍編輯表單（帶入既有資料） |
| **更新書籍** | POST | `/books/<id>/edit` | — | 接收編輯表單、更新資料庫後重導向至詳情頁 |
| **刪除書籍** | POST | `/books/<id>/delete` | — | 刪除書籍及其關聯的心得與標籤關聯 |
| **新增心得頁面** | GET | `/books/<id>/notes/create` | `notes/create.html` | 顯示為特定書籍新增心得的表單 |
| **建立心得** | POST | `/books/<id>/notes/create` | — | 接收心得內容與金句，存入資料庫 |
| **編輯心得頁面** | GET | `/notes/<id>/edit` | `notes/edit.html` | 顯示心得編輯表單 |
| **更新心得** | POST | `/notes/<id>/edit` | — | 更新特定心得內容 |
| **刪除心得** | POST | `/notes/<id>/delete` | — | 刪除單筆心得 |
| **分類管理頁面** | GET | `/categories` | `categories/list.html` | 顯示所有分類與新增分類表單 |
| **建立分類** | POST | `/categories/create` | — | 接收分類名稱與顏色，存入資料庫 |
| **刪除分類** | POST | `/categories/<id>/delete` | — | 刪除分類（受保護操作，避免誤刪） |
| **搜尋結果** | GET | `/search` | `search/results.html` | 根據關鍵字 `q` 進行跨欄位模糊搜尋 |

## 2. 路由詳細說明

### 2.1 書籍模組 (`/books`)
- **GET `/books`**:
    - 輸入：`category` (選填), `rating` (選填), `sort` (選填)。
    - 邏輯：呼叫 `Book.get_all()` 並套用篩選。
- **POST `/books/create`**:
    - 輸入：書名、作者、出版年份、ISBN、封面 URL、分類、狀態。
    - 處理：使用 `BookForm` 驗證，呼叫 `Book.create()`。
    - 錯誤：驗證失敗則重新渲染 `books/create.html` 並顯示錯誤。

### 2.2 心得模組 (`/notes`)
- **POST `/books/<id>/notes/create`**:
    - 輸入：心得內容、重點摘錄、開始/結束日期。
    - 處理：呼叫 `Note.create(book_id=id, ...)`。
    - 輸出：重導向至 `books/detail.html`。

### 2.3 搜尋模組 (`/search`)
- **GET `/search?q=...`**:
    - 輸入：`q` (關鍵字)。
    - 邏輯：查詢 `Book.title`、`Book.author` 與 `Note.content` 包含 `q` 的結果。

## 3. Jinja2 模板清單

所有模板皆繼承 `base.html`。

- `base.html`: 包含導覽列、搜尋框與 flash 訊息區域。
- `index.html`: 儀表板。
- `books/list.html`: 書單。
- `books/detail.html`: 書籍詳情與心得列表。
- `books/create.html`: 新增書籍。
- `books/edit.html`: 編輯書籍。
- `notes/create.html`: 新增心得。
- `notes/edit.html`: 編輯心得。
- `categories/list.html`: 分類管理與新增。
- `search/results.html`: 搜尋結果顯示。

## 4. 路由骨架程式碼

已在 `app/routes/` 建立對應的 Blueprint：
- `main.py`
- `books.py`
- `notes.py`
- `categories.py`
- `search.py`
