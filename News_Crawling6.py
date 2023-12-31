# 테슬라 키워드로 페이지 제한 없이 수집하다가 마지막 페이지를 만나면 종료하는 코드 작성

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def get_news(keyword):

    urls = []
    Data = []

    page = 1
    while True:

        print("page: ", page)

        start = (int(page) - 1) * 10 + 1

        res = requests.get(f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword}&sort=1&photo=0&field=0&pd=4&ds=2023.09.23.16.31&de=2023.09.24.16.31&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:1d,a:all&start={start}")
        soup = BeautifulSoup(res.text, "html.parser")

        if soup.select_one("div.not_found02") != None:
            break

        for a in soup.select("ul.list_news div.news_area a"):
            if a.text == "네이버뉴스":
                urls.append(a["href"])

        for url in urls:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            
            title = soup.select_one("h2#title_area > span").text
            date = soup.select_one("div.media_end_head_info_datestamp span")["data-date-time"]
            media = soup.select_one("div.media_end_head_top img.media_end_head_top_logo_img.light_type")["title"]
            content = re.sub("\<br\/>|\<em.*\>.*\<\/em\>|[a-zA-Z]*\@[a-zA-Z]*\.com|뉴욕=.*|\<[^\>]*\>", "", str(soup.select_one("article#dic_area")).replace("\t", "").replace("\n", "").strip())

            data = (title, date, media, content, url)
            Data.append(data)

        page += 1

    return pd.DataFrame(Data, columns=["제목", "날짜", "매체명", "본문", "URL"])
