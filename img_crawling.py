# Importing packages
import time
from urllib.request import urlretrieve
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import pymysql
import os

# Chrome Browser Init
chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome('C:/STUDY/chromedriver.exe', chrome_options=chrome_options)

def naver_search(text):
    browser.get(f'https://search.shopping.naver.com/search/all?query={text}')

    while browser.current_url == 'https://search.shopping.naver.com/too-many-request':
        print('너무 많은 요청(1)')
        time.sleep(10)
        browser.get(f'https://search.shopping.naver.com/search/all?query={text}')

    # 전체 소스를 받도록 페이지 끝으로 이동 ( xpath를 못찾네..?) # from selenium.webdriver import ActionChains
    # scroll = browser.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div[2]/div[4]/div[1]/div[3]/div/span')
    # action = ActionChains(browser)
    # action.move_to_element(scroll).perform()

    # body 찾아서 페이지 다운 한번 누르기
    body = browser.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

    # 브라우저에서 현재 페이지 추출
    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')

    items = soup.find_all('div', {'class': 'basicList_info_area__17Xyo'})
    images = soup.find_all('div', {'class': 'basicList_img_area__a3NRA'})

    for item, image in zip(items, images):
        item_img = image.find('img').get('src')
        item_price_str = item.find('div', {'class': 'basicList_price_area__1UXXR'}).get_text()

        if item_price_str[0:2] != '광고':
            urlretrieve(item_img, f'./img/{text}.jpg')
            break


    time.sleep(1.5)

def select_test():
    conn = pymysql.connect(host='localhost', user='root', password='irlab', db='test', charset='utf8')

    try:
        with conn.cursor() as cursor:
            sql = 'select * from foods'
            cursor.execute(sql)
            rows = cursor.fetchall()

            for row in rows:
                print(row[1], '제품 Data')
                try:
                    naver_search(row[1])
                except Exception:
                    print('네이버 쇼핑에 이 제품이 없거나 이미지 파일이 없습니다.\n', Exception)
    finally:
        conn.close()

if __name__ == '__main__':
    img_dir = './img'

    if not os.path.isdir(img_dir):
        os.mkdir('./img')

    select_test()
