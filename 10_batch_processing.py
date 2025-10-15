# 10) 배치 처리 예시 — 여러 문서 요약 표 만들기
# pip install pandas

import ollama
import pandas as pd


def ask(model, task, system="한국어로 간결하고 정확하게 답해줘.", **options):
    return ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": task}
        ],
        options=options or {}
    )['message']['content']


paragraphs = [
    "전자상거래에서는 고객지원 자동화가 중요한 과제로 부상했다. AI 챗봇과 검색 시스템이 핵심이다.",
    "검색결합형(RAG) 접근은 내부 문서를 참조하여 최신 정보를 제공한다. 기업 도입이 증가하고 있다.",
    "로컬 추론은 개인정보와 기밀문서 보호에 유리하다. Ollama 같은 도구가 이를 가능하게 한다."
]

rows = []
for i, p in enumerate(paragraphs, start=1):
    out = ask('gemma3:4b', f"두 문장으로 요약하고 핵심 키워드 3개를 해시태그로: {p}", temperature=0.2)
    rows.append({"id": i, "summary": out})

df = pd.DataFrame(rows)
print(df)

