from App.database import db
from flask_login import UserMixin


class Article(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String, nullable=False)
    author =  db.Column(db.String, nullable=False)
    url =  db.Column(db.String, nullable=False)
    content =  db.Column(db.String, nullable=False)
    publish =  db.Column(db.String, nullable=False)
    img =  db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __init__(self, title, author, url, content, publish, img):
      self.title = title
      self.author = author
      self.url = url
      self.content = content
      self.publish = publish
      self.img = img

    def toJSON(self):
        return{
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'url': self.url,
            'content': self.content,
            'publish': self.publish,
            'img': self.img
        }  
