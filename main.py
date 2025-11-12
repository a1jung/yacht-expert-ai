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

# ✅ 대화 히스토리 저장용
chat_history = {}

# ✅ /ask POST API
@app.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
        user_id = data.get("user_id", "default")
        message = data.get("message", "").lower()

        if user_id not in chat_history:
            chat_history[user_id] = []

        # 대화 기록에 사용자 메시지 추가
        chat_history[user_id].append({"role": "user", "message": message})

        # 질문 키워드 매칭
        matches = []
        for item in sailing_data:
            if isinstance(item, dict) and "질문" in item and "답변" in item:
                if any(word in message for word in item["질문"].lower().split()):
                    matches.append(item)

        if matches:
            best_match = random.choice(matches)
            answer = best_match["답변"]
            # 추천 질문 생성 (데이터에 있는 다른 질문 중 최대 3개)
            other_questions = [q["질문"] for q in sailing_data
                               if isinstance(q, dict) and "질문" in q
                               and q["질문"] != best_match["질문"]]
            recommended = random.sample(other_questions, min(3, len(other_questions)))
        else:
            answer = random.choice([
                "그 부분은 아직 데이터에 없어요. 조금 더 구체적으로 질문해 주세요.",
                "조금 더 자세히 설명해 주시면 이어서 답변드릴 수 있습니다.",
                "데이터가 부족하지만 다른 질문을 해주시면 도움이 됩니다."
            ])
            # 추천 질문: 데이터에서 랜덤 3개
            recommended = random.sample([q["질문"] for q in sailing_data if isinstance(q, dict) and "질문" in q], 
                                        min(3, len(sailing_data)))

        # 대화 기록에 봇 답변 추가
        chat_history[user_id].append({"role": "bot", "message": answer})

        return JSONResponse({"message": answer, "recommended": recommended})

    except Exception as e:
        return JSONResponse({"message": f"서버 처리 중 오류: {str(e)}", "recommended": []})
