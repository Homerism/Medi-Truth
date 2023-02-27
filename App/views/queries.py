from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for
from flask_login import login_user, login_required, current_user 
from App.database import db
from App.forms.query import QueryForm
from App.models import User, Query

queries_views = Blueprint('queries_views', __name__, template_folder='../templates')


@queries_views.route('/queries', methods=['GET'])
@login_required
def index_page():
    curr_user_id = current_user.id
    curr_user = User.query.get(curr_user_id)
    return render_template('queries.html', user=curr_user)