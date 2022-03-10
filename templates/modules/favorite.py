from ..modules import * 
import requests
from flask import Flask, render_template, request, jsonify, url_for, Blueprint
import jwt
import datetime
import hashlib
from pymongo import MongoClient
import requests, math
from dotenv import load_dotenv
import os 

blueprint= Blueprint('favorite', __name__, template_folder="../html", url_prefix='/favorite')

SECRET_KEY = "sparta"


def mongo_connect():
    client = MongoClient('mongodb+srv://diasm:83XZZ8LwO0rI95en@cluster0.mye6i.mongodb.net/cluster0?retryWrites=true&w=majority')
    # client = MongoClient(os.environ.get('MONGO_URL'))
    db = client.cluster0
    return db


db = mongo_connect()


#################################
##  HTML을 주는 부분             ##
#################################

##############################
##  유저 정보 관련 API       ##
##############################
@app.route('/user_check', methods=['POST'])
def find_user_favorite():
    user_receive = request.form['user_give']
    try:
        user_data = db.favorite.find_one({'user':user_receive})
        return jsonify({'favorite': user_data['favorite']})
    except:
        return jsonify({'favorite': []})

@app.route('/add_heart', methods=['POST'])
def add_user_favorite():
    user_receive = request.form['user_give']
    drink_receive = request.form['drink_give']
    print(user_receive, drink_receive)
    user_data = db.user.update_one({'username':user_receive}, {'$push':{'favorite': drink_receive}})
    return jsonify({'msg': '즐겨찾기에 추가되었습니다.'})

@app.route('/delete_heart', methods=['POST'])
def delete_user_favorite():
    user_receive = request.form['user_give']
    drink_receive = request.form['drink_give']
    user_data = db.user.update_one({'username':user_receive}, {'$pull':{'favorite': drink_receive}})
    return jsonify({'msg': '즐겨찾기에 제거되었습니다.'})