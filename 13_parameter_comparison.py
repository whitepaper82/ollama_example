# 13) 프롬프트 엔지니어링 - 파라미터에 따른 추론 결과 비교
import ollama
import time


def compare_responses(model, prompt, configs, title=""):
    """여러 설정으로 같은 프롬프트를 실행하고 결과 비교"""
    print("\n" + "=" * 80)
    print(f"{title}")
    print("=" * 80)
    print(f"프롬프트: {prompt}")
    print("-" * 80)
    
    results = []
    for config in configs:
        print(f"\n[설정: {config['name']}]")
        for key, value in config['options'].items():
            print(f"  {key}: {value}")
        
        start_time = time.time()
        resp = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            options=config['options']
        )
        elapsed = time.time() - start_time
        
        result = resp['message']['content']
        print(f"\n응답 (소요시간: {elapsed:.2f}초):")
        print(result)
        print("-" * 80)
        
        results.append({
            'name': config['name'],
            'result': result,
            'time': elapsed
        })
    
    return results


# ============================================================================
# 1. Temperature 비교 - 창의성 vs 일관성
# ============================================================================
print("\n🌡️  TEMPERATURE 비교 - 창의성과 일관성의 균형")
print("낮을수록: 결정론적, 일관성 있는 답변 (사실 기반 질문에 적합)")
print("높을수록: 창의적, 다양한 답변 (창작, 브레인스토밍에 적합)")

temp_configs = [
    {"name": "Temperature 0.0 (최소)", "options": {"temperature": 0.0, "num_predict": 100}},
    {"name": "Temperature 0.5 (보통)", "options": {"temperature": 0.5, "num_predict": 100}},
    {"name": "Temperature 1.0 (높음)", "options": {"temperature": 1.0, "num_predict": 100}},
    {"name": "Temperature 1.5 (매우 높음)", "options": {"temperature": 1.5, "num_predict": 100}},
]

compare_responses(
    'gemma3:1b',
    "혁신적인 스마트폰 앱 아이디어를 하나 제안해줘.",
    temp_configs,
    "Temperature 비교 - 창의성 테스트"
)


# ============================================================================
# 2. Top-P (Nucleus Sampling) 비교
# ============================================================================
print("\n\n🎯 TOP-P 비교 - 토큰 선택 범위")
print("낮을수록: 가장 확률 높은 소수의 토큰만 선택 (집중적)")
print("높을수록: 더 많은 토큰 후보 고려 (다양성)")

top_p_configs = [
    {"name": "Top-P 0.1 (매우 집중)", "options": {"top_p": 0.1, "temperature": 0.8}},
    {"name": "Top-P 0.5 (보통)", "options": {"top_p": 0.5, "temperature": 0.8}},
    {"name": "Top-P 0.9 (기본값)", "options": {"top_p": 0.9, "temperature": 0.8}},
    {"name": "Top-P 1.0 (최대)", "options": {"top_p": 1.0, "temperature": 0.8}},
]

compare_responses(
    'gemma3:1b',
    "AI의 미래에 대해 짧게 설명해줘.",
    top_p_configs,
    "Top-P 비교"
)


# ============================================================================
# 3. Top-K 비교
# ============================================================================
print("\n\n🔝 TOP-K 비교 - 고려할 토큰 개수")
print("낮을수록: 상위 K개 토큰만 고려 (보수적)")
print("높을수록: 더 많은 토큰 후보 고려 (다양성)")

top_k_configs = [
    {"name": "Top-K 5 (매우 제한)", "options": {"top_k": 5, "temperature": 0.8}},
    {"name": "Top-K 20 (제한적)", "options": {"top_k": 20, "temperature": 0.8}},
    {"name": "Top-K 40 (기본값)", "options": {"top_k": 40, "temperature": 0.8}},
    {"name": "Top-K 100 (넓음)", "options": {"top_k": 100, "temperature": 0.8}},
]

compare_responses(
    'gemma3:1b',
    "클라우드 컴퓨팅의 장점 3가지를 나열해줘.",
    top_k_configs,
    "Top-K 비교"
)


# ============================================================================
# 4. Repeat Penalty 비교 - 반복 방지
# ============================================================================
print("\n\n🔁 REPEAT PENALTY 비교 - 반복 억제")
print("1.0: 패널티 없음 (반복 가능)")
print("높을수록: 같은 단어/구문 반복 강하게 억제")

repeat_configs = [
    {"name": "Repeat Penalty 1.0 (없음)", "options": {"repeat_penalty": 1.0, "temperature": 0.8}},
    {"name": "Repeat Penalty 1.1 (기본값)", "options": {"repeat_penalty": 1.1, "temperature": 0.8}},
    {"name": "Repeat Penalty 1.3 (강함)", "options": {"repeat_penalty": 1.3, "temperature": 0.8}},
    {"name": "Repeat Penalty 1.5 (매우 강함)", "options": {"repeat_penalty": 1.5, "temperature": 0.8}},
]

compare_responses(
    'gemma3:1b',
    "Python의 장점을 설명해줘. 특히 'Python'이라는 단어를 여러 번 사용해서.",
    repeat_configs,
    "Repeat Penalty 비교"
)


# ============================================================================
# 5. Num Predict 비교 - 응답 길이 제한
# ============================================================================
print("\n\n📏 NUM PREDICT 비교 - 생성 토큰 수 제한")
print("응답의 최대 길이를 제어합니다.")

