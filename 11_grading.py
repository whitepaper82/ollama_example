# 11) 간단 "정답 체크" 루브릭(자체평가) — 채점 프롬프트
import ollama
import json


def ask(model, task, system="한국어로 간결하고 정확하게 답해줘.", **options):
    return ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": task}
        ],
        options=options or {}
    )['message']['content']


student_answer = ask('gemma3:1b', "RAG의 정의를 한 문장으로 설명해줘.", temperature=0)

rubric = """
채점 기준:
1) 정의의 정확성(0~4)
2) 간결성(0~3)
3) 핵심 용어 사용(0~3)
총점=10, JSON으로만 출력: {"score": <0-10>, "feedback": "<한줄 피드백>"}
학생 답변:
""" + student_answer

grade = ollama.chat(
    model='gemma3:1b',
    messages=[{"role": "user", "content": rubric}],
    format='json',
    options={"temperature": 0}
)

print("학생 답변:", student_answer)
print("\n채점 결과:")
print(json.dumps(json.loads(grade['message']['content']), indent=2, ensure_ascii=False))

