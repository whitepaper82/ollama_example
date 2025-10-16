# ============================================================================
# 미션 샘플 코드 모음
# ============================================================================
import ollama
import json

# ============================================================================
# Slack 설정 (메시지 전송용)
# ============================================================================
SLACK_ENABLED = True  # Slack 전송 활성화 여부
SLACK_CHANNEL = "본인의_채널명"  # 실제 채널명으로 변경하세요 (예: "ai-mission-results")

def send_slack_summary(mission_name, summary_data):
    """미션 완료 후 요약 정보를 Slack으로 전송"""
    if not SLACK_ENABLED:
        print(f"ℹ️ Slack 전송 비활성화됨: {mission_name}")
        return
    
    try:
        # Block Kit 형식으로 메시지 구성
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🎉 {mission_name} 완료!",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": summary_data
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Mission.py에서 자동 생성된 보고서"
                    }
                ]
            }
        ]
        
        # 실제 Slack 전송 (MCP 함수 사용)
        # 방법 1: 채널 이름으로 찾기
        # channel_result = mcp_mcp_hub_slack_cafe24.find_channel_by_name(SLACK_CHANNEL)
        # channel_id = channel_result['channel']['id']
        
        # 방법 2: 채널 ID를 직접 사용 (더 빠름)
        # mcp_mcp_hub_slack_cafe24.post_block_message(
        #     channel_id=SLACK_CHANNEL,  # 또는 "C01234567" 형식의 채널 ID
        #     blocks=blocks,
        #     text=mission_name,
        #     auto_join=True
        # )
        
        # 현재는 시뮬레이션 모드
        print(f"\n📨 [Slack 전송 시뮬레이션]")
        print(f"   채널: {SLACK_CHANNEL}")
        print(f"   제목: {mission_name}")
        print(f"   필드 수: {len(summary_data)}")
        print(f"   ✅ 실제 전송하려면 위 주석을 해제하세요")
        
    except Exception as e:
        print(f"⚠️ Slack 전송 실패: {e}")


def format_slack_field(label, value):
    """Slack 필드 포맷"""
    return {
        "type": "mrkdwn",
        "text": f"*{label}*\n{value}"
    }


# ============================================================================
# 미션 1: 영화 리뷰 분석 (4_json_extraction.py 관련)
# ============================================================================
print("="*80)
print("🎬 미션 1: 영화 리뷰 분석 - JSON 추출 연습")
print("="*80)

# 여러 개의 영화 리뷰 데이터
movie_reviews = [
    """
    봉준호 감독의 '기생충'은 블랙 코미디 스릴러 장르의 걸작이다.
    계급 갈등을 예리하게 그려냈고, 연출과 연기 모두 완벽하다.
    반전이 충격적이며 사회적 메시지도 강렬하다.
    다만 일부 잔인한 장면이 있어 호불호가 갈릴 수 있다.
    그럼에도 한국 영화의 위상을 높인 명작이다. 5점 만점에 4.8점.
    """,
    
    """
    제임스 카메론의 '아바타'는 판타지 액션 영화로, 3D 기술이 혁신적이다.
    시각적 스펙터클이 압도적이고 판도라 행성의 세계관이 매력적이다.
    환경 보호 메시지도 의미있다.
    하지만 스토리가 다소 뻔하고 예측 가능한 전개가 아쉽다.
    그래도 영화관에서 꼭 봐야 할 영화. 5점 만점에 4.2점.
    """,
    
    """
    드니 빌뇌브 감독의 '듄'은 SF 대서사시로, 원작 소설을 충실히 재현했다.
    영상미가 압권이고 음악도 웅장하다. 배우들의 연기도 훌륭하다.
    다만 2시간 35분의 긴 러닝타임이 부담스럽고, 원작을 모르면 이해가 어렵다.
    후속작을 기대하게 만드는 영화. 5점 만점에 4.0점.
    """,
    
    """
    마이클 베이의 '트랜스포머'는 액션 SF 영화다.
    로봇들의 변신과 전투 장면은 볼만하다.
    하지만 스토리가 너무 단순하고 캐릭터 깊이가 없다.
    과도한 액션으로 피로감을 느끼게 한다.
    팝콘 무비로는 괜찮지만 추천하기는 어렵다. 5점 만점에 3.2점.
    """
]

