from App.database import db
from flask_login import UserMixin


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String, nullable=True)
    author =  db.Column(db.String, nullable=True)
    url =  db.Column(db.String, nullable=True)
    content =  db.Column(db.String, nullable=True)
    publish =  db.Column(db.String, nullable=True)
    img =  db.Column(db.String, nullable=True)
    query_id = db.Column(db.Integer, db.ForeignKey('query.id'), nullable=False)
    

    def __init__(self, title, author, url, content, publish, img, query_id):
      self.title = title
      self.author = author
      self.url = url
      self.content = content
      self.publish = publish
      self.img = img
      self.query_id = query_id

    def toJSON(self):
        return{
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'url': self.url,
            'content': self.content,
            'publish': self.publish,
            'img': self.img,
            'query_id': self.query_id
        } 
     
