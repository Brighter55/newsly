import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from newspaper import Article
from openai import OpenAI
from pymongo import MongoClient
from pathlib import Path
import json

def clean(text):
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    return "\n".join(lines)

# get links
utc_datetime = datetime.now(timezone.utc)
utc_date = utc_datetime.date()
utc_yesterday = str(utc_date - timedelta(days=1))
url = "https://api.thenewsapi.com/v1/news/top"
root_dir = Path(__file__).resolve().parents[1]
load_dotenv(root_dir / ".env")

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
mongo_client = MongoClient("localhost", 27017)
for category in links:
    for link in links[category]:
        article = Article(link)
        article.download()
        article.parse()
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
        db = mongo_client.testdb
        collection = db.summaries
        collection.insert_one(reply)
