from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# =========================================================
# Chat
# =========================================================


class ConversationMessage(BaseModel):
    """
    사용자와 AI 사이의 단일 대화 메시지.
    """

    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)


class PlanPreferences(BaseModel):
    """
    행사 계획에 대한 사용자 선호 조건.
    """

    maxAdditionalCostKrw: int | None = Field(
        default=None,
        ge=0,
    )

    avoidItems: list[str] = Field(
        default_factory=list,
    )

    priority: str | None = None


class PlanDraft(BaseModel):
    """
    대화 과정에서 구조화되는 행사 계획 초안.

    대화 중에는 일부 정보가 없을 수 있으므로
    대부분 Optional로 둔다.
    """

    activityType: str | None = None
    destination: str | None = None

    participantCount: int | None = Field(
        default=None,
        gt=0,
    )

    durationDays: int | None = Field(
        default=None,
        gt=0,
    )

    transport: str | None = None

    roundTripDistanceKm: float | None = Field(
        default=None,
        ge=0,
    )

    mealPlan: str | None = None
    lodgingPlan: str | None = None
    suppliesPlan: str | None = None

    budgetKrw: int | None = Field(
        default=None,
        ge=0,
    )

    preferences: PlanPreferences | None = None

    model_config = ConfigDict(
        extra="allow",
    )


class ChatRequest(BaseModel):
    """
    POST /api/chat 요청.
    """

    conversation: list[ConversationMessage] = Field(
        min_length=1,
    )

    currentPlan: PlanDraft | None = None


class ChatResponse(BaseModel):
    """
    POST /api/chat 응답.
    """

    assistantMessage: str

    missingFields: list[str] = Field(
        default_factory=list,
    )

    planDraft: PlanDraft

    isReadyToAnalyze: bool


# =========================================================
# Plan Analysis Request
# =========================================================


class PlanSelection(BaseModel):
    """
    사용자가 현재 계획에서 선택한 개별 항목.
    """

    category: str = Field(
        min_length=1,
    )

    itemId: str = Field(
        min_length=1,
    )

    quantity: float = Field(
        gt=0,
    )


class PlanAnalysisRequest(BaseModel):
    """
    POST /api/plans/analyze 요청.
    """

    activityType: str = Field(
        min_length=1,
    )

    destination: str = Field(
        min_length=1,
    )

    participantCount: int = Field(
        gt=0,
    )

    roundTripDistanceKm: float = Field(
        ge=0,
    )

    budgetKrw: int = Field(
        ge=0,
    )

    preferences: PlanPreferences = Field(
        default_factory=PlanPreferences,
    )

    selections: list[PlanSelection] = Field(
        min_length=1,
    )


# =========================================================
# Plan Analysis Response
# =========================================================


class CarbonBreakdown(BaseModel):
    category: str

    carbonKgCo2e: float | None = None

    sharePercent: float | None = None


class CurrentPlanAnalysis(BaseModel):
    totalCarbonKgCo2e: float | None = None
    totalCostKrw: float = Field(ge=0)
    breakdown: list[CarbonBreakdown] = Field(
        default_factory=list,
    )


class AlternativePlan(BaseModel):
    """
    현재 계획을 대체할 수 있는 대안.
    """

    id: str

    name: str

    changedCategories: list[str] = Field(
        default_factory=list,
    )

    totalCarbonKgCo2e: float = Field(
        ge=0,
    )

    totalCostKrw: float = Field(
        ge=0,
    )

    carbonReductionPercent: float

    costDifferenceKrw: float

    constraintsSatisfied: bool


class PlanAnalysisResponse(BaseModel):
    """
    POST /api/plans/analyze 최종 응답.
    """

    currentPlan: CurrentPlanAnalysis

    hotspots: list[str] = Field(
        default_factory=list,
    )

    alternatives: list[AlternativePlan] = Field(
        default_factory=list,
    )

    recommendedAlternativeId: str | None = None

    recommendationReason: str | None = None

    disclaimer: str = (
        "결과는 입력값과 등록된 배출계수에 기반한 추정치입니다."
    )