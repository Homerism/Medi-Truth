from nltk.corpus import stopwords
from collections import Counter
from App.database import db
from App.models import Article, ArticleRate
import requests
import string
import json
import nltk

# Set up News API credentials and base URL

a1 = "3e40cfef90d74e9"
a2 = "5b4cdbcd55e912715"

newsapi_key = a1+a2
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
   commonwords = ' OR '.join(words)
   #'bbc.com','cnn.com','nytimes.com','theatlantic.com','npr.org','forbes.com','time.com',
   credible_sources = ['medgadget.com','news-medical.net','medscape.com','medicalnewstoday.com',
                    'webmd.com','mayoclinic.org','medicalxpress.com','bmj.com','healio.com',
                    'mobihealthnews.com','khn.org','who.int','fda.gov','cdc.gov',
                    'discovermagazine.com','knowablemagazine.org',
                    'livescience.com','mdedge.com','medicaldaily.com','medpagetoday.com'
                    'newscientist.com','quantamagazine.org','reuters.com',
                    'scientificamerican.com','statnews.com','beckershospitalreview.com',
                    'fiercehealthcare.com','hcplive.com','healthaffairs.org','healthitoutcomes.com',
                    'healthcaredive.com','mmm-online.com','modernhealthcare.com','pharmacytimes.com',
                    'practiceupdate.com','the-hospitalist.org','pharmaceutical-journal.com','fiercebiotech.com',
                    'healthcareitnews.com','imedicalapps.com','technologyreview.com','mobihealthnews.com',
                    'health.com','ajog.org','youngwomenshealth.org','contemporaryobgyn.net','healthywomen.org',
                    'iwhc.org','menopause.org','ourbodiesourselves.org','rcog.org.uk','obgyn.onlinelibrary.wiley.com'
                    'womenshealthmag.com','womenshealth.gov','theferret.scot','factcheck.org','fullfact.org',
                    'healthfeedback.org','health.harvard.edu','my.clevelandclinic.org','hopkinsmedicine.org',
                    'healthline.com', 'nih.gov', 'thelancet.com','sciencedaily.com','nejm.org','medpagetoday.com',
                    'ama-assn.org','jamanetwork.com','healthaffairs.org','medlineplus.gov','healthday.com',
                    'statnews.com','bmj.com','cancer.org','heart.org','diabetes.org','alz.org','arthritis.org',
                    'parkinson.org','politifact.com','washingtonpost.com','snopes.com','washingtonpost.com',
                    'mediabiasfactcheck.com'] #Top 50 credible news websites
   
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
   return articles_to_append

def similar_claim(claim):
    url = 'https://factchecktools.googleapis.com/v1alpha1/claims:search'

    a1 ='AIzaSyAs2Hwd06'
    a2 = 'hW4Zj8dOym89'
    a3 = '-aZHv0dQ91SB4'
    api_key = a1+a2+a3

    params = { #Parameters for the API request
        'query': claim,
        'key': api_key,
    }
    response = requests.get(url, params=params) #API request and get the response
    data = json.loads(response.text)
    
    if not data:
        return []
    else:
        similar_claims = data["claims"]
        return similar_claims
        
def create_article(articles, query_id): #function to add user articles to the database
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

def create_article_for_doctors(articles, stored_articles): #adding articles(no repeats) for the doctor feed
    check = False
    
    for article in articles:
        for each in stored_articles:
            if each.title == article["title"]:
                check = True
                break
        
        if(not check):    
            userarticle = ArticleRate(title=article["title"],
                                author=article["author"],
                                url=article["url"],
                                content=article["content"],
                                publish=article["publishedAt"],
                                img=article["urlToImage"])
            db.session.add(userarticle)
            db.session.commit() 
        else:
            check = False           

