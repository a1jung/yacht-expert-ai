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
    response = free_mode_answer(message.user_input)
    return {"response": response}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Yacht Expert AI (무료 모드)</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(to bottom, #e0f7fa, #80deea);
                color: #004d40;
                text-align: center;
                padding: 30px;
            }
            h1 { 
                font-size: 2.5em; 
                margin-bottom: 10px;
            }
            p { font-size: 1.2em; }
            button {
                background-color: #00796b;
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 5px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1em;
            }
            button:hover { background-color: #004d40; }
            input {
                padding: 10px;
                width: 300px;
                border-radius: 5px;
                border: 1px solid #004d40;
                font-size: 1em;
            }
            #response {
                margin-top: 20px;
                font-size: 1.2em;
                background-color: #b2dfdb;
                padding: 15px;
                border-radius: 8px;
                display: inline-block;
                max-width: 80%;
                word-wrap: break-word;
            }
        </style>
    </head>
    <body>
        <h1>Yacht Expert AI</h1>
        <p>버튼을 클릭하거나 직접 질문을 입력해보세요.</p>

        <!-- 카테고리 버튼 -->
        <button onclick="sendPreset('세일')">세일</button>
        <button onclick="sendPreset('튜닝')">튜닝</button>
        <button onclick="sendPreset('레이스')">레이스</button>
        <button onclick="sendPreset('해상훈련')">해상훈련</button>
        <button onclick="sendPreset('육상훈련')">육상훈련</button>
        <button onclick="sendPreset('안전')">안전</button>

        <br><br>
        <input id="userInput" placeholder="질문을 입력하세요"/>
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
    </body>
    </html>
    """
