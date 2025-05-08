from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
from tqdm import tqdm
import requests

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]


def fetch_urls_selenium(query, start_date, end_date, max_news=50):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")

    driver = webdriver.Chrome(options=chrome_options)
    urls = set()

    try:
        for start in tqdm(range(1, 1000, 10), desc="뉴스 URL 수집 중"):
            if len(urls) >= max_news:
                break

            url = (
                f"https://search.naver.com/search.naver?where=news&query={query}"
                f"&sm=tab_pge&sort=0&photo=0&field=0&pd=3&ds={start_date}&de={end_date}&start={start}"
            )
            driver.get(url)

            # ✅ 페이지 로딩 대기
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a"))
            )

            soup = BeautifulSoup(driver.page_source, "html.parser")
            a_tags = soup.select("a")

            for a in a_tags:
                href = a.get("href", "")
                span = a.find("span")
                if "n.news.naver.com" in href and span and "네이버뉴스" in span.text:
                    urls.add(href)
                    if len(urls) >= max_news:
                        break
    finally:
        driver.quit()

    return list(urls)


def fetch_news_content_requests(url):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": "https://search.naver.com/",
        "Accept-Language": "ko-KR,ko;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            company_tag = soup.select_one("meta[property='me2:category1']")
            company = company_tag["content"] if company_tag else "None"

            title_tag = soup.select_one("h2#title_area") or soup.select_one("title")
            title = title_tag.text.strip() if title_tag else "None"

            content_tag = soup.select_one("article#dic_area") or soup.select_one("div#newsct_article")
            content = content_tag.get_text(separator=" ", strip=True) if content_tag else "None"

            return {
                "company": company,
                "url": url,
                "title": title,
                "content": content,
            }
    except Exception as e:
        print(f"[본문 수집 실패] {url} | {e}")

    return {
        "company": "None",
        "url": url,
        "title": "None",
        "content": "None",
    }


def start_crawling(search_content, startdays, enddays, max_news=50):
    all_urls = set()
    for start_day, end_day in zip(startdays, enddays):
        urls = fetch_urls_selenium(search_content, start_day, end_day, max_news)
        all_urls.update(urls)

    all_urls = list(all_urls)[:max_news]
    print(f"[INFO] 최종 수집된 뉴스 URL 수: {len(all_urls)}")

    news_data = []
    for url in tqdm(all_urls, desc="뉴스 본문 수집 중"):
        article = fetch_news_content_requests(url)
        news_data.append(article)
        time.sleep(0.5)

    df_news = pd.DataFrame(news_data)
    if "content" not in df_news.columns:
        print("[ERROR] 'content' 컬럼이 없습니다. 수집 실패.")
        return []

    df_news = df_news[df_news['content'].str.len() > 50]
    return df_news.to_dict(orient="records")
