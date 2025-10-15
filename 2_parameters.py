# 2) 파라미터 맛보기 (온도/토큰/컨텍스트)
import ollama

options = {
    "temperature": 0.2,   # 창의성/일관성
    "num_ctx": 4096,      # 컨텍스트 윈도(메모리/VRAM 영향)
    "num_predict": 256    # 생성 토큰 제한
}

resp = ollama.chat(
    model='gemma3:4b',
    messages=[{"role": "user", "content": "한 문단짜리 한국어 격언을 창의적으로 지어줘."}],
    options=options
)
print(resp['message']['content'])

# 팁: temperature 낮추면 사실 중심/일관성이, 높이면 창의성이 올라갑니다.

