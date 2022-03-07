import requests
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
# client = MongoClient('mongodb+srv://<id>:<pw>@cluster0.xkvvx.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.dbsparta
URL = "www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita&api_key=1"

r = requests.get(url = URL)

print(r)


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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
    