from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # relationship for all user's queries
    queries = db.relationship('Query', backref='user', lazy=True, cascade="all, delete-orphan")

    def __init__(self, username, type, password):
        self.username = username
        self.type = type
        self.set_password(password)

    def toJSON(self):
        return{
            'id': self.id,
            'type': self.type,
            'username': self.username,
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)