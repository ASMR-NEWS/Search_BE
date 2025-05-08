from flask import Flask, jsonify, request
from flask_cors import CORS
from crawler import start_crawling
from sentiment_analysis import analyze_and_map_sentiments
from summarizer import summarize_with_sentiment
import traceback
import os

app = Flask(__name__)
CORS(app)

@app.route('/topic-search', methods=['POST'])
def topic_search():
    try:
        data = request.get_json()
        search_content = data.get('topic')
        max_news = 50

        if not search_content:
            return jsonify({"error": "검색어를 입력해주세요."}), 400

        startday = ["2025.04.01"]
        endday = ["2025.05.07"]
        news_data = start_crawling(search_content, startday, endday, max_news)

        # 크롤링 결과 없음 예외 처리
        if not news_data:
            return jsonify({"error": "크롤링된 뉴스가 없습니다."}), 404

        texts = [news.get('title', '') for news in news_data]
        sentiments = analyze_and_map_sentiments(texts)

        sentiment_mapping = {
            "POSITIVE": "긍정",
            "NEGATIVE": "부정",
            "NEUTRAL": "중립"
        }
        mapped_sentiments = [sentiment_mapping.get(s, "중립") for s in sentiments]

        # 뉴스 요약 및 감정 추가
        for i, news in enumerate(news_data):
            sentiment = mapped_sentiments[i] if i < len(mapped_sentiments) else "중립"
            content = news.get("content", "")
            news["sentiment"] = sentiment
            news["content_summarized"] = summarize_with_sentiment(content, sentiment)

        return jsonify({"news": news_data})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)