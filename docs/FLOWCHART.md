# 讀書筆記本 系統 — 流程圖文件（FLOWCHART）

**版本：** v1.0  
**撰寫日期：** 2026-04-15  
**對應文件：** docs/PRD.md v1.0、docs/ARCHITECTURE.md v1.0

---

## 1. 使用者流程圖（User Flow）

> 描述使用者從進入網站到完成各項操作的完整路徑。

```mermaid
flowchart LR
    A([🌐 使用者開啟網頁]) --> B[首頁 / 儀表板\n閱讀統計 & 近期筆記]

    B --> C{選擇操作}

    %% ── 書籍管理 ──
    C -->|查看書單| D[書單列表頁\n全部書籍]
    D --> E{書單操作}
    E -->|新增書籍| F[填寫書籍表單\n書名、作者、分類…]
    F --> F1{表單驗證}
    F1 -->|通過| F2[儲存至資料庫] --> D
    F1 -->|失敗| F3[顯示錯誤提示] --> F

    E -->|點擊書籍| G[書籍詳情頁\n心得 & 評分]
    G --> H{詳情頁操作}
    H -->|編輯書籍| I[編輯書籍表單] --> F1
    H -->|刪除書籍| J{確認刪除？}
    J -->|確認| K[從資料庫刪除] --> D
    J -->|取消| G

    %% ── 心得筆記 ──
    H -->|新增 / 編輯心得| L[心得編輯頁\n文字輸入 + 金句摘錄]
    L --> L1{表單驗證}
    L1 -->|通過| L2[儲存心得] --> G
    L1 -->|失敗| L3[顯示錯誤] --> L

    %% ── 評分 ──
    H -->|點選星星評分| M[更新評分 1–5 顆星] --> G

    %% ── 分類管理 ──
    C -->|管理分類| N[分類列表頁]
    N --> N1{分類操作}
    N1 -->|新增分類| N2[填寫分類名稱] --> N
    N1 -->|刪除分類| N3{確認刪除？} -->|確認| N4[刪除分類] --> N

    %% ── 搜尋 ──
    C -->|輸入關鍵字搜尋| O[輸入搜尋關鍵字]
    O --> P[搜尋結果頁\n符合的書籍列表]
    P -->|點擊結果| G

    %% ── 篩選 ──
    D -->|依分類 / 評分篩選| Q[套用篩選條件] --> D
```

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 新增書籍

> 描述使用者填寫書籍表單、送出，到資料成功儲存並導回書單的完整系統互動。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route<br/>(books.py)
    participant Model as Book Model<br/>(SQLAlchemy)
    participant DB as SQLite

    User->>Browser: 點擊「新增書籍」
    Browser->>Flask: GET /books/create
    Flask-->>Browser: 回傳空白表單 (create.html)

    User->>Browser: 填寫書名、作者、分類等欄位並送出
    Browser->>Flask: POST /books/create

    Flask->>Flask: 驗證表單（Flask-WTF）

    alt 驗證失敗
        Flask-->>Browser: 重新渲染表單 + 錯誤訊息
        Browser-->>User: 顯示錯誤提示
    else 驗證通過
        Flask->>Model: Book(**form_data)
        Model->>DB: INSERT INTO books (...)
        DB-->>Model: 回傳新 book.id
        Model-->>Flask: 成功
        Flask-->>Browser: redirect → GET /books
        Browser-->>User: 顯示書單列表（含新書）
    end
```

---

### 2.2 關鍵字搜尋

> 描述使用者輸入關鍵字，系統跨欄位查詢並回傳結果的流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route<br/>(search.py)
    participant Model as Book / Note Model
    participant DB as SQLite

    User->>Browser: 在搜尋框輸入關鍵字並送出
    Browser->>Flask: GET /search?q=關鍵字

    Flask->>Model: 查詢 Book.title LIKE '%q%'<br/>OR Book.author LIKE '%q%'<br/>OR Note.content LIKE '%q%'
    Model->>DB: SELECT ... WHERE ... LIKE ...
    DB-->>Model: 回傳符合資料列

    alt 有結果
        Model-->>Flask: 書籍列表
        Flask-->>Browser: 渲染 search/results.html（有結果）
        Browser-->>User: 顯示搜尋結果列表
    else 無結果
        Model-->>Flask: 空列表
        Flask-->>Browser: 渲染 search/results.html（無結果）
        Browser-->>User: 顯示「找不到相關書籍」
    end
```

---

### 2.3 刪除書籍

> 描述使用者確認刪除後，系統從資料庫移除書籍及相關心得的流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route<br/>(books.py)
    participant Model as Book Model
    participant DB as SQLite

    User->>Browser: 點擊「刪除」按鈕
    Browser-->>User: 顯示 JavaScript 確認對話框

    alt 使用者取消
        User->>Browser: 點擊「取消」
        Browser-->>User: 停留在書籍詳情頁
    else 使用者確認
        User->>Browser: 點擊「確認刪除」
        Browser->>Flask: POST /books/<id>/delete

        Flask->>Model: Book.query.get(id)
        Model->>DB: DELETE FROM notes WHERE book_id = id
        Model->>DB: DELETE FROM books WHERE id = id
        DB-->>Model: 成功

        Flask-->>Browser: redirect → GET /books
        Browser-->>User: 顯示書單列表（書籍已移除）
    end
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | 對應說明 |
|---|---|---|---|
| 首頁 / 儀表板 | `/` | GET | 顯示閱讀統計與近期筆記 |
| 書單列表 | `/books` | GET | 顯示所有書籍（支援分類篩選）|
| 新增書籍表單 | `/books/create` | GET | 顯示空白新增表單 |
| 儲存新書籍 | `/books/create` | POST | 驗證並儲存書籍至資料庫 |
| 書籍詳情 | `/books/<id>` | GET | 顯示書籍詳情、心得、評分 |
| 編輯書籍表單 | `/books/<id>/edit` | GET | 顯示預填編輯表單 |
| 更新書籍 | `/books/<id>/edit` | POST | 驗證並更新書籍資料 |
| 刪除書籍 | `/books/<id>/delete` | POST | 刪除書籍及其心得 |
| 新增心得 | `/books/<id>/notes/create` | GET / POST | 新增閱讀心得 |
| 編輯心得 | `/notes/<id>/edit` | GET / POST | 編輯既有心得 |
| 刪除心得 | `/notes/<id>/delete` | POST | 刪除單筆心得 |
| 分類列表 | `/categories` | GET | 顯示所有分類 |
| 新增分類 | `/categories/create` | POST | 新增分類 |
| 刪除分類 | `/categories/<id>/delete` | POST | 刪除分類 |
| 關鍵字搜尋 | `/search?q=<keyword>` | GET | 全文搜尋書名、作者、心得 |

---

*本文件依據 PRD v1.0 與 ARCHITECTURE v1.0 產出，若功能頁面有異動，請同步更新本流程圖與對照表。*
