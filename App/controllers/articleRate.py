import math
from App.database import db
from App.models import ArticleRate, DoctorReaction

def calculate_rating(article_id):
    countApprove = 0
    countDisapprove = 0
    articles = DoctorReaction.query.filter_by(article_id=article_id).all()
    for article in articles:
        if article.react == 'Approve':
            countApprove += 1
        elif article.react == 'Disapprove':
            countDisapprove += 1
    total = countApprove+countDisapprove
    if total == 0:
        return 0
    else:
        approve_percentage = (countApprove / total) * 100
        finalScore = math.ceil(approve_percentage)
    return finalScore

def get_article_id(title):
    articles = ArticleRate.query.all()
    article_id = None
    for article in articles:
        if article.title == title:
            article_id = article.id
            break
    return article_id

def create_reaction(user_id, react, article_id):
    allReactions = DoctorReaction.query.all()
    for eachReaction in allReactions:
        if ((eachReaction.user_id==user_id) and (eachReaction.article_id==article_id)):
            eachReaction.react = react
            db.session.commit()
            return

    newuser = DoctorReaction(user_id=user_id, react=react, article_id=article_id)
    db.session.add(newuser)
    db.session.commit()
    return newuser

#filters articles based on search term provided
def article_search(search):
  return ArticleRate.query.filter(
    ArticleRate.title.like( '%'+search+'%' )
    | ArticleRate.author.like( '%'+search+'%' )
    | ArticleRate.content.like( '%'+search+'%' )
    )