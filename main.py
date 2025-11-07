from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai

# OpenAI API 키 설정 (환경 변수로 관리하는 것이 안전)
openai.api_key = "YOUR_OPENAI_API_KEY"

app = FastAPI()

# CORS 설정 (웹 브라우저에서 호출 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    user_input: str

@app.post("/chat")
def chat(message: Message):
    user_input = message.user_input
    # OpenAI GPT 모델 호출
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    answer = response.choices[0].message.content
    return {"response": answer}

@app.get("/")
def read_root():
    return {"message": "Hello Yacht Expert AI"}
