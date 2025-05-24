from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
# 👇 TEMPORARY: replace with your real OpenAI key directly
client = OpenAI(api_key="da104e4458ae76858573c0c7fe")

app = FastAPI()

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
    prompt = f"""Write a blog post:

Title: {data.title}
Summary: {data.summary}
Trending Because: {data.reason_trending}
Source: {data.source_link}

Structure:
- Catchy introduction
- 2–3 detailed subheadings
- Strong conclusion
Tone: Professional and engaging.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return {"blog": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
