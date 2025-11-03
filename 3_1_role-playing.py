import ollama

options = {
    "temperature": 0.2,   # 창의성/일관성
    "num_ctx": 1024,      # 컨텍스트 윈도(메모리/VRAM 영향)
    "num_predict": 1024    # 생성 토큰 제한
}
# 기본 프롬프트
prompt_basic = "인공지능의 미래에 대해 설명해줘."

# 역할을 부여한 프롬프트 (Role-playing)
prompt_role = """
너는 세계 최고의 SF 소설가야.
독자들이 흥미진진하게 읽을 수 있도록, 인공지능의 미래에 대해 한 편의 짧은 소설처럼 묘사해줘.
"""

print("--- [기본 프롬프트 결과] ---")
response_basic = ollama.chat(
    model='gemma3:1b',
    messages=[{'role': 'user', 'content': prompt_basic}],
    options=options
)
print(response_basic['message']['content'])

print("\n\n--- [역할 부여 프롬프트 결과] ---")
response_role = ollama.chat(
    model='gemma3:1b',
    messages=[{'role': 'user', 'content': prompt_role}],
    options=options
)
print(response_role['message']['content'])


"""
[미션]
1. 원하는 역할과 질문을 설명하도록 프롬프트를 만들고, 해당 결과를를 본인 slack 채널에 결과를 공유하는 코드를 아래 작성하세요.
   ex) '5살 아이에게 설명하는 과학자' 역할을 부여하여 '양자역학'에 대해 설명하도록 프롬프트를 작성
"""