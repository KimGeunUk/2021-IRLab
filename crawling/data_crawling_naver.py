import time
import math
from selectorlib import Extractor
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
from selenium import webdriver
import pandas as pd
import pymysql
import csv
import datetime

# Chrome Browser Init
chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome('C:/STUDY/chromedriver.exe', chrome_options=chrome_options)

# Class used to perform all naver scraping.
class naver_review_scraper:
    def __init__(self, naver_site, product_asin, sleep_time, start_page=1, end_page=None):
        # 상품 고유 값(ASIN)
        self.product_asin = product_asin

        # 리뷰 페이지
        self.url = f"https://{naver_site}/catalog/{product_asin}?"

        # Captcha 방지를 위해 interval 조정
        self.sleep_time = sleep_time

        # 시작 페이지와 마지막 페이지 번호
        self.start_page = start_page
        if (end_page == None):
            self.end_page = self.total_pages()
        else:
            self.end_page = min(end_page, self.total_pages())

    def total_pages(self):
        # Request를 만들고 전체 리뷰 HTML page get
        page_html = self.request_wrapper(self.url)

        # HTML page를 parse
        soup = BeautifulSoup(page_html, 'html.parser')

        caution = soup.find_all('h2', {'class': 'style_head__2HGCm'})

        if len(caution) >= 1:
            raise Exception

        # 전체 리뷰 수 Find and Counting
        content = soup.find_all("a", {"data-nclick": "N=a:rev.grd"})

        total_reviews = int(content[0].find_all('em')[0].get_text().strip().split(" ")[0].replace(',', '').replace('(', '').replace(')', ''))

        # 전체 리뷰수 / 10으로 전체 페이지수를 구함
        total_pages = math.ceil(total_reviews / 20)

        return total_pages

    def scrape(self):
        print("Started!", flush=True)

        # 리뷰 수가 10페이지보다 적을때
        if self.end_page < 100:
            for page in tqdm(range(self.start_page, self.end_page)):
                # Scrape page
                self.page_scraper(page)

                # 다음 Scrape까지 대기
                time.sleep(self.sleep_time)
        # 시작 페이지 - 마지막 페이지 Crawling
        else:
            for page in tqdm(range(self.start_page, 100)):
                # Scrape page
                self.page_scraper(page)

                # 다음 Scrape까지 대기
                time.sleep(self.sleep_time)
        print('\n')

    def page_scraper(self, page):
        # Get HTML page
        if page == 1:
            url = self.url
            while browser.current_url == 'https://search.shopping.naver.com/too-many-request':
                print('너무 많은 요청(2)\n')
                time.sleep(10)
                browser.get(url)
            page_html = self.request_wrapper(url)
            # 최신순 클릭
            browser.find_element_by_xpath('//*[@id="section_review"]/div[2]/div[1]/div[1]/a[2]').click()
            time.sleep(0.5)
        else:
            count = 0
            while browser.current_url == 'https://search.shopping.naver.com/too-many-request':
                print('너무 많은 요청(3)\n')
                count += 1
                time.sleep(10)
                for i in range(count):
                    browser.back()
            page_html = browser.page_source

        data = extractor_NAVER.extract(page_html)

        # 긍정 1 부정 0 .csv
        for review in data['reviews']:
            if review['rating'][3] == '4' or review['rating'][3] == '5':
                writer.writerow(['1', review['content']])
            elif review['rating'][3] == '1' or review['rating'][3] == '2':
                writer.writerow(['0', review['content']])

        # 다음 페이지 클릭
        if page < 11:
            browser.find_element_by_xpath(f'//*[@id="section_review"]/div[3]/a[{page+1}]').click()
        else:
            browser.find_element_by_xpath(f'//*[@id="section_review"]/div[3]/a[{(page%10)+2}]').click()

        time.sleep(self.sleep_time)

    def request_wrapper(self, url):
        # Get HTML Request
        browser.get(url)

        # 브라우저에서 현재 페이지 추출
        page_html = browser.page_source

        return page_html

# 네이버에서 제품명을 검색하여 제일 첫번째에 있는 제품의 사이트로 이동하는 함수이다.
def naver_search(text):
    browser.get(f'https://search.shopping.naver.com/search/all?query={text}')

    while browser.current_url == 'https://search.shopping.naver.com/too-many-request':
        print('너무 많은 요청(1)')
        time.sleep(10)
        browser.back()

    # 브라우저에서 현재 페이지 추출
    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')

    items = soup.find_all('div', {'class': 'basicList_info_area__17Xyo'})

    for item in items:
        item_asin = item.find('a', {'class': 'basicList_link__1MaTN'}).get('href')
        item_price_str = item.find('div', {'class': 'basicList_price_area__1UXXR'}).get_text()

        if item_price_str[0:2] != '광고':
            item_asin = item_asin[(item_asin.find('nvMid=') + 6):item_asin.find('&catId=')]
            return item_asin

    time.sleep(1.5)

def select_test():
    conn = pymysql.connect(host='localhost', user='root', password='irlab', db='test', charset='utf8')

    try:
        with conn.cursor() as cursor:
            sql = 'select name from all_foods where num between 9500 and 27000'
            cursor.execute(sql)
            rows = cursor.fetchall()

            for row in rows:
                print(row[0], '제품 Data')
                try:
                    # 네이버 리뷰를 크롤링하는 Class의 속성값 부여
                    naver_scraper = naver_review_scraper(naver_site="search.shopping.naver.com", product_asin=naver_search(row[0]), sleep_time=1.2)
                    # 네이버 리뷰 크롤링
                    naver_scraper.scrape()
                except Exception:
                    print('네이버 쇼핑에 이 제품이 없습니다.\n', Exception)
                    time.sleep(1)
    finally:
        conn.close()

if __name__ == '__main__':
    # 크롤링한 리뷰 데이터를 현재 날짜로 저장
    f = open(f'{datetime.date.today()}.csv', 'w', encoding='utf-8')
    writer = csv.writer(f)

    # CSS 태그정보를 불러옴
    extractor_NAVER = Extractor.from_yaml_file('naver_selectors.yml')

    # MySQL DB에서 제품명 정보를 들고옴
    select_test()

    f.close()
