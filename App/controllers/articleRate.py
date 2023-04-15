import math
from App.database import db
from App.models import ArticleRate, DoctorReaction

def calculate_rating(article_id):
    approve_count = DoctorReaction.query.filter_by(article_id=article_id, react='Approve').count()
    disapprove_count = DoctorReaction.query.filter_by(article_id=article_id, react='Disapprove').count()
    total = approve_count + disapprove_count
    if total == 0:
        return 0
    approve_percentage = (approve_count / total) * 100
    final_score = math.ceil(approve_percentage)
    return final_score

def get_article_id(title):
    article = ArticleRate.query.filter_by(title=title).first()
    if article:
        return article.id
    return None

def create_reaction(user_id, react, article_id):
    reaction = DoctorReaction.query.filter_by(user_id=user_id, article_id=article_id).first()
    if reaction:
        reaction.react = react
        db.session.commit()
        return
    new_reaction = DoctorReaction(user_id=user_id, react=react, article_id=article_id)
    db.session.add(new_reaction)
    db.session.commit()
    return new_reaction

#filters articles based on search term provided
def article_search(search):
  return ArticleRate.query.filter(
    ArticleRate.title.like( '%'+search+'%' )
    | ArticleRate.author.like( '%'+search+'%' )
    | ArticleRate.content.like( '%'+search+'%' )
    )