# JSON 추출 함수
def extract_movie_info(review_text):
    """영화 리뷰에서 정보 추출"""
    prompt = f"""
아래 영화 리뷰 텍스트에서 정보를 추출하여 JSON으로 출력해줘.

스키마:
{{
  "title": str,           // 영화 제목
  "director": str,        // 감독
  "genre": str,           // 장르
  "rating": float,        // 평점 (0.0 ~ 5.0)
  "pros": [str],          // 장점 리스트
  "cons": [str],          // 단점 리스트
  "recommended": bool     // 추천 여부
}}

리뷰 텍스트:
{review_text}

반드시 JSON만 출력하고, 텍스트에서 유추 가능한 모든 정보를 포함해줘.
"""
    
    response = ollama.chat(
        model='gemma3:1b',
        messages=[{"role": "user", "content": prompt}],
        format='json',
        options={"temperature": 0}
    )
    
    return json.loads(response['message']['content'])


# 1️⃣ 과제 1 & 2: 여러 개의 리뷰 처리 (반복문)
print("\n📝 과제 1 & 2: 여러 영화 리뷰 처리\n")

all_movie_data = []

for i, review in enumerate(movie_reviews, 1):
    print(f"[{i}/{len(movie_reviews)}] 리뷰 처리 중...")
    movie_data = extract_movie_info(review)
    all_movie_data.append(movie_data)
    
    print(f"✅ {movie_data.get('title', 'N/A')} - 평점: {movie_data.get('rating', 'N/A')}/5.0")

print(f"\n총 {len(all_movie_data)}개의 영화 리뷰 처리 완료!")


# 2️⃣ 과제 3: JSON 데이터를 파일로 저장
print("\n" + "-"*80)
print("💾 과제 3: JSON 파일로 저장")
print("-"*80)

output_file = "movie_reviews.json"

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_movie_data, f, indent=2, ensure_ascii=False)

print(f"✅ {output_file} 파일에 저장 완료!")
print(f"   - 총 {len(all_movie_data)}개의 영화 데이터 저장")


# 3️⃣ 과제 4: 평점 4.0 이상 + 추천하는 영화만 필터링
print("\n" + "-"*80)
print("🔍 과제 4: 고평점 + 추천 영화 필터링 (평점 4.0 이상 & recommended=true)")
print("-"*80)

recommended_movies = [
    movie for movie in all_movie_data 
    if movie.get('rating', 0) >= 4.0 and movie.get('recommended', False)
]

print(f"\n필터 조건을 만족하는 영화: {len(recommended_movies)}편\n")

for movie in recommended_movies:
    print("🎬" + "="*76)
    print(f"제목: {movie.get('title', 'N/A')}")
    print(f"감독: {movie.get('director', 'N/A')}")
    print(f"장르: {movie.get('genre', 'N/A')}")
    print(f"⭐ 평점: {movie.get('rating', 'N/A')}/5.0")
    print(f"👍 추천: {'예' if movie.get('recommended', False) else '아니오'}")
    
    print(f"\n✅ 장점:")
    for pro in movie.get('pros', []):
        print(f"  • {pro}")
    
    print(f"\n❌ 단점:")
    for con in movie.get('cons', []):
        print(f"  • {con}")
    print()


# 4️⃣ 추가: 통계 분석
print("="*80)
print("📊 추가 분석: 전체 통계")
print("="*80)

total_movies = len(all_movie_data)
recommended_count = sum(1 for m in all_movie_data if m.get('recommended', False))
avg_rating = sum(m.get('rating', 0) for m in all_movie_data) / total_movies if total_movies > 0 else 0
high_rating_count = sum(1 for m in all_movie_data if m.get('rating', 0) >= 4.0)

