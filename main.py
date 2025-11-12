from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import random
import os

app = FastAPI()

# ✅ CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ✅ static 폴더 연결
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ sailing_knowledge.json 로드
json_path = os.path.join(os.path.dirname(__file__), "sailing_knowledge.json")
with open(json_path, "r", encoding="utf-8") as f:
    sailing_data = json.load(f)

# ✅ UI 페이지
@app.get("/", response_class=HTMLResponse)
async def get_ui():
    with open(os.path.join("static", "index.html"), "r", encoding="utf-8") as f:
        return f.read()

# ✅ 대화 히스토리 저장용 (서버가 살아 있는 동안)
chat_history = {}

# ✅ /ask POST API (대화 문맥 유지)
@app.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
        user_id = data.get("user_id", "default")  # 사용자 구분용
        message = data.get("message", "").lower()

        if user_id not in chat_history:
            chat_history[user_id] = []

        # 이전 대화 기록에 추가
        chat_history[user_id].append({"role": "user", "message": message})

        # 질문 키워드 매칭
        matches = []
        for item in sailing_data:
            if any(word in message for word in item["질문"].lower().split()):
                matches.append(item)

        if matches:
            best_match = random.choice(matches)
            answer = best_match["답변"]
        else:
            # 이전 대화 참고 + 랜덤 보충 답변
            if chat_history[user_id]:
                answer = random.choice([
                    "이전 대화를 참고하면 조금 더 명확하게 질문하실 수 있어요.",
                    "조금 더 자세히 설명해 주시면 이어서 답변드릴 수 있습니다.",
                    "그 부분은 데이터가 부족하지만, 다른 질문을 해주시면 도움이 됩니다."
                ])
            else:
                answer = random.choice([
                    "안녕하세요! 무엇이 궁금하신가요?",
                    "좋은 질문이에요! 하지만 데이터가 부족합니다.",
                    "조금 더 구체적으로 질문해 주세요."
                ])

        # 대화 기록에 봇 답변 추가
        chat_history[user_id].append({"role": "bot", "message": answer})

        return JSONResponse({"message": answer})

    except Exception as e:
        return JSONResponse({"message": f"서버 처리 중 오류: {str(e)}"})
