# 9) 스트리밍 출력 받기 (토큰 나오자마자 표시)
import ollama
from sys import stdout

stream = ollama.chat(
    model='gemma3:4b',
    messages=[{"role": "user", "content": "생성형 AI의 장단점을 항목별로 정리해줘."}],
    stream=True,  # 스트리밍
    options={"temperature": 0.3}
)

buf = []
for chunk in stream:
    token = chunk['message']['content']
    buf.append(token)
    stdout.write(token)
stdout.flush()

print("\n\n전체 응답:", "".join(buf))

