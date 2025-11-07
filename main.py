from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import openai, os

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

@app.post("/chat")
def chat(message: Message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message.user_input}]
    )
    return {"response": response.choices[0].message.content}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Yacht Expert AI</h1>
    <input id="userInput" placeholder="Type your message"/>
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
    """
