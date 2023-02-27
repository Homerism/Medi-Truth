from App.database import db
import pickle

vector = pickle.load(open("App/controllers/dection-vector.pkl",'rb')) 
model = pickle.load(open("App/controllers/dection-model.pkl", 'rb')) 

def health_classification(news):
  input_data = [news]
  vector_data = vector.transform(input_data)
  prediction = model.predict(vector_data)
  return prediction

def add_query(user):
  db.session.add(user)
  db.session.commit()

