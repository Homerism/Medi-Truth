from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for
from flask_login import login_user, login_required, current_user 
from App.database import db
from App.forms.query import QueryForm
from App.models import User, Query, Article

details_views = Blueprint('details_views', __name__, template_folder='../templates')


@details_views.route('/details', methods=['POST'])
@login_required
def index_page():
    queryId = request.form['details']
    curr_query = Query.query.get(queryId)
    
    return render_template('details.html', details=curr_query)