import requests
import os
import time
import html
from bs4 import BeautifulSoup

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def clean_html_text(text):
    """HTML 엔티티 디코딩 및 태그 제거"""
    if not text:
        return ""
    text = html.unescape(text)
    return BeautifulSoup(text, "html.parser").get_text()

def search_news_naver_api(query, start_date, end_date, max_news=15):
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }

    collected = []
    display = 15
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
                "title": clean_html_text(item["title"]),
                "url": item["link"],
                "content": clean_html_text(item["description"]),
                "company": item.get("originallink", "Naver"),
            })
            if len(collected) >= max_news:
                break

        start += display
        time.sleep(0.5)

    print(f"[INFO] API로 수집된 뉴스 수: {len(collected)}")
    return collected
