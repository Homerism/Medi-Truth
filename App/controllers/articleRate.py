import math
from App.models import articleRate

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