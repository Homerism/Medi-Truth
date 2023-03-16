from App.database import db
from flask_login import UserMixin

        
class ArticleRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String, nullable=True)
    author =  db.Column(db.String, nullable=True)
    url =  db.Column(db.String, nullable=True)
    content =  db.Column(db.String, nullable=True)
    publish =  db.Column(db.String, nullable=True)
    img =  db.Column(db.String, nullable=True)
    # approveNum = db.Column(db.Integer, nullable=False)
    # disapproveNum = db.Column(db.Integer, nullable=False)
    

    def __init__(self, title, author, url, content, publish, img):
      self.title = title
      self.author = author
      self.url = url
      self.content = content
      self.publish = publish
      self.img = img
    #   self.approveNum = 0
    #   self.disapproveNum = 0

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


# class ArticleRate(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     title =  db.Column(db.String, nullable=False)
#     approveNum = db.Column(db.Integer, nullable=False)
#     disapproveNum = db.Column(db.Integer, nullable=False)
    
    

#     def __init__(self, title):
#         self.title = title
#         self.approveNum = 0
#         self.disapproveNum = 0

#     def toJSON(self):
#         return{
#             'id': self.id,
#             'title': self.title
#         }           