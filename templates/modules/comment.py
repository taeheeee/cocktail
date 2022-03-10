from ..modules import * 
import math
import requests, math
from flask import Flask, render_template, request, jsonify, url_for, Blueprint
import jwt
import datetime, time
import hashlib
from pymongo import MongoClient
import os
from dotenv import load_dotenv


blueprint= Blueprint('commnet', __name__, template_folder="../html", url_prefix='/comment')



client = MongoClient(os.environ.get('MONGO_URL'))
db = client.cluster0

SECRET_KEY = 'SPARTA'



## TODO: 삭제 수정 업데이트 해야함

#################################
##  COMMENT  CURD             ##
#################################


##  코멘트 쓰기 
##  End point
##  /comment/write
##  TODO : increased number 해야함
@blueprint.route('/write', methods=['POST'])
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

##  코멘트 삭제 
##  End point
##  /comment/delete
# @app.route('/delete')
# def delete_comment():
#     user_receive = request.form['user_give']
#     drink_receive = request.form['drink_give']
#     user_data = db.user.update_one({'username':user_receive}, {'$pull':{'favorite': drink_receive}})
#     return jsonify({'msg': '즐겨찾기에 제거되었습니다.'})


##  코멘트 수정 
##  End point
##  /comment/update
# @app.route('/update') 
# def update_comment():
#     user_receive = request.form['user_give']
#     drink_receive = request.form['drink_give']
#     user_data = db.user.update_one({'username':user_receive}, {'$pull':{'favorite': drink_receive}})
#     return jsonify({'msg': '즐겨찾기에 제거되었습니다.'})
