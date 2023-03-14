from nltk.corpus import stopwords
from collections import Counter
from App.database import db
from App.models import Article
import requests
import string
import json
import nltk

# Set up News API credentials and base URL
newsapi_key = "3e40cfef90d74e95b4cdbcd55e912715"
base_url = "https://newsapi.org/v2/everything"

def most_frequent_words(paragraph):
    nltk.download('stopwords')
    paragraph = paragraph.lower() # Convert paragraph to lowercase
    words = paragraph.translate(str.maketrans('', '', string.punctuation)).split() # Remove punctuation and split paragraph into words
    stop_words = set(stopwords.words('english')) # Remove stopwords
    words = [word for word in words if word not in stop_words]
    word_counts = Counter(words) # Count word frequencies and return the top three most frequent words
    return [word for word, count in word_counts.most_common(3)]

def get_news_articles(user_input):
   words = most_frequent_words(user_input) #5 most frequent words from the 
   commonwords = '+'.join(words)
   credible_sources = ['medgadget.com','news-medical.net','medscape.com','medicalnewstoday.com',
                    'webmd.com','mayoclinic.org','medicalxpress.com','bmj.com','healio.com',
                    'mobihealthnews.com','khn.org','who.int','fda.gov','cdc.gov','theatlantic.com',
                    'bbc.com','cnn.com','discovermagazine.com','forbes.com','knowablemagazine.org',
                    'livescience.com','mdedge.com','medicaldaily.com','medpagetoday.com'
                    'newscientist.com','nytimes.com','npr.org','quantamagazine.org','reuters.com',
                    'scientificamerican.com','statnews.com','time.com','beckershospitalreview.com',
                    'fiercehealthcare.com','hcplive.com','healthaffairs.org','healthitoutcomes.com',
                    'healthcaredive.com','mmm-online.com','modernhealthcare.com','pharmacytimes.com',
                    'practiceupdate.com','the-hospitalist.org','pharmaceutical-journal.com','fiercebiotech.com',
                    'healthcareitnews.com','imedicalapps.com','technologyreview.com','mobihealthnews.com',
                    'health.com','ajog.org','youngwomenshealth.org','contemporaryobgyn.net','healthywomen.org',
                    'iwhc.org','menopause.org','ourbodiesourselves.org','rcog.org.uk','obgyn.onlinelibrary.wiley.com'
                    'womenshealthmag.com','womenshealth.gov'] #Top 50 credible news websites
   
   sources = ','.join(credible_sources)
   
   params = { # News API request URL with the most common word
       "apiKey": newsapi_key,
       "q": commonwords,
       "language": "en",
       "sortBy": "relevancy",
       "domains": sources
   }
   
   response = requests.get(base_url, params=params) #Json request
   data = json.loads(response.text)
   
   if not data:
        return []
   else:
       articles = data['articles']
       articles_to_append = []
    
       for article in articles:# Get the article content and check if it contains any of the words in the list
           content = article['content']
           title = article['title']
           description = article['description']
           if any(word in content for word in commonwords):
               if any(word in title for word in commonwords):
                   if any(word in description for word in commonwords):  # If the article contains one of the words, append it to the list to be saved
                       articles_to_append.append(article)
   return articles_to_append[:20]


def similar_claim(claim):
    url = 'https://factchecktools.googleapis.com/v1alpha1/claims:search'
    api_key = 'AIzaSyAs2Hwd06hW4Zj8dOym89-aZHv0dQ91SB4' # Set up the API key 
    params = { #Parameters for the API request
        'query': claim,
        'key': api_key,
        'pageSize': 20,
    }
    response = requests.get(url, params=params) #API request and get the response
    data = json.loads(response.text)  #JSON format
    
    if not data:
        return []
    else:
        similar_claims = data["claims"]
        return similar_claims[:20]
        

#function to add user articles to the database
def create_article(articles, query_id):
    for article in articles:
        userarticle = Article(title=article["title"],
                              author=article["author"],
                              url=article["url"],
                              content=article["content"],
                              publish=article["publishedAt"],
                              img=article["urlToImage"], 
                              query_id=query_id)
        db.session.add(userarticle)
        db.session.commit()
