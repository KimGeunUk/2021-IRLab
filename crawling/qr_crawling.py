from selenium import webdriver
import pymysql
import time

# Chrome Browser Init
chrome_options = webdriver.ChromeOptions()
# Chrome Crash 방지를 위해 옵션 추가
chrome_options.add_argument('--no-sandbox')
browser = webdriver.Chrome('C:/STUDY/chromedriver.exe', chrome_options=chrome_options)

def qr_search_url(name, url):
    # qr코드 생성 사이트 이동
    browser.get('https://ko.online-qrcode-generator.com/')
    time.sleep(1)

    # url생성 버튼 클릭
    browser.find_element_by_xpath('//*[@id="QR_CODE_Generator_URL_LI"]/a').click()
    time.sleep(1)

    # url 입력
    browser.find_element_by_xpath('//*[@id="QR_CODE_Generator_URL"]').send_keys(url)
    time.sleep(0.5)

    # 저장을 위한 qr코드 이미지 클릭
    browser.find_element_by_xpath('//*[@id="canvasshow"]').click()
    time.sleep(1)

    # 파일명(name) 입력
    browser.find_element_by_xpath('//*[@id="save_qr_code"]').send_keys(name)
    time.sleep(1)

    # 다운로드 버튼 클릭
    browser.find_element_by_xpath('//*[@id="download"]').click()
    time.sleep(1)

def qr_search_name(name, num):
    # qr코드 생성 사이트 이동
    browser.get('https://ko.online-qrcode-generator.com/')
    time.sleep(1)

    # text 입력
    browser.find_element_by_xpath('//*[@id="QR_CODE_Generator_FREE_TEXT"]').send_keys(num+','+name)
    time.sleep(0.5)

    # 저장을 위한 qr코드 이미지 클릭
    browser.find_element_by_xpath('//*[@id="canvasshow"]').click()
    time.sleep(1)

    # 파일명(name) 입력
    browser.find_element_by_xpath('//*[@id="save_qr_code"]').send_keys(name)
    time.sleep(1)

    # 다운로드 버튼 클릭
    browser.find_element_by_xpath('//*[@id="download"]').click()
    time.sleep(1)

def select_test():
    conn = pymysql.connect(host='localhost', user='root', password='irlab', db='test', charset='utf8')

    try:
        with conn.cursor() as cursor:
            sql = 'select name, product_num from new_foods where num between 1 and 100'
            cursor.execute(sql)
            rows = cursor.fetchall()

            # URL
            for row in rows:
                print(row[0], '제품 Data')
                try:
                    # qr코드 생성 사이트로 이동하여 제품명 or 고유번호를 넣어 qr코드 이미지를 저장하는 함수이다
                    qr_search_name(row[0], row[1])
                except Exception:
                    print('제품명이 없습니다.\n', Exception)
    finally:
        conn.close()
        browser.quit()

if __name__ == '__main__':
    select_test()
