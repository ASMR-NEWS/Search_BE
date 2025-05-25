import requests
import os
import time

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def search_news_naver_api(query, start_date, end_date, max_news=15):
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }

    collected = []
    display = 15  # 한번에 가져올 기사 수 (최대 100, 기본 10)
    start = 1

    while len(collected) < max_news:
        url = "https://openapi.naver.com/v1/search/news.json"
        params = {
            "query": query,
            "display": display,
            "start": start,
            "sort": "date",
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"[ERROR] Naver API 호출 실패: {response.status_code}")
            break

        items = response.json().get("items", [])
        if not items:
            break

        for item in items:
            collected.append({
                "title": item["title"],
                "url": item["link"],
                "content": item["description"],
                "company": item.get("originallink", "Naver"),
            })
            if len(collected) >= max_news:
                break

        start += display
        time.sleep(0.5)  # Rate limit 회피용

    print(f"[INFO] API로 수집된 뉴스 수: {len(collected)}")
    return collected
