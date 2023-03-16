from App.database import db
from flask_login import UserMixin


class ArticleRate(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String, nullable=False)
    approveNum = db.Column(db.Integer, nullable=False)
    disapproveNum = db.Column(db.Integer, nullable=False)
    
    

    def __init__(self, title):
        self.title = title
        self.approveNum = 0
        self.disapproveNum = 0

    def toJSON(self):
        return{
            'id': self.id,
            'title': self.title
        }    
        