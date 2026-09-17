import { useState } from "react";
import axios from "axios";

import {
  analyzePlan,
} from "../services/api";

import {
  buildAnalysisRequest,
} from "../utils/buildAnalysisRequest";

import type {
  AnalysisQuantityInputs,
} from "../utils/buildQuantities";

import type {
  PlanAnalysisResponse,
  PlanDraft,
} from "../types/plan";


export function useAnalysis() {
  const [result, setResult] =
    useState<PlanAnalysisResponse | null>(
      null,
    );

  const [isLoading, setIsLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);


  async function runAnalysis(
    plan: PlanDraft,
    inputs: AnalysisQuantityInputs,
  ): Promise<PlanAnalysisResponse | null> {
    setIsLoading(true);
    setError(null);

    try {
      const request =
        await buildAnalysisRequest(
          plan,
          inputs,
        );

      const response =
        await analyzePlan(request);

      setResult(response);

      return response;

    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail =
          err.response?.data?.detail;

        if (typeof detail === "string") {
          setError(detail);
        } else {
          setError(
            "분석 요청 중 서버 오류가 발생했습니다.",
          );
        }

      } else if (err instanceof Error) {
        setError(err.message);

      } else {
        setError(
          "알 수 없는 오류가 발생했습니다.",
        );
      }

      return null;

    } finally {
      setIsLoading(false);
    }
  }


  function resetAnalysis() {
    setResult(null);
    setError(null);
    setIsLoading(false);
  }


  return {
    result,
    isLoading,
    error,
    runAnalysis,
    resetAnalysis,
  };
}