from flask import Blueprint,render_template, flash
from flask_login import login_required, current_user 
from App.database import db
from App.models import ArticleRate
feed_views = Blueprint('feed_views', __name__, template_folder='../templates')

from App.controllers import (
    create_reaction
)

@feed_views.route('/feed', methods=['GET'])
@login_required
def index_page():
    doctorArticles = ArticleRate.query.all()
    return render_template('doctorFeed.html', articles=doctorArticles)

@feed_views.route('/like/<int:article_id>')
def like(article_id):
    doctorArticles = ArticleRate.query.all()
    curr_user_id = current_user.id
    create_reaction(curr_user_id, "Approve", article_id)
    return render_template('doctorFeed.html', articles=doctorArticles)

@feed_views.route('/dislike/<int:article_id>')
def dislike(article_id):
    doctorArticles = ArticleRate.query.all()
    curr_user_id = current_user.id
    create_reaction(curr_user_id, "Disapprove", article_id)
    return render_template('doctorFeed.html', articles=doctorArticles)

#@feed_views.route('/search', methods=['POST'])
#def search_product():
  #doctorArticles = ArticleRate.query.all()
  #queryresults = str(request.form["searcharticle"]) #requests search term
  #results = article_search(queryresults) #Searches for product in database
  #count=0
  #Checking the amount of items in results (Returns item not found if count = 0)
  #for article in results:
    #count+=1
  #if queryresults is None or queryresults =="": 
    #flash("Please enter an article keyword")
    #return render_template('doctorFeed.html', articles=doctorArticles)
  #if count == 0: 
    #flash("Sorry No articles was found.")
    #return render_template('doctorFeed.html', articles=doctorArticles)
  #else:
    #return render_template('doctorFeed.html', articles=doctorArticles, results=results)