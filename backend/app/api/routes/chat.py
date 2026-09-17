from fastapi import APIRouter

from app.schemas.plan import ChatRequest, ChatResponse
from app.services.llm_service import process_chat


router = APIRouter(
    tags=["Chat"],
)


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="AI 대화 및 행사 계획 구조화",
)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    사용자와의 대화 내용을 기반으로 행사 계획 정보를 구조화한다.

    - 사용자 대화에서 행사 정보를 추출한다.
    - 현재까지 수집된 계획과 합친다.
    - 필수 정보 중 누락된 항목을 확인한다.
    - 누락 정보가 있으면 추가 질문을 생성한다.
    - 분석 가능한 상태인지 반환한다.
    """

    return await process_chat(request)
