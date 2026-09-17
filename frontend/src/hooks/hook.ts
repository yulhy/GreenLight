import { useState } from "react";
import axios from "axios";

import { sendChat } from "../services/api";

import type {
  ChatResponse,
  ConversationMessage,
  PlanDraft,
} from "../types/plan";


export function useChat() {
  const [conversation, setConversation] = useState<
    ConversationMessage[]
  >([]);

  const [planDraft, setPlanDraft] =
    useState<PlanDraft | null>(null);

  const [missingFields, setMissingFields] =
    useState<string[]>([]);

  const [isReadyToAnalyze, setIsReadyToAnalyze] =
    useState(false);

  const [isLoading, setIsLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);


  async function sendMessage(
    content: string,
  ): Promise<ChatResponse | null> {
    const trimmedContent = content.trim();

    if (!trimmedContent) {
      return null;
    }

    const userMessage: ConversationMessage = {
      role: "user",
      content: trimmedContent,
    };

    const nextConversation = [
      ...conversation,
      userMessage,
    ];

    setConversation(nextConversation);
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendChat({
        conversation: nextConversation,
        currentPlan: planDraft,
      });

      const assistantMessage: ConversationMessage = {
        role: "assistant",
        content: response.assistantMessage,
      };

      setConversation([
        ...nextConversation,
        assistantMessage,
      ]);

      setPlanDraft(
        response.planDraft,
      );

      setMissingFields(
        response.missingFields,
      );

      setIsReadyToAnalyze(
        response.isReadyToAnalyze,
      );

      return response;
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail =
          err.response?.data?.detail;

        if (typeof detail === "string") {
          setError(detail);
        } else {
          setError(
            "서버 요청 중 오류가 발생했습니다.",
          );
        }
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


  function resetChat() {
    setConversation([]);
    setPlanDraft(null);
    setMissingFields([]);
    setIsReadyToAnalyze(false);
    setIsLoading(false);
    setError(null);
  }


  return {
    conversation,
    planDraft,
    missingFields,
    isReadyToAnalyze,
    isLoading,
    error,
    sendMessage,
    resetChat,
  };
}