from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests
import os

# Load API key from .env
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Define response model
class Topic(BaseModel):
    title: str
    summary: str
    reason_trending: str
    source_link: str

@app.get("/get-topics", response_model=List[Topic])
def get_trending_topics(niche: str = Query(..., description="Blog topic niche")):
    # Date range: past 7 days
    from_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    to_date = datetime.today().strftime('%Y-%m-%d')

    # Construct NewsAPI request
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={niche}&from={from_date}&to={to_date}&sortBy=popularity&pageSize=10&apiKey={NEWS_API_KEY}"
    )

    # Fetch data from NewsAPI
    response = requests.get(url)
    data = response.json()

    print("API Key:", NEWS_API_KEY)         # Debug: check API key
    print("API Response:", data)            # Debug: check full response

    # Error handling
    if data.get("status") != "ok":
        return {"error": data.get("message", "Failed to fetch data")}

    # Parse articles into Topic model
    topics = []
    for article in data.get("articles", []):
        topics.append(Topic(
            title=article["title"],
            summary=article["description"] or "No summary available.",
            reason_trending=f"Published by {article['source']['name']} on {article['publishedAt'][:10]}",
            source_link=article["url"]
        ))

    return topics
