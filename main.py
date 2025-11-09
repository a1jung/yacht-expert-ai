from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import json
from pathlib import Path

app = FastAPI()

base_path = Path(__file__).parent
sailing_file = base_path / "sailing_knowledge.json"
fitness_file = base_path / "fitness_knowledge.json"

with open(sailing_file, "r", encoding="utf-8") as f:
    sailing_data = json.load(f)

with open(fitness_file, "r", encoding="utf-8") as f:
    fitness_data = json.load(f)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "YachtExpertAI API is running!"}

@app.get("/sailing")
def get_sailing_knowledge():
    return sailing_data

@app.get("/fitness")
def get_fitness_knowledge():
    return fitness_data
