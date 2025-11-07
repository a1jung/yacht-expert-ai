from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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
    # 무료 모드 AI
    response_text = free_mode_answer(message.user_input)
    return {"response": response_text}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
    <title>Yacht Expert AI</title>
    <style>
        body { font-family: Arial, sans-serif; background: #e0f7fa; text-align: center; margin-top: 50px;}
        h1 { color: #006064; }
        input { padding: 10px; width: 300px; border-radius: 5px; border: 1px solid #006064; }
        button { padding: 10px 20px; border-radius: 5px; border: none; background: #006064; color: white; cursor: pointer; }
        button:hover { background: #004d40; }
        p { margin-top: 20px; font-size: 18px; color: #004d40; }
        #chatBox { margin-top: 20px; max-width: 600px; margin-left: auto; margin-right: auto; text-align:left; background:white; padding:15px; border-radius:10px; }
    </style>
    </head>
    <body>
        <h1>Yacht Expert AI</h1>
        <input id="userInput" placeholder="요트 관련 질문을 입력하세요"/>
        <button onclick="sendMessage()">Send</button>
        <div id="chatBox"></div>
        <script>
        async function sendMessage() {
            const input = document.getElementById("userInput").value;
            if(!input) return;
            const res = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({user_input: input})
            });
            const data = await res.json();
            const chatBox = document.getElementById('chatBox');
            chatBox.innerHTML += `<p><b>질문:</b> ${input}</p><p><b>답변:</b> ${data.response}</p><hr/>`;
            document.getElementById("userInput").value = '';
        }
        </script>
    </body>
    </html>
    """
