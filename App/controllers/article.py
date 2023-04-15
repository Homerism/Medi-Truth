from nltk.corpus import stopwords
from collections import Counter
from App.database import db
from App.models import Article, ArticleRate
import requests
import json
import nltk
import re

# News API credentials and base URL
a1 = "3e40cfef90d74e9"
a2 = "5b4cdbcd55e912715"

newsapi_key = a1+a2
base_url = "https://newsapi.org/v2/everything"

def most_common_words(paragraph):
  stop_words = set(stopwords.words('english'))
  paragraph = re.sub(r'\W+', ' ', paragraph)
  modal_verbs = ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would',
                'ought to', 'had better', 'need to', 'have to', 'has to', 'be able to', 
                'be allowed to', 'may as well', 'might as well', 'will have to', 'would have to',
                'should have to', 'could have to', 'must have to', 'might have to', 'will be able to',
                'would be able to', 'should be able to', 'could be able to', 'must be able to', 
                'might be able to', 'may have to', 'might have to', 'will need to', 'would need to',
                'should need to', 'could need to', 'must need to', 'might need to', 'may be able to',
                'might be able to', 'shall be able to', 'should be able to', 'could be able to',
                'must be able to', 'might have been able to', 'may have been able to', 'should have been able to',
                'could have been able to', 'must have been able to', 'would have been able to', 'can do',
                'could do', 'may do', 'might do', 'must do', 'shall do', 'should do', 'will do', 
                'would do', 'ought to do', 'had better do', 'need to do', 'have to do', 'has to do', 
                'be able to do', 'be allowed to do', 'may as well do', 'might as well do', 'will have to do',
                'would have to do', 'should have to do', 'could have to do', 'must have to do', 'might have to do', 
                'may be able to do', 'might be able to do', 'shall be able to do', 'should be able to do',
                'could be able to do', 'must be able to do', 'might have been able to do', 'may have been able to do',
                'should have been able to do', 'could have been able to do', 'must have been able to do', 'be supposed to',
                'be expected to', 'be obliged to', 'be required to', 'be allowed to', 'be permitted to',
                'be compelled to', 'be forbidden to', 'be entitled to', 'be empowered to', 'be authorised to',
                'be mandated to', 'be ordered to', 'be directed to', 'be requested to', 'be advised to']

  conjunctions = ['although', 'and', 'as', 'because', 'before', 'but', 'even if', 'even though', 
                  'if', 'in order that', 'once', 'provided that', 'since', 'so', 'that', 'though',
                  'unless', 'until', 'when', 'whenever', 'where', 'whereas', 'wherever', 'whether',
                  'while', 'yet']

  nltk.download('punkt', quiet=True)
  tokens = nltk.word_tokenize(paragraph)
  tokens = [token.lower() for token in tokens if token.lower() not in stop_words and not token.isnumeric() and token.lower() not in modal_verbs and token.lower() not in conjunctions]
  freq_dist = nltk.FreqDist(tokens)
  most_frequent = freq_dist.most_common(50)
  words=[]
  for word, freq in most_frequent:
      words.append(word)
  return words

def get_news_articles(user_input):
   words = most_common_words(user_input) #5 most frequent words from the 
   commonwords = ' OR '.join(words)
   credible_sources = ['medgadget.com','news-medical.net','medscape.com','medicalnewstoday.com',
                    'webmd.com','mayoclinic.org','medicalxpress.com','bmj.com','healio.com',
                    'mobihealthnews.com','khn.org','who.int','fda.gov','cdc.gov',
                    'discovermagazine.com','knowablemagazine.org',
                    'livescience.com','mdedge.com','medicaldaily.com','medpagetoday.com'
                    'newscientist.com','quantamagazine.org',
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
   return articles_to_append[:20]

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
    
    if "claims" in data:
        similar_claims = data["claims"]
        return similar_claims
    else:
        return []
        
def create_article(articles, query_id):
    articles_data = []
    for article in articles:
        articles_data.append({
            'title': article["title"],
            'author': article["author"],
            'url': article["url"],
            'content': article["content"],
            'publish': article["publishedAt"],
            'img': article["urlToImage"],
            'query_id': query_id
        })
    db.session.bulk_insert_mappings(Article, articles_data)
    db.session.commit()

def create_article_for_doctors(articles, stored_titles):
    for article in articles:
        if article["title"] not in stored_titles:
            userarticle = ArticleRate(title=article["title"],
                                      author=article["author"],
                                      url=article["url"],
                                      content=article["content"],
                                      publish=article["publishedAt"],
                                      img=article["urlToImage"])
            db.session.add(userarticle)
            db.session.commit()       

