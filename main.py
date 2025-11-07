from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    user_input: str

# 간단 로컬 지식베이스
YACHT_KNOWLEDGE_PARAS = {
    "세일": "세일 트리밍은 풍향과 풍속에 따라 깊이와 각도를 조정합니다.",
    "레이스": "레이스 전략: 스타트 타이밍, 코스 파악, 상대 위치선점 중요.",
    "안전": "안전수칙: 구명조끼, VHF 점검, 비상 절차 숙지.",
    "마스트": "마스트와 밴드: 팽팽하면 세일 평평, 느슨하면 세일 깊음."
}

def local_answer(user_text: str) -> str:
    txt = user_text.lower()
    for kw, para in YACHT_KNOWLEDGE_PARAS.items():
        if re.search(r"\b" + re.escape(kw.lower()) + r"\b", txt):
            return para
    if "안녕" in txt or "hello" in txt:
        return "안녕하세요! 요트 전문가 AI 테스트 모드입니다."
    return "무료 모드: 요트 관련 키워드(세일, 레이스, 안전, 마스트)로 질문해보세요."

@app.post("/chat")
def chat(message: Message):
    return {"response": local_answer(message.user_input)}

@app.get("/", response_class=HTMLResponse)
def home():
    return """<html>
<head>
<title>Yacht Expert AI (Free Mode)</title>
<meta charset="utf-8">
</head>
<body>
<h1>Yacht Expert AI</h1>
<input id="userInput" placeholder="메시지를 입력하세요"/>
<button onclick="sendMessage()">Send</button>
<p id="response"></p>
<script>
async function sendMessage() {
    const input = document.getElementById("userInput").value;
    if(!input) return;
    const res = await fetch('/chat', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({user_input:input})
    });
    const data = await res.json();
    document.getElementById('response').innerText = data.response;
}
</script>
</body>
</html>"""
