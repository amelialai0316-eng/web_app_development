# 路由設計 (Routes Design)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 計分引擎儀表板 | GET | `/calculator` | `calculator/index.html` | 顯示學分統計與 GPA 概況 |
| 新增課程頁面 | GET | `/calculator/add` | `calculator/add.html` | 顯示新增課程表單 |
| 執行新增課程 | POST | `/calculator/add` | — | 接收資料、計算學分、重導向回儀表板 |
| 編輯課程頁面 | GET | `/calculator/edit/<id>` | `calculator/edit.html` | 顯示編輯表單 |
| 執行更新課程 | POST | `/calculator/update/<id>` | — | 更新資料庫紀錄 |
| 執行刪除課程 | POST | `/calculator/delete/<id>` | — | 刪除紀錄並重導向 |
| 切換 GPA 制式 | POST | `/calculator/toggle-scale` | — | 切換 4.0/4.3 計算標準 |

---

## 2. 每個路由的詳細說明

### `GET /calculator`
- **處理邏輯**：從 DB 讀取所有 `Course` 紀錄。分別加總已完成、修習中、待修習學分。計算 4.3 與 4.0 GPA。
- **渲染模板**：`calculator/index.html`
- **傳遞數據**：`courses`, `total_credits`, `completed_credits`, `gpa_43`, `gpa_40`...

### `POST /calculator/add`
- **輸入**：`name`, `credits`, `category`, `status`, `score` (optional), `grade` (optional)。
- **處理邏輯**：
    1. 驗證資料。
    2. 若有 `score` 但無 `grade`，呼叫 `Course.score_to_grade()` 自動轉換。
    3. 調用 `Course.create()`。
- **輸出**：重導向至 `/calculator`。

### `POST /calculator/toggle-scale`
- **處理邏輯**：修改 Session 中的 `gpa_scale` 變數（4.0 或 4.3）。
- **輸出**：重導向回原頁面。

---

## 3. Jinja2 模板清單

| 模板檔案 | 繼承對象 | 說明 |
| :--- | :--- | :--- |
| `base.html` | — | 基礎佈局 (Header, Footer, CSS links) |
| `calculator/index.html` | `base.html` | 數據摘要儀表板與課程清單 |
| `calculator/add.html` | `base.html` | 新增課程的互動式表單 |
| `calculator/edit.html` | `base.html` | 編輯現有課程紀錄的表單 |

---

## 4. 路由骨架程式碼

- **路徑**：`app/routes/calculator.py`
- 定義 `calculator_bp` 並建立上述路由的函式定義。
