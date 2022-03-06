import re
import csv
import time
import math
import datetime

import pymysql
from selectorlib import Extractor
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Chrome Browser Init
chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome('D:/Program/study/chromedriver.exe', chrome_options=chrome_options)

# Class used to perform all naver scraping.
class st11_review_scraper:
    def __init__(self, st11_site, product_asin, product, sleep_time, start_page=1, end_page=None):
        # 상품 고유 값(ASIN)
        self.product_asin = product_asin

        # 상품 명
        self.product = product

        # 리뷰 페이지
        self.url = f"https://{st11_site}/products/{product_asin}?"

        # Captcha 방지를 위해 interval 조정
        self.sleep_time = sleep_time

        # 시작 페이지와 마지막 페이지 번호
        self.start_page = start_page

        if (end_page == None):
            self.end_page = self.total_pages()
        else:
            self.end_page = min(end_page, self.total_pages())

        f = open(f'./product_review_data/{product}.csv', 'w', encoding='utf-8')
        self.writer = csv.writer(f)

    def total_pages(self):
        # Request를 만들고 전체 리뷰 HTML page get
        page_html = self.request_wrapper(self.url)

        # HTML page를 parse
        soup = BeautifulSoup(page_html, 'html.parser')

        # 페이지 다운 3번
        page_down = browser.find_element_by_css_selector('body')
        for i in range(3):
            page_down.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)

        # 리뷰 버튼 클릭
        review_btn = '//*[@id="tabMenuDetail2"]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, review_btn)))
        browser.execute_script('arguments[0].click()', (browser.find_element_by_xpath(review_btn)))
        time.sleep(1)

        # 전체 리뷰 수 Find and Counting
        content = soup.find("button", {"aria-controls": "tabpanelDetail2"})
        content = content.get_text()
        total_reviews = int(re.sub(r'[^0-9]', '', content))

        # 전체 리뷰수 / 10으로 전체 페이지수를 구함
        total_pages = math.ceil(total_reviews / 20)

        return total_pages

    def scrape(self):
        # Get HTML page
        url = self.url

        # 리뷰 프레임으로 변경
        browser.implicitly_wait(10)
        browser.switch_to.frame('ifrmReview')

        # # 평점 1점 클릭
        # browser.implicitly_wait(10)
        # browser.execute_script('arguments[0].click()',
        #                        (browser.find_element_by_xpath('//*[@id="star-score-div"]/div[1]')))
        # time.sleep(0.5)
        # browser.execute_script('arguments[0].click()',
        #                        (browser.find_element_by_xpath('//*[@id="star-score"]/dd[6]/label/span')))
        # time.sleep(1)

        print("Started!", flush=True)
        # 시작 페이지 - 마지막 페이지 Crawling
        for page in tqdm(range(self.start_page, self.end_page + 1)):
            try:
                browser.execute_script('arguments[0].click()', (browser.find_element_by_xpath(
                    '//*[@id="review-list-page-area"]/div/button')))
            except NoSuchElementException:
                self.page_scraper(url)

            # 다음 Scrape 까지 대기
            time.sleep(self.sleep_time)

    def page_scraper(self, url):        # 브라우저에서 현재 페이지 추출
        page_html = browser.page_source
        data = extractor_st11.extract(page_html)
        # if data['reviews'] == None:
        #     print('부정 데이터 리뷰가 없습니다.')
        #     raise Exception

        # 긍정 1 부정 0 .csv
        for review in data['reviews']:
            if review['content'] == None:
                pass
            elif review['rating'][3] == '4' or review['rating'][3] == '5':
                self.writer.writerow(['1', review['content']])
            elif review['rating'][3] == '1' or review['rating'][3] == '2':
                self.writer.writerow(['0', review['content']])

        time.sleep(self.sleep_time)

    def request_wrapper(self, url):
        # Get HTML Request
        browser.get(url)

        # 브라우저에서 현재 페이지 추출
        page_html = browser.page_source

        return page_html

