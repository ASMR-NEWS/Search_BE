from flask import Flask, jsonify, request
from flask_cors import CORS
from crawler import start_crawling
from sentiment_analysis import analyze_and_map_sentiments
from summarizer import summarize_with_sentiment
import traceback
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/ping', methods=['GET'])
    def ping():
        return jsonify({"status": "ok"}), 200

    @app.route('/topic-search', methods=['POST'])
    def topic_search():
        try:
            data = request.get_json()
            search_content = data.get('topic')
            print(f"[DEBUG] 검색어: {search_content}")

            max_news = 5
            if not search_content:
                return jsonify({"error": "검색어를 입력해주세요."}), 400

            startday = ["2025.04.01"]
            endday = ["2025.05.07"]
            # news_data = start_crawling(...)
            news_data = start_crawling(search_content, startday, endday, max_news)
            if not news_data:
                return jsonify({"error": "크롤링된 뉴스가 없습니다."}), 404

            texts = [news.get('title', '') for news in news_data]
            sentiments = ["중립"] * len(news_data)
            sentiment_mapping = {
                "POSITIVE": "긍정",
                "NEGATIVE": "부정",
                "NEUTRAL": "중립"
            }
            mapped_sentiments = [sentiment_mapping.get(s, "중립") for s in sentiments]

            for i, news in enumerate(news_data):
                sentiment = mapped_sentiments[i] if i < len(mapped_sentiments) else "중립"
                content = news.get("content", "")
                summary = content[:80] + "..."  # 그냥 잘라내기
                news["sentiment"] = sentiment
                news["content_summarized"] = summary

            return jsonify({"news": news_data})

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    return app

# Render가 gunicorn으로 import할 수 있도록 아래 객체 제공
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
