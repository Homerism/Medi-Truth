# -*- coding: utf-8 -*-
"""Algorithm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AMuF8WRRu_fqC2GgWQq1oQV-WKDVm2JG
"""
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords
import pandas as pd
import string
import nltk
import csv
import re

nltk.download('stopwords')

# Define word optimization function to clean text data
def clean_text(text):
    claim = text.lower()
    claim = re.sub('\[.*?\]', '', text)
    claim = re.sub("\\W"," ",text) 
    claim = re.sub('https?://\S+|www\.\S+', '', text)
    claim = re.sub('<.*?>+', '', text)
    claim = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    claim = re.sub('\n', '', text)
    claim = re.sub('\w*\d\w*', '', text)    
    return claim

stemmer = PorterStemmer()
def stem(text):
    claim = re.sub('[^a-zA-Z]',' ',text)
    claim = claim.lower()
    claim = claim.split()
    claim = [stemmer.stem(word) for word in claim if not word in stopwords.words('english')]
    claim = ' '.join(claim)
    return claim

def algorithm():
    nltk.download('stopwords')
    health_claims = pd.read_csv('App/controllers/claims.csv')
    health_claims.shape 
    health_claims = health_claims.fillna('')
    health_claims = health_claims.drop_duplicates()
    health_claims['contents'] = health_claims['statement']
    health_claims['contents'] = health_claims['contents'].apply(stem)
    health_claims['contents'] = health_claims['contents'].apply(clean_text)
    X = health_claims.drop(columns='rating', axis=1)
    Y = health_claims['rating']
    X = health_claims['contents'].values
    Y = health_claims['rating'].values
    vector = TfidfVectorizer(stop_words='english', max_df=0.7)
    vector.fit(X)
    X = vector.transform(X)
    x_train, x_test, y_train, y_test = train_test_split(X, Y, stratify=Y, test_size=0.2, random_state=2)
    model = PassiveAggressiveClassifier(max_iter=100)
    model.fit(x_train,y_train)
    return model, vector

def data_in_csv_check(statement):
    with open('App/controllers/claims.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[2].strip() == statement:
                return True
        return False