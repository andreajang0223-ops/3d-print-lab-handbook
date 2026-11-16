# AGENTS.md

本專案的 AI 工作規則統一寫在 **[CLAUDE.md](CLAUDE.md)**。
不論你是 Claude、Codex、Gemini 或其他程式助理，動手前請先完整讀完 CLAUDE.md，並依第 6 節「新增頁面的標準流程」與第 10 節「完成前檢查清單」工作。

最重要的五條（完整版見 CLAUDE.md）：

1. 只有四種頁面：線材、印表機、問題排解、實測紀錄；新增頁面一律從 `templates/` 複製。
2. 頁面清單只寫在 `data/pages.json`，不要手改 `index.html` 的列表。
3. 不確定的數值寫「待確認」，絕對不要編造。
4. 只用 `assets/style.css` 已有的 class，不寫 inline style、不引入外部套件。
5. 每次變更都記錄在 `CHANGELOG.md`。
