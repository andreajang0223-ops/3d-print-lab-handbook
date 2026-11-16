# 3D 列印實驗室手冊

工業設計系實驗室的 3D 列印知識手冊：線材設定、印表機注意事項、問題排解與實測紀錄。

- 網站：https://andreajang0223-ops.github.io/3d-print-lab-handbook/
- AI 工作規則：[CLAUDE.md](CLAUDE.md)（其他 AI 工具請看 [AGENTS.md](AGENTS.md)）
- 變更紀錄：[CHANGELOG.md](CHANGELOG.md)

## 怎麼新增內容

把需求告訴 AI 助理，並請它依 CLAUDE.md 處理，例如：

> 依 CLAUDE.md 新增一個問題排解頁：第一層不黏。

AI 會從 `templates/` 複製對應範本、填入內容、登錄到 `data/pages.json`、補上相關頁面的連結，並記錄在 `CHANGELOG.md`。首頁會自動出現新頁面。

## 本機預覽

首頁用 JavaScript 讀取 `data/pages.json`，直接雙擊 `index.html` 會因瀏覽器安全限制讀不到資料。請在專案資料夾執行：

```
python -m http.server 8000
```

再開啟 http://localhost:8000 。

## 作者

雲科大工設碩一 張芫瑞（生成式 AI 課程第九週作業）
