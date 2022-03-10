from flask import Flask, render_template, request, jsonify, g,redirect, url_for
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import os 
from datetime import datetime
from bson.objectid import ObjectId
from . import comment, search, user, index 

## TEMPLTATES location
app = Flask(__name__, template_folder="../html")

##환경변수 설정
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['MONGO_URI'] = os.environ.get('MONGO_URL')

##몽고디비 함수
def mongo_connect():
    client = MongoClient(os.environ.get('MONGO_URL'))
    db = client.cluster0



## 모듈화 
## index : 메인 페이지
## comment : 코멘트 작성, 수정, 삭제 
## user : 로그인 관련 및 토큰 
## search : 검색 기능 관련 기능
## 

app.register_blueprint(index.blueprint)
app.register_blueprint(comment.blueprint)
app.register_blueprint(user.blueprint)
app.register_blueprint(search.blueprint)



def clever_function(keyword):
    print(keyword)
    # r = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?c={keyword}")
    # result = r.json()
    # print(result)
    return u'HELLO' 

app.jinja_env.globals.update(clever_function=clever_function)