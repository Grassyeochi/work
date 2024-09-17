import requests
from bs4 import BeautifulSoup
import time

# 검색 키워드 목록
keywords = ["보훈", "피해 장병", "군대", "복지", "예비역", "군 병원"]

# 결과를 저장할 파일
output_file = "crawling.txt"

# 기본 URL
base_url = "https://search.naver.com/search.naver?where=news&query="


def fetch_news(keyword, page):
    url = f"{base_url}{keyword}&start={(page - 1) * 10 + 1}"  # 페이지네이션
    response = requests.get(url)
    response.raise_for_status()  # 응답 상태 코드가 200이 아닐 경우 예외 발생
    return response.text


def parse_news(html):
    soup = BeautifulSoup(html, 'html.parser')
    news_list = []

    # 뉴스 리스트를 찾습니다.
    news_items = soup.select('ul.list_news._infinite_list > li.bx')

    for item in news_items:
        # 제목과 링크 추출
        title_tag = item.select_one('div.news_wrap.api_ani_send div.news_area div.news_contents a.news_tit')
        if title_tag:
            title = title_tag.get('title')
            link = title_tag.get('href')
        else:
            title = None
            link = None

        # 언론사 추출
        press_tag = item.select_one('div.info_group > a')
        press = press_tag.text.strip() if press_tag else None

        if title and link and press:
            news_list.append((title, link, press))

    return news_list


def save_to_file(news_items, keyword, page, max_page):
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f"-----------------------------------------\n주제 : {keyword} / {page}페이지 \n-----------------------------------------\n\n")
        for title, link, press in news_items:
            f.write(f"제목 : {title}\n링크 : {link}\n언론사 : {press}\n\n")
        if(page == max_page):
            f.write("-----------------------------------------\n\n\n")


def main():
    max_page = 2

    for keyword in keywords:
        print(f"Fetching news for keyword: {keyword}")
        for page in range(1, max_page + 1):
            html = fetch_news(keyword, page)
            news_items = parse_news(html)
            save_to_file(news_items, keyword, page, max_page)
            time.sleep(1)  # 서버에 부담을 주지 않기 위해 잠시 대기


if __name__ == "__main__":
    main()
