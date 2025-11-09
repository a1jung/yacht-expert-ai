from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from sentence_transformers import SentenceTransformer, util
import torch
import json, os

app = FastAPI()

# ===== AI 임베딩 모델 로드 =====
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# ===== JSON 파일 자동 로드 =====
knowledge_data = {}

for filename in os.listdir():
    if filename.endswith(".json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                knowledge_data[filename.replace(".json", "")] = data
        except Exception as e:
            print(f"⚠️ {filename} 불러오기 오류:", e)

print("📚 로드된 지식 파일:", list(knowledge_data.keys()))

# ===== 모든 문장 임베딩 사전 구축 =====
knowledge_sentences = []
knowledge_sources = []

def flatten_json(data, prefix=""):
    """JSON 내용을 한 줄 텍스트로 평탄화"""
    if isinstance(data, dict):
        for k, v in data.items():
            flatten_json(v, f"{prefix}{k}: ")
    elif isinstance(data, list):
        for i, v in enumerate(data):
            flatten_json(v, f"{prefix}[{i}] ")
    else:
        sentence = f"{prefix}{data}"
        knowledge_sentences.append(sentence)
        knowledge_sources.append(prefix)

for source_name, data in knowledge_data.items():
    flatten_json(data, f"{source_name} - ")

# 모든 지식 문장 임베딩
embeddings = model.encode(knowledge_sentences, convert_to_tensor=True)

# ===== 홈 =====
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>Yacht Expert AI</title></head>
        <body style="font-family:sans-serif; text-align:center; padding-top:50px;">
            <h1>⛵ Yacht Expert AI (의미 기반 검색)</h1>
            <p>요트, 피트니스 등 전문 지식 기반으로 질문에 답합니다.</p>
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
    q_embedding = model.encode(question, convert_to_tensor=True)
    cos_scores = util.cos_sim(q_embedding, embeddings)[0]
    top_k = torch.topk(cos_scores, k=3)

    response = "<h3>질문:</h3>" + question + "<hr>"
    response += "<h3>가장 관련 있는 지식:</h3>"

    for idx, score in zip(top_k.indices, top_k.values):
        response += f"<p><b>출처:</b> {knowledge_sources[idx]}<br>"
        response += f"<b>내용:</b> {knowledge_sentences[idx]}<br>"
        response += f"<i>유사도 점수:</i> {score:.3f}</p><hr>"

    return f"""
    <html>
        <body style="font-family:sans-serif; padding:30px;">
            {response}
            <a href="/">⬅ 돌아가기</a>
        </body>
    </html>
    """