print(f"\n총 영화 수: {total_movies}편")
print(f"추천 영화: {recommended_count}편 ({recommended_count/total_movies*100:.1f}%)")
print(f"평균 평점: {avg_rating:.2f}/5.0")
print(f"고평점 영화 (4.0 이상): {high_rating_count}편 ({high_rating_count/total_movies*100:.1f}%)")

# 장르별 통계
genres = {}
for movie in all_movie_data:
    genre = movie.get('genre', '기타')
    genres[genre] = genres.get(genre, 0) + 1

print(f"\n장르별 분포:")
for genre, count in sorted(genres.items(), key=lambda x: x[1], reverse=True):
    print(f"  • {genre}: {count}편")


# 5️⃣ 최종: 필터링된 데이터도 별도 파일로 저장
recommended_output = "recommended_movies.json"

with open(recommended_output, 'w', encoding='utf-8') as f:
    json.dump(recommended_movies, f, indent=2, ensure_ascii=False)

print(f"\n✅ 추천 영화만 따로 저장: {recommended_output}")
print("="*80)

print("\n🎉 미션 1 완료!")
print("\n생성된 파일:")
print(f"  1. {output_file} - 전체 영화 데이터")
print(f"  2. {recommended_output} - 추천 영화만")

# Slack으로 결과 전송
mission1_summary = [
    format_slack_field("📊 총 영화 수", f"{total_movies}편"),
    format_slack_field("⭐ 평균 평점", f"{avg_rating:.2f}/5.0"),
    format_slack_field("👍 추천 영화", f"{recommended_count}편 ({recommended_count/total_movies*100:.1f}%)"),
    format_slack_field("🎬 고평점 영화", f"{high_rating_count}편"),
    format_slack_field("💾 생성 파일", f"• {output_file}\n• {recommended_output}")
]
send_slack_summary("미션 1: 영화 리뷰 분석", mission1_summary)

print("\n"+"="*80+"\n")


# ============================================================================
# 미션 2: 코드 리뷰 자동화 (11_grading.py 관련)
# ============================================================================
print("="*80)
print("💻 미션 2: 파이썬 코드 품질 평가 시스템")
print("="*80)

# 평가할 학생 코드 샘플들
student_codes = [
    {
        "student_name": "학생 A",
        "task": "리스트의 합계를 계산하는 함수",
        "code": """
def calculate_sum(numbers):
    result = 0
    for i in range(len(numbers)):
        result = result + numbers[i]
    return result

# 테스트
print(calculate_sum([1, 2, 3, 4, 5]))
"""
    },
    {
        "student_name": "학생 B",
        "task": "리스트의 합계를 계산하는 함수",
        "code": """
def calculate_sum(numbers):
    return sum(numbers)

# 테스트
print(calculate_sum([1, 2, 3, 4, 5]))
"""
    },
    {
        "student_name": "학생 C",
        "task": "리스트의 합계를 계산하는 함수",
        "code": """
def calculate_sum(numbers):
    s=0
    for n in numbers:s+=n
    return s

print(calculate_sum([1,2,3,4,5]))
"""
    },
    {
        "student_name": "학생 D",
        "task": "리스트에서 짝수만 필터링하는 함수",
        "code": """
def filter_even(numbers):
    '''리스트에서 짝수만 반환합니다.
    
    Args:
        numbers: 정수 리스트
        
    Returns:
        짝수만 포함된 리스트
    '''
    return [num for num in numbers if num % 2 == 0]

# 테스트
result = filter_even([1, 2, 3, 4, 5, 6])
print(f"짝수: {result}")
"""
    }
]


