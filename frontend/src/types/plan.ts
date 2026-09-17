export type ChatRole = "user" | "assistant";

export interface ConversationMessage {
  role: ChatRole;
  content: string;
}

export interface PlanPreferences {
  maxAdditionalCostKrw?: number | null;
  avoidItems: string[];
  priority?: string | null;
}

export interface PlanDraft {
  activityType?: string | null;
  purpose?: string | null;
  origin?: string | null;
  destination?: string | null;

  participantCount?: number | null;
  durationDays?: number | null;

  transport?: string | null;
  roundTripDistanceKm?: number | null;

  mealPlan?: string | null;
  lodgingPlan?: string | null;
  suppliesPlan?: string | null;
  printingPlan?: string | null;

  budgetKrw?: number | null;

  preferences?: PlanPreferences | null;

  [key: string]: unknown;
}

export interface ChatRequest {
  conversation: ConversationMessage[];
  currentPlan?: PlanDraft | null;
}

export interface ChatResponse {
  assistantMessage: string;
  missingFields: string[];
  planDraft: PlanDraft;
  isReadyToAnalyze: boolean;
}

export interface PlanSelection {
  category: string;
  itemId: string;
  quantity: number;
}

export interface PlanAnalysisRequest {
  activityType: string;
  destination: string | null;
  participantCount: number;
  durationDays: number | null;
  roundTripDistanceKm: number | null;
  budgetKrw: number | null;

  preferences: PlanPreferences;
  selections: PlanSelection[];
}

export interface CarbonBreakdown {
  category: string;
  carbonKgCo2e: number | null;
  sharePercent: number | null;
}

export interface CurrentPlanAnalysis {
  totalCarbonKgCo2e: number | null;
  totalCostKrw: number;
  breakdown: CarbonBreakdown[];
}

export interface AlternativeExplanation {
  summary: string;
  advantages: string;
  tradeoff: string;
}

export interface AlternativePlan {
  id: string;
  name: string;

  changedCategories: string[];

  changes: string[];

  totalCarbonKgCo2e: number;
  totalCostKrw: number;

  carbonReductionPercent: number;
  costDifferenceKrw: number;

  constraintsSatisfied: boolean;

  explanation:
    AlternativeExplanation | null;
}

export interface PlanAnalysisResponse {
  currentPlan: CurrentPlanAnalysis;
  hotspots: string[];
  alternatives: AlternativePlan[];
  recommendedAlternativeId: string | null;
  recommendationReason: string | null;
  disclaimer: string;
}
