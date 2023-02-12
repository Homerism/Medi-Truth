from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    articleName = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name):
        self.articleName = name


    def __repr__(self):
        return f'User: {self.user.username} | Rated Article: {self.articleName}.'