from ..modules import * 
import math
import requests, math
from flask import Flask, render_template, request, jsonify, url_for
import jwt
import datetime, time
import hashlib
from pymongo import MongoClient
import os
from dotenv import load_dotenv


blueprint= Blueprint('index', __name__, template_folder="../html", url_prefix='/')



client = MongoClient(os.environ.get('MONGO_URL'))
db = client.cluster0

SECRET_KEY = 'SPARTA'




#################################
##  HTML을 주는 부분             ##
#################################


@blueprint.route('/<i>' )
def home(i=1):
    r = requests.get(f"http://www.thecocktaildb.com/api/json/v1/1/list.php?c=list")
    result2 = r.json()

    req = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=")
    result = req.json()
    if i == "favicon.ico": i = 1
    return render_template("index.html", result2 = result2, len = math.ceil(len(result['drinks'])/6), result= result["drinks"][6*(int(i)-1):6*int(i)])

    req = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=")
    get_data = req.json()

##무슨 작업페이지일까?
@blueprint.route('/favorte')
def favorite():
    return render_template('favorte.html')

##로그인 가능한 페이지
@blueprint.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

##회원 가입페이지
@blueprint.route('/register')
def register():
    msg = request.args.get("msg")
    return render_template('register.html')

##아이템 선택시 들어가지는 페이지 ( 로그인시 본인의 코멘트 수정 삭제 가능 / 즐겨찾기 추가 )
@blueprint.route('/drink/<drinkname>')
def sub_page(drinkname):
    ##인증 절차
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        userinfo = db.user.find_one({'userid': payload['userid']}, {'_id': 0})
        is_login = 'success'
        username = userinfo['username']
    except:
        is_login= 'fail'

    if is_login == "success":
        user_data = db.user.find_one({'username':username})
    elif is_login == "fail":
        user_data = None

    req = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=")
    result = req.json()

    ##코멘트 리스트 불러오기(username, comment_list)
    comment_list = list(db.comment.find({"drink_name" : drinkname})) 
        
    for row in result['drinks']:
        if row['strDrink'] == drinkname:
            return render_template("detail.html",comments = comment_list, drinkname = drinkname, row= row,result = is_login , user = user_data)





#################################
##  인덱스 페이지 API  및 함수      ##
#################################

##검색 키워드 받아서 리스트로 반환하는 함수
def searchByName(keyword):
    r = requests.get(f"http://www.thecocktaildb.com/api/json/v1/1/search.php?s={keyword}")
    result = r.json()['drinks']
    list1 =[] 
    for x in result:
        list1.append(x['strDrink'])
    # print(list1)
    return list1 

def token_auth():
    ##인증 절차
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        userinfo = db.user.find_one({'userid': payload['userid']}, {'_id': 0})
        is_login = 'success'
        username = userinfo['username']
    except:
        is_login= 'fail'

    if is_login == "success":
        user_data = db.user.find_one({'username':username})
    elif is_login == "fail":
        user_data = None
    return user_data

##검색 결과물을 보여준다
@blueprint.route('/result', methods=["POST"] )
def search():
    keyword_receive = request.form['keyword_give']
    result= searchByName(keyword_receive)
    print(result)
    if result is not None:
        print("nothin") 
        return jsonify({"result" : result, "msg" : "success"})
    # return render_template("search.html", result2=result2 )
    else : 
        return jsonify({ "msg" : "failed"}) 
