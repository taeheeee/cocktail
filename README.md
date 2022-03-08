5조프로젝트- cocktail

개요 1. 칵테일 레시피와 재료 API를 이용한 검색 리뷰 사이트

1. 프로젝트 목표

   1. 기본 CURD를 이용한 웹 어플리케이션 작성
   2. JINA2 를 이용한 서버 사이드 렌더링의 이해
   3. JWT 토큰을 이용한 프로그램
   <!-- 4. 필요한 기능을 올바르게 구현했나 -->

2. 참고 api

   1. https://www.thecocktaildb.com/api.php

3. DB 구조화 ()

   "user" : {
   "userid" : string,
   "username" : string,
   "password" : string,
   "\_id" : integer,
   favorite : list
   }

   comment :{
   "\_id" : integer,
   "userid" : string,
   "comments" : string,
   "number" : integer,
   "idDrink" : integer,
   }

4. API
   /user/api/login	POST	{userid[string], password[string]}	로그인
/user/api/register	POST	{userid[string], username[string], password[string]}	회원가입
/api/nick	GET	{userid[string],_id[int]}	유저정보 확인
comment/write	POST	{userid, idDrink, comments }	코멘트 쓰기
comment/update	POST	{userid, idDrink, comments}	코멘트 업데이트
comment/delete	POST	{userid, idDrink}	코멘트 제거
comment/list	GET	{ "userid" , "comments", "date" } {}	코멘트 리스트 확인

5. 사용된 모듈

- flask
  - blueprint
  - jinja2
  - url_for
  - render_template
  - request
  - jsonfiy
  - render_template
- requests
- dotenv -> secured enviornment
-

6. 폴더 구조 및 설명

- static
  - css
    - comment.css
    - filter.css
    - index.css
    - list.css
- templates

  - html
    - commnet.html <---코멘트 기능
    - filter.html <-----필터 기능
    - list.html
    - login.html
  - modules
    - comment.py
    - filter.py
    - list.py
    - login.py
