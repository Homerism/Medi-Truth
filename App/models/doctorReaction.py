from App.database import db

class DoctorReaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    react =  db.Column(db.String, nullable=True)
    article_id = db.Column(db.Integer, nullable=True)
    
    def __init__(self, user_id, react, article_id):
      self.user_id = user_id
      self.react = react
      self.article_id = article_id

    def toJSON(self):
        return{
           'user_id': self.user_id,
           'react': self.react,
           'article_id': self.article_id
        }