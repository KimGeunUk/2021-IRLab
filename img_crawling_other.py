# Importing packages
import re
import time
from urllib.request import urlretrieve
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql
import os

# Chrome Browser Init
chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome('D:/Program/study/chromedriver.exe', chrome_options=chrome_options)

table = 'test_foods'

def update_test(where, col1):
    conn = pymysql.connect(host='localhost', user='root', password='irlab', db='irlab', charset='utf8')

    try:
        with conn.cursor() as cursor:
            sql = 'update test_foods set img=%s where name=%s'
            cursor.execute(sql, (col1, where))
        conn.commit()
    finally:
        conn.close()

# DB Delet example
def delete_test(where):
    conn = pymysql.connect(host='localhost', user='root', password='irlab', db='irlab', charset='utf8')
    try:
        with conn.cursor() as cursor:
            sql = 'delete from test_foods where name=%s'
            cursor.execute(sql, where)
        conn.commit()
    finally:
        conn.close()

def nodata_search(name, manufac):
    # 해당 제조사로 이동하여 제품명을 검색한다.
    st11 = 'https://search.11st.co.kr/Search.tmall?kwd='
    browser.get(st11+name)

    # 브라우저에서 현재 페이지 추출
    browser.implicitly_wait(10)
    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')

    # 제품이 없으면 no_data의 길이가 1 이상이되고 있으면 0이 된다
    no_data = soup.find_all('p', {'class': 'nodata_text'})

    if len(no_data) >= 1:
        delete_test(name)
        raise Exception
        return 0
    else:
        items = soup.find_all('div', {'class': 'c_listing'})
        # 제품의 이미지와 가격을 불러온다.
        for item in items:
            item_price = item.find('span', {'class': 'value'}).get_text()
            item_img = item.find('img').get('src')
            item_price_str = int(re.sub(r'[^0-9]', '', item_price))
            urlretrieve(item_img, f'./img2/{name}.jpg')

            update_test(name, item_img)
            break

    time.sleep(1)


def ottogi_search(name, manufac):
    ottogi = 'http://www.ottogimall.co.kr/'
    browser.get(ottogi)

    browser.implicitly_wait(10)
    search_box = '//*[@id="top"]/div/div[3]/div/form/fieldset/div/input[1]'
    browser.find_element_by_xpath(search_box).send_keys(name)
    browser.find_element_by_xpath(search_box).send_keys(Keys.ENTER)

    time.sleep(1)
    # 브라우저에서 현재 페이지 추출
    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')

    no_data = soup.find_all('div', {'class': 'no-data'})

    if len(no_data) >= 1:
        print(name + '데이터 삭제')
        delete_test(name)
        raise Exception
    else:
        items = soup.find_all('div', {'class': 'list'})

        for item in items:
            item_price = item.find('span', {'class': 'cost'}).get_text()
            item_img = item.find('img').get('src')
            item_price_str = int(re.sub(r'[^0-9]', '', item_price))
            urlretrieve(ottogi+item_img, f'./img2/{name}.jpg')

            update_test(name, ottogi+item_img)
            break

    time.sleep(1)

def lotte_search(name, manufac):
    lotte = 'https://www.lotteon.com/search/search/search.ecn?render=search&platform=pc&q='
    browser.get(lotte+name)

    browser.implicitly_wait(10)

    # 브라우저에서 현재 페이지 추출
    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')

    no_data = soup.find_all('section', {'class': 'srchResultNull srchNullCharacter1'})

    if len(no_data) >= 1:
        delete_test(name)
        raise Exception
    else:
        items = soup.find_all('ul', {'class': 'srchProductList on'})

        for item in items:
            item_price = item.find('span', {'class': 's-product-price__number'}).get_text()
            item_img = item.find('img').get('src')
            item_price_str = int(re.sub(r'[^0-9]', '', item_price))
            urlretrieve(item_img, f'./img2/{name}.jpg')

            update_test(name, item_img)
            break

    time.sleep(1)

def haitai_search(name, manufac):
    haitai = 'https://www.haitaimall.co.kr/product/search.html?banner_action=&keyword='
    browser.get(haitai+name)

    browser.implicitly_wait(10)

    # 브라우저에서 현재 페이지 추출
    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')

    no_data = soup.find_all('div', {'class': 'noData'})

    if len(no_data) >= 1:
        delete_test(name)
        raise Exception
    else:
        items = soup.find_all('ul', {'class': 'prdList grid4'})

        for item in items:
            item_price = item.find('span', {'title': '판매가'}).get_text()
            item_img = item.find('img').get('src')
            item_price_str = int(re.sub(r'[^0-9]', '', item_price))
            urlretrieve('http'+item_img, f'./img2/{name}.jpg')

            update_test(name, 'http'+item_img)
            break

    time.sleep(1)

