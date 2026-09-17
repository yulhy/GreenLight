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
  destination?: string | null;

  participantCount?: number | null;
  durationDays?: number | null;

  transport?: string | null;
  roundTripDistanceKm?: number | null;

  mealPlan?: string | null;
  lodgingPlan?: string | null;
  suppliesPlan?: string | null;

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
  destination: string;
  participantCount: number;
  roundTripDistanceKm: number;
  budgetKrw: number;

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

export interface AlternativePlan {
  id: string;
  name: string;
  changedCategories: string[];
  totalCarbonKgCo2e: number;
  totalCostKrw: number;
  carbonReductionPercent: number;
  costDifferenceKrw: number;
  constraintsSatisfied: boolean;
}

export interface PlanAnalysisResponse {
  currentPlan: CurrentPlanAnalysis;
  hotspots: string[];
  alternatives: AlternativePlan[];
  recommendedAlternativeId: string | null;
  recommendationReason: string;
  disclaimer: string;
}