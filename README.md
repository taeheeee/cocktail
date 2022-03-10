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
   favorite : array
   }

   comment :{
   "\_id" : integer,
   "userid" : string,
   "comments" : string,
   "number" : integer,
   "idDrink" : integer,
   }

4. API
   | URL | METHOD | DATA |
   |------|------|-----|
   | user/api/login    | POST   | {userid[string], password[string], \_id[objectID] }                                  |
   | user/api/register | POST   | {userid[string], username[string], password[string], \_id[objectID], favorite[list]} |
   | search/result     | POST   | {drink_name[string]}                                                                 |
   | favorite/user_check| POST   | {username[string], favorite[array] }                                                |
   | favorite/add_heart| POST   | {username[string], drink_name[string], favorite[array]}                              |
   | favorite/delete_heart| POST   | {username[string], drink_name[string], favorite[array]}                           |
   | comment/write     | POST   | {userid[ogjectID], idDrink[objectID], comments[string]}                              |
   | comment/update    | POST   | {userid[ogjectID], idDrink[objectID], comments[string]}                              |
   | comment/delete    | POST   | {userid[ogjectID], idDrink[objectID], comments[string]}                              |
5.  Route Name

| ROOT ROUTE NAME   | SUB ROUTE NAME | FUNCTIONS                                                                            | LOCATION |
|-------------------|----------------|--------------------------------------------------------------------------------------|----------|
| /                 | 1,2,3,4......  | Pagination                                                                           | index.py|
| /favorite         | favorite.html  | Check your favorite cocktail if you're my memeber                                    | index.py|
| /register         | registr.html   | Register member with ID, PW                                                          | index.py|
| /login            | login.html     | Log-in if you're my memeber                                                          | index.py|
| /drink/<drinkname>| detail.html    | Show cocktail's detail that you are interseted in                                    | index.py|


6. 사용된 모듈

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
