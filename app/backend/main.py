from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
import os
import json
from dotenv import load_dotenv
from groq import Groq
import base64
import mysql.connector
from datetime import datetime
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

GROQ_CLOUD_API_KEY = os.getenv("GROQ_CLOUD_API_KEY")
GROQ_CLOUD_MODEL = os.getenv("GROQ_CLOUD_MODEL")

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PORT = os.getenv("MYSQL_PORT")

app = FastAPI()

client = Groq(api_key=GROQ_CLOUD_API_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FeedbackResponse(BaseModel):
    score: int
    comment: str

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        port=MYSQL_PORT
    )

@app.post("/analyze-thumbnail/", response_model=FeedbackResponse)
async def analyze_thumbnail(file: UploadFile = File(...)):
    image_content = await file.read()
    encoded_image = base64.b64encode(image_content).decode('utf-8')
    image_data_url = f"data:{file.content_type};base64,{encoded_image}"

    completion = client.chat.completions.create(
        model=GROQ_CLOUD_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "This image is Youtube thumbnail. Please provide a score(between 1 or 10) of feedback in json format, it only has the field of 'score' and 'feedback'"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data_url
                        }
                    }
                ]
            },
            {
            "role": "assistant",
            "content": ""
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    response_data = json.loads(completion.choices[0].message.content)
    score = response_data.get("score", 1)
    comment = response_data.get("feedback", "No feedback available.")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedback (image_url, score, comment, created_at) VALUES (%s, %s, %s, %s)",
        (image_data_url, score, comment, datetime.now())
    )
    conn.commit()
    cursor.close()
    conn.close()

    return FeedbackResponse(score=score, comment=comment)
