from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
import random

# 내부 지식 데이터 불러오기
from sailing_knowledge import get_yacht_answer
from fitness_knowledge import get_fitness_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- 데이터 모델 ----------
class Message(BaseModel):
    user_input: str
    user_profile: dict | None = None  # 운동 루틴 생성용 신체정보


# --------- 챗봇 엔진 ----------
@app.post("/chat")
async def chat(message: Message):
    user_input = message.user_input.strip()
    profile = message.user_profile

    # 운동 루틴 요청일 경우
    if any(word in user_input for word in ["운동", "훈련", "루틴", "체력"]):
        response = get_training_answer(user_input, profile)
    else:
        response = get_yacht_answer(user_input)

    if not response:
        response = (
            "🤖 현재 지식 범위를 벗어난 질문이에요. "
            "요트(세일, 레이스, 마스트, 트림) 또는 훈련 관련 질문을 해주세요!"
        )

    return JSONResponse({"response": response})


# --------- UI 화면 ----------
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>Yacht Expert AI</title>
        <style>
            body { font-family: Pretendard, sans-serif; background: #f4f6fa; margin:0; display:flex; flex-direction:column; align-items:center; height:100vh;}
            h1 { margin-top:40px; color:#004aad; font-size:2rem;}
            #chat-box { background:white; width:90%; max-width:600px; height:65vh; overflow-y:auto; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); padding:20px; margin-top:20px;}
            .msg { margin:8px 0; }
            .user { text-align:right; color:#004aad; }
            .bot { text-align:left; color:#333; background:#eef3ff; display:inline-block; padding:8px 12px; border-radius:8px;}
            #input-area { display:flex; justify-content:center; margin-top:15px; width:90%; max-width:600px;}
            input { flex:1; padding:10px; border:1px solid #ccc; border-radius:8px; font-size:1rem;}
            button { margin-left:10px; background:#004aad; color:white; border:none; border-radius:8px; padding:10px 16px; cursor:pointer; font-weight:bold;}
            button:hover { background:#003380; }
        </style>
    </head>
    <body>
        <h1>⛵ Yacht Expert AI</h1>
        <div id="chat-box"><div class="bot msg">안녕하세요! 요트 세일 트림, 마스트 튜닝, 훈련 루틴에 대해 물어보세요 ⚓</div></div>
        <div id="input-area">
            <input id="userInput" placeholder="메시지를 입력하세요..." onkeypress="if(event.key==='Enter'){sendMessage()}">
            <button onclick="sendMessage()">Send</button>
        </div>
        <script>
        async function sendMessage() {
            const input = document.getElementById("userInput");
            const chatBox = document.getElementById("chat-box");
            const text = input.value.trim();
            if (!text) return;
            chatBox.innerHTML += `<div class='user msg'>${text}</div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            const res = await fetch("/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({user_input: text})
            });
            const data = await res.json();
            chatBox.innerHTML += `<div class='bot msg'>${data.response}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
