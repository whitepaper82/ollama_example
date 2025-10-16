# 5) 요약(Summarization) — 길이 제한 & 톤 제어
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


article = """
생성형 AI는 기업의 문서 검색, 고객지원 자동화, 코드 리뷰 등 다양한 영역에 적용되고 있다.
특히 검색결합형(RAG) 방식은 내부 문서를 실시간으로 참조하여 최신 정보를 제공할 수 있어,
많은 기업들이 도입을 검토하고 있다. 로컬 추론 환경에서도 충분히 활용 가능하다.
"""

prompt = f"""
다음 글을 3문장 이내로 요약하고, 마지막에 핵심 키워드 3개를 해시태그로 제시해줘.
글:
{article}
"""

print(ask('gemma3:1b', prompt, temperature=0.3))

