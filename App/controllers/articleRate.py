import math
from App.database import db
from App.models import ArticleRate, DoctorReaction

#def rateArticle(verdict, title):
#    article = ArticleRate.query.filter_by(title=title).first()
#    if(verdict=="approve"):
#        article.approveNum += 1
#    else:
#        article.disapproveNum += 1    
#    return    

#def approvalScore(title):
#     article = ArticleRate.query.filter_by(title=title).first()
#     approvals = article.approveNum
#     disapprovals = article.disapproveNum
#     score = (approvals / disapprovals) * 100
#     finalScore = math.ceil(score)
#     return finalScore

def calculate_rating(article_id):
    countApprove = 0
    countDisapprove = 0
    articles = DoctorReaction.query.all()
    for article in articles:
        if article.id == article_id:
            if article.react == "Approve":
                countApprove += 1
            if article.react == "Disapprove":
                countDisapprove+=1
    total = countApprove+countDisapprove
    #if total == 0:
    #    return 0
    #else:
        #approve_percentage = (countApprove / total) * 100
        #disapprove_percentage = (countDisapprove / total) * 100
        #finalScore = math.ceil(approve_percentage)
    return countApprove

def get_article_id(title):
    articles = ArticleRate.query.all()
    for article in articles:
        if article.title == title:
            article_id = article.id
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
