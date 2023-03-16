from flask import Blueprint,render_template, request, flash
from flask_login import login_required, current_user 
from App.database import db
from App.forms.query import QueryForm
from App.models import Query, ArticleRate

query_views = Blueprint('query_views', __name__, template_folder='../templates')

from App.controllers import (
    health_classification,
    add_query,
    get_news_articles,
    similar_claim,
    create_article,
    generate_response,
    call_until_return,
    remove_query,
    get_user,
    get_query,
    create_query,
    create_article_for_doctors
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
       curr_user = get_user(curr_user_id)
       queryInList = False
       prediction = health_classification(form.textarea.data)
       response = call_until_return(generate_response,form.textarea.data)
       news = get_news_articles(form.textarea.data)
       
       #for doctor feed
       storedArticles = ArticleRate.query.all()
       create_article_for_doctors(news,storedArticles)
       #end doctor feed

       prediction_int = int(prediction)
       similar_claims = similar_claim(form.textarea.data)
       if prediction_int == 1:
            verdict = "this claim is most likely credible"
            for eachQuery in curr_user.queries:
                if (eachQuery.query_text == form.textarea.data):
                    queryInList = True
                    break
            if not queryInList:
                query = create_query(form.textarea.data, response, verdict)
                curr_user.queries.append(query)
                add_query(curr_user)
                create_article(news,query.id)
                queryInList = False
            flash(f" {prediction_int} {verdict} {response}")    
       else:
            verdict = "this claim is most likely NOT credible"
            for eachQuery in curr_user.queries:
                if (eachQuery.query_text == form.textarea.data):
                    queryInList = True
                    break
            if not queryInList:
                query = create_query(form.textarea.data, response, verdict)
                curr_user.queries.append(query)
                add_query(curr_user)
                create_article(news,query.id)
                queryInList = False
            flash(f" {prediction_int} {verdict} {response}")    
    return render_template('profile.html', form=form, news=news, similar_claims=similar_claims)

@query_views.route('/queries', methods=['GET'])
@login_required
def queries_page():
    curr_user_id = current_user.id
    curr_user = get_user(curr_user_id)
    return render_template('queries.html', user=curr_user)

@query_views.route('/remove', methods=['POST'])
@login_required
def queries_page_remove():
    curr_user_id = current_user.id
    curr_user = get_user(curr_user_id)
    queryId = request.form['removal']
    remove_query(queryId)
    flash(f"Your query was successfully removed")    
    return render_template('queries.html', user=curr_user)

@query_views.route('/details', methods=['POST'])
@login_required
def details_page():
    queryId = request.form['details']
    curr_query = Query.query.get(queryId)
    return render_template('details.html', details=curr_query)