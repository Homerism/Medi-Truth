from flask import Blueprint, render_template, flash
from App.forms.query import QueryForm

index_views = Blueprint('index_views', __name__, template_folder='../templates')

from App.controllers import (
    health_classification,
    get_news_articles,
    similar_claim,
    generate_response,
    call_until_return
)

@index_views.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@index_views.route('/about', methods=['GET'])
def index_about():
    return render_template('about-us.html')

@index_views.route('/checkclaim', methods=['GET'])
def index_checkclaim():
    form = QueryForm()
    return render_template('claimcheck.html', form=form)

@index_views.route('/checkclaim', methods=['POST'])
def checkclaimAction():
    form = QueryForm()
    if form.validate:
       prediction = health_classification(form.textarea.data)
       response = call_until_return(generate_response,form.textarea.data)
       news = get_news_articles(form.textarea.data)
       prediction_int = int(prediction)
       similar_claims = similar_claim(form.textarea.data)
       if prediction_int == 1:
            verdict = "this claim is most likely credible"
            flash(f" {prediction_int} {verdict} {response}")    
       else:
            verdict = "this claim is most likely NOT credible"
            flash(f" {prediction_int} {verdict} {response}")    
    return render_template('claimcheck.html', form=form, news=news, similar_claims=similar_claims)
