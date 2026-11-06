import json
import os
from pathlib import Path
from typing import Literal

from ollama import chat
from pydantic import BaseModel

MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")


class Sentiment(BaseModel):
    stock: str
    sentiment: Literal["正面", "中性", "負面"]
    reason: str
    confidence: float


def classify(title: str) -> Sentiment:
    resp = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是股市新聞分析助理。針對新聞標題，找出主要相關的股票或產業，判斷情緒，並用一句話說明理由。信心為 0 到 1。",
            },
            {"role": "user", "content": title},
        ],
        format=Sentiment.model_json_schema(),
        options={"temperature": 0},
    )
    return Sentiment.model_validate_json(resp.message.content)


def main():
    titles = json.loads(Path("data/headlines.json").read_text(encoding="utf-8"))
    results = []
    for t in titles:
        r = classify(t)
        print(t, "->", r.sentiment)
        results.append({"title": t, **r.model_dump()})
    Path("docs").mkdir(exist_ok=True)
    Path("docs/results.json").write_text(
        json.dumps({"model": MODEL, "results": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()