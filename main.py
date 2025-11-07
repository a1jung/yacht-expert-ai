from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sailing_knowledge import get_sailing_knowledge
from fitness_knowledge import get_fitness_routine

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Message(BaseModel):
    user_input: str
    age: int = None  # optional
    focus: str = None  # optional, ex: "전신", "상체"

@app.post("/chat")
def chat(message: Message):
    text = message.user_input.lower()
    
    # 요트 전문 지식
    if "470" in text or "레이저" in text:
        response_text = get_sailing_knowledge("470_마스트_튜닝" if "470" in text else "레이저_튜닝")
    
    # 체력 훈련
    elif "체력" in text or "운동" in text or "훈련" in text:
        if message.age and message.focus:
            routine = get_fitness_routine(message.age, message.focus)
            response_text = f"{message.focus} 운동 추천 (나이 {message.age} 기준): {routine}"
        else:
            response_text = "나이와 운동 부위를 입력해야 맞춤 운동 루틴을 추천할 수 있습니다. 예: {'age':16, 'focus':'전신'}"
    
    else:
        response_text = "죄송합니다. 해당 주제에 대한 정보가 없습니다. 요트 세일 트림, 바람 조건, 체력 훈련 키워드로 질문해주세요."
    
    return {"response": response_text}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Yacht Expert AI</h1>
    <p>체력 훈련은 {'age': 나이, 'focus': '전신/상체/하체/팔/다리/인터벌/코어'} 형태로 질문</p>
    <input id="userInput" placeholder="Type your message" onkeypress="if(event.keyCode==13) sendMessage()"/>
    <input id="ageInput" placeholder="나이 입력 (체력 훈련용)"/>
    <input id="focusInput" placeholder="운동 부위 입력"/>
    <button onclick="sendMessage()">Send</button>
    <p id="response"></p>
    <script>
    async function sendMessage() {
        const input = document.getElementById("userInput").value;
        const age = parseInt(document.getElementById("ageInput").value) || null;
        const focus = document.getElementById("focusInput").value || null;
        const res = await fetch('/chat', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({user_input: input, age: age, focus: focus})
        });
        const data = await res.json();
        document.getElementById('response').innerText = data.response;
    }
    </script>
    """

