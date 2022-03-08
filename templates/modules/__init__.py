from flask import Flask, render_template, request, jsonify, g,redirect, url_for
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import os 
from datetime import datetime
from bson.objectid import ObjectId
from . import comment, filter, list, login



app = Flask(__name__)

# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['MONGO_URI'] = os.environ.get('MONGO_URL')


# app.register_blueprint(comment.blueprint)
app.register_blueprint(filter.blueprint)
app.register_blueprint(list.blueprint)
# app.register_blueprint(login.blueprint)



#  지역별 필터 기능
# @app.route("/mnt_select", methods=["GET"])
# def mnt_select():
#     doc = []  # 검색을 마친 자료가 들어갈 배열입니다.
#     area_receive = request.args.get("area_give")
#     mountains = list(db.mnt_info.find({}, {'_id': False}))  # 산의 전체 목록을 mountains 변수로 받아옵니다.
#     for mountain in mountains:
#         if area_receive in mountain['mnt_address']:  # 산의 세부 설명에서 mnt_receive로 받은 검색어를 찾아봅니다.
#             doc.append(mountain)  # 일치하는 명산의 번호를 doc 배열에 집어넣습니다.
#     return jsonify({'search_list': doc, 'msg': '검색완료!'})

# @app.route("/mnt_info", methods=["GET"])
# def mnt_get():
#     all_mnt = list(db.mnt_info.find({},{'_id':False}))
#     return jsonify({'mnt': all_mnt})



# def mongo_connect():
#     client = MongoClient(os.environ.get('MONGO_URL'))
#     db = client.cluster0
#     return db

## filters function 
## 카테고리 : 
## 검색 방법 : 1. 이름 
##  1. 칵테일 이름  = www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita
##  2. 재료 이름  =  www.thecocktaildb.com/api/json/v1/1/search.php?i=vodka
##  3. 알콜 = www.thecocktaildb.com/api/json/v1/1/filter.php?a=Alcoholic
##  4. 무알콜 = www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic

# @app.route('/', methods=['GET'])
# def home():
#     r = requests.get(f"http://www.thecocktaildb.com/api/json/v1/1/list.php?c=list")
#     result = r.json()
#     return render_template('index.html',  result=result)

# @app.route('/search/<keyword>')
# def search(keyword):
#     r = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?c={keyword}")
#     result = r.json()
#     print(result)
#     return render_template('search.html', result= result)

# if __name__ == '__main__':
#     app.jinja_env.auto_reload =True
#     app.config['TEMPLATES_AUTO_RELOAD'] = True
#     app.run('0.0.0.0', port=4000, debug=True)