def nongshim_search(name, manufac):
    nongshim = 'https://www.elandmall.com/search/search.action?kwd='
    browser.get(nongshim+name)

    browser.implicitly_wait(10)
    # 브라우저에서 현재 페이지 추출
    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')

    no_data = soup.find_all('div', {'class': 'rsch_txt'})

    if len(no_data) >= 1:
        print(name + '데이터 삭제')
        delete_test(name)
        raise Exception
    else:
        items = soup.find_all('ul', {'class': 'list'})

        for item in items:
            #item_price = item.find('span', {'title': '판매가'}).get_text()
            item_img = item.find('img').get('src')
            #item_price_str = int(re.sub(r'[^0-9]', '', item_price))
            #urlretrieve(item_img, f'./img2/{name}.jpg')
            update_test(name, 'https:'+item_img)
            break

    time.sleep(1)

def orion_search(name, manufac):
    orion = 'http://corners2.auction.co.kr/SmileDelivery/Search?keyword='
    browser.get(orion+name)

    browser.implicitly_wait(10)
    # 브라우저에서 현재 페이지 추출
    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')

    no_data = soup.find_all('div', {'class': 'wrap__empty-keyword-result'})

    if len(no_data) >= 1:
        print(name + '데이터 삭제')
        delete_test(name)
        raise Exception
    else:
        items = soup.find_all('ul', {'class': 'list__deals'})

        for item in items:
            #item_price = item.find('span', {'title': '판매가'}).get_text()
            item_img = item.find('img').get('src')
            #item_price_str = int(re.sub(r'[^0-9]', '', item_price))
            #urlretrieve(item_img, f'./img2/{name}.jpg')
            update_test(name, item_img)
            break

    time.sleep(1)

def select_test():
    conn = pymysql.connect(host='localhost', user='root', password='irlab', db='irlab', charset='utf8')

    try:
        with conn.cursor() as cursor:
            # 제품명과 제조사를 들고오는 sql문
            sql = 'select name, manufac from test_foods'
            cursor.execute(sql)
            rows = cursor.fetchall()

            # 반복문을 통해 DB에 있는 데이터를 하나씩 접근한다.
            for row in rows:
                # 조건문을 통해 해당 데이터의 제조사가 일치하면 실행하도록 하였다.
                # if row[1] == '오뚜기':
                #     print(row[0], '제품 Data')
                #     try:
                #         # 해당 제조사의 공식 판매처로 이동하여 이미지 주소를 들고와 MySQL에 저장하는 함수
                #         ottogi_search(row[0], row[1])
                #     except Exception:
                #         print('오뚜기에 이 제품이 없거나 이미지 파일이 없습니다.\n')
                #
                # elif row[1] == '롯데':
                #     print(row[0], '제품 Data')
                #     try:
                #         lotte_search(row[0], row[1])
                #     except Exception:
                #         print('롯데에 이 제품이 없거나 이미지 파일이 없습니다.\n')
                #
                # elif row[1] == '해태':
                #     print(row[0], '제품 Data')
                #     try:
                #         haitai_search(row[0], row[1])
                #     except Exception:
                #         print('해태에 이 제품이 없거나 이미지 파일이 없습니다.\n')
                #
                # elif row[1] == '농심':
                #     print(row[0], '제품 Data')
                #     try:
                #         nongshim_search(row[0], row[1])
                #     except Exception:
                #         print('농심에 이 제품이 없거나 이미지 파일이 없습니다.\n')

                if row[1] == '오리온':
                    print(row[0], '제품 Data')
                    try:
                        orion_search(row[0], row[1])
                    except Exception:
                        print('오리온에 이 제품이 없거나 이미지 파일이 없습니다.\n')

                # else:
                #     print(row[0], '제품 Data')
                #     try:
                #         nodata_search(row[0], row[1])
                #     except Exception:
                #         print('11번가에도 이 제품이 없거나 이미지 파일이 없습니다.\n')

                time.sleep(1)
    finally:
        conn.close()
        browser.quit()

if __name__ == '__main__':
    # 이미지를 저장할 폴더를 지정, 없으면 생성한다.
    img_dir = './img2'
    if not os.path.isdir(img_dir):
        os.mkdir('./img2')

    # MySQL 에서 제품명을 들고오는 함수이다.
    select_test()

