from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for
from flask_login import login_user, login_required, current_user 
from App.database import db
from App.forms.query import QueryForm
from App.models import User, Query

query_views = Blueprint('query_views', __name__, template_folder='../templates')

from App.controllers import (
    health_classification
)

@query_views.route('/query', methods=['GET'])
@login_required
def index_page():
    form = QueryForm()
    return render_template('profile.html', form=form)


@query_views.route('/query', methods=['POST'])
@login_required
def queryAction():
    form = QueryForm()
    if form.validate:
       curr_user_id = current_user.id
       curr_user = User.query.get(curr_user_id)
       
       prediction = health_classification(form.textarea.data)
       news = get_news_articles(form.textarea.data)
       prediction_int = int(prediction)
       if prediction_int == 1:
            verdict = "this claim is most likely credible"
            curr_user.queries.append(Query(form.textarea.data, verdict))
            add_query(curr_user)
            flash(f" {prediction_int} this claim is most likely credible")
       else:
        flash(f" {prediction_int} this claim is most likely NOT credible")
      
    return render_template('profile.html', form=form)