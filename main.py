from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import random

app = FastAPI()

# ✅ CORS 설정 (모든 도메인, 모든 메서드, 모든 헤더 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 모든 도메인 허용
    allow_methods=["*"],        # GET, POST, OPTIONS 등 모두 허용
    allow_headers=["*"],        # 모든 헤더 허용
)

# ✅ static 폴더 연결
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ 예시 데이터
sailing_data = [
    {"질문": "요트란", "답변": "요트는 바다나 호수에서 항해하는 작은 선박입니다."},
    {"질문": "마스트", "답변": "마스트는 요트의 세일을 지탱하는 기둥입니다."},
    {"질문": "세일", "답변": "세일은 바람을 받아 요트를 앞으로 나아가게 합니다."}
]

# ✅ UI 페이지
@app.get("/", response_class=HTMLResponse)
async def get_ui():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# ✅ /ask POST API
@app.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "").lower()

        # 데이터 검색
        best_match = None
        for item in sailing_data:
            if item["질문"].lower() in message:
                best_match = item
                break

        if best_match:
            answer = best_match["답변"]
        else:
            answer = random.choice([
                "그 부분은 아직 데이터에 없어요. 조금 더 구체적으로 질문해 주세요.",
                "조금 더 자세히 설명해 주시면 답변드릴 수 있어요.",
                "해당 주제에 대한 데이터가 아직 부족해요. 곧 업데이트할게요!"
            ])

        return JSONResponse({"message": answer})

    except Exception as e:
        return JSONResponse({"message": f"서버 처리 중 오류: {str(e)}"})
