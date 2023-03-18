from flask import Blueprint,render_template, flash, request
from flask_login import login_required, current_user 
from App.database import db
from App.models import ArticleRate, DoctorReaction
feed_views = Blueprint('feed_views', __name__, template_folder='../templates')

from App.controllers import (
    create_reaction,
    article_search
)

@feed_views.route('/feed', methods=['GET'])
@login_required
def index_page():
    doctorArticles = ArticleRate.query.all()
    return render_template('doctorFeed.html', articles=doctorArticles)

@feed_views.route('/rankedfeed', methods=['GET'])
@login_required
def ranked_queries_page():
    curr_user_id = current_user.id
    rankedArticles = DoctorReaction.query.filter_by(user_id=curr_user_id)
    doctorArticles = ArticleRate.query.all()
    doctorArticleList = []

    for eachArticle in rankedArticles:
       for eachDoctorArticle in doctorArticles:
          if(eachArticle.article_id == eachDoctorArticle.id):
            doctorArticleList.append(eachDoctorArticle)

    return render_template('doctorFeed.html', articles=doctorArticleList)    
    

@feed_views.route('/like/<int:article_id>')
@login_required
def like(article_id):
    doctorArticles = ArticleRate.query.all()
    curr_user_id = current_user.id
    create_reaction(curr_user_id, "Approve", article_id)
    return render_template('doctorFeed.html', articles=doctorArticles)

@feed_views.route('/dislike/<int:article_id>')
@login_required
def dislike(article_id):
    doctorArticles = ArticleRate.query.all()
    curr_user_id = current_user.id
    create_reaction(curr_user_id, "Disapprove", article_id)
    return render_template('doctorFeed.html', articles=doctorArticles)

@feed_views.route('/feed', methods=['POST'])
@login_required
def search_product():
  doctorArticles = ArticleRate.query.all()
  queryresults = str(request.form["keyword"]) #requests search term
  results = article_search(queryresults) #Searches for articles in database
  count=0
  #Checking the amount of items in results (Returns item not found if count = 0)
  for article in results:
    count+=1
  if queryresults is None or queryresults =="": 
    flash("Please enter an article keyword")
    return render_template('doctorFeed.html', articles=doctorArticles)
  if count == 0: 
    flash("Sorry No articles was found.")
    return render_template('doctorFeed.html', articles=doctorArticles)
  else:
    return render_template('doctorFeed.html', articles=results)