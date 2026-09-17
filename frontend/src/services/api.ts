import axios from "axios";

import type {
  ChatRequest,
  ChatResponse,
  PlanAnalysisRequest,
  PlanAnalysisResponse,
} from "../types/plan";


const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  "http://localhost:8000";


const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});


export interface HealthResponse {
  status: string;
  service: string;
  environment: string;
}


export async function getHealth(): Promise<HealthResponse> {
  const response = await apiClient.get<HealthResponse>(
    "/api/health",
  );

  return response.data;
}


export async function sendChat(
  request: ChatRequest,
): Promise<ChatResponse> {
  const response = await apiClient.post<ChatResponse>(
    "/api/chat",
    request,
  );

  return response.data;
}


export async function analyzePlan(
  request: PlanAnalysisRequest,
): Promise<PlanAnalysisResponse> {
  const response =
    await apiClient.post<PlanAnalysisResponse>(
      "/api/plans/analyze",
      request,
    );

  return response.data;
}


export default apiClient;