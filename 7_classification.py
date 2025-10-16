# 7) 분류(Classification) — 라벨 집합 고정 & 근거 포함
import ollama

reviews = [
    "배송이 빠르고 포장도 안전했어요.",
    "설명과 다른 제품이 왔고 반품 진행이 너무 느렸습니다.",
    "가격은 좋지만 내구성이 아쉽네요."
]

label_set = ["positive", "neutral", "negative"]

for r in reviews:
    prompt = f"""
아래 리뷰를 {label_set} 중 하나로 분류하고, 한 문장 근거를 제시해.
JSON만 출력:
{{"label": <label>, "reason": <string>}}
리뷰: "{r}"
"""
    out = ollama.chat(
        model='gemma3:1b',
        messages=[{"role": "user", "content": prompt}],
        format='json',
        options={"temperature": 0}
    )
    print(r, "->", out['message']['content'])