num_predict_configs = [
    {"name": "50 토큰 (짧음)", "options": {"num_predict": 50, "temperature": 0.3}},
    {"name": "100 토큰 (보통)", "options": {"num_predict": 100, "temperature": 0.3}},
    {"name": "200 토큰 (길음)", "options": {"num_predict": 200, "temperature": 0.3}},
    {"name": "500 토큰 (매우 길음)", "options": {"num_predict": 500, "temperature": 0.3}},
]

compare_responses(
    'gemma3:1b',
    "머신러닝과 딥러닝의 차이를 자세히 설명해줘.",
    num_predict_configs,
    "Num Predict 비교"
)


# ============================================================================
# 6. 복합 설정 비교 - 실전 사용 예시
# ============================================================================
print("\n\n⚙️  복합 설정 비교 - 실전 시나리오")

complex_configs = [
    {
        "name": "정확한 사실 답변용",
        "options": {
            "temperature": 0.1,
            "top_p": 0.9,
            "top_k": 20,
            "repeat_penalty": 1.1,
            "num_predict": 200
        }
    },
    {
        "name": "창의적 글쓰기용",
        "options": {
            "temperature": 1.0,
            "top_p": 0.95,
            "top_k": 100,
            "repeat_penalty": 1.3,
            "num_predict": 300
        }
    },
    {
        "name": "간결한 요약용",
        "options": {
            "temperature": 0.3,
            "top_p": 0.9,
            "top_k": 30,
            "repeat_penalty": 1.2,
            "num_predict": 100
        }
    },
    {
        "name": "브레인스토밍용",
        "options": {
            "temperature": 1.3,
            "top_p": 0.95,
            "top_k": 80,
            "repeat_penalty": 1.4,
            "num_predict": 250
        }
    }
]

compare_responses(
    'gemma3:1b',
    "전자상거래 플랫폼을 개선할 수 있는 방법을 제안해줘.",
    complex_configs,
    "복합 설정 비교 - 목적별 최적화"
)


# ============================================================================
# 7. 컨텍스트 윈도우 비교 - 메모리/처리 속도
# ============================================================================
print("\n\n💾 NUM_CTX 비교 - 컨텍스트 윈도우 크기")
print("높을수록: 더 긴 대화/문서 처리 가능 (VRAM 사용량 증가)")

ctx_configs = [
    {"name": "2048 토큰 (작음)", "options": {"num_ctx": 2048, "temperature": 0.3}},
    {"name": "4096 토큰 (기본)", "options": {"num_ctx": 4096, "temperature": 0.3}},
    {"name": "8192 토큰 (큼)", "options": {"num_ctx": 8192, "temperature": 0.3}},
]

long_text = """
인공지능(AI)은 컴퓨터 과학의 한 분야로, 기계가 인간의 지능적인 행동을 모방하도록 만드는 기술입니다.
최근 딥러닝의 발전으로 이미지 인식, 자연어 처리, 음성 인식 등 다양한 분야에서 획기적인 성과를 내고 있습니다.
특히 대규모 언어 모델(LLM)의 등장으로 챗봇, 번역, 코드 생성 등의 작업에서 인간 수준의 성능을 보이고 있습니다.
"""

compare_responses(
    'gemma3:1b',
    f"다음 텍스트를 한 문장으로 요약해줘:\n\n{long_text}",
    ctx_configs,
    "Num CTX 비교"
)


# ============================================================================
# 파라미터 가이드 요약
# ============================================================================
print("\n\n" + "=" * 80)
print("📚 파라미터 가이드 요약")
print("=" * 80)

guide = """
1. **Temperature** (0.0 ~ 2.0)
   - 0.0~0.3: 사실 기반 질문, 정확한 답변 필요 시
   - 0.5~0.7: 균형잡힌 답변
   - 0.8~1.2: 창의적 글쓰기, 아이디어 생성
   - 1.3~2.0: 실험적, 매우 창의적 (일관성 낮음)

2. **Top-P** (0.0 ~ 1.0)
   - 0.1~0.5: 집중적, 보수적 선택
   - 0.9: 기본값, 대부분 상황에 적합
   - 1.0: 모든 토큰 고려

3. **Top-K** (1 ~ 100+)
   - 5~20: 매우 보수적
   - 40: 기본값
   - 80~100: 다양성 증가

4. **Repeat Penalty** (1.0 ~ 2.0)
   - 1.0: 패널티 없음
   - 1.1: 기본값, 자연스러운 반복 허용
   - 1.3~1.5: 반복 강하게 억제

5. **Num Predict** (1 ~ 무제한)
   - 50~100: 짧은 답변
   - 200~300: 중간 길이
   - 500+: 긴 설명, 에세이

6. **Num CTX** (512 ~ 32768+)
   - 2048: 빠른 응답, 짧은 대화
   - 4096: 기본값, 대부분 상황 적합
   - 8192+: 긴 문서, 복잡한 대화

🎯 **추천 조합**

• 정확한 답변: temperature=0.2, top_p=0.9, top_k=30
• 창의적 글쓰기: temperature=1.0, top_p=0.95, top_k=80
• 코드 생성: temperature=0.1, top_p=0.9, repeat_penalty=1.2
• 브레인스토밍: temperature=1.3, top_p=0.95, top_k=100
• 요약: temperature=0.3, num_predict=150
"""

print(guide)
print("=" * 80)

