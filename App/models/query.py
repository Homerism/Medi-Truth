from App.database import db
from flask_login import UserMixin


class Query(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    query_text =  db.Column(db.String, nullable=False)
    verdict =  db.Column(db.String, nullable=False)

    def __init__(self, query_text, verdict):
      self.query_text = query_text
      self.verdict = verdict

    def toJSON(self):
        return{
            'id': self.id,
            'query': self.query_text,
            'verdict': self.verdict
        }  
