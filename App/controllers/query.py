from App.models import Query
from App.database import db
from openai import error
import joblib
import openai
import nltk

from App.controllers.algorithm import (
   clean_text, 
   stem
)

nltk.download('stopwords')
# Import the vectorizer
vector = joblib.load('App/controllers/vector.joblib')
# Import the model
model = joblib.load('App/controllers/model.joblib')

def health_classification(claim):
  claim = clean_text(claim)
  claim = stem(claim)
  input_data = [claim]
  vector_data = vector.transform(input_data)
  prediction = model.predict(vector_data)
  return prediction

def add_query(user):
  db.session.add(user)
  db.session.commit()

a = "sk-oWkyQ3ANmuoa5gJTJ"
b = "FoZT3BlbkFJDVww"
c = "4CwsV9llX8q61MCm"

openai.api_key = a+b+c
def generate_response(health_claim):
    if not health_claim:
       return None
    try:
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
    except error.APIConnectionError as e:
        # Handle the APIConnectionError exception here
        print("Error communicating with OpenAI:", e)
        return None

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

def query_check(user_query, input):
    return any(query.query_text == input for query in user_query)