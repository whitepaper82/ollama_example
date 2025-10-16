# 4) 구조화 출력(JSON)로 정보추출
import ollama
import json

text = """
주문 3건:
1) 상품: 무선마우스, 수량 2, 가격 25,000원
2) 상품: 기계식 키보드, 수량 1, 가격 89,000원
3) 상품: USB-C 케이블, 수량 3, 가격 9,900원
총 배송지는 서울시 강남구 테헤란로 1
"""

prompt = f"""
아래 텍스트에서 주문 항목을 JSON으로 추출해.
스키마:
{{
  "orders":[{{"item":str,"qty":int,"price_krw":int}}],
  "shipping_address": str,
  "total_price_krw": int
}}
텍스트:
{text}
반드시 JSON만 출력.
"""

resp = ollama.chat(
    model='gemma3:1b',
    messages=[{"role": "user", "content": prompt}],
    format='json',  # JSON 모드
    options={"temperature": 0}
)

data = json.loads(resp['message']['content'])
print(json.dumps(data, indent=2, ensure_ascii=False))

