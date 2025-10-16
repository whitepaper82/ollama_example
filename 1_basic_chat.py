# 1) "헬로 LLM" — 가장 기본 대화
import ollama

resp = ollama.chat(
    model='gemma3:1b',
    messages=[
        {"role": "system", "content": "You are a concise Korean assistant."},
        {"role": "user", "content": "LangChain의 필요성을 한 문장으로 설명해줘."}
    ]
)
print(resp['message']['content'])

