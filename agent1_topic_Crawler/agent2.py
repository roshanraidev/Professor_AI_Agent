import openai
from openai import OpenAI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BlogInput(BaseModel):
    title: str
    summary: str
    reason_trending: str
    source_link: str

@app.post("/generate-blog")
def generate_blog(data: BlogInput):
    prompt = f"""
Write a blog post on the topic below:

Title: {data.title}
Summary: {data.summary}
Trending because: {data.reason_trending}
Source: {data.source_link}

Structure it with:
- Engaging introduction
- 2–3 subheadings
- Clear conclusion
Tone: professional but human
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        blog = response.choices[0].message.content
        return {"blog": blog}
    except Exception as e:
        return {"error": str(e)}