# 코드 평가 함수
def evaluate_code(student_name, task, code):
    """학생 코드를 자동으로 평가"""
    rubric_prompt = f"""
다음 학생의 파이썬 코드를 평가해주세요.

과제: {task}

학생 코드:
```python
{code}
```

채점 기준 (총 20점):
1. 코드 정확성 (0-7점): 요구사항 충족, 버그 없음, 예외 처리
2. 가독성 (0-5점): 변수명, 들여쓰기, 주석, 코드 구조
3. 효율성 (0-4점): 불필요한 반복 없음, 최적화된 로직
4. 코드 스타일 (0-4점): PEP8 준수, 파이썬 관례

JSON 형식으로 출력:
{{
  "total_score": 0-20,
  "scores": {{
    "correctness": 0-7,
    "readability": 0-5,
    "efficiency": 0-4,
    "style": 0-4
  }},
  "grade": "A/B/C/D/F",
  "feedback": "전체적인 평가 (2-3문장)",
  "strengths": ["강점1", "강점2"],
  "weaknesses": ["약점1", "약점2"],
  "suggestions": ["개선사항1", "개선사항2"]
}}

엄격하게 평가하되, 건설적인 피드백을 제공하세요.
"""
    
    response = ollama.chat(
        model='gemma3:1b',
        messages=[{"role": "user", "content": rubric_prompt}],
        format='json',
        options={"temperature": 0}
    )
    
    return json.loads(response['message']['content'])


# 모든 학생 코드 평가
print("\n📊 코드 평가 진행 중...\n")

all_evaluations = []

for student_data in student_codes:
    print(f"[평가 중] {student_data['student_name']} - {student_data['task']}")
    
    evaluation = evaluate_code(
        student_data['student_name'],
        student_data['task'],
        student_data['code']
    )
    
    evaluation['student_name'] = student_data['student_name']
    evaluation['task'] = student_data['task']
    evaluation['code'] = student_data['code']
    
    all_evaluations.append(evaluation)
    
    print(f"  ✅ 평가 완료 - 총점: {evaluation.get('total_score', 'N/A')}/20 (등급: {evaluation.get('grade', 'N/A')})")

print(f"\n총 {len(all_evaluations)}명의 코드 평가 완료!\n")


# 개별 결과 상세 출력
print("="*80)
print("📝 개별 평가 결과 상세")
print("="*80)

for i, eval_data in enumerate(all_evaluations, 1):
    print(f"\n{'='*80}")
    print(f"👤 {eval_data['student_name']} - {eval_data['task']}")
    print('='*80)
    
    print("\n📄 제출 코드:")
    print("-"*80)
    print(eval_data['code'])
    print("-"*80)
    
    print(f"\n📊 점수 상세:")
    print(f"  • 정확성: {eval_data['scores'].get('correctness', 0)}/7")
    print(f"  • 가독성: {eval_data['scores'].get('readability', 0)}/5")
    print(f"  • 효율성: {eval_data['scores'].get('efficiency', 0)}/4")
    print(f"  • 스타일: {eval_data['scores'].get('style', 0)}/4")
    print(f"\n  🎯 총점: {eval_data.get('total_score', 0)}/20")
    print(f"  🏆 등급: {eval_data.get('grade', 'N/A')}")
    
    print(f"\n💬 피드백:")
    print(f"  {eval_data.get('feedback', 'N/A')}")
    
    print(f"\n✅ 강점:")
    for strength in eval_data.get('strengths', []):
        print(f"  • {strength}")
    
    print(f"\n⚠️ 약점:")
    for weakness in eval_data.get('weaknesses', []):
        print(f"  • {weakness}")
    
    print(f"\n💡 개선 제안:")
    for suggestion in eval_data.get('suggestions', []):
        print(f"  • {suggestion}")


# 통계 및 비교 분석
print("\n" + "="*80)
print("📈 전체 통계 및 비교 분석")
print("="*80)

total_students = len(all_evaluations)
avg_score = sum(e.get('total_score', 0) for e in all_evaluations) / total_students

grade_distribution = {}
for eval_data in all_evaluations:
    grade = eval_data.get('grade', 'F')
    grade_distribution[grade] = grade_distribution.get(grade, 0) + 1

print(f"\n📊 기본 통계:")
print(f"  • 평가 대상: {total_students}명")
print(f"  • 평균 점수: {avg_score:.1f}/20")
print(f"  • 최고 점수: {max(e.get('total_score', 0) for e in all_evaluations)}/20")
print(f"  • 최저 점수: {min(e.get('total_score', 0) for e in all_evaluations)}/20")

