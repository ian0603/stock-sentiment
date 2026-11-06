import json
from collections import Counter
from html import escape
from pathlib import Path

DATA_NOTE = "資料為 2026/11/5～11/6 前後的台股新聞，標題由我根據報導自行改寫，數字為約數。"

AI_NOTE = [
    "使用的工具：用 Claude 協助規劃專案架構、撰寫程式與除錯；用本地 Ollama 模型 qwen2.5:7b 做新聞標題情緒分類。",
    "用在哪裡:Claude 協助寫 main.py、build_site.py 與 GitHub Actions workflow；Ollama 在 main.py 中以結構化輸出回傳股票、情緒、理由與信心。",
    "我自己做的事：自己挑選並整理 16 則新聞標題，逐則檢查模型的分類結果。",
    "我發現的問題：「自營商連續 7 日賣超」被分成中性，我認為應為負面 跟著外資在倒才賣那麼多。",
    "我發現的問題：台積電盤中自跌停附近明顯反彈，收盤跌幅收斂至約 4.7% -> 被分成中性，我認為應為正面 因為這種大場面對比之前關稅還能打開算不錯了拉了快2000點上來。",
    "我發現的問題：台積電盤中一度跌停，爆出近 10.9 萬張巨量，散戶與實戶進場承接 -> 被分成中性，我認為應為正面 因為爆量有人願意承接 這是好事 且收長下影紅K。",
]

data = json.loads(Path("docs/results.json").read_text(encoding="utf-8"))
rows = data["results"]
count = Counter(r["sentiment"] for r in rows)

tr = "".join(
    f"<tr><td>{escape(r['title'])}</td><td>{escape(r['stock'])}</td>"
    f"<td>{escape(r['sentiment'])}</td><td>{escape(r['reason'])}</td>"
    f"<td>{r['confidence']:.2f}</td></tr>"
    for r in rows
)
ai_items = "".join(f"<li>{escape(x)}</li>" for x in AI_NOTE)

html = f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>台股新聞標題情緒分類</title>
<style>
body{{font-family:system-ui,"Microsoft JhengHei",sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;line-height:1.7}}
table{{border-collapse:collapse;width:100%}}
td,th{{border:1px solid #ccc;padding:.5rem;text-align:left;vertical-align:top}}
th{{background:#f3f3f3}}
.note{{background:#fff8e1;padding:.8rem;border-radius:6px}}
pre{{background:#f6f8fa;padding:.8rem;border-radius:6px;overflow-x:auto}}
</style></head><body>
<h1>台股新聞標題情緒分類</h1>
<p class="note">免責聲明：本專案僅為課堂練習，不構成任何投資建議。</p>

<h2>1. 做了什麼</h2>
<p>用本地 Ollama 模型（{escape(data['model'])}）讀取台股新聞標題，以結構化輸出（JSON schema）回傳股票或產業、情緒（正面／中性／負面）、理由與信心。</p>
<p>{escape(DATA_NOTE)}</p>

<h2>2. 怎麼執行</h2>
<pre>ollama pull {escape(data['model'])}
uv sync
uv run main.py
uv run build_site.py</pre>

<h2>3. 執行結果</h2>
<p>共 {len(rows)} 則：正面 {count['正面']} 則、中性 {count['中性']} 則、負面 {count['負面']} 則。</p>
<div style="overflow-x:auto"><table>
<tr><th>標題</th><th>股票／產業</th><th>情緒</th><th>理由</th><th>信心</th></tr>
{tr}
</table></div>

<h2>4. AI 使用說明</h2>
<ul>{ai_items}</ul>
</body></html>"""

Path("docs/index.html").write_text(html, encoding="utf-8")
print("已產生 docs/index.html")