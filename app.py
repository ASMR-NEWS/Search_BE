from flask import Flask, jsonify, request
from flask_cors import CORS
from crawler import start_crawling
from gpt_sentiment_summary import analyze_and_summarize  # 통합된 GPT 분석 함수
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

            max_news = 15
            if not search_content:
                return jsonify({"error": "검색어를 입력해주세요."}), 400

            startday = ["2025.03.01"]
            endday = ["2025.05.20"]

            news_data = start_crawling(search_content, startday, endday, max_news)
            if not news_data:
                return jsonify({"error": "크롤링된 뉴스가 없습니다."}), 404

            contents = [news.get('content', '') for news in news_data]
            analysis_results = analyze_and_summarize(contents)

            sentiment_mapping = {
                "POSITIVE": "긍정",
                "NEGATIVE": "부정",
                "NEUTRAL": "중립",
                "ERROR": "분석 실패"
            }

            for i, news in enumerate(news_data):
                result = analysis_results[i]
                sentiment_kr = sentiment_mapping.get(result["sentiment"], "중립")
                news["sentiment"] = sentiment_kr
                news["content_summarized"] = result["summary"]

            return jsonify({"news": news_data})

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    return app

# Render나 gunicorn을 위한 엔트리 포인트
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
