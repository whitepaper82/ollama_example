# 8) 미니 RAG — 로컬 FAISS + Ollama 결합
# 사전 준비: ollama pull nomic-embed-text
# pip install faiss-cpu numpy pandas

import ollama
from typing import List
import numpy as np
import faiss


def ask(model, task, system="한국어로 간결하고 정확하게 답해줘.", **options):
    return ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": task}
        ],
        options=options or {}
    )['message']['content']


docs = [
    "LangChain은 LLM을 외부 데이터/툴과 연결하는 프레임워크다.",
    "Ollama는 로컬에서 LLM을 쉽게 돌릴 수 있게 해주는 런타임이다.",
    "RAG는 검색 결과를 LLM 프롬프트에 주입해 최신/사내 지식을 활용한다.",
    "Gemma3 4B는 가벼운 로컬 추론에 적합한 중소형 모델이다."
]


# 1) 임베딩 함수 (Ollama embeddings API)
def embed_texts(texts: List[str]) -> np.ndarray:
    vecs = []
    for t in texts:
        e = ollama.embeddings(model='nomic-embed-text', prompt=t)
        vecs.append(np.array(e['embedding'], dtype='float32'))
    return np.vstack(vecs)


doc_vecs = embed_texts(docs)

# 2) FAISS 색인
index = faiss.IndexFlatIP(doc_vecs.shape[1])
faiss.normalize_L2(doc_vecs)
index.add(doc_vecs)


def retrieve(query, k=2):
    qv = embed_texts([query])
    faiss.normalize_L2(qv)
    D, I = index.search(qv, k)
    return [docs[i] for i in I[0]]


# 3) 질의 → 검색 → 답변 생성
def rag_answer(question):
    ctx = "\n".join(retrieve(question, k=3))
    prompt = f"""
아래 컨텍스트를 참고해 질문에 한국어로 답해줘.
컨텍스트:
{ctx}

질문: {question}
답변은 간결하지만 정확하게.
"""
    return ask('gemma3:1b', prompt, temperature=0)


print(rag_answer("RAG가 왜 필요한가요?"))

