from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import json, os

app = FastAPI()

# ===== 지식 데이터 자동 로드 =====
knowledge_data = {}

for filename in os.listdir():
    if filename.endswith(".json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                knowledge_data[filename.replace(".json", "")] = data
        except Exception as e:
            print(f"⚠️ {filename} 불러오기 오류:", e)

print("📘 로드된 지식 파일:", list(knowledge_data.keys()))

# ===== 홈 UI =====
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>Yacht Expert AI</title></head>
        <body style="font-family:sans-serif; text-align:center; padding-top:50px;">
            <h1>⛵ Yacht Expert AI</h1>
            <p>요트 및 피트니스 지식 기반 AI 시스템</p>
            <form action="/ask" method="post">
                <textarea name="question" rows="5" cols="50" placeholder="질문을 입력하세요"></textarea><br><br>
                <button type="submit">질문하기</button>
            </form>
        </body>
    </html>
    """

# ===== 질문 처리 =====
@app.post("/ask")
def ask(question: str = Form(...)):
    response = ""

    # 키워드 기반 응답 (단순 예시)
    q = question.lower()

    # 요트 관련
    if "요트" in q or "세일" in q:
        sailing = knowledge_data.get("sailing_knowledge", {})
        if sailing:
            response += "🏄‍♂️ 요트 관련 지식에서 찾은 내용입니다:<br>"
            for k, v in sailing.items():
                response += f"<b>{k}</b>: {str(v)[:200]}...<br>"
        else:
            response = "요트 관련 데이터가 없습니다."

    # 피트니스 관련
    elif "운동" in q or "트레이닝" in q:
        fitness = knowledge_data.get("fitness_knowledge", {})
        if fitness:
            response += "💪 피트니스 관련 지식에서 찾은 내용입니다:<br>"
            for cat, content in fitness.items():
                if isinstance(content, dict):
                    response += f"<b>{cat}</b>: {content.get('description', '')}<br>"
        else:
            response = "피트니스 관련 데이터가 없습니다."

    else:
        response = "❓ 관련 데이터를 찾을 수 없습니다."

    return f"""
    <html>
        <body style="font-family:sans-serif; padding:30px;">
            <h2>질문:</h2><p>{question}</p>
            <hr>
            <h2>AI 응답:</h2><p>{response}</p>
            <br><a href="/">돌아가기</a>
        </body>
    </html>
    """

