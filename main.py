from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai

from yacht_knowledge import yacht_data
from fitness_knowledge import fitness_data

openai.api_key = os.getenv("OPENAI_API_KEY")

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
    focus: str = None

def get_response(message: Message):
    # 체력 루틴 관련 질문이면 fitness_data 사용
    if "운동" in message.user_input or "체력" in message.user_input:
        age_group = "teen" if message.age and message.age < 20 else "adult"
        focus = message.focus if message.focus in fitness_data[age_group] else "전신"
        routine = fitness_data[age_group][focus]
        return f"{age_group} {focus} 운동 루틴 추천: {routine}"
    
    # 요트 질문이면 yacht_data 사용
    for key, content in yacht_data.items():
        if key in message.user_input:
            return content
    
    # OpenAI 무료 fallback
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.user_input}]
        )
        return response.choices[0].message.content
    except:
        return "죄송합니다, 현재 요트 전문 지식 또는 무료 AI 모드에서 답변할 수 없습니다."

@app.post("/chat")
async def chat(message: Message):
    reply = get_response(message)
    return {"response": reply}

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Yacht Expert AI</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background: #f0f8ff; }
        #chatBox { width: 500px; max-height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; background: #fff; }
        #userInput { width: 400px; padding: 5px; }
        button { padding: 5px 10px; }
        .msg { margin: 5px 0; }
        .user { color: blue; }
        .ai { color: green; }
    </style>
    </head>
    <body>
        <h1>Yacht Expert AI</h1>
        <div id="chatBox"></div>
        <input id="userInput" placeholder="질문을 입력하세요"/>
        <button onclick="sendMessage()">Send</button>

        <script>
        const chatBox = document.getElementById("chatBox");
        document.getElementById("userInput").addEventListener("keydown", function(e){
            if(e.key === "Enter") sendMessage();
        });

        async function sendMessage(){
            const input = document.getElementById("userInput").value;
            if(!input) return;
            chatBox.innerHTML += `<div class="msg user">You: ${input}</div>`;
            document.getElementById("userInput").value = "";
            const res = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({user_input: input})
            });
            const data = await res.json();
            chatBox.innerHTML += `<div class="msg ai">AI: ${data.response}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        </script>
    </body>
    </html>
    """
