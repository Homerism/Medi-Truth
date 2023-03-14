from App.database import db
from App.models import Query
import pickle
import openai
import os

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

a1 = "sk-DE438X2CUbLc8"
a2 = "z9wUMQ2T3BlbkFJfo"
a3 = "pbtAsSDH9f02awv8ib"
openai.api_key = a1+a2+a3

def generate_response(health_claim):
    
    model_engine = "text-davinci-002"
    prompt = f"Health claim: {health_claim}\nResponse:"
    temperature = 0.7
    max_tokens = 100
    stop = "\n"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=stop
    )
    generated_text = response.choices[0].text.strip()
    return generated_text

def call_until_return(func,text):
    result = func(text)
    while not result:
        result = func(text)
    return result

def remove_query(id):
  obj = Query.query.filter_by(id=id).one()
  db.session.delete(obj)
  db.session.commit()

def create_query(text, response, verdict):
    newquery = Query(query_text=text, response=response, verdict=verdict)
    return newquery

def get_query(id):
    return Query.query.get(id)