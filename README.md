<div align=center> <h2> 2021-IRLab-Project </h2> </div>
   
모바일 웹에서 제품의 QR코드를 인식하면 해당 제품의 리뷰 감성분석 정보와, 
열량 정보를 분석하여 제공해주는 서비스를 개발하려고 한다.

- Mobile Web 구현

- 제품 Review data and Train data 수집

- 제품 목록, 제품 정보 Database 구축

- BERT를  single sentence classification 으로 fine tuning 하여 sentiment analysis를 할 수 있도록 설계    

> 이 Github에는 제가 구현한 2번, 3번 사항의 코드를 업로드 하였습니다..

<div align=center> <h2> 흐름도 </h2>

![image](https://user-images.githubusercontent.com/74355042/157233175-6e697127-ed83-4038-896a-af08c52b8380.png)

</div>    

### Moblie Web

- CSS
- JavaScript
- Node js

### Database

- MySQL

  ##### [참고] 식품의약품안전처 DB

  식품의약품안전처는 식품·건강기능 식품·의약품·마약류·화장품·의약외품·의료기기 등의 안전에 관한 사무를 관장하는 정부 대표기관이다.
  그중에서 식품영양성분 DB는 국내의 국가기관, 연구기관 및 산업체가 중심이 되어 식품영양성분 데이터를 생산을 총괄 관리하며, 일반에게도 무료로 공개하고 있다.
  이 DB에는 여러 제조사의 제품 목록과 영양 정보 데이터베이스의 정보를 52,925행, 241열로 구성하여 제공하고 있다.   


### Review Data Mining

- Python

  BeautifulSoup, selenium 을 사용하여 필요한 제품 정보(제품명, 제품가격, 제품이미지, 리뷰 등)을 각종 포털 사이트에서 수집하였다.

### Model

- BERT
   + sentimnet analysis를 위한 single sentence classification 으로 fine tuning

<div align=center> <h2> 결과 </h2> </div>

![image](https://user-images.githubusercontent.com/74355042/157233049-43702590-60c5-46b1-868f-c4ab0e790d10.png)
![image](https://user-images.githubusercontent.com/74355042/157233070-87f0c883-7b5d-4dc9-868c-6ced21789bd0.png)
![image](https://user-images.githubusercontent.com/74355042/157233084-36280802-2e79-455f-b6a6-3f4442fc0b6d.png)
![image](https://user-images.githubusercontent.com/74355042/157233095-4fcbc15d-4e71-4084-9f3f-21df392072de.png)
![image](https://user-images.githubusercontent.com/74355042/157233106-5ebd828c-0c7f-422f-8bf9-14647871da6c.png)

