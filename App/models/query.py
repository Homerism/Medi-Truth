from App.database import db
from flask_login import UserMixin


class Query(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    query_text = db.Column(db.String, nullable=False)
    verdict = db.Column(db.String, nullable=False)
    response = db.Column(db.String, nullable=True)
    articles = db.relationship('Article', backref='query', lazy=True, cascade="all, delete-orphan")

    def __init__(self, query_text, verdict, response):
      self.query_text = query_text
      self.verdict = verdict
      self.response = response

    def toJSON(self):
        return{
            'id': self.id,
            'query': self.query_text,
            'verdict': self.verdict,
            'response': self.response
        }  