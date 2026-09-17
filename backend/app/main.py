import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from app.api.routes.catalog import router as catalog_router
from app.api.routes.chat import router as chat_router
from app.api.routes.plans import router as plans_router


APP_ENV = os.getenv(
    "APP_ENV",
    "development",
)

FRONTEND_ORIGINS = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5173",
)

allowed_origins = [
    origin.strip()
    for origin in FRONTEND_ORIGINS.split(",")
    if origin.strip()
]


app = FastAPI(
    title="GreenMate API",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "GreenMate API",
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "service": "greenmate-backend",
        "environment": APP_ENV,
    }


app.include_router(
    chat_router,
    prefix="/api",
)

app.include_router(
    plans_router,
    prefix="/api",
)

app.include_router(
    catalog_router,
    prefix="/api",
)