from flask import Blueprint,render_template, request, flash
from flask_login import login_required, current_user 
from App.models import Query, ArticleRate
from App.database import db

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
    create_query,
    create_article_for_doctors,
    calculate_rating,
    get_article_id,
    query_check,
    scholar_articles
)

@query_views.route('/query', methods=['GET'])
@login_required
def index_page():
    return render_template('profile.html')

@query_views.route('/query', methods=['POST'])
def queryAction():
    input = request.form.get("claim")
    prediction = health_classification(input)
    prediction_int = int(prediction)
    similar_claims = similar_claim(input)
    curr_user = get_user(current_user.id)
    curr_user_queries = curr_user.queries
    check_query = query_check(curr_user_queries, input)
    if not check_query:
        response = call_until_return(generate_response, input)
        news = get_news_articles(input)
        scholar = scholar_articles(input)
        storedArticles = ArticleRate.query.all()
        create_article_for_doctors(news, storedArticles)
        verdict = "This Claim Is Most Likely Credible." if prediction_int == 1 else "This Claim Is Most Likely NOT Credible."
        query = create_query(input, response, verdict)
        curr_user.queries.append(query)
        add_query(curr_user)
        create_article(news, query.id)
        flash(f"  {verdict}")
        flash(f"  {response}")
    else:
        news = get_news_articles(input)
        scholar = scholar_articles(input)
        response = call_until_return(generate_response, input)
        verdict = "This Claim Is Most Likely Credible." if prediction_int == 1 else "This Claim Is Most Likely NOT Credible."
        flash(f"  {verdict}")
        flash(f"  {response}")
    return render_template('profile.html', news=news, scholar=scholar, similar_claims=similar_claims, get_article_id=get_article_id, calculate_rating=calculate_rating, str=str, int=int)

@query_views.route('/queries', methods=['GET'])
@login_required
def queries_page():
    curr_user_id = current_user.id
    curr_user = get_user(curr_user_id)
    return render_template('queries.html', user=curr_user)

@query_views.route('/filter/<int:id>')
@login_required
def filter(id):
    curr_user_id = current_user.id
    curr_user = get_user(curr_user_id)
    verdict =""
    if id == 1:
        verdict = "This Claim Is Most Likely Credible."
    else:
        verdict = "This Claim Is Most Likely NOT Credible."
    results = Query.query.filter_by(user_id=curr_user_id, verdict=verdict).all()
    if not results:
        flash(f"None Found.")
    return render_template('queries.html', user=curr_user, results=results)

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
    return render_template('details.html', details=curr_query,get_article_id=get_article_id, calculate_rating=calculate_rating,str=str)