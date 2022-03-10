from ..modules import * 
from flask import Blueprint, render_template

blueprint= Blueprint('search', __name__, template_folder="../html", url_prefix='/search')



## 검색 결과를 리스트로 return 
def searchByName(keyword):

    r = requests.get(f"http://www.thecocktaildb.com/api/json/v1/1/search.php?s={keyword}")

    result = r.json()['drinks']
    list1 =[] 

    for x in result:
        list1.append(x['strDrink'])

    return list1 




##칵테일 이름으로 검색 결과 
## End point
## /search/result
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


