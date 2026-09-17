import traceback

from fastapi import APIRouter, HTTPException
from openai import APIError, RateLimitError

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
async def chat(
    request: ChatRequest,
) -> ChatResponse:
    try:
        return await process_chat(request)

    except RateLimitError as exc:
        print("\n===== LLM RATE LIMIT ERROR =====")
        traceback.print_exc()
        print("================================\n")

        raise HTTPException(
            status_code=429,
            detail=f"AI 사용량 한도 초과: {str(exc)}",
        ) from exc

    except APIError as exc:
        print("\n===== LLM API ERROR =====")
        traceback.print_exc()
        print("=========================\n")

        raise HTTPException(
            status_code=502,
            detail=f"AI 서비스 호출 오류: {str(exc)}",
        ) from exc

    except Exception as exc:
        print("\n===== UNEXPECTED CHAT ERROR =====")
        traceback.print_exc()
        print("=================================\n")

        raise HTTPException(
            status_code=500,
            detail=f"채팅 처리 오류: {str(exc)}",
        ) from exc