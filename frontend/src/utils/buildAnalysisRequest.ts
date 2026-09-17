import {
  resolveCatalogItem,
} from "../services/api";

import {
  buildQuantityForItem,
  type AnalysisQuantityInputs,
} from "./buildQuantities";

import type {
  PlanAnalysisRequest,
  PlanDraft,
  PlanSelection,
} from "../types/plan";


type AnalysisCategory =
  | "transport"
  | "food"
  | "accommodation"
  | "supplies";


interface CategoryValue {
  category:
    AnalysisCategory;

  value:
    string | null | undefined;
}


async function createSelection(
  plan: PlanDraft,
  category: AnalysisCategory,
  value: string,
  inputs: AnalysisQuantityInputs,
): Promise<PlanSelection> {
  const matched =
    await resolveCatalogItem(
      category,
      value,
    );

  const quantity =
    buildQuantityForItem(
      plan,
      matched,
      inputs,
    );

  return {
    category,
    itemId:
      matched.item_id,
    quantity,
  };
}


export async function buildAnalysisRequest(
  plan: PlanDraft,
  inputs: AnalysisQuantityInputs,
): Promise<PlanAnalysisRequest> {
  if (!plan.activityType) {
    throw new Error(
      "행사 유형이 없습니다.",
    );
  }

  if (!plan.destination) {
    throw new Error(
      "목적지가 없습니다.",
    );
  }

  if (!plan.participantCount) {
    throw new Error(
      "참가 인원이 없습니다.",
    );
  }

  if (
    plan.transport
    && plan.roundTripDistanceKm == null
  ) {
    throw new Error(
      "왕복 이동거리가 없습니다.",
    );
  }

  if (plan.budgetKrw == null) {
    throw new Error(
      "예산이 없습니다.",
    );
  }


  const categoryValues:
    CategoryValue[] = [
      {
        category:
          "transport",
        value:
          plan.transport,
      },
      {
        category:
          "food",
        value:
          plan.mealPlan,
      },
      {
        category:
          "accommodation",
        value:
          plan.lodgingPlan,
      },
      {
        category:
          "supplies",
        value:
          plan.suppliesPlan,
      },
    ];


  const selections:
    PlanSelection[] = [];


  for (
    const entry
    of categoryValues
  ) {
    if (!entry.value) {
      continue;
    }

    selections.push(
      await createSelection(
        plan,
        entry.category,
        entry.value,
        inputs,
      ),
    );
  }


  if (
    selections.length === 0
  ) {
    throw new Error(
      "분석할 항목이 없습니다.",
    );
  }


  return {
    activityType:
      plan.activityType,

    destination:
      plan.destination,

    participantCount:
      plan.participantCount,

    durationDays:
      plan.durationDays
      ?? null,

    roundTripDistanceKm:
      plan.roundTripDistanceKm
      ?? 0,

    budgetKrw:
      plan.budgetKrw,

    preferences: {
      maxAdditionalCostKrw:
        plan.preferences
          ?.maxAdditionalCostKrw
        ?? null,

      avoidItems:
        plan.preferences
          ?.avoidItems
        ?? [],

      priority:
        plan.preferences
          ?.priority
        ?? null,
    },

    selections,
  };
}