import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from newspaper import Article
from newspaper.article import ArticleException
from openai import OpenAI
from pymongo import MongoClient
from pathlib import Path
import json
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from helper import create_html_body, clean, create_html_message


# get links
utc_datetime = datetime.now(timezone.utc)
utc_date = utc_datetime.date()
utc_yesterday = str(utc_date - timedelta(days=1))
url = "https://api.thenewsapi.com/v1/news/top"
root_dir = Path(__file__).resolve().parents[1]
load_dotenv(root_dir / ".env")
"""
params = {
    "api_token": os.getenv("THENEWSAPI_TOKEN"),
    "locale": "us,ca",
    "categories": "business",
    "language": "en",
    "published_on": utc_yesterday,
}
response = requests.get(url, params=params)
articles = response.json()["data"]  # list of articles
links = {"Business": [], "World Events": [], "Politics": []}
for article in articles:
    links["Business"].append(article["url"])

params = {
    "api_token": os.getenv("THENEWSAPI_TOKEN"),
    "categories": "general",
    "exclude_categories": "entertainment,food",
    "language": "en",
    "published_on": utc_yesterday,
}
response = requests.get(url, params=params)
articles = response.json()["data"]
for article in articles:
    links["World Events"].append(article["url"])

params = {
    "api_token": os.getenv("THENEWSAPI_TOKEN"),
    "locale": "us",
    "categories": "politics",
    "language": "en",
    "published_on": utc_yesterday,
}
response = requests.get(url, params=params)
articles = response.json()["data"]
for article in articles:
    links["Politics"].append(article["url"])


#scrape website and send to openai and store data in MongoDB
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client.newslydb
collection = db.summaries
for category in links:
    for link in links[category]:
        article = Article(link)
        try:
            article.download()
            article.parse()
        except ArticleException:
            continue
        text = article.text
        text = clean(text)
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a summarizer for a 5 year old.  Only respond in strict JSON with the fields: Title, Short Summary, What, When, Where, Who, How. Do not add any extra text, explanation, or markdown like ```json."},
                {"role": "user", "content": text}
            ]
        )
        reply = json.loads(response.choices[0].message.content)
        reply["date"] = utc_yesterday
        reply["url"] = link
        reply["categories"] = category
        collection.insert_one(reply)

""" #
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client.newslydb
collection = db.summaries
# construct bodies for html_email
html_bodies_data = {"Business": [], "World Events": [], "Politics": []}
for summary in collection.find({"date": utc_yesterday}):
    body = create_html_body(summary)
    html_bodies_data[summary["categories"]].append(body)

# get users data from postgresDB
engine = create_engine(os.getenv("POSTGRESDB_URI"))
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    categories = Column(JSON, nullable=False)

user_objects = session.query(User).all()
users = []
for user in user_objects:
    users.append({"email": user.email, "categories": user.categories})

# send emails to every user
url = "https://bulk.api.mailtrap.io/api/send"
for user in users:
    html_body = ""
    for category in user["categories"]:
        for bodies_category in html_bodies_data:
            if category == bodies_category:
                for body in html_bodies_data[category]:
                    html_body = html_body + body
    html_message = create_html_message(html_body, user["categories"], utc_yesterday)
    payload = {
        "from": {
            "email": "noreply@new-sly.com",
            "name": "Newsly Summarizer AI",
        },
        "to": [
            {
                "email": user["email"],
            }
        ],
        "subject": f"Your Newsly for {utc_yesterday}",
        "html": html_message,
        "category": "Summaries",
    }
    headers = {
        "Authorization": os.getenv("MAILTRAP_TOKEN"),
        "Content-Type": "application/json"
    }
    requests.request("POST", url, headers=headers, json=payload)

