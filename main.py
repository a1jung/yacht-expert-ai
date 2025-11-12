from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import random

app = FastAPI()

# ✅ CORS 허용 (로컬 테스트용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ static 폴더 연결 (UI 파일용)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ 데이터 예시
try:
    with open("sailing_knowledge.json", "r", encoding="utf-8") as f:
        sailing_data = json.load(f)
except FileNotFoundError:
    sailing_data = []  # 데이터 없으면 빈 리스트

# ✅ 기본 UI 페이지
@app.get("/", response_class=HTMLResponse)
async def get_ui():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# ✅ /ask API
@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    message = data.get("message", "").lower()

    # 데이터베이스에서 질문 검색
    best_match = None
    for item in sailing_data:
        if item.get("질문", "").lower() in message:
            best_match = item
            break

    if best_match:
        answer = best_match.get("답변", "답변이 없습니다.")
    else:
        # 랜덤 기본 답변
        answer = random.choice([
            "그 부분은 아직 데이터에 없어요. 조금 더 구체적으로 질문해 주시겠어요?",
            "조금 더 자세히 설명해주시면 답변드릴 수 있을 것 같아요.",
            "해당 주제에 대한 데이터가 아직 부족해요. 곧 업데이트할게요!"
        ])

    return JSONResponse({"message": answer})
