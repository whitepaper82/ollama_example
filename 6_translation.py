# 6) 번역(Translation) — 스타일 전환 포함
import ollama


def ask(model, task, system="한국어로 간결하고 정확하게 답해줘.", **options):
    return ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": task}
        ],
        options=options or {}
    )['message']['content']


english = """
We propose a lightweight retrieval-augmented pipeline for customer support emails.
The system combines semantic search with local LLM inference to provide accurate responses.
"""

prompt = f"""
다음 영어 문단을 '대학 강의노트' 스타일의 한국어로 번역해줘.
필요하면 용어를 각주 형식으로 보충 설명 (각주는 괄호로).
텍스트:
{english}
"""

print(ask('gemma3:4b', prompt, temperature=0.2))

