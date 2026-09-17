import type { CatalogItem } from "../types/catalog";
import type { PlanDraft } from "../types/plan";


export interface AnalysisQuantityInputs {
  vehicleCount: number;
  foodCountPerPerson: number;
  suppliesCount: number;
}


export function buildQuantityForItem(
  plan: PlanDraft,
  item: CatalogItem,
  inputs: AnalysisQuantityInputs,
): number {
  const participantCount =
    plan.participantCount;

  const durationDays =
    plan.durationDays;

  const distance =
    plan.roundTripDistanceKm;


  if (!participantCount || participantCount <= 0) {
    throw new Error(
      "참가 인원이 필요합니다.",
    );
  }


  switch (item.unit) {
    case "vehicle_km":
      if (distance == null) {
        throw new Error(
          "왕복 이동거리가 필요합니다.",
        );
      }

      if (inputs.vehicleCount <= 0) {
        throw new Error(
          "차량 수는 1 이상이어야 합니다.",
        );
      }

      return inputs.vehicleCount * distance;


    case "person_km":
      if (distance == null) {
        throw new Error(
          "왕복 이동거리가 필요합니다.",
        );
      }

      return participantCount * distance;


    case "person_meal":
      if (inputs.foodCountPerPerson <= 0) {
        throw new Error(
          "1인당 식사 횟수가 필요합니다.",
        );
      }

      return (
        participantCount
        * inputs.foodCountPerPerson
      );


    case "person_item":
      if (inputs.suppliesCount <= 0) {
        throw new Error(
          "1인당 제공 수량이 필요합니다.",
        );
      }

      return (
        participantCount
        * inputs.suppliesCount
      );


    case "person_night": {
      if (!durationDays || durationDays <= 0) {
        throw new Error(
          "행사 기간이 필요합니다.",
        );
      }

      const nights =
        Math.max(durationDays - 1, 0);

      return participantCount * nights;
    }


    case "item":
    case "can":
      if (inputs.suppliesCount <= 0) {
        throw new Error(
          `${item.item_name}의 수량이 필요합니다.`,
        );
      }

      return inputs.suppliesCount;


    case "item_night": {
      if (!durationDays || durationDays <= 0) {
        throw new Error(
          "행사 기간이 필요합니다.",
        );
      }

      if (inputs.suppliesCount <= 0) {
        throw new Error(
          `${item.item_name}의 대여 수량이 필요합니다.`,
        );
      }

      const nights =
        Math.max(durationDays - 1, 0);

      return (
        inputs.suppliesCount
        * nights
      );
    }


    case "page":
      throw new Error(
        "인쇄물 수량 계산은 아직 연결되지 않았습니다.",
      );


    default:
      throw new Error(
        `지원하지 않는 계산 단위입니다: ${item.unit}`,
      );
  }
}