# knowledge.py
# 요트 관련 무료 모드 지식 DB

YACHT_KNOWLEDGE_PARAS = {
    "세일": "세일 트리밍은 풍향과 풍속에 따라 깊이와 각도를 조정합니다.",
    "레이스": "레이스 전략: 스타트 타이밍, 코스 파악, 상대 위치선점 중요.",
    "안전": "안전수칙: 구명조끼, VHF 점검, 비상 절차 숙지.",
    "마스트": "마스트와 밴드: 팽팽하면 세일 평평, 느슨하면 세일 깊음.",
    "돛각": "돛각 조절은 풍향과 코스에 맞춰 미세하게 조정합니다.",
    "핀": "키 핀 조정으로 배의 방향 안정성을 확보합니다."
}

def free_mode_answer(user_input: str) -> str:
    """
    무료 모드: 입력 키워드와 지식 DB를 매칭
    """
    for key, answer in YACHT_KNOWLEDGE_PARAS.items():
        if key in user_input:
            return answer
    return "죄송해요, 그 질문에 대한 정보는 무료 모드에 없습니다."
