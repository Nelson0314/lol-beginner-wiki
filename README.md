# 英雄聯盟新手 LLM Wiki 與教學簡報

以 LLM 協作建立的英雄聯盟新手入門 Wiki，並只以此 Wiki 為知識來源產生教學型 HTML 簡報。對象為完全沒玩過 MOBA 的人；範圍限召喚峽谷 5v5。

- Wiki 瀏覽頁：`index.html`（GitHub Pages 根目錄）
- 教學簡報：`slides/index.html`（16:9 橫式，26 張，每張標註對應 Wiki 頁）
- 撰寫規則、workflow 與檢查清單：[CLAUDE.md](CLAUDE.md)
- 討論、ingest、檢查與退回紀錄：[wiki/log.md](wiki/log.md)

## 結構

```
wiki/
  index.md        頁面清單
  log.md          流程與檢查紀錄
  glossary.md     術語中英對照
  sources/        11 份來源摘要（官方 3、官方授權 wiki 7、第三方 1）
  concepts/       遊戲目標、地圖、兵線與補兵、經驗與金錢、技能、視野、中立資源、常見錯誤
  roles/          五個位置總覽、上路、打野、中路、下路、輔助
  draft/          選角流程、怎麼挑英雄、符文與召喚師技能
  items/          出裝基礎
slides/index.html 教學簡報
tools/
  check_wiki.py   ④ 交叉比對的自動檢查（出處、術語、第三方標記、連結）
  check_slides.py ⑦ 簡報的自動檢查（可追溯、術語先定義後使用、份量、範圍）
```

## 檢查

```
python tools/check_wiki.py
python tools/check_slides.py
```

## 說明

- 譯名採台服繁中，英文原名放括號；官方頁未出現的譯名在 glossary 標註。
- 簡報為 16:9 橫式（26 張），圖片取自 Riot 官方 Data Dragon（`tools/fetch_ddragon.py` 下載，來源記錄於 `assets/img/manifest.json`）；流程圖與示意圖以 SVG 自行繪製。前一份作業 `ee-study-notes` 的 `core.js` 為電子學繪圖專用，本專案未沿用。
- 不追蹤版本號；涉及版本的敘述以 26.1 更新說明為依據。

## 聲明

lol-beginner-wiki was created under Riot Games' "Legal Jibber Jabber" policy using assets owned by Riot Games. Riot Games does not endorse or sponsor this project.
