from App.database import db
import pickle

vector = pickle.load(open("App/controllers/dection-vector.pkl",'rb')) 
model = pickle.load(open("App/controllers/dection-model.pkl", 'rb')) 

def health_classification(news):
  input_data = [news]
  vector_data = vector.transform(input_data)
  prediction = model.predict(vector_data)
  return prediction


#print(prediction)
#if (prediction == '1'):
  #print("This is Real...")
#else:
  #print("False")


