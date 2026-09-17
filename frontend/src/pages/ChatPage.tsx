import { useState } from "react";

import { useChat } from "../hooks/hook";
import type { PlanDraft } from "../types/plan";


interface ChatPageProps {
  onAnalyzeReady: (plan: PlanDraft) => void;
}


const progressItems = [
  {
    key: "activityType",
    label: "행사 유형",
  },
  {
    key: "destination",
    label: "목적지",
  },
  {
    key: "participantCount",
    label: "참가 인원",
  },
  {
    key: "durationDays",
    label: "기간",
  },
  {
    key: "transport",
    label: "이동수단",
  },
  {
    key: "roundTripDistanceKm",
    label: "왕복 거리",
  },
  {
    key: "budgetKrw",
    label: "예산",
  },
];


function ChatPage({
  onAnalyzeReady,
}: ChatPageProps) {
  const [input, setInput] = useState("");

  const {
    conversation,
    planDraft,
    missingFields,
    isReadyToAnalyze,
    isLoading,
    error,
    sendMessage,
  } = useChat();


  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    const message = input.trim();

    if (!message || isLoading) {
      return;
    }

    setInput("");

    await sendMessage(message);
  }


  function getProgressClass(
    field: string,
  ): string {
    if (!planDraft) {
      return "";
    }

    const value =
      planDraft[
        field as keyof PlanDraft
      ];

    if (
      value !== null
      && value !== undefined
      && value !== ""
    ) {
      return "is-done";
    }

    if (missingFields[0] === field) {
      return "is-active";
    }

    return "";
  }


  return (
    <section className="screen is-visible">
      <p className="screen-eyebrow">
        계획 입력
      </p>

      <h2 className="chat-page-heading">
        어떤 행사를 준비하고 있나요?
      </h2>

      <p className="screen-description">
        행사에 대해 편하게 이야기해주세요.
        GreenMate가 필요한 정보를 하나씩 정리할게요.
      </p>


      <div className="chat-layout">
        <div className="chat-card">
          <div className="messages">
            {conversation.length === 0 && (
              <p className="bubble assistant">
                안녕하세요! 준비 중인 행사에 대해
                자유롭게 알려주세요.
                예를 들어 "30명이 가평으로 MT를 가려고 해요."
                처럼 입력할 수 있어요.
              </p>
            )}

            {conversation.map(
              (message, index) => (
                <p
                  key={`${message.role}-${index}`}
                  className={
                    message.role === "user"
                      ? "bubble user"
                      : "bubble assistant"
                  }
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


          <form
            className="message-form"
            onSubmit={handleSubmit}
          >
            <label
              htmlFor="chat-input"
              className="sr-only"
            >
              행사 계획 입력
            </label>

            <input
              id="chat-input"
              type="text"
              value={input}
              placeholder="행사 계획을 입력해주세요"
              disabled={isLoading}
              onChange={(event) =>
                setInput(event.target.value)
              }
            />

            <button
              type="submit"
              aria-label="메시지 보내기"
              disabled={
                isLoading
                || input.trim().length === 0
              }
            >
              ↑
            </button>
          </form>


          {error && (
            <p className="option-note">
              {error}
            </p>
          )}
        </div>


        <aside className="progress-card">
          <p>계획 진행 상황</p>

          <ol>
            {progressItems.map(
              (item, index) => {
                const stateClass =
                  getProgressClass(item.key);

                return (
                  <li
                    key={item.key}
                    className={stateClass}
                  >
                    <span>
                      {stateClass === "is-done"
                        ? "✓"
                        : index + 1}
                    </span>

                    {item.label}
                  </li>
                );
              },
            )}
          </ol>


          {isReadyToAnalyze && planDraft && (
            <button
              type="button"
              className="primary-button"
              onClick={() =>
                onAnalyzeReady(planDraft)
              }
            >
              계획 확인하기
              <span>→</span>
            </button>
          )}
        </aside>
      </div>
    </section>
  );
}


export default ChatPage;