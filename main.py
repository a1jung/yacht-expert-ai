from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(title="YachtExpertAI")

# CORS 설정 (필요 시)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JSON 파일 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAILING_FILE = os.path.join(BASE_DIR, "sailing_knowledge.json")
FITNESS_FILE = os.path.join(BASE_DIR, "fitness_knowledge.json")

# JSON 불러오기 함수
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# 데이터 로드
sailing_data = load_json(SAILING_FILE)
fitness_data = load_json(FITNESS_FILE)

# 루트 라우트
@app.get("/")
def root():
    return {"message": "YachtExpertAI API is running!"}

# 세일링 지식 라우트
@app.get("/sailing")
def get_sailing():
    return sailing_data

# 피트니스 지식 라우트
@app.get("/fitness")
def get_fitness():
    return fitness_data