print(f"\n🏆 등급 분포:")
for grade in ['A', 'B', 'C', 'D', 'F']:
    count = grade_distribution.get(grade, 0)
    if count > 0:
        percentage = (count / total_students) * 100
        bar = '█' * count
        print(f"  {grade}: {bar} ({count}명, {percentage:.1f}%)")

# 카테고리별 평균 점수
print(f"\n📊 카테고리별 평균 점수:")
categories = ['correctness', 'readability', 'efficiency', 'style']
max_scores = [7, 5, 4, 4]
category_names = ['정확성', '가독성', '효율성', '스타일']

for cat, max_score, name in zip(categories, max_scores, category_names):
    avg = sum(e['scores'].get(cat, 0) for e in all_evaluations) / total_students
    percentage = (avg / max_score) * 100
    print(f"  • {name}: {avg:.1f}/{max_score} ({percentage:.1f}%)")


# 우수 학생 선정
print(f"\n🌟 우수 학생 (15점 이상):")
excellent_students = [e for e in all_evaluations if e.get('total_score', 0) >= 15]

if excellent_students:
    for student in sorted(excellent_students, key=lambda x: x.get('total_score', 0), reverse=True):
        print(f"  🏅 {student['student_name']}: {student.get('total_score', 0)}/20 ({student.get('grade', 'N/A')})")
else:
    print("  해당 학생 없음")

# 주의 필요 학생 (10점 미만)
print(f"\n⚠️ 추가 지도 필요 (10점 미만):")
struggling_students = [e for e in all_evaluations if e.get('total_score', 0) < 10]

if struggling_students:
    for student in sorted(struggling_students, key=lambda x: x.get('total_score', 0)):
        print(f"  ⚡ {student['student_name']}: {student.get('total_score', 0)}/20 ({student.get('grade', 'N/A')})")
else:
    print("  해당 학생 없음")


# 평가 결과 파일로 저장
print("\n" + "="*80)
print("💾 평가 결과 저장")
print("="*80)

output_file = "code_evaluations.json"

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_evaluations, f, indent=2, ensure_ascii=False)

print(f"✅ {output_file} 파일에 저장 완료!")

# 요약 리포트 생성
summary_report = {
    "evaluation_date": "2025-10-16",
    "total_students": total_students,
    "average_score": round(avg_score, 2),
    "grade_distribution": grade_distribution,
    "category_averages": {
        category_names[i]: round(sum(e['scores'].get(cat, 0) for e in all_evaluations) / total_students, 2)
        for i, cat in enumerate(categories)
    },
    "excellent_students": [e['student_name'] for e in excellent_students],
    "struggling_students": [e['student_name'] for e in struggling_students]
}

summary_file = "code_evaluation_summary.json"

with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump(summary_report, f, indent=2, ensure_ascii=False)

print(f"✅ {summary_file} 파일에 요약 리포트 저장 완료!")

print("\n🎉 미션 2 완료!")
print("\n생성된 파일:")
print(f"  1. {output_file} - 전체 평가 결과 상세")
print(f"  2. {summary_file} - 요약 리포트")

# Slack으로 결과 전송
top_students = ", ".join([e['student_name'] for e in excellent_students[:3]])
mission2_summary = [
    format_slack_field("👥 평가 대상", f"{total_students}명"),
    format_slack_field("📊 평균 점수", f"{avg_score:.1f}/20"),
    format_slack_field("🏆 등급 분포", "\n".join([f"{g}: {grade_distribution.get(g, 0)}명" for g in ['A', 'B', 'C', 'D', 'F'] if grade_distribution.get(g, 0) > 0])),
    format_slack_field("🌟 우수 학생", top_students if top_students else "없음"),
    format_slack_field("💾 생성 파일", f"• {output_file}\n• {summary_file}")
]
send_slack_summary("미션 2: 코드 리뷰 자동화", mission2_summary)

print("\n"+"="*80+"\n")


# ============================================================================
# 미션 3: Chain of Thought 답변 검증 (14_chain_of_thought.py 관련)
# ============================================================================
print("="*80)
print("🧠 미션 3: CoT 답변 자동 검증 시스템")
print("="*80)
print("\n14_chain_of_thought.py의 1, 3, 4, 5, 7번 질문 답변을 검증합니다.\n")

