import requests
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
app = Flask(__name__)


@app.route('/')
def home():
    req = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=")
    result = req.json()
    print(len(result['drinks']))
    return render_template("index.html", result= result["drinks"])

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)