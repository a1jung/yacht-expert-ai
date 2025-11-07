# knowledge.py
YACHT_KNOWLEDGE_PARAS = {
    "세일": "세일 트리밍: 풍향과 풍속에 맞춰 세일 각도와 깊이를 조절합니다. 플러를 당기면 평평해지고, 풀러를 늦추면 깊어집니다.",
    "튜닝": "마스트 밴드, 하드너 등 튜닝을 조정해 풍속에 맞춰 추진력 최적화.",
    "레이스": "스타트 타이밍, 코스 읽기, 상대 위치 선점 중요. 포트/스타보드 스타트 시 전략 달라짐.",
    "해상훈련": "트리밍, 핸들링, 턴 연습 → 레이스 시뮬레이션 → 위기 상황 대응 연습 단계별 훈련.",
    "육상훈련": "코어 강화, 상체·하체 근력, 균형 감각, 지구력 훈련 병행.",
    "체력루틴": "월-수: 해상, 화-목: 육상, 금: 시뮬레이터, 주말: 레이스 전략 연습.",
    "안전": "구명조끼 착용, VHF 점검, 날씨 확인, 구조 장비 확인 필수.",
    "마스트": "밴드 팽팽하면 세일 평평, 느슨하면 깊음. 미세 조절로 추진력 최적화.",
    "돛각": "바람과 코스에 맞춰 세일 각도 조정, 속도와 안정성 영향."
}

def free_mode_answer(user_input: str) -> str:
    """사용자 질문에 키워드 매칭으로 답변"""
    matches = []
    for key, answer in YACHT_KNOWLEDGE_PARAS.items():
        if key in user_input:
            matches.append(answer)
    if matches:
        return "\n\n".join(matches)
    # 키워드 없으면 AI 유도 질문
    suggested = ", ".join(list(YACHT_KNOWLEDGE_PARAS.keys()))
    return f"죄송해요, 해당 질문 정보는 무료 모드에 없습니다. 대신 이런 키워드로 질문해보세요: {suggested}"