# CoT 문제와 정답 정의
cot_problems = [
    {
        "id": 1,
        "category": "수학 문제",
        "question": "한 가게에 사과가 23개 있었습니다. 아침에 16개를 팔고, 점심에 29개를 새로 들여왔습니다. 오후에 12개를 더 팔았다면 현재 몇 개의 사과가 남았을까요?",
        "correct_answer": "24개",
        "solution": "23 - 16 + 29 - 12 = 24",
        "cot_prompt": True
    },
    {
        "id": 3,
        "category": "Few-Shot CoT",
        "question": "도서관에 소설책 45권, 과학책 38권, 역사책 27권이 있습니다. 오늘 소설책 12권과 역사책 8권을 대출했고, 과학책 15권을 새로 구입했습니다. 현재 전체 책은 몇 권인가요?",
        "correct_answer": "105권",
        "solution": "(45 + 38 + 27) - 12 - 8 + 15 = 110 - 20 + 15 = 105",
        "cot_prompt": True
    },
    {
        "id": 4.1,
        "category": "Zero-Shot CoT",
        "question": "12 x 13 + 8 x 7을 계산해주세요.",
        "correct_answer": "212",
        "solution": "12 x 13 = 156, 8 x 7 = 56, 156 + 56 = 212",
        "cot_prompt": True
    },
    {
        "id": 4.2,
        "category": "Zero-Shot CoT",
        "question": "만약 내일이 어제였다면, 모레는 무슨 요일일까요? (오늘이 수요일이라면)",
        "correct_answer": "수요일",
        "solution": "내일=어제 → 오늘이 기준. 오늘이 수요일이면 모레도 수요일",
        "cot_prompt": True
    },
    {
        "id": 4.3,
        "category": "Zero-Shot CoT",
        "question": "3명이 3분 동안 3개의 사과를 먹는다면, 9명이 9개의 사과를 먹는데 몇 분이 걸릴까요?",
        "correct_answer": "3분",
        "solution": "3명이 3분에 3개 → 1명당 1개를 3분에 먹음. 9명이 9개 → 각자 1개씩 동시에 먹으면 3분",
        "cot_prompt": True
    },
    {
        "id": 5,
        "category": "복잡한 추론",
        "question": """한 회사에서 프로젝트 일정을 계획하고 있습니다:
- 설계 단계: 5일 소요
- 개발 단계: 설계 완료 후 시작, 12일 소요
- 테스트 단계: 개발의 50% 완료 시점부터 시작 가능, 8일 소요
- 배포 준비: 테스트와 개발이 모두 완료된 후 시작, 3일 소요

월요일에 시작한다면, 배포 준비가 완료되는 날은 언제인가요?
(주말 작업 없음, 토일요일 제외)""",
        "correct_answer": "4주차 목요일 또는 22일째 평일",
        "solution": "설계 5일 → 개발 12일(테스트는 6일차부터 8일) → 배포 3일. 총 20일(평일) = 4주",
        "cot_prompt": True
    },
    {
        "id": 7,
        "category": "Self-Consistency",
        "question": """한 농장에 닭과 토끼가 총 20마리 있습니다. 
다리 개수를 세어보니 총 56개였습니다.
닭은 다리가 2개, 토끼는 다리가 4개입니다.
닭과 토끼는 각각 몇 마리인가요?""",
        "correct_answer": "닭 12마리, 토끼 8마리",
        "solution": "x + y = 20, 2x + 4y = 56 → x = 12, y = 8",
        "cot_prompt": True
    }
]


def get_cot_answer(question):
    """CoT를 사용하여 문제 풀기"""
    cot_prompt = f"""{question}

Let's think step by step:"""
    
    response = ollama.chat(
        model='gemma3:1b',
        messages=[{"role": "user", "content": cot_prompt}],
        options={"temperature": 0.3, "num_predict": 400}
    )
    
    return response['message']['content']