def st11_asin_search(text):
    # 카테고리 개수
    for i in range(1, 6):
        # 제조사를 검색한 사이트로 이동
        browser.get(f'https://search.11st.co.kr/Search.tmall?kwd={text}')

        # 카테고리 더보기
        browser.implicitly_wait(10)
        browser.execute_script('arguments[0].click()', (browser.find_element_by_xpath(
            '//*[@id="layBodyWrap"]/div/div/div[3]/section/div[5]/div[2]/div[2]/button')))
        # 카테고리 클릭
        browser.implicitly_wait(10)
        try:
            browser.execute_script('arguments[0].click()', (browser.find_element_by_xpath(
                f'//*[@id="layBodyWrap"]/div/div/div[3]/section/div[5]/div[2]/ul/li[{i}]/span')))
        except NoSuchElementException:
            break

        # 필터 더보기 클릭
        browser.implicitly_wait(10)
        browser.execute_script('arguments[0].click()', (browser.find_element_by_xpath(
            '//*[@id="layBodyWrap"]/div/div/div[3]/div/div[2]/div/div[2]/div/div/button')))
        # 많은 리뷰순 클릭
        time.sleep(0.5)
        browser.execute_script('arguments[0].click()', (browser.find_element_by_xpath(
            '//*[@id="layBodyWrap"]/div/div/div[3]/div/div[2]/div/div[2]/div/ul/li[4]/button')))

        # 브라우저에서 현재 페이지 추출
        time.sleep(1)
        page_html = browser.page_source
        soup = BeautifulSoup(page_html, 'html.parser')

        # 제품 리스트
        item_list = soup.find('ul', {'class': 'c_listing c_listing_view_type_list'}).find_all('li')
        for item in item_list:
            item_asin = item.find('div', {'class': 'c_prd_thumb'}).find('a')['data-log-body']
            item_asin = item_asin[(item_asin.find('content_no') + 13):item_asin.find('","content_name"')]

            asin_list.append(item_asin)

def st11_asin_product_search(text):
    # 제조사를 검색한 사이트로 이동
    # 많은 리뷰순 으로 정렬
    browser.get(f'https://search.11st.co.kr/Search.tmall?kwd={text}#sortCd%%I%%많은%20리뷰순%%1')

    # 브라우저에서 현재 페이지 추출
    time.sleep(1)
    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')

    # 제품 리스트
    item_list = soup.find('ul', {'class': 'c_listing c_listing_view_type_list'}).find_all('li')
    for item in item_list:
        try:
            item_asin = item.find('div', {'class': 'c_prd_thumb'}).find('a')['data-log-body']
            item_asin = item_asin[(item_asin.find('content_no') + 13):item_asin.find('","content_name"')]
        except Exception:
            print('제품이 없습니다')

        try:
            st11_scraper = st11_review_scraper(st11_site="11st.co.kr", product_asin=item_asin, product=text,
                                               sleep_time=1, end_page=250)
            st11_scraper.scrape()
        except Exception:
            print('리뷰 스크랩 오류')
        break

    time.sleep(1)

def select_test():
    conn = pymysql.connect(host='localhost', user='root',
                           password='irlab', db='irlab', charset='utf8')

    try:
        with conn.cursor() as cursor:
            # sql = 'select name from test_foods where num between 497 and 800'
            # cursor.execute(sql)
            # rows = cursor.fetchall()
            rows = [['오뚜기 참깨라면 '], ['델몬트스퀴즈레몬에이드'], ['밀키스'], ['갈릭소보로'], ['둥근달2입'], ['초코칩쿠키']]
            for row in rows:
                st11_asin_product_search(row[0])
    except:
        print(f'{row[0]} 제품 select 실패')
    finally:
        conn.close()

if __name__ == '__main__':
    # CSS 태그정보를 불러옴
    extractor_st11 = Extractor.from_yaml_file('./selector/st11_selectors.yml')

    # 제조사를 검색 후 나온 제품들의 고유번호를 저장하는 배열이다.
    asin_list = []

    # # 제품을 검색할 제조사를 입력한다.
    # manufac_list = ['농심', '오뚜기', '해태', '롯데', '오리온']
    # # 모은 데이터를 현재날짜.csv 파일로 저장한다.
    # f = open(f'./review_data/{datetime.date.today()}.csv', 'w', encoding='utf-8')
    # writer = csv.writer(f)
    # # 제조사별 부정 데이터만 검색
    # for manufac in manufac_list:
    #     print(manufac, 'All Data')
    #     # 제조사를 검색 후 제품의 고유번호를 저장하는 코드를 실행
    #     st11_asin_search(manufac)
    #
    #     for asin in asin_list:
    #         st11_scraper = st11_review_scraper(st11_site="11st.co.kr", product_asin=asin, sleep_time=1, end_page=10)
    #         st11_scraper.scrape()
    #         # try:
    #         #     st11_scraper = st11_review_scraper(st11_site="11st.co.kr", product_asin=asin, sleep_time=1, end_page=10)
    #         #     st11_scraper.scrape()
    #         # except Exception:
    #         #     print('이 제품의 부정 데이터 리뷰가 없습니다.\n')
    #         #     time.sleep(1)
    #         # finally:
    #         #     browser.quit()
    #         #     f.close()

    # 제품명 긍정, 부정 데이터 한 페이지씩 검색

    select_test()

    browser.quit()
