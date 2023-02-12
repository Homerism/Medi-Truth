from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)

    def __init__(self, text):
      self.text = text

    def __repr__(self):
        return f'user: {self.user.username} | String to query: {self.text}.'