import requests, math
from flask import Flask, render_template, request, jsonify, url_for
import jwt
import datetime, time
import hashlib
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/comment/write', methods=['POST'])
def add_comment():
    token_receive = request.cookies.get('mytoken')

    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    userinfo = db.user.find_one({'userid': payload['userid']}, {'_id': 0})
    is_login = 'success'
    username = userinfo['username']
    write_date= time.strftime('%c', time.localtime(time.time()))
    drink_receive = request.form['drink_give']
    comment_receive = request.form['comment_give']
    
    print(drink_receive,username,comment_receive) 
# {'$inc':{'num': int(1)}
    db.comment.insert_one({'username': username, 'drink_name' : drink_receive, 'comment' : comment_receive, 'write_date': write_date } )
    return jsonify({'msg': '코멘트가 추가되었습니다.'})

# @app.route('/drink/delete', methods=['POST'])
# def delete_user_favorite():
#     user_receive = request.form['user_give']
#     drink_receive = request.form['drink_give']
#     user_data = db.user.update_one({'username':user_receive}, {'$pull':{'favorite': drink_receive}})
#     return jsonify({'msg': '즐겨찾기에 제거되었습니다.'})

DB_URL = 'mongodb+srv://diasm:83XZZ8LwO0rI95en@cluster0.mye6i.mongodb.net/cluster0?retryWrites=true&w=majority'

client = MongoClient(DB_URL)
db = client.cluster0

SECRET_KEY = 'SPARTA'


# URL = "www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita&api_key=1"
#
# r = requests.get(url = URL)
#
# print(r)

#################################
##  HTML을 주는 부분             ##
#################################

@app.route("/")
@app.route('/<i>')
def home(i=1):
    req = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=")
    result = req.json()
    if i == "favicon.ico": i = 1
    return render_template("index.html", len = math.ceil(len(result['drinks'])/6), result= result["drinks"][6*(int(i)-1):6*int(i)])


@app.route('/favorte')
def favorite():
    return render_template('favorte.html')


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/register')
def register():
    msg = request.args.get("msg")
    return render_template('register.html')

@app.route('/drink/<drinkname>')
def sub_page(drinkname):
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'userid': payload['userid']}, {'_id': 0})
        # return jsonify({'result': 'success', 'username': userinfo['username']})
        is_login = 'success'
        username = userinfo['username']
    except:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        is_login= 'fail'

    if is_login == "success":
        user_data = db.user.find_one({'username':username})
    elif is_login == "fail":
        user_data = None

    req = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=")
    result = req.json()

    comment_list = list(db.comment.find({"drink_name" : drinkname})) 


    print(comment_list) 

    for row in result['drinks']:
        if row['strDrink'] == drinkname:
            return render_template("detail.html",comments = comment_list, drinkname = drinkname, row= row,result = is_login , user = user_data)



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

    db.user.insert_one({'userid': id_receive, 'password': pw_hash, 'username': username_receive, 'favorite': []})


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
    if result is not None:
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

    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})



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

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'userid': payload['userid']}, {'_id': 0})
        return jsonify({'result': 'success', 'username': userinfo['username']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

##############################
##  유저 정보 관련 API       ##
##############################
@app.route('/db/user', methods=['POST'])
def find_user_favorite():
    user_receive = request.form['user_give']
    try:
        user_data = db.favorite.find_one({'user':user_receive})
        return jsonify({'favorite': user_data['favorite']})
    except:
        return jsonify({'favorite': []})

@app.route('/db/add', methods=['POST'])
def add_user_favorite():
    user_receive = request.form['user_give']
    drink_receive = request.form['drink_give']
    print(user_receive, drink_receive)
    user_data = db.user.update_one({'username':user_receive}, {'$push':{'favorite': drink_receive}})
    return jsonify({'msg': '즐겨찾기에 추가되었습니다.'})

@app.route('/db/delete', methods=['POST'])
def delete_user_favorite():
    user_receive = request.form['user_give']
    drink_receive = request.form['drink_give']
    user_data = db.user.update_one({'username':user_receive}, {'$pull':{'favorite': drink_receive}})
    return jsonify({'msg': '즐겨찾기에 제거되었습니다.'})





if __name__ == '__main__':
    app.run('0.0.0.0', port=4200, debug=True)