from ..modules import * 
from flask import Blueprint, render_template


blueprint= Blueprint('filter', __name__, template_folder="../html", url_prefix='/filter')


# @blueprint.route('/', methods=['GET'])
# def filter_home():
#     return render_template('filter.html' )

@blueprint.route('/', methods=['GET'])
def home():
    r = requests.get(f"http://www.thecocktaildb.com/api/json/v1/1/list.php?c=list")
    result = r.json()
    return render_template('base.html',  result=result)

@blueprint.route('/search/<keyword>')
def search(keyword):
    r = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?c={keyword}")
    result = r.json()
    print(result)
    return render_template('child.html', result= result)