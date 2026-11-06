# 台股新聞標題情緒分類

用本地 Ollama 模型，以**結構化輸出**（JSON schema）對台股新聞標題做情緒分類，並用 GitHub Actions 自動部署成 GitHub Pages 作品頁。

> 免責聲明：本專案僅為課堂練習，不構成任何投資建議。

## 功能

- 讀取 `data/headlines.json` 的新聞標題（2026/11/5～11/6 前後的台股新聞，標題為自行改寫）
- 呼叫本地 Ollama 模型，回傳股票或產業、情緒（正面／中性／負面）、理由、信心
- 結果存成 `docs/results.json`，並產生作品頁 `docs/index.html`
- GitHub Actions 將 `docs/` 自動部署到 GitHub Pages

## 環境需求

- [Ollama](https://ollama.com/)（需保持開啟）與模型 `qwen2.5:7b`
- [uv](https://docs.astral.sh/uv/)
- Git

## 執行步驟

```bash
ollama pull qwen2.5:7b
uv sync
uv run main.py
uv run build_site.py
```

可用環境變數 `OLLAMA_MODEL` 更換模型，範例見 `.env.example`。

## 專案結構

```
.
├── main.py               # 呼叫 Ollama 做情緒分類
├── build_site.py         # 產生作品頁
├── data/headlines.json   # 新聞標題
├── docs/                 # results.json 與 index.html（Pages 部署內容）
├── .github/workflows/pages.yml
├── .env.example
└── pyproject.toml
```

## 說明

GitHub Actions 的執行環境沒有本地 Ollama，因此模型推論在本機完成，結果（`docs/`）一併 commit，Actions 只負責部署。

## 作品頁

（https://github.io/ian0603/stock-sentiment）