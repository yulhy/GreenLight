import { useState } from "react";

import ChatPage from "./pages/ChatPage";
import type { PlanDraft } from "./types/plan";


type Screen =
  | "home"
  | "chat"
  | "summary"
  | "analysis"
  | "alternatives"
  | "saved";


function App() {
  const [currentScreen, setCurrentScreen] =
    useState<Screen>("home");

  const [confirmedPlan, setConfirmedPlan] =
    useState<PlanDraft | null>(null);


  function renderScreen() {
    switch (currentScreen) {
      case "chat":
        return (
          <ChatPage
            onAnalyzeReady={(plan) => {
              setConfirmedPlan(plan);
              setCurrentScreen("summary");
            }}
          />
        );

      case "summary":
        return (
          <section className="screen is-visible">
            <div className="content-narrow">
              <p className="screen-eyebrow">
                계획 확인
              </p>

              <h2>
                입력한 계획을 확인해주세요.
              </h2>

              <p className="screen-description">
                분석을 시작하기 전에 행사 정보를
                한 번 더 확인해주세요.
              </p>

              {!confirmedPlan ? (
                <p>
                  확인할 계획 정보가 없습니다.
                </p>
              ) : (
                <>
                  <dl className="summary-list">
                    <div>
                      <dt>행사 유형</dt>
                      <dd>
                        {confirmedPlan.activityType ?? "-"}
                      </dd>
                    </div>

                    <div>
                      <dt>목적지</dt>
                      <dd>
                        {confirmedPlan.destination ?? "-"}
                      </dd>
                    </div>

                    <div>
                      <dt>참가 인원</dt>
                      <dd>
                        {confirmedPlan.participantCount
                          ? `${confirmedPlan.participantCount}명`
                          : "-"}
                      </dd>
                    </div>

                    <div>
                      <dt>기간</dt>
                      <dd>
                        {confirmedPlan.durationDays
                          ? `${confirmedPlan.durationDays}일`
                          : "-"}
                      </dd>
                    </div>

                    <div>
                      <dt>이동수단</dt>
                      <dd>
                        {confirmedPlan.transport ?? "-"}
                      </dd>
                    </div>

                    <div>
                      <dt>왕복 거리</dt>
                      <dd>
                        {confirmedPlan.roundTripDistanceKm
                          ? `${confirmedPlan.roundTripDistanceKm}km`
                          : "-"}
                      </dd>
                    </div>

                    <div>
                      <dt>식사 계획</dt>
                      <dd>
                        {confirmedPlan.mealPlan ?? "-"}
                      </dd>
                    </div>

                    <div>
                      <dt>숙박 계획</dt>
                      <dd>
                        {confirmedPlan.lodgingPlan ?? "-"}
                      </dd>
                    </div>

                    <div>
                      <dt>소모품 계획</dt>
                      <dd>
                        {confirmedPlan.suppliesPlan ?? "-"}
                      </dd>
                    </div>

                    <div>
                      <dt>예산</dt>
                      <dd>
                        {confirmedPlan.budgetKrw
                          ? `${confirmedPlan.budgetKrw.toLocaleString()}원`
                          : "-"}
                      </dd>
                    </div>
                  </dl>

                  <div className="button-row">
                    <button
                      type="button"
                      className="secondary-button"
                      onClick={() =>
                        setCurrentScreen("chat")
                      }
                    >
                      수정하기
                    </button>

                    <button
                      type="button"
                      className="primary-button"
                      onClick={() =>
                        setCurrentScreen("analysis")
                      }
                    >
                      분석 시작
                      <span>→</span>
                    </button>
                  </div>
                </>
              )}
            </div>
          </section>
        );

      case "analysis":
        return (
          <section className="screen is-visible">
            <p className="screen-eyebrow">
              탄소 분석
            </p>

            <h2>
              탄소배출량을 분석합니다.
            </h2>
          </section>
        );

      case "alternatives":
        return (
          <section className="screen is-visible">
            <p className="screen-eyebrow">
              대안 비교
            </p>

            <h2>
              저탄소 대안을 비교합니다.
            </h2>
          </section>
        );

      case "saved":
        return (
          <section className="screen is-visible">
            <p className="screen-eyebrow">
              저장된 계획
            </p>

            <h2>
              저장된 계획을 확인하세요.
            </h2>
          </section>
        );

      case "chat":
        return (
          <ChatPage
            onAnalyzeReady={(plan) => {
              setConfirmedPlan(plan);
              setCurrentScreen("summary");
            }}
          />
        );

      case "home":
      default:
        return (
          <section className="screen is-visible">
            <div className="home-layout">
              <div className="home-copy">
                <div className="leaf-badge">
                  G
                </div>

                <p className="screen-eyebrow">
                  GreenMate
                </p>

                <h2>
                  행사 계획부터
                  <br />
                  친환경 대안까지
                </h2>

                <p className="screen-description">
                  AI와 대화하면서 행사 계획을 정리하고,
                  탄소배출량과 비용을 비교해 현실적인
                  저탄소 대안을 찾아보세요.
                </p>

                <button
                  type="button"
                  className="primary-button"
                  onClick={() =>
                    setCurrentScreen("chat")
                  }
                >
                  새 계획 시작하기
                  <span>→</span>
                </button>
              </div>
            </div>
          </section>
        );
    }
  }


  return (
    <>

      <main className="experience">
        <div className="app-shell">
          <aside className="sidebar">
            <div className="brand">
              <span className="brand-mark">○</span>
              <span>GreenMate</span>
            </div>

            <nav className="side-nav">
              <button
                className="side-link"
                onClick={() => setCurrentScreen("home")}
              >
                홈
              </button>

              <button
                className="side-link"
                onClick={() => setCurrentScreen("chat")}
              >
                새 계획
              </button>

              <button
                className="side-link"
                onClick={() => setCurrentScreen("saved")}
              >
                저장된 계획
              </button>
            </nav>

            <p className="side-quote">
              더 나은 선택으로
              <br />
              더 가벼운 발자국을.
            </p>
          </aside>

          <section className="workspace">
            <header className="workspace-header">
              <p>
                친환경 단체활동 계획 도우미
              </p>
            </header>

            <div className="screen-container">
              {renderScreen()}
            </div>
          </section>
        </div>
      </main>
    </>
  );
}


export default App;