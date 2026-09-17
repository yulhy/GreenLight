import json
import os

from openai import AsyncOpenAI
from pydantic import BaseModel

from app.schemas.plan import (
    ChatRequest,
    ChatResponse,
    PlanDraft,
)


# =========================================================
# LLM Client
# =========================================================

# ---------------------------------------------------------
# [임시] Gemini API
# ---------------------------------------------------------

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash",
)


# ---------------------------------------------------------
# [추후] OpenAI API
# Gemini 사용을 중단할 때 위 client / MODEL_NAME을 주석 처리하고
# 아래 코드를 주석 해제해서 사용
# ---------------------------------------------------------

# client = AsyncOpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
# )
#
# MODEL_NAME = os.getenv(
#     "OPENAI_MODEL",
#     "gpt-5.6-luna",
# )


# =========================================================
# Required fields
# =========================================================

REQUIRED_FIELDS = [
    "activityType",
    "destination",
    "participantCount",
    "durationDays",
    "transport",
    "roundTripDistanceKm",
    "mealPlan",
    "lodgingPlan",
    "suppliesPlan",
    "budgetKrw",
]


# =========================================================
# Structured LLM output
# =========================================================

class LLMChatResult(BaseModel):
    """
    LLM에게 직접 받을 구조화 응답.

    missingFields와 isReadyToAnalyze는
    서버에서 직접 계산하기 때문에 포함하지 않는다.
    """

    assistantMessage: str
    planDraft: PlanDraft


# =========================================================
# Prompt
# =========================================================

SYSTEM_PROMPT = """
당신은 친환경 단체 행사 계획 서비스 GreenMate의 대화형 AI입니다.

당신의 역할은 사용자의 자연어 대화에서 행사 계획 정보를 추출하고,
아직 필요한 정보가 부족하면 적절한 추가 질문을 생성하는 것입니다.

반드시 다음 규칙을 지키세요.

[역할]
1. 행사 계획에 관한 자연어 대화를 처리합니다.
2. 사용자의 입력에서 행사 관련 정보를 추출합니다.
3. 기존 계획 정보와 새롭게 추출한 정보를 합칩니다.
4. 필수 정보 중 누락된 항목을 확인합니다.
5. 누락 정보가 있다면 한 번에 1~2개의 관련 질문만 합니다.
6. 정보가 충분하면 분석 가능 상태임을 알려줍니다.

[절대 하지 말아야 할 것]
- 탄소배출계수를 임의로 생성하지 마세요.
- 비용을 임의로 생성하지 마세요.
- 사용자가 제공하지 않은 필수 정보를 추측하여 확정하지 마세요.
- 이동거리 등 알 수 없는 숫자를 임의로 추정하지 마세요.
- 탄소 감축률을 계산하거나 임의로 제시하지 마세요.
- 카탈로그에 없는 데이터의 수치를 만들어내지 마세요.

[추출 가능한 정보]
- activityType: 행사 유형
- destination: 목적지
- participantCount: 참가 인원
- durationDays: 행사 기간(일)
- transport: 이동수단
- roundTripDistanceKm: 왕복 이동거리(km)
- mealPlan: 식사 계획
- lodgingPlan: 숙박 계획
- suppliesPlan: 소모품 계획
- budgetKrw: 전체 예산(원)

- preferences:
  - maxAdditionalCostKrw
  - avoidItems
  - priority

[중요]
- 사용자가 새로운 값을 명확하게 말하면 기존 값보다 새 값을 우선하세요.
- 사용자가 말하지 않은 정보는 null 상태를 유지하세요.
- 기존 currentPlan에 값이 있고 사용자가 수정하지 않았다면 그 값을 유지하세요.
- assistantMessage에는 다음으로 필요한 정보를 자연스럽게 질문하세요.
"""


# =========================================================
# Helpers
# =========================================================

def _build_input(
    request: ChatRequest,
) -> str:
    """
    현재 대화와 기존 계획을 LLM 입력용 JSON 문자열로 변환한다.
    """

    conversation = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in request.conversation
    ]

    current_plan = (
        request.currentPlan.model_dump(
            exclude_none=True,
        )
        if request.currentPlan
        else {}
    )

    payload = {
        "conversation": conversation,
        "currentPlan": current_plan,
    }

    return json.dumps(
        payload,
        ensure_ascii=False,
    )


def _find_missing_fields(
    plan: PlanDraft,
) -> list[str]:
    """
    분석에 필요한 필수 정보 중
    값이 없는 필드를 반환한다.
    """

    plan_data = plan.model_dump()

    missing_fields: list[str] = []

    for field in REQUIRED_FIELDS:
        value = plan_data.get(field)

        if value is None:
            missing_fields.append(field)

    return missing_fields


# =========================================================
# Main service
# =========================================================

async def process_chat(
    request: ChatRequest,
) -> ChatResponse:
    """
    사용자 대화를 분석하고 PlanDraft를 갱신한다.
    """

    completion = await client.beta.chat.completions.parse(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": _build_input(request),
            },
        ],
        response_format=LLMChatResult,
    )

    parsed = completion.choices[0].message.parsed

    if parsed is None:
        raise ValueError(
            "LLM의 구조화 응답을 해석하지 못했습니다."
        )

    plan_draft = parsed.planDraft

    missing_fields = _find_missing_fields(
        plan_draft
    )

    return ChatResponse(
        assistantMessage=parsed.assistantMessage,
        missingFields=missing_fields,
        planDraft=plan_draft,
        isReadyToAnalyze=(
            len(missing_fields) == 0
        ),
    )