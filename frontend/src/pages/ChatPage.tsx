import { useState } from "react";

import { useChat } from "../hooks/hook";
import type { PlanDraft } from "../types/plan";


interface ChatPageProps {
  onAnalyzeReady: (plan: PlanDraft) => void;
}


const suggestions = [
  "동아리 MT를 계획하고 있어요",
  "탄소와 비용을 줄이고 싶어요",
  "체험학습 예산을 비교해 주세요",
];


function ChatPage({
  onAnalyzeReady,
}: ChatPageProps) {
  const [input, setInput] =
    useState("");

  const {
    conversation,
    planDraft,
    isReadyToAnalyze,
    isLoading,
    error,
    sendMessage,
  } = useChat();


  async function submitMessage(
    message: string,
  ) {
    const trimmed =
      message.trim();

    if (!trimmed || isLoading) {
      return;
    }

    setInput("");

    await sendMessage(trimmed);
  }


  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    await submitMessage(input);
  }


  const hasMessage =
    conversation.length > 0;


  return (
    <section
      className={
        hasMessage
          ? "chat-start has-message"
          : "chat-start"
      }
    >
      <div className="chat-welcome">
        <p className="chat-kicker">
          GREENMATE
        </p>

        <h1>
          어떤 모임을 계획하고 있나요?
        </h1>

        <p>
          떠오르는 계획을 편하게 이야기해 주세요.
        </p>
      </div>


      {hasMessage && (
        <div className="conversation">
          {conversation.map(
            (message, index) => (
              <p
                key={`${message.role}-${index}`}
                className={`bubble ${message.role}`}
              >
                {message.content}
              </p>
            ),
          )}

          {isLoading && (
            <p className="bubble assistant">
              계획을 정리하고 있어요...
            </p>
          )}
        </div>
      )}


      <form
        className="chat-composer"
        onSubmit={handleSubmit}
      >
        <label
          className="sr-only"
          htmlFor="chat-input"
        >
          GreenMate에게 모임에 대해 질문하기
        </label>

        <textarea
          id="chat-input"
          value={input}
          placeholder="모임 · 인원 · 예산을 자유롭게"
          disabled={isLoading}
          onChange={(event) =>
            setInput(event.target.value)
          }
        />

        <div className="composer-bottom">
          <span>
            GreenMate에게 모임에 대해 질문하기
          </span>

          <button
            type="submit"
            aria-label="메시지 보내기"
            disabled={
              isLoading
              || !input.trim()
            }
          >
            ↑
          </button>
        </div>
      </form>


      {!hasMessage && (
        <div className="prompt-suggestions">
          {suggestions.map(
            (suggestion) => (
              <button
                key={suggestion}
                type="button"
                onClick={() =>
                  submitMessage(suggestion)
                }
              >
                {suggestion}
              </button>
            ),
          )}
        </div>
      )}


      {error && (
        <p className="error">
          {error}
        </p>
      )}


      {isReadyToAnalyze && planDraft && (
        <div className="actions">
          <button
            type="button"
            className="primary"
            onClick={() =>
              onAnalyzeReady(planDraft)
            }
          >
            예상 결과 보기
            <span>→</span>
          </button>
        </div>
      )}


      <p className="chat-disclaimer">
        입력 내용을 바탕으로 행사 계획을 정리하고
        탄소배출량과 비용을 비교합니다.
      </p>
    </section>
  );
}


export default ChatPage;