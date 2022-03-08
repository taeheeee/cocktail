import requests, math
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
app = Flask(__name__)

@app.route('/<i>')
def home(i):
    req = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=")
    result = req.json()
    return render_template("index.html", i = int(i), len = math.ceil(len(result['drinks'])//6), result= result["drinks"][6*(int(i)-1):6*int(i)])


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)