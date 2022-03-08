from ..modules import * 
from flask import Blueprint, render_template
import requests, math

blueprint= Blueprint('list', __name__, template_folder="../html", url_prefix='/list')


@blueprint.route('/<i>')
def list(i):
    req = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=")
    result = req.json()
    return render_template("list.html", i = int(i), len = math.ceil(len(result['drinks'])//6), result= result["drinks"][6*(int(i)-1):6*int(i)])


