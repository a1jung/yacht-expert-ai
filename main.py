from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
from openai import OpenAI

# OpenAI 클라이언트
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 모델
class Message(BaseModel):
    user_input: str

# 요트 전문 지식 컨텍스트
YACHT_KNOWLEDGE = """
요트 조종, 항해 기술, 세일 세팅, 마스트 조정, 스프레더 사용,
풍향 분석, 레이스 전략, 안전 규칙 등 요트 관련 전반적인 전문 지식
"""

@app.post("/chat")
def chat(message: Message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"당신은 요트 전문가입니다. {YACHT_KNOWLEDGE}"},
                {"role": "user", "content": message.user_input}
            ],
            max_tokens=150
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Error: {str(e)}"
    return {"response": answer}

@app.get("/", response_class=HTMLResponse)
def home():
    # HTML은 들여쓰기 없이 맨 앞부터 시작
    return """<html>
<head>
<title>Yacht Expert AI</title>
<style>
body { font-family: 'Segoe UI', sans-serif; background-color: #f2f5f9; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
h1 { color: #0d47a1; }
#chatBox { width: 400px; height: 400px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px; }
.user, .bot { padding: 10px; border-radius: 10px; max-width: 80%; }
.user { background: #0d47a1; color: white; align-self: flex-end; }
.bot { background: #e3f2fd; color: #0d47a1; align-self: flex-start; }
#inputBox { margin-top: 10px; display: flex; gap: 10px; }
#userInput { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 14px; }
button { background-color: #0d47a1; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; transition: 0.3s; }
button:hover { background-color: #1565c0; }
</style>
</head>
<body>
<h1>Yacht Expert AI</h1>
<div id="chatBox"></div>
<div id="inputBox">
<input id="userInput" placeholder="메시지를 입력하세요" onkeypress="handleKey(event)">
<button onclick="sendMessage()">Send</button>
</div>
<script>
const chatBox = document.getElementById("chatBox");
function addMessage(content, sender) {
    const msg = document.createElement("div");
    msg.classList.add(sender);
    msg.innerText = content;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}
async function sendMessage() {
    const input = document.getElementById("userInput");
    const text = input.value.trim();
    if (!text) return;
    addMessage(text, "user");
    input.value = "";
    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: text })
    });
    const data = await res.json();
    addMessage(data.response, "bot");
}
function handleKey(e) { if (e.key === "Enter") sendMessage(); }
</script>
</body>
</html>"""
