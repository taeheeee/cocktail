import requests, math
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient('mongodb+srv://test:qwerty1@cluster0.yhkrb.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

req = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=")
result = req.json()

@app.route('/')
@app.route('/<i>')
def home(i=1):
    return render_template("index.html", i = int(i), len = math.ceil(len(result['drinks'])//6), result= result["drinks"][6*(int(i)-1):6*int(i)])

@app.route('/drink', methods=['POST'])
def add_comment():
    drink_receive = request.form['drink_give']
    user_receive = request.form['username_give']
    comment_receive = request.form['comment_give']

    doc = {
        'name' : drink_receive,
        'user' : user_receive,
        'comment' : comment_receive
    }

    db.drinks.insert_one(doc)
    
    return jsonify({'msg' : '성공적으로 작성되었습니다!'})

# 서브 페이지 작업 중
@app.route('/drink/<drinkname>')
def sub_page(drinkname):
    comment_list = db.drinks.find({'name': drinkname})
    for row in result['drinks']:
        if row['strDrink'] == drinkname:
            return render_template("detail.html", comments = comment_list, row= row)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)