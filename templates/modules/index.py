from ..modules import * 
from flask import Blueprint, render_template


blueprint= Blueprint('index', __name__, template_folder="../html", url_prefix='/index')


# @blueprint.route('/', methods=['GET'])
# def filter_home():
#     return render_template('filter.html' )

@blueprint.route('/', methods=['GET'])
def home():
    r = requests.get(f"http://www.thecocktaildb.com/api/json/v1/1/list.php?c=list")
    result = r.json()
    print(result)
    return render_template('index.html',  result=result)