def verify_answer(problem, ai_answer):
    """AI 답변이 정답인지 검증"""
    verification_prompt = f"""
다음 수학/논리 문제에 대한 AI의 답변이 정확한지 검증하고 채점해주세요.

문제: {problem['question']}

정답: {problem['correct_answer']}
풀이: {problem['solution']}

AI 답변:
{ai_answer}

채점 기준 (총 10점):
1. 최종 답의 정확성 (0-5점): 정답과 일치하는가?
2. 풀이 과정의 논리성 (0-3점): 단계별 추론이 올바른가?
3. 설명의 명확성 (0-2점): 이해하기 쉬운가?

JSON 형식으로만 출력:
{{
  "score": 0-10,
  "answer_correct": true/false,
  "reasoning_quality": "excellent/good/fair/poor",
  "feedback": "한 줄 피드백",
  "improvements": "개선이 필요한 부분 (없으면 '없음')"
}}
"""
    
    response = ollama.chat(
        model='gemma3:1b',
        messages=[{"role": "user", "content": verification_prompt}],
        format='json',
        options={"temperature": 0}
    )
    
    return json.loads(response['message']['content'])


# 모든 문제 풀이 및 검증
print("📝 CoT로 문제 풀이 및 검증 진행 중...\n")

all_verifications = []

for i, problem in enumerate(cot_problems, 1):
    print(f"[{i}/{len(cot_problems)}] 문제 {problem['id']} 처리 중...")
    print(f"   카테고리: {problem['category']}")
    
    # CoT로 답변 생성
    ai_answer = get_cot_answer(problem['question'])
    
    # 답변 검증
    verification = verify_answer(problem, ai_answer)
    
    # 결과 저장
    result = {
        "problem_id": problem['id'],
        "category": problem['category'],
        "question": problem['question'],
        "correct_answer": problem['correct_answer'],
        "ai_answer": ai_answer,
        "verification": verification
    }
    
    all_verifications.append(result)
    
    status = "✅" if verification.get('answer_correct', False) else "❌"
    print(f"   {status} 점수: {verification.get('score', 0)}/10")
    print(f"   답변: {'정답' if verification.get('answer_correct', False) else '오답'}")
    print()


# 상세 결과 출력
print("="*80)
print("📊 검증 결과 상세")
print("="*80)

for result in all_verifications:
    print(f"\n{'='*80}")
    print(f"🔢 문제 {result['problem_id']}: {result['category']}")
    print('='*80)
    
    print(f"\n❓ 질문:")
    print(f"{result['question'][:100]}...")
    
    print(f"\n✅ 정답: {result['correct_answer']}")
    
    print(f"\n🤖 AI 답변:")
    print("-"*80)
    # 답변이 너무 길면 처음 300자만
    answer_preview = result['ai_answer'][:300] + "..." if len(result['ai_answer']) > 300 else result['ai_answer']
    print(answer_preview)
    print("-"*80)
    
    verification = result['verification']
    print(f"\n📊 검증 결과:")
    print(f"  • 점수: {verification.get('score', 0)}/10")
    print(f"  • 정답 여부: {'✅ 정답' if verification.get('answer_correct', False) else '❌ 오답'}")
    print(f"  • 추론 품질: {verification.get('reasoning_quality', 'N/A')}")
    print(f"  • 피드백: {verification.get('feedback', 'N/A')}")
    print(f"  • 개선점: {verification.get('improvements', 'N/A')}")


# 전체 통계
print("\n" + "="*80)
print("📈 전체 통계")
print("="*80)

total_problems = len(all_verifications)
correct_answers = sum(1 for r in all_verifications if r['verification'].get('answer_correct', False))
avg_score = sum(r['verification'].get('score', 0) for r in all_verifications) / total_problems

print(f"\n총 문제 수: {total_problems}개")
print(f"정답 개수: {correct_answers}개")
print(f"정답률: {(correct_answers/total_problems)*100:.1f}%")
print(f"평균 점수: {avg_score:.1f}/10")

# 카테고리별 정답률
print(f"\n📊 카테고리별 성과:")
categories = {}
for result in all_verifications:
    cat = result['category']
    if cat not in categories:
        categories[cat] = {'total': 0, 'correct': 0, 'scores': []}
    
    categories[cat]['total'] += 1
    if result['verification'].get('answer_correct', False):
        categories[cat]['correct'] += 1
    categories[cat]['scores'].append(result['verification'].get('score', 0))

