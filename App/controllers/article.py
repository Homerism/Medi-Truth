from App.database import db
import requests
import json


# function to get health news articles based on user input
def recommend_health_articles(user_input): # make a GET request to the news API
    url = "https://newsapi.org/v2/everything?q=" + user_input + "&sort_by=relevancy&domains=medicalnewstoday.com,webmd.com,mayoclinic.org&apiKey=dec26edbe90945e8a53cfb47014bcba6"
    response = requests.get(url)
    data = json.loads(response.text)
    credible_articles = [] # filter out articles from credible sources
    credible_articles = data["articles"]
    return credible_articles # return the credible articles


#function to add user articles to the database
#def create_article(user_input):
    #credible_articles = recommend_health_articles(user_input)
    #for article in credible_articles:
      #userarticle = Article(title=article["title"], author=article["author"], url=article["url"], content=article["content"], publish=article["publishedAt"], img=article["urlToImage"])
      #db.session.add(userarticle)
    #db.session.commit()
    #return userarticle



