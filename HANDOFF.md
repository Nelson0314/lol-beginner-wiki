# 交接檔：英雄聯盟新手 LLM Wiki + 教學 HTML 簡報

新 session 從這裡開始。讀完本檔即可開工，不需要回看前一個對話。

## 作業要求（課程「AI 協作」第 N 週，期限 2026-11-23 23:59）

1. 建立一個主題的 LLM Wiki，「先討論、後生成」，至少 ingest 5 篇資料。
2. 讓 AI 只用 Wiki 當知識來源，產出教學型 HTML 簡報，讓完全不懂的人能理解。
3. 說明 loop / graph：取得資料 → 查 Wiki → 整理 → 檢查 → 產生簡報；哪些步驟重複、哪裡檢查或重生成、為什麼。
4. 實際執行一次並留下檢查紀錄；反思「哪個節點最常出錯、檢查往前移到哪一步、有沒有改 workflow」。
5. 繳交：Wiki 主題與介紹、Wiki 連結、簡報連結、流程圖或說明、執行／檢查紀錄、反思。
   標題格式：`交大 112511193 電機四 翁鈺翔 <主題>`。
6. 評分 9–10 分的條件：Wiki 與簡報內容明確對應、loop 設計合理、有實際執行與檢查紀錄、有反思、簡報教學結構清楚。

## 已討論並確定的決定（2026-11-14，這段即為「先討論」的紀錄，要寫進 wiki/log.md）

| 項目 | 決定 |
|------|------|
| 主題 | 英雄聯盟新手入門：遊戲介紹、選角規則與邏輯、各分路工作、出裝，以及其他新手應知事項 |
| 觀眾 | 完全沒玩過 MOBA 的人；從「這是什麼遊戲、怎樣算贏」講起 |
| 譯名 | 台服譯名（繁中），英文原名放括號 |
| 選角範圍 | 選角階段流程（禁用、輪流選角、交換、符文與召喚師技能）＋怎麼挑英雄（角色類型、新手推薦、陣容搭配：坦／輸出／控場）。不講克制與禁用策略 |
| 模式 | 只講召喚峽谷 5v5；其他模式最多一張投影片帶過 |
| 版本 | 使用者明確表示不需追版本號，內容大致正確即可。不做版本比對 |
| 版權 | 不使用官方英雄美術圖；地圖、分路等示意圖自行以 SVG 繪製 |
| 專案位置 | 新 repo `lol-beginner-wiki`（本資料夾），與前一份作業 `ee-study-notes` 分開；README 註明沿用其 `assets/js/core.js` 繪圖函式 |

## 候選來源（至少 ingest 5 篇）

1. 官方遊戲玩法（繁中）：https://leagueoflegends.com/zh-tw/how-to-play — 遊戲目標、地圖、經驗與金錢、台服譯名基準
2. 官方 26.1 更新說明（繁中）：https://www.leagueoflegends.com/zh-tw/news/game-updates/patch-26-1-notes/ — 定位任務（所有分路都有任務）、裝備調整
3. Mobalytics 新手指南：https://mobalytics.gg/blog/absolute-beginners-guide-to-league-of-legends/ — 分路職責、角色類型
4. Red Bull 新手技巧：https://www.redbull.com/ke-en/league-of-legends-beginner-tips-guide — 新手常見錯誤與習慣
5. League of Legends Wiki（Fandom）選角階段與裝備相關頁 — 選角流程、裝備分類
6. （可選）games.gg 26.1 中文解析：https://games.gg/zh-Hant/league-of-legends/guides/英雄聯盟-2026賽季261-版本更新全解析/

來源規則：遊戲機制以官方為準；第三方只用於「建議」類內容。每份來源在 `wiki/sources/` 一頁摘要（自行重寫，不整段複製）。

## 建議的檔案結構

```
lol-beginner-wiki/
├── AGENTS.md / CLAUDE.md   Wiki 與簡報的撰寫規則、檢查清單
├── wiki/
│   ├── index.md            頁面清單＋一句話摘要
│   ├── log.md              討論紀錄、每次 ingest、每次檢查結果與退回原因
│   ├── sources/            每份來源一頁
│   ├── concepts/           遊戲目標、地圖、兵線、經驗與金錢、視野、中立資源（小龍／巴龍／預示者）
│   ├── roles/              上路、打野、中路、射手、輔助
│   ├── draft/              選角流程、怎麼挑英雄
│   ├── items/              出裝邏輯、鞋子、消耗品
│   └── glossary.md         術語中英對照
├── slides/index.html       教學簡報（約 20–25 張；每張標註對應 Wiki 頁）
└── docs/ 或根目錄          GitHub Pages：Wiki 瀏覽頁 + 簡報
```

Wiki 頁的共同格式：frontmatter（title、sources、related）、內文、`## 來源` 段列出 sources/ 頁面、`## 相關頁面` 互相連結。

## Loop / graph 設計（初版，執行後依實際問題修訂並記錄於反思）

```
① 討論範圍 → ② 取得來源 → ③ 寫 Wiki 頁（標出處）
                 ▲              │
                 └── 不通過 ── ④ 交叉比對（官方 vs 第三方衝突、術語未定義、無出處的敘述）
                                │ 通過
                                ▼
⑤ 規劃簡報大綱（每張對應 Wiki 頁）→ ⑥ 產生投影片 → ⑦ 檢查
                 ▲                                  │
                 └──── 不通過：退回 ⑤ 或 ③ ─────────┘
⑦ 檢查：每個說法可追溯到 Wiki 頁、名詞首次出現有解釋、一張一重點、新手可讀
所有退回與修正都寫入 wiki/log.md（這就是繳交用的檢查紀錄）
```

反思素材預期：⑥→⑦ 最常出錯的是「投影片出現 Wiki 沒有的說法」或「用到未定義的術語」；可把「術語定義檢查」往前移到 ③（寫 Wiki 時就要求每個術語連到 glossary）、把「可追溯性」往前移到 ⑤（大綱階段就綁定 Wiki 頁）。實際以執行結果為準，不預先捏造。

## 待辦

1. 建 AGENTS.md / CLAUDE.md（規則與檢查清單）。
2. 把上方「已討論決定」寫成 wiki/log.md 第一筆。
3. 逐篇 ingest 來源（WebFetch），寫 sources/ 與概念頁，每篇 ingest 後在 log.md 記錄。
4. 執行 ④ 交叉比對並記錄結果。
5. 規劃大綱 → 產生簡報 → ⑦ 檢查 → 記錄退回與修正。
6. 使用者建立 GitHub repo `lol-beginner-wiki`（public）→ push → 開 Pages。
7. 截圖放桌面、產出繳交純文字（直接貼在對話中給使用者）。

## 使用者偏好（來自前一份作業）

- 繳交只要純文字（直接貼在對話）與截圖（直接放桌面），不要多餘檔案。
- 書面產出用客觀、精確的語氣；對話回覆精簡。
- 推上 GitHub、開 Pages 等對外動作，使用者已在前一份作業同意由 Claude 操作其已登入的 Chrome；新 repo 仍需使用者先建立。
- Windows 環境，Python 指令為 `python`；PDF 無法用 Read 渲染時改用 pypdf；截圖可用 Playwright（已安裝）＋本機 Chrome。
