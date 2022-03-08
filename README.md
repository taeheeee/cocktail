5조프로젝트- cocktail

개요 1. 칵테일 레시피와 재료 API를 이용한 검색 리뷰 사이트

1. 프로젝트 목표

   1. 기본 CURD를 이용한 웹 어플리케이션 작성
   2. JINA2 를 이용한 서버 사이드 렌더링의 이해
   3. JWT 토큰을 이용한 프로그램
   <!-- 4. 필요한 기능을 올바르게 구현했나 -->

2.

3. DB 구조화 (DB models.py)

   User : {
   }

   comment :{

   }

4. API
   | URL | METHOD | DATA |
   |-------------------|--------|-------------------------------------------------------------------------------------|
   | user/api/login | POST | {userid[string], password[string], \_id[objectID] } |
   | user/api/register | POST | {userid[string], username[string], password[string], \_id[objectID], favorite[list]} |
   | user/api/logout | GET | {} |
   | user/api/token | POST | {} |
   | comment/write | POST | {} |
   | comment/update | POST | {} |
   | comment/delete | POST | {} |

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
    - commnet.html <---코멘트 ㅏ능 >
    - filter.html <-----필터기능>
  - modules

    - 
