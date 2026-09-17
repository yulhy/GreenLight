import type { CatalogItem } from "../types/catalog";
import type { PlanDraft } from "../types/plan";

export interface AnalysisQuantityInputs {
  vehicleCount: number;
  foodCountPerPerson: number;
  suppliesCount: number;
  printingCount: number;
}

export function buildQuantityForItem(
  plan: PlanDraft,
  item: CatalogItem,
  inputs: AnalysisQuantityInputs,
): number {
  const participantCount = plan.participantCount;
  const durationDays = plan.durationDays;
  const distance = plan.roundTripDistanceKm;

  if (!participantCount || participantCount <= 0) {
    throw new Error("참가 인원이 필요합니다.");
  }

  switch (item.unit) {
    case "vehicle_km":
      if (distance == null) {
        throw new Error("왕복 이동거리가 필요합니다.");
      }

      if (inputs.vehicleCount <= 0) {
        throw new Error("차량 수는 1 이상이어야 합니다.");
      }

      return inputs.vehicleCount * distance;

    case "person_km":
      if (distance == null) {
        throw new Error("왕복 이동거리가 필요합니다.");
      }

      return participantCount * distance;

    case "person_meal":
      if (inputs.foodCountPerPerson <= 0) {
        throw new Error("1인당 식사/사용 횟수가 필요합니다.");
      }

      return participantCount * inputs.foodCountPerPerson;

    case "person_item": {
      const perPersonCount =
        item.category === "food"
          ? inputs.foodCountPerPerson
          : inputs.suppliesCount;

      if (perPersonCount <= 0) {
        throw new Error(`${item.item_name}의 1인당 수량이 필요합니다.`);
      }

      return participantCount * perPersonCount;
    }

    case "person_night": {
      if (!durationDays || durationDays <= 0) {
        throw new Error("행사 기간이 필요합니다.");
      }

      const nights = Math.max(durationDays - 1, 0);

      if (nights <= 0) {
        throw new Error(
          "숙박 계획이 있지만 계산 가능한 숙박일수가 없습니다.",
        );
      }

      return participantCount * nights;
    }

    case "page":
      if (inputs.printingCount <= 0) {
        throw new Error(`${item.item_name}의 인쇄 수량이 필요합니다.`);
      }

      return inputs.printingCount;

    case "item": {
      const count =
        item.category === "printing"
          ? inputs.printingCount
          : inputs.suppliesCount;

      if (count <= 0) {
        throw new Error(`${item.item_name}의 수량이 필요합니다.`);
      }

      return count;
    }

    case "can":
      if (inputs.suppliesCount <= 0) {
        throw new Error(`${item.item_name}의 수량이 필요합니다.`);
      }

      return inputs.suppliesCount;

    case "item_night": {
      if (!durationDays || durationDays <= 0) {
        throw new Error("행사 기간이 필요합니다.");
      }

      if (inputs.suppliesCount <= 0) {
        throw new Error(`${item.item_name}의 대여 수량이 필요합니다.`);
      }

      const nights = Math.max(durationDays - 1, 0);

      if (nights <= 0) {
        throw new Error(
          "대여 계획이 있지만 계산 가능한 숙박일수가 없습니다.",
        );
      }

      return inputs.suppliesCount * nights;
    }

    default:
      throw new Error(
        `지원하지 않는 계산 단위입니다: ${item.unit}`,
      );
  }
}
