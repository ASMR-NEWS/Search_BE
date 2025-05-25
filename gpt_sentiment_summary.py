import openai
import os
import time
from tqdm import tqdm

# OpenAI API 키 설정 (환경변수에서 로드)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def analyze_and_summarize(texts):
    results = []

    for text in tqdm(texts, desc="Processing GPT Sentiment + Summary"):
        try:
            prompt = f"""
다음은 뉴스 기사입니다. 이 기사의 감정을 분류하고, 그 감정에 맞춰 요약문을 작성하세요.

요구사항:
1. 감정 분류는 POSITIVE, NEGATIVE, NEUTRAL 중 하나로 대문자로 작성하세요.
2. 요약은 감정에 따라 작성 방식이 달라야 하며, 100자 이내의 줄글 형식으로 작성하세요.
   - POSITIVE - 기사의 내용이 희망적이거나 개선, 진전, 호의적 평가 등을 포함할 경우
   - NEGATIVE - 문제 제기, 충돌, 부정적 결과, 불만, 비판, 갈등, 손해 등을 포함할 경우
   - NEUTRAL - 사실 전달이나 감정적 편향이 없이 객관적으로 서술된 경우
3. 명사형 마무리 금지, '-'나 괄호, 감정 표시 없이 자연스럽게 끝나야 합니다.

주의:
- '부정'은 단순히 부정적인 단어가 아니라, **실질적인 사회적/경제적/정서적 문제**가 강조될 때 사용하세요.
- 논란, 비판, 손실, 위험, 갈등은 부정으로 간주하세요.

뉴스 기사:
{text}

응답 형식:
감정: 감정값
요약: 요약문
"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for classifying sentiment and summarizing news articles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )

            output = response.choices[0].message["content"].strip()
            lines = output.split("\n")
            sentiment = "NEUTRAL"
            summary = "요약 실패"

            for line in lines:
                if line.strip().upper().startswith("감정:"):
                    sentiment = line.split(":", 1)[1].strip().upper()
                    if sentiment not in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']:
                        sentiment = "NEUTRAL"
                elif line.strip().startswith("요약:"):
                    summary = line.split(":", 1)[1].strip()

            results.append({
                "sentiment": sentiment,
                "summary": summary
            })

        except Exception as e:
            print(f"[ERROR] Failed to process text: {text[:30]}... | {e}")
            results.append({
                "sentiment": "ERROR",
                "summary": "요약 실패"
            })
            time.sleep(1)

    return results
