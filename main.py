import json
import os

# --- JSON 파일 경로 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAILING_FILE = os.path.join(BASE_DIR, "sailing_knowledge.json")
FITNESS_FILE = os.path.join(BASE_DIR, "fitness_knowledge.json")

# --- JSON 읽기 함수 ---
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# --- 데이터 불러오기 ---
sailing_knowledge = load_json(SAILING_FILE)
fitness_knowledge = load_json(FITNESS_FILE)

# --- 예시 함수: 요트 정보 조회 ---
def get_sailing_info(yacht_class):
    yacht = sailing_knowledge.get(yacht_class)
    if not yacht:
        return f"{yacht_class} 클래스 정보가 없습니다."
    info = f"클래스: {yacht_class}\n설명: {yacht['description']}\n"
    info += "풍향별 세일 조정:\n"
    for wind, adjustment in yacht.get("wind_adjustments", {}).items():
        info += f"  {wind} 바람: {adjustment}\n"
    return info

# --- 예시 함수: 피트니스 정보 조회 ---
def get_fitness_info(topic):
    ft = fitness_knowledge.get(topic)
    if not ft:
        return f"{topic} 정보가 없습니다."
    info = f"주제: {topic}\n설명: {ft.get('definition', '없음')}\n"
    if 'benefits' in ft:
        info += "효과:\n"
        benefits = ft['benefits']
        if isinstance(benefits, list):
            for b in benefits:
                info += f"  - {b}\n"
        elif isinstance(benefits, dict):
            for k, v in benefits.items():
                info += f"  {k}: {v}\n"
    return info

# --- 실행 예시 ---
if __name__ == "__main__":
    print("=== 요트 정보 ===")
    for yacht_class in sailing_knowledge["classes"]:
        print(get_sailing_info(yacht_class))
        print("-" * 40)

    print("\n=== 피트니스 정보 ===")
    for topic in fitness_knowledge.keys():
        print(get_fitness_info(topic))
        print("-" * 40)
