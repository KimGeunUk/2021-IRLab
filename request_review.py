import time
import pymysql
import requests
import pandas as pd

def request_api(name):
    url = 'http://192.168.0.17:8000/IRLABFile'
    path = f'./product_review_data_new/{name}.csv'

    data = pd.read_csv(path, names=['num', 'r'])
    data = data.drop('num', axis=1)
    data = data.to_dict()
    data = data['r']

    headers = {'content-type': 'application/json; charset=utf-8-sig'}
    r = requests.post(url, json=data, headers=headers)

    average = r.text.split(':')[1].split(',')[0]
    best = r.text.split(':')[2].split(',')[0].strip('"')
    worst = r.text.split(':')[3].split(',')[0].lstrip('"').rsplit('"}')[0]

    update_test(name, best, worst, average)

def update_test(name, best, worst, average):
    conn = pymysql.connect(host='localhost', user='root', password='irlab', db='irlab', charset='utf8')

    try:
        with conn.cursor() as cursor:
            sql = 'update test_foods set best_review=%s, worst_review=%s, average_review=%s where name=%s'
            cursor.execute(sql, (best, worst, average, name))
        conn.commit()
    finally:
        conn.close()

def select_test():
    conn = pymysql.connect(host='localhost', user='root', password='irlab', db='irlab', charset='utf8')

    try:
        with conn.cursor() as cursor:
            # 제품명과 제조사를 들고오는 sql문
            sql = 'select name from test_foods where num between 24 and 497'
            cursor.execute(sql)
            rows = cursor.fetchall()

            # 반복문을 통해 DB에 있는 데이터를 하나씩 접근한다.
            for row in rows:
                try:
                    request_api(row[0])
                except Exception:
                    print('리뷰가 없는 데이터 입니다.')
                    no_data.append(row[0])
            time.sleep(1)
    finally:
        conn.close()

if __name__ == '__main__':
    no_data = []
    select_test()
    print(no_data)