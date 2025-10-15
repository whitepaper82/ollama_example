# Ollama Python 예제 모음

Ollama를 활용한 다양한 LLM 활용 예제입니다.

## 사전 준비

### 1. Ollama 설치
```bash
# https://ollama.ai 에서 다운로드 및 설치
```
→ LLM 모델을 실행하는 **서버 프로그램**입니다.

### 2. 모델 다운로드
```bash
# Ollama 설치 후 터미널에서 실행
ollama pull gemma3:4b
ollama pull nomic-embed-text  # RAG 예제용
```

### 3. Python 라이브러리 설치
```bash
# requirements.txt를 이용한 일괄 설치
pip install -r requirements.txt

# 또는 개별 설치
pip install ollama          # Python에서 Ollama 서버와 통신하기 위한 클라이언트 라이브러리
pip install pandas          # 배치 처리 예제용
pip install faiss-cpu numpy # RAG 예제용
```
→ Python에서 Ollama를 사용하기 위한 **클라이언트 라이브러리**입니다.

## 예제 목록

1. **1_basic_chat.py** - 가장 기본적인 대화 예제
2. **2_parameters.py** - temperature, num_ctx, num_predict 등 파라미터 조정
3. **3_prompt_template.py** - 재사용 가능한 프롬프트 함수 래핑
4. **4_json_extraction.py** - 구조화된 JSON 출력으로 정보 추출
5. **5_summarization.py** - 텍스트 요약 및 키워드 추출
6. **6_translation.py** - 번역 및 스타일 전환
7. **7_classification.py** - 텍스트 분류 및 근거 제시
8. **8_mini_rag.py** - FAISS + Ollama를 활용한 간단한 RAG 구현
9. **9_streaming.py** - 실시간 스트리밍 출력
10. **10_batch_processing.py** - 여러 문서 배치 처리
11. **11_grading.py** - AI 자체 평가 및 채점
12. **12_few_shot_learning.py** - Few-shot Learning (예시로 패턴 학습)

## 실행 방법

```bash
python 1_basic_chat.py
python 2_parameters.py
# ... 등등
```

## 팁

- **temperature**: 낮을수록(0.0~0.3) 일관성↑, 높을수록(0.7~1.0) 창의성↑
- **num_ctx**: 컨텍스트 윈도 크기 (메모리/VRAM 사용량에 영향)
- **num_predict**: 생성할 최대 토큰 수
- **format='json'**: JSON 형식으로 구조화된 출력 강제

## 주의사항

- Ollama 서비스가 실행 중이어야 합니다
- 모델이 다운로드되어 있어야 합니다
- RAG 예제는 추가 패키지(faiss, numpy)가 필요합니다

## 라이센스

MIT License - 자유롭게 사용, 수정, 배포하실 수 있습니다.

