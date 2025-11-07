from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import random

# 무료 모드용 데이터베이스 import
from yacht_knowledge import yacht_data
from training_knowledge import training_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    user_input: str
    age: int = None
    height: float = None
    weight: float = None

# 무료 fallback 모드: 입력된 키워드로 지식베이스에서 답변
@app.post("/chat")
def chat(message: Message):
    user_text = message.user_input.lower()
    response = "죄송해요, 관련 정보가 없습니다."

    # 요트 지식 검색
    for keyword, info in yacht_data.items():
        if keyword in user_text:
            response = info
            break
    
    # 체력 훈련 요청 감지
    if "운동" in user_text or "루틴" in user_text:
        age_group = "teen" if message.age and message.age < 19 else "adult"
        response = training_data[age_group]
        if message.height and message.weight:
            bmi = message.weight / ((message.height / 100) ** 2)
            response += f"\n추가로 BMI: {bmi:.1f} 기준 맞춤 루틴 추천 가능"

    return {"response": response}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Yacht Expert AI - 무료 모드</h1>
    <input id="userInput" placeholder="질문을 입력하세요" style="width:300px"/>
    <button onclick="sendMessage()">Send</button>
    <p id="response"></p>
    <script>
    async function sendMessage() {
        const input = document.getElementById("userInput").value;
        const res = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({user_input: input})
        });
        const data = await res.json();
        document.getElementById('response').innerText = data.response;
    }
    </script>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        input, button { padding: 5px; margin: 5px 0; }
        p { font-weight: bold; }
    </style>
    """
