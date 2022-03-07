from ..modules import * 
from flask import Blueprint, render_template


blueprint= Blueprint('list', __name__, template_folder="../html", url_prefix='/filter')


@blueprint.route('/', methods=['GET'])
def list_home():
    return render_template('list.html' )