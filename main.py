from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import random
import os

app = FastAPI()

# ✅ static 폴더 연결 (UI 파일용)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ JSON 데이터 로드
with open("sailing_knowledge.json", "r", encoding="utf-8") as f:
    sailing_data = json.load(f)

# ✅ 기본 루트 — UI 페이지 연결
@app.get("/", response_class=HTMLResponse)
async def get_ui():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# ✅ AI 답변 API
@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question", "").lower()

    # 데이터베이스에서 일치하는 내용 검색
    best_match = None
    for item in sailing_data:
        if item["질문"].lower() in question:
            best_match = item
            break

    # 답변 구성
    if best_match:
        answer = best_match["답변"]
    else:
        answer = random.choice([
            "그 부분은 아직 데이터에 없어요. 조금 더 구체적으로 질문해 주시겠어요?",
            "조금 더 자세히 설명해주시면 답변드릴 수 있을 것 같아요.",
            "해당 주제에 대한 데이터가 아직 부족해요. 곧 업데이트할게요!"
        ])

    return JSONResponse({"answer": answer})
