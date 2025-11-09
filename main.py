from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI()

# JSON 파일 경로
base_path = Path(__file__).parent
sailing_file = base_path / "sailing_knowledge.json"
fitness_file = base_path / "fitness_knowledge.json"

# 파일 읽기
with open(sailing_file, "r", encoding="utf-8") as f:
    sailing_data = json.load(f)

with open(fitness_file, "r", encoding="utf-8") as f:
    fitness_data = json.load(f)

# 기본 경로
@app.get("/")
def read_root():
    return {"message": "YachtExpertAI API is running!"}

# Sailing knowledge
@app.get("/sailing")
def get_sailing_knowledge():
    return sailing_data

# Fitness knowledge
@app.get("/fitness")
def get_fitness_knowledge():
    return fitness_data
