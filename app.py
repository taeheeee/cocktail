from dotenv import load_dotenv
import os
load_dotenv()

import requests
from flask import Flask, render_template, request, jsonify,url_for
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient(os.getenv('DB_URL'))
db = client.dbsparta

SECRET_KEY = os.getenv('SECRETKEY')

import jwt

import datetime

import hashlib


#수정했다. 

# URL = "www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita&api_key=1"
#
# r = requests.get(url = URL)
#
# print(r)

#################################
##  HTML을 주는 부분             ##
#################################

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/favorte')
def favorite():
    return render_template('favorte.html')


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/register')
def register():
    return render_template('register.html')




#################################
##  로그인을 위한 API            ##
#################################

# [회원가입 API]
# userid, password, username을 받아서, mongoDB에 저장한다
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/user/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']

    pw_receive = request.form['pw_give']

    username_receive = request.form['name_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'userid': id_receive, 'password': pw_hash, 'username': username_receive})


    if(id_receive==''):
        return  jsonify({'result': 'fail','msg':'아이디를 입력하세요'})
    elif(pw_receive==''):
        return jsonify({'result': 'fail', 'msg': '비밀번호를 입력하세요'})
    elif (username_receive == ''):
        return jsonify({'result': 'fail', 'msg': '이름을 입력하세요'})
    else:
        return jsonify({'result': 'success'})




# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/user/api/login', methods=['POST'])
# /api/login 창구를 만들어서 그창구에서는 post만 받는것을  def api_login()쪽으로와라
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'userid': id_receive, 'password': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if(id_receive==''):
        return jsonify({'result': 'fail', 'msg': '아이디를 입력해주세요.'})
    elif(pw_receive==''):
        return jsonify({'result': 'fail', 'msg': '비밀번호를 입력해주세요.'})
    elif(result is not None):

        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'userid': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

    # 찾지 못하면




# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
@app.route('/api/nick', methods=['GET'])
# /api/nick 창구를 만들어서 그창구에는 get만 받는것은 api_vlid()쪽으로와라
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'userid': payload['userid']}, {'_id': 0})
        return jsonify({'result': 'success', 'username': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


# 회원가입할때 아이디 중복되는지 확인하는 API

@app.route('/user/api/registerch',methods=['POST'])
def regis_check():
    id_receive = request.form['id_receive']
    exists = bool(db.user.find_one({"userid":id_receive}))
    return jsonify({'result':'success','exists':exists})






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

# @app.route("/mnt_info", meth                                                                            ods=["GET"])
# def mnt_get():
#     all_mnt = list(db.mnt_info.find({},{'_id':False}))
#     return jsonify({'mnt': all_mnt})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
    
