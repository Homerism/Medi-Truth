from flask import Blueprint, render_template, flash, request
index_views = Blueprint('index_views', __name__,template_folder='../templates')

from App.controllers import (
    health_classification,
    get_news_articles,
    similar_claim,
    generate_response,
    call_until_return,
    scholar_articles
)

@index_views.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@index_views.route('/about', methods=['GET'])
def index_about():
    return render_template('about-us.html')

@index_views.route('/checkclaim', methods=['GET'])
def index_checkclaim():
    return render_template('claimcheck.html')

@index_views.route('/checkclaim', methods=['POST'])
def checkclaimAction():
    input = request.form.get("claim")
    prediction = health_classification(input)
    response = call_until_return(generate_response, input)
    news = get_news_articles(input)
    scholar = scholar_articles(input)
    prediction_int = int(prediction)
    similar_claims = similar_claim(input)
    if prediction_int == 1:
        verdict = "this claim is most likely credible"
        flash(f"  {verdict}")
        flash(f"  {response}")
    else:
        verdict = "this claim is most likely NOT credible"
        flash(f"  {verdict}")
        flash(f"  {response}")
    return render_template('claimcheck.html', news=news, scholar=scholar, similar_claims=similar_claims)
