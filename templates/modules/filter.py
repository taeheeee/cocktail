from ..modules import * 
from flask import Blueprint, render_template


blueprint= Blueprint('filter', __name__, template_folder="../html", url_prefix='/filter')


@blueprint.route('/', methods=['GET'])
def filter_home():
    return render_template('filter.html' )