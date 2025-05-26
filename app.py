from flask import Flask, jsonify, request
from flask_cors import CORS
from crawler import search_news_naver_api
from gpt_sentiment_summary import analyze_and_summarize
import traceback
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({"message": "News sentiment API is running"}), 200

    @app.route('/ping', methods=['GET'])
    def ping():
        return jsonify({"status": "ok"}), 200

    @app.route('/topic-search', methods=['POST'])
    def topic_search():
        try:
            data = request.get_json()
            search_content = data.get('topic')
            print(f"[DEBUG] 검색어: {search_content}")

            if not search_content:
                return jsonify({"error": "검색어를 입력해주세요."}), 400

            max_news = 15
            start_day = "2025.03.01"
            end_day = "2025.05.20"

            news_data = search_news_naver_api(search_content, start_day, end_day, max_news)
            if not news_data:
                return jsonify({"error": "검색된 뉴스가 없습니다."}), 404

            texts = [news.get("content", "") for news in news_data]
            results = analyze_and_summarize(texts)

            sentiment_mapping = {
                "POSITIVE": "긍정",
                "NEGATIVE": "부정",
                "NEUTRAL": "중립",
                "ERROR": "분석 실패"
            }

            for i, news in enumerate(news_data):
                result = results[i]
                news["sentiment"] = sentiment_mapping.get(result["sentiment"], "중립")
                news["content_summarized"] = result["summary"]

            return jsonify({"news": news_data})

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    return app


# Render, Gunicorn용 엔트리포인트
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
