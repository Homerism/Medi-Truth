from App.models import User
from App.database import db
import requests
import json

def create_user(username, type, password):
    newuser = User(username=username, type=type, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.toJSON() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None

def get_npi_number(user_input):
       # make a GET request to the NPI API
    url = "https://npiregistry.cms.hhs.gov/api/?number="+ user_input + "&version=2.1"
    response = requests.get(url)
    data = json.loads(response.text)

    if(data['result_count'] == 1):
        return True
    else:
        return False

def check_npi (num_string):
    result=False
    npi_length=len(num_string)

    if npi_length<10 or npi_length>10:
        result = True
    else:    
        for each in num_string:
            try:
                int(each)
            except:
                result=True
                break

    if result:
        return False
    else:
        return True