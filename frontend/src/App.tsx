import { useState } from "react";

import ChatPage from "./pages/ChatPage";
import ResultPage from "./pages/ResultPage";

import { useAnalysis } from "./hooks/useAnalysis";

import type { PlanDraft } from "./types/plan";


type Step =
  | "input"
  | "result"
  | "alternative"
  | "final";


const steps = [
  {
    id: "input" as Step,
    label: "정보 입력",
  },
  {
    id: "result" as Step,
    label: "예상 결과",
  },
  {
    id: "alternative" as Step,
    label: "대안 선택",
  },
  {
    id: "final" as Step,
    label: "최종 결과",
  },
];


function App() {
  const [selectedAlternativeId, setSelectedAlternativeId] =
    useState<string | null>(null);

  const [currentStep, setCurrentStep] =
    useState<Step>("input");

  const [confirmedPlan, setConfirmedPlan] =
    useState<PlanDraft | null>(null);

  const [transportQuantity, setTransportQuantity] =
    useState(1);

  const [foodCountPerPerson, setFoodCountPerPerson] =
  useState(1);

  const [suppliesCount, setSuppliesCount] =
    useState(1);

  const {
    result: analysisResult,
    isLoading: isAnalyzing,
    error: analysisError,
    runAnalysis,
    resetAnalysis,
  } = useAnalysis();


  const currentStepIndex =
    steps.findIndex(
      (step) => step.id === currentStep,
    );


  async function handleAnalyzeReady(
    plan: PlanDraft,
  ) {
    setConfirmedPlan(plan);
  }


  async function handleRunAnalysis() {
    if (!confirmedPlan) {
      return;
    }

    const result = await runAnalysis(
      confirmedPlan,
      {
        vehicleCount:
          transportQuantity,

        foodCountPerPerson,

        suppliesCount,
      },
    );

    if (result) {
      setCurrentStep("result");
    }
  }


  function handleStartOver() {
    setConfirmedPlan(null);
    setTransportQuantity(1);
    resetAnalysis();
    setCurrentStep("input");
    setSelectedAlternativeId(null);
    setFoodCountPerPerson(1);
    setSuppliesCount(1);
  }


  function renderContent() {
    const selectedAlternative =
      analysisResult?.alternatives.find(
        (alternative) =>
          alternative.id === selectedAlternativeId,
      ) ?? null;
    /*
     * Chat에서 필수 정보 수집이 끝났지만
     * 아직 분석을 실행하지 않은 상태
     */
    if (
      currentStep === "input"
      && confirmedPlan
    ) {
      return (
        <section>
          <h1>
            계획을 분석하기 전에 확인해 주세요
          </h1>

          <p className="context">
            입력한 계획을 기준으로 탄소배출량과
            예상 비용을 계산합니다.
          </p>


          <div className="notice">
            <strong>
              {confirmedPlan.activityType ?? "행사"}
            </strong>

            {confirmedPlan.destination && (
              <>
                {" · "}
                {confirmedPlan.destination}
              </>
            )}

            {confirmedPlan.participantCount && (
              <>
                {" · "}
                {confirmedPlan.participantCount}명
              </>
            )}
          </div>


          <div className="budget-row">
            <label htmlFor="transport-quantity">
              이동수단 수량
            </label>

            <div className="money-input">
              <input
                id="transport-quantity"
                type="number"
                min="1"
                step="1"
                value={transportQuantity}
                disabled={isAnalyzing}
                onChange={(event) => {
                  const value =
                    Number(event.target.value);

                  setTransportQuantity(
                    Number.isFinite(value)
                      ? value
                      : 1,
                  );
                }}
              />

              <span>
                대
              </span>
            </div>
          </div>
          <div className="budget-row">
            <label htmlFor="food-count">
              1인당 식사/제공 횟수
            </label>

            <div className="money-input">
              <input
                id="food-count"
                type="number"
                min="1"
                step="1"
                value={foodCountPerPerson}
                disabled={isAnalyzing}
                onChange={(event) => {
                  const value =
                    Number(event.target.value);

                  setFoodCountPerPerson(
                    Number.isFinite(value)
                      ? value
                      : 1,
                  );
                }}
              />

              <span>
                회
              </span>
            </div>
          </div>
          {confirmedPlan.suppliesPlan && (
            <div className="budget-row">
              <label htmlFor="supplies-count">
                물품·소모품 수량
              </label>

              <div className="money-input">
                <input
                  id="supplies-count"
                  type="number"
                  min="1"
                  step="1"
                  value={suppliesCount}
                  disabled={isAnalyzing}
                  onChange={(event) => {
                    const value =
                      Number(event.target.value);

                    setSuppliesCount(
                      Number.isFinite(value)
                        ? value
                        : 1,
                    );
                  }}
                />

                <span>
                  개
                </span>
              </div>
            </div>
          )}
          <p className="small">
            현재 이동수단의 수량을 입력해 주세요.
            식사·숙박·식기 수량은 참가 인원과
            행사 기간을 기준으로 계산합니다.
          </p>


          {analysisError && (
            <p className="error">
              {analysisError}
            </p>
          )}


          <div className="actions">
            <button
              type="button"
              className="secondary back"
              disabled={isAnalyzing}
              onClick={() => {
                setConfirmedPlan(null);
                resetAnalysis();
              }}
            >
              계획 수정
            </button>

            <button
              type="button"
              className="primary"
              disabled={
                isAnalyzing
                || transportQuantity < 1
              }
              onClick={handleRunAnalysis}
            >
              {isAnalyzing
                ? "분석 중..."
                : "예상 결과 보기"}

              {!isAnalyzing && (
                <span>
                  →
                </span>
              )}
            </button>
          </div>
        </section>
      );
    }


    switch (currentStep) {
      case "input":
        return (
          <ChatPage
            onAnalyzeReady={
              handleAnalyzeReady
            }
          />
        );


      case "result":
        if (!confirmedPlan) {
          return (
            <section>
              <h1>
                계획 정보가 없습니다.
              </h1>

              <div className="actions">
                <button
                  type="button"
                  className="primary"
                  onClick={handleStartOver}
                >
                  계획 입력하기
                </button>
              </div>
            </section>
          );
        }

        return (
          <ResultPage
            plan={confirmedPlan}
            result={analysisResult}
            isLoading={isAnalyzing}
            error={analysisError}
            onBack={() =>
              setCurrentStep("input")
            }
            onNext={() =>
              setCurrentStep("alternative")
            }
          />
        );


      case "alternative":
        return (
          <section>
            <h1>
              어떤 대안을 선택할까요?
            </h1>

            <p className="context">
              현재 계획보다 탄소배출량을 줄일 수 있는
              대안을 비교해보세요.
            </p>


            {analysisResult?.alternatives.length ? (
              <div id="options">
                {analysisResult.alternatives.map(
                  (alternative) => (
                    <label
                      className="option"
                      key={alternative.id}
                    >
                      <input
                        type="radio"
                        name="alternative"
                        value={alternative.id}
                        checked={
                          selectedAlternativeId === alternative.id
                        }
                        onChange={() =>
                          setSelectedAlternativeId(alternative.id)
                        }
                      />

                      <span className="option-title">
                        {alternative.name}

                        <span className="option-desc">
                          변경 항목:{" "}
                          {alternative.changedCategories.join(
                            ", ",
                          )}
                        </span>
                      </span>

                      <span
                        className="change"
                        data-label="탄소 변화"
                      >
                        -
                        {alternative.carbonReductionPercent.toFixed(
                          1,
                        )}
                        %
                      </span>

                      <span
                        className={
                          alternative.costDifferenceKrw > 0
                            ? "change increase"
                            : "change"
                        }
                        data-label="비용 변화"
                      >
                        {alternative.costDifferenceKrw > 0
                          ? "+"
                          : ""}

                        {alternative.costDifferenceKrw.toLocaleString()}
                        원
                      </span>
                    </label>
                  ),
                )}
              </div>
            ) : (
              <div className="notice">
                비교할 수 있는 대안이 없습니다.
              </div>
            )}


            <div className="actions">
              <button
                type="button"
                className="secondary back"
                onClick={() =>
                  setCurrentStep("result")
                }
              >
                이전
              </button>

              <button
                type="button"
                className="primary"
                disabled={!selectedAlternativeId}
                onClick={() =>
                  setCurrentStep("final")
                }
              >
                선택한 대안으로 계속
                <span>
                  →
                </span>
              </button>
            </div>
          </section>
        );


      case "final":
        return (
          <section>
            <h1>
              더 가벼운 계획이 완성됐어요
            </h1>

            <p className="context">
              선택한 대안을 적용했을 때의
              예상 효과입니다.
            </p>


            <div className="impact">
              <div>
                <p>
                  탄소 절감
                </p>

                <strong>
                  {selectedAlternative
                    ? `${selectedAlternative.carbonReductionPercent.toFixed(1)}%`
                    : "-"}
                </strong>
              </div>

              <div className="extra-cost">
                <p>
                  비용 변화
                </p>

                <strong>
                  {selectedAlternative
                    ? `${selectedAlternative.costDifferenceKrw > 0 ? "+" : ""}${selectedAlternative.costDifferenceKrw.toLocaleString()}원`
                    : "-"}
                </strong>
              </div>
            </div>


            <div className="final-cost">
              <span>
                최종 예상 비용
              </span>

              <strong>
                {selectedAlternative
                  ? `${selectedAlternative.totalCostKrw.toLocaleString()}원`
                  : "-"}
              </strong>
            </div>


            <div className="actions">
              <button
                type="button"
                className="secondary back"
                onClick={() =>
                  setCurrentStep("alternative")
                }
              >
                대안 다시 보기
              </button>

              <button
                type="button"
                className="secondary"
                onClick={handleStartOver}
              >
                새 계획
              </button>

              <button
                type="button"
                className="primary"
              >
                계획 저장
              </button>
            </div>
          </section>
        );
    }
  }


  return (
    <div className="app">
      <a
        href="#main-content"
        className="skip"
      >
        본문으로 이동
      </a>


      <header>
        <a
          href="/"
          className="brand"
          onClick={(event) => {
            event.preventDefault();
            handleStartOver();
          }}
        >
          <span className="leaf">
            ◆
          </span>

          GreenMate
        </a>

        <button
          type="button"
          className="quiet"
        >
          내 기록
        </button>
      </header>


      <main id="main-content">
        <nav aria-label="진행 단계">
          <ol className="steps">
            {steps.map(
              (step, index) => {
                const isCurrent =
                  currentStep === step.id;

                const isDone =
                  index < currentStepIndex;

                return (
                  <li key={step.id}>
                    <button
                      type="button"
                      aria-current={
                        isCurrent
                          ? "step"
                          : undefined
                      }
                      className={
                        isDone
                          ? "done"
                          : undefined
                      }
                      disabled={
                        index > currentStepIndex
                      }
                      onClick={() => {
                        if (
                          index
                          <= currentStepIndex
                        ) {
                          setCurrentStep(
                            step.id,
                          );
                        }
                      }}
                    >
                      <span>
                        {index + 1}
                      </span>

                      {step.label}
                    </button>
                  </li>
                );
              },
            )}
          </ol>
        </nav>


        {renderContent()}


        <footer>
          <span>
            GreenMate
          </span>

          <span>
            · 모임의 더 나은 선택
          </span>
        </footer>
      </main>
    </div>
  );
}


export default App;