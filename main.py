from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# CORS 허용 (브라우저 테스트용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 경로
app.mount("/static", StaticFiles(directory="static"), name="static")

# 지식 JSON 파일 불러오기
with open("sailing_knowledge.json", "r", encoding="utf-8") as f:
    sailing_knowledge = json.load(f)

with open("fitness_knowledge.json", "r", encoding="utf-8") as f:
    fitness_knowledge = json.load(f)

@app.get("/", response_class=HTMLResponse)
async def home():
    # index.html 반환
    path = os.path.join("static", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("message", "").lower()

    # 간단한 키워드 기반 매칭
    if "sailing" in question or "요트" in question:
        response = sailing_knowledge
    elif "fitness" in question or "운동" in question:
        response = fitness_knowledge
    else:
        response = {"message": "죄송합니다. 관련 지식이 없습니다."}

    return JSONResponse(content=response)
