import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

# get links
utc_datetime = datetime.now(timezone.utc)
utc_date = utc_datetime.date()
utc_yesterday = utc_date - timedelta(days=1)
url = "https://api.thenewsapi.com/v1/news/top"
load_dotenv()

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




