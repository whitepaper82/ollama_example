# 3) 프롬프트 템플릿화 (함수로 래핑)
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


print(ask('gemma3:1b', "대한민국을을 한 문장으로 설명해줘."))

