from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def detail():
    c = requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php?s=')
    response = c.json()
    cocktails = response['drinks']
    return render_template("list.html", cocktails=cocktails)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)