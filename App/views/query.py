from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for
from flask_login import login_user, login_required, current_user 
from App.database import db
from App.forms.query import QueryForm
from App.models import User

query_views = Blueprint('query_views', __name__, template_folder='../templates')

from App.controllers import (
    health_classification,
    get_news_articles
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
       prediction = health_classification(form.textarea.data)
       news = get_news_articles(form.textarea.data)
       prediction_int = int(prediction)
       if prediction_int == 1:
        flash(f" {prediction_int} this claim is most likely credible")
       else:
        flash(f" {prediction_int} this claim is most likely NOT credible")
    return render_template('profile.html', form=form, news=news)