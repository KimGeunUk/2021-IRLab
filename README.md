<h2> INTRODUCTION </h2>
   
본 프로젝트의 자세한 설명은 다음 블로그에서 확인할 수 있습니다.

[제품 리뷰를 분석하여 소비자에게 다양한 정보를 제공하는 모바일 웹 개발](https://geunuk.tistory.com/90?category=900414)

<h2> My CODE </h2>

<h3> Crawling </h3>

- data_crawling
: 해당 포털 사이트에서 리뷰 데이터를 수집합니다.

- img_crawling
: DB에 등록되어 있는 제품의 제조사 홈페이지로 이동하여 해당 제품의 이미지를 수집합니다.

- qr_crawling
: qr코드 제작 홈페이지에서 DB에 등록되어 있는 제품 코드를 사용하여 qr코드 이미지를 생성합니다.
: 제품 순번, 제품 코드, 제품 명, 제조사, 분류, 용량, 칼로리, 단백질, 지방, 탄수화물, 당, 칼슘, 칼륨, 염분, 콜레스테롤, 포화지방 데이터를 삽입하였습니다.


<h3> DataBase </h3>

- excel_to_db
: 식품의약품안전처에서 받은 제품 정보 DB를 전처리하여 필요한 데이터만 MySQL에 INSERT 하였습니다.

- update_price_url
: DB에 등록되어 있는 제품의 가격, 이미지 url, 제품이 등록되어 있는 url 을 수집하여 UPDATE 하였습니다.

- request_review
: API를 통해 저장된 제품명, 제품 리뷰 파일을 전송하여 도출된 리뷰의 긍·부정 수치, 리뷰 데이터를 DB에 업데이트 하였습니다.

<h2> RESULT </h2>

![image](https://user-images.githubusercontent.com/74355042/157233049-43702590-60c5-46b1-868f-c4ab0e790d10.png)
![image](https://user-images.githubusercontent.com/74355042/157233070-87f0c883-7b5d-4dc9-868c-6ced21789bd0.png)
![image](https://user-images.githubusercontent.com/74355042/157233084-36280802-2e79-455f-b6a6-3f4442fc0b6d.png)
![image](https://user-images.githubusercontent.com/74355042/157233095-4fcbc15d-4e71-4084-9f3f-21df392072de.png)
![image](https://user-images.githubusercontent.com/74355042/157233106-5ebd828c-0c7f-422f-8bf9-14647871da6c.png)

