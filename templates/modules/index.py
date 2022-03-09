from ..modules import * 
import math
from flask import Blueprint, render_template, jsonify


blueprint= Blueprint('index', __name__, template_folder="../html", url_prefix='/')


@blueprint.route('/', methods=['GET'])
# def filter_home():
#     return render_template('filter.html' )

def home():
    return redirect(url_for('index.index', i=1 ))


def searchByName(keyword):
    r = requests.get(f"http://www.thecocktaildb.com/api/json/v1/1/search.php?s={keyword}")
    result = r.json()['drinks']
    list1 =[] 
    for x in result:
        list1.append(x['strDrink'])
    # print(list1)
    return list1 

@blueprint.route('/<i>' )
def index(i):

    r = requests.get(f"http://www.thecocktaildb.com/api/json/v1/1/list.php?c=list")
    result2 = r.json()

    req = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=")
    get_data = req.json()

    length = math.ceil(len(get_data['drinks'])//6)
    result = get_data["drinks"][6*(int(i)-1):6*int(i)]

    return render_template("child.html",result2=result2, result=result, i = int(i), len = length  )

@blueprint.route('/result', methods=["POST"] )
def search():
    keyword_receive = request.form['keyword_give']
    result= searchByName(keyword_receive)
    print(result)
    if result is not None:
        print("nothin") 
        return jsonify({"result" : result, "msg" : "success"})
    # return render_template("search.html", result2=result2 )
    else : 
        return jsonify({ "msg" : "failed"}) 
