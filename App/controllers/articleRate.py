import math
from App.database import db
from App.models import articleRate, DoctorReaction

def rateArticle(verdict, title):
    article = articleRate.query.filter_by(title=title).first()
    if(verdict=="approve"):
        article.approveNum += 1
    else:
        article.disapproveNum += 1    
    return    

def approvalScore(title):
     article = articleRate.query.filter_by(title=title).first()
     approvals = article.approveNum
     disapprovals = article.disapproveNum
     score = (approvals / disapprovals) * 100
     finalScore = math.ceil(score)
     return finalScore

def create_reaction(user_id, react, article_id):
    newuser = DoctorReaction(user_id=user_id, react=react, article_id=article_id)
    db.session.add(newuser)
    db.session.commit()
    return newuser