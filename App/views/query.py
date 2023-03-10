from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for
from flask_login import login_user, login_required, current_user 
from App.database import db
from App.forms.query import QueryForm
from App.models import User, Query, Article

query_views = Blueprint('query_views', __name__, template_folder='../templates')

from App.controllers import (
    health_classification,
    add_query,
    get_news_articles,
    similar_claim,
    create_article
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
       queryInList = False
       prediction = health_classification(form.textarea.data)
       news = get_news_articles(form.textarea.data)
       prediction_int = int(prediction)
       similar_claims = similar_claim(form.textarea.data)

       if prediction_int == 1:
            verdict = "this claim is most likely credible"
            for eachQuery in curr_user.queries:
                if (eachQuery.query_text == form.textarea.data):
                    queryInList = True
                    break
            if not queryInList:
                query = Query(form.textarea.data, verdict)
                curr_user.queries.append(query)
                add_query(curr_user)
                create_article(news,query.id)
                queryInList = False
            flash(f" {prediction_int} this claim is most likely credible")
       else:
            verdict = "this claim is most likely NOT credible"
            for eachQuery in curr_user.queries:
                if (eachQuery.query_text == form.textarea.data):
                    queryInList = True
                    break
            if not queryInList:
                query = Query(form.textarea.data, verdict)
                curr_user.queries.append(query)
                add_query(curr_user)
                create_article(news,query.id)
                queryInList = False
            flash(f" {prediction_int} this claim is most likely NOT credible")
      
    return render_template('profile.html', form=form, news=news, similar_claims=similar_claims)