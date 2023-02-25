from App.database import db
import pickle
import collections
import nltk

nltk.download('punkt')
nltk.download('stopwords')

vector = pickle.load(open("App/controllers/dection-vector.pkl",'rb')) 
model = pickle.load(open("App/controllers/dection-model.pkl", 'rb')) 

def health_classification(news):
  input_data = [news]
  vector_data = vector.transform(input_data)
  prediction = model.predict(vector_data)
  return prediction

#function for the most frequent word in a paragraph
def most_frequent_word(paragraph):
    words = nltk.word_tokenize(paragraph.lower())
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    word_counts = collections.Counter(words)
    most_common_word = word_counts.most_common(1)[0][0]
    most_common_word = [word for word in most_common_word.split() if word not in stop_words]
    return most_common_word[0]
