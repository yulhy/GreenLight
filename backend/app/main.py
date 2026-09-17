import os

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router
from app.api.routes.plans import router as plans_router


APP_ENV = os.getenv("APP_ENV", "development")
FRONTEND_ORIGIN = os.getenv(
    "FRONTEND_ORIGIN",
    "http://localhost:5173",
)


app = FastAPI(
    title="GreenMate API",
    description=(
        "단체활동 계획의 탄소배출량과 비용을 분석하고 "
        "실행 가능한 저탄소 대안을 추천하는 GreenMate 백엔드 API"
    ),
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "service": "greenmate-backend",
        "environment": APP_ENV,
    }


app.include_router(chat_router, prefix="/api")
app.include_router(plans_router, prefix="/api")