for cat, stats in categories.items():
    accuracy = (stats['correct'] / stats['total']) * 100
    avg_cat_score = sum(stats['scores']) / len(stats['scores'])
    print(f"  • {cat}: {stats['correct']}/{stats['total']} (정답률 {accuracy:.0f}%, 평균 {avg_cat_score:.1f}점)")

# 추론 품질 분석
print(f"\n🎯 추론 품질 분포:")
quality_counts = {}
for result in all_verifications:
    quality = result['verification'].get('reasoning_quality', 'unknown')
    quality_counts[quality] = quality_counts.get(quality, 0) + 1

for quality in ['excellent', 'good', 'fair', 'poor', 'unknown']:
    count = quality_counts.get(quality, 0)
    if count > 0:
        bar = '█' * count
        print(f"  {quality.capitalize()}: {bar} ({count}개)")

# 오답 분석
incorrect_problems = [r for r in all_verifications if not r['verification'].get('answer_correct', False)]
if incorrect_problems:
    print(f"\n⚠️ 오답 문제 분석:")
    for problem in incorrect_problems:
        print(f"  • 문제 {problem['problem_id']} ({problem['category']})")
        print(f"    정답: {problem['correct_answer']}")
        print(f"    개선점: {problem['verification'].get('improvements', 'N/A')}")
else:
    print(f"\n🎉 모든 문제를 정답으로 풀었습니다!")

# 결과 저장
print("\n" + "="*80)
print("💾 검증 결과 저장")
print("="*80)

output_file = "cot_verification.json"

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_verifications, f, indent=2, ensure_ascii=False)

print(f"✅ {output_file} 파일에 저장 완료!")

# 요약 리포트
summary = {
    "total_problems": total_problems,
    "correct_answers": correct_answers,
    "accuracy": round((correct_answers/total_problems)*100, 2),
    "average_score": round(avg_score, 2),
    "category_performance": {
        cat: {
            "accuracy": round((stats['correct'] / stats['total']) * 100, 2),
            "avg_score": round(sum(stats['scores']) / len(stats['scores']), 2)
        }
        for cat, stats in categories.items()
    },
    "quality_distribution": quality_counts,
    "incorrect_problem_ids": [r['problem_id'] for r in incorrect_problems]
}

summary_file = "cot_verification_summary.json"

with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(f"✅ {summary_file} 파일에 요약 저장 완료!")

print("\n🎉 미션 3 완료!")
print("\n생성된 파일:")
print(f"  1. {output_file} - 전체 검증 결과 상세")
print(f"  2. {summary_file} - 요약 통계")

# Slack으로 결과 전송
quality_summary = "\n".join([f"{q.capitalize()}: {quality_counts.get(q, 0)}개" for q in ['excellent', 'good', 'fair', 'poor'] if quality_counts.get(q, 0) > 0])
mission3_summary = [
    format_slack_field("🔢 총 문제 수", f"{total_problems}개"),
    format_slack_field("✅ 정답 개수", f"{correct_answers}개 ({(correct_answers/total_problems)*100:.1f}%)"),
    format_slack_field("📊 평균 점수", f"{avg_score:.1f}/10"),
    format_slack_field("🎯 추론 품질", quality_summary),
    format_slack_field("💾 생성 파일", f"• {output_file}\n• {summary_file}")
]
send_slack_summary("미션 3: CoT 답변 검증", mission3_summary)

print("\n"+"="*80+"\n")


# ============================================================================
# 여기에 다른 미션들의 샘플 코드가 추가될 예정입니다
# ============================================================================

"""
💡 향후 추가될 미션들:
- 미션 4: Few-Shot Learning 응용 (12_few_shot_learning.py)
- 미션 5: 역할 부여 프롬프트 (3_1_role-playing.py)
- 미션 6: 다양한 요약 스타일 (5_summarization.py)
- 미션 7: 다국어 번역 (6_translation.py)
- ...
"""

