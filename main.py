from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from knowledge import free_mode_answer

app = FastAPI()

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
    # 무료 모드 자체 지식 기반 답변
    response = free_mode_answer(message.user_input)
    return {"response": response}

@app.get("/", response_class=HTMLResponse)
def home():
    # UI: 버튼 + 입력창 + 결과 표시
    return """
    <h1>Yacht Expert AI (무료 모드)</h1>
    <p>버튼을 클릭하거나 직접 질문을 입력해보세요.</p>
    
    <!-- 카테고리 버튼 -->
    <button onclick="sendPreset('세일')">세일</button>
    <button onclick="sendPreset('튜닝')">튜닝</button>
    <button onclick="sendPreset('레이스')">레이스</button>
    <button onclick="sendPreset('해상훈련')">해상훈련</button>
    <button onclick="sendPreset('육상훈련')">육상훈련</button>
    <button onclick="sendPreset('안전')">안전</button>
    
    <br><br>
    <!-- 직접 질문 입력 -->
    <input id="userInput" placeholder="질문을 입력하세요" size="50"/>
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

    async function sendPreset(category) {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({user_input: category})
        });
        const data = await res.json();
        document.getElementById('response').innerText = data.response;
    }
    </script>
    """
