from selectorlib import Extractor                   # 홈페이지의 필요한 tag를 저장해두고 한번에 들고오기 위해
from bs4 import BeautifulSoup                       # 홈페이지의 페이지 소스를 받아오기 위해
from selenium import webdriver                      # 세부적인 이동을 할때의 자동화를 위해
from selenium.webdriver.common.keys import Keys     # 키보드 입력을 위해
import pymysql                                      # MySQL을 사용하기 위해
import time                                         # 일정한 간격을 두기 위해
import csv                                          # .csv 파일로 저장하기 위해
import re                                           # 문장을 정제하기 위해

# DB Update test
def update_test(where, col1, col2):
    conn = pymysql.connect(host='localhost', user='root', password='irlab', db='test', charset='utf8')

    try:
        with conn.cursor() as cursor:
            sql = 'update new_foods set price=%s, url=%s where name=%s'
            cursor.execute(sql, (col1, col2, where))

        conn.commit()
    finally:
        conn.close()


# DB Delet example
def delete_test(num):
    conn = pymysql.connect(host='localhost', user='root', password='irlab', db='test', charset='utf8')
    try:
        with conn.cursor() as cursor:
            sql = 'delete from foods where food_no=%s'
            cursor.execute(sql, num)
        conn.commit()
        with conn.cursor() as cursor:
            sql = 'delete from food_manufac where food_no=%s'
            cursor.execute(sql, num)
        conn.commit()
    finally:
        conn.close()

def naver_search(text):
    # 받아온 text(제품명)을 검색한 주소를 입력하여 이동한다.
    browser.get(f'https://search.shopping.naver.com/search/all?query={text}')
    time.sleep(1)

    # 너무 많은 요청을 할때 잠시 사이트가 자동적으로 변경되는데 10초 후 다시 이동하게 설정
    while browser.current_url == 'https://search.shopping.naver.com/too-many-request':
        time.sleep(10)
        browser.get(f'https://search.shopping.naver.com/search/all?query={text}')

    # 브라우저에서 현재 페이지 추출
    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')

    # 첫 페이지 제품 리스트 정보 선택
    items = soup.find_all('div', {'class': 'basicList_info_area__17Xyo'})

    # 이후 반복문을 통해 광고인 제품이 아니면 업데이트
    for item in items:
        # 제품 링크와 가격 정보를 선택
        item_link = item.find('a', {'class': 'basicList_link__1MaTN'}).get('href')
        item_price_str = item.find('div', {'class': 'basicList_price_area__1UXXR'}).get_text()

        if item_price_str[0:2] != '광고':
            # 가격 정보를 원하는 형태로 정제
            item_price = ''.join(re.findall('\d+', item_price_str[:(item_price_str.find('원'))]))
            # 링크 정보로 이동 후 반환
            browser.get(item_link)
            time.sleep(3)
            item_link = browser.current_url
            # 업데이트 함수 실행
            update_test(text, item_price, item_link)
            break

    time.sleep(1)

def select_test():
    conn = pymysql.connect(host='localhost', user='root', password='irlab', db='test', charset='utf8')

    try:
        with conn.cursor() as cursor:
            sql = 'select * from new_foods'
            cursor.execute(sql)
            rows = cursor.fetchall()

            for row in rows:
                if row[3] == None and row[4] == None:
                    # 업데이트 할때
                    print(f'{row[1]} 제품 update ...')
                    naver_search(row[1])
                    time.sleep(1)
    except:
        print(f'{row[1]} 제품 update 실패')
    finally:
        conn.close()

if __name__ == '__main__':
    # Chrome Browser Init
    chrome_options = webdriver.ChromeOptions()
    browser = webdriver.Chrome('C:/STUDY/chromedriver.exe', chrome_options=chrome_options)

    select_test()