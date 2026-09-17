import type {
  PlanAnalysisResponse,
  PlanDraft,
} from "../types/plan";


interface ResultPageProps {
  plan: PlanDraft;
  result: PlanAnalysisResponse | null;
  isLoading?: boolean;
  error?: string | null;

  onBack: () => void;
  onNext: () => void;
}


function formatCarbon(
  value: number | null,
): string {
  if (value === null) {
    return "데이터 준비 중";
  }

  return `${value.toFixed(1)} kgCO₂e`;
}


function formatPercent(
  value: number | null,
): string {
  if (value === null) {
    return "-";
  }

  return `${value.toFixed(1)}%`;
}


function ResultPage({
  plan,
  result,
  isLoading = false,
  error = null,
  onBack,
  onNext,
}: ResultPageProps) {
  if (isLoading) {
    return (
      <section>
        <h1>
          현재 계획을 분석하고 있어요
        </h1>

        <p className="context">
          탄소배출량과 예상 비용을 계산하고 있습니다.
        </p>
      </section>
    );
  }


  if (error) {
    return (
      <section>
        <h1>
          분석 중 문제가 발생했어요
        </h1>

        <p className="error">
          {error}
        </p>

        <div className="actions">
          <button
            type="button"
            className="secondary back"
            onClick={onBack}
          >
            이전
          </button>
        </div>
      </section>
    );
  }


  return (
    <section>
      <h1>
        현재 계획의 예상 결과
      </h1>

      <p className="context">
        {plan.destination
          ? `${plan.destination}에서 진행하는 `
          : ""}

        {plan.activityType ?? "행사"} 계획을 기준으로
        예상 결과를 확인해보세요.
      </p>


      <div className="metrics">
        <div>
          <p>
            예상 탄소배출량
          </p>

          <strong>
            {result
              ? formatCarbon(
                  result.currentPlan
                    .totalCarbonKgCo2e,
                )
              : "-"}
          </strong>
        </div>


        <div>
          <p>
            예상 총비용
          </p>

          <strong>
            {result
              ? result.currentPlan.totalCostKrw
                  .toLocaleString()
              : "-"}

            {result && (
              <small>
                원
              </small>
            )}
          </strong>
        </div>
      </div>


      {result?.currentPlan.totalCarbonKgCo2e === null ? (
        <div className="notice">
          탄소배출계수 데이터가 아직 연결되지 않아
          현재는 비용 중심으로 결과를 표시합니다.
        </div>
      ) : result?.hotspots.length ? (
        <div className="notice">
          가장 큰 탄소 배출 항목은{" "}
          <strong>
            {result.hotspots.join(", ")}
          </strong>
          입니다. 이 항목을 중심으로 대안을 찾아볼게요.
        </div>
      ) : (
        <div className="notice">
          현재 계획의 주요 탄소 배출 항목을 분석합니다.
        </div>
      )}


      <details className="breakdown">
        <summary>
          카테고리별 상세 내역 보기
        </summary>

        <dl>
          {result?.currentPlan.breakdown.length ? (
            result.currentPlan.breakdown.map(
              (item) => (
                <div key={item.category}>
                  <dt>
                    {item.category}
                  </dt>

                  <dd>
                    {formatCarbon(
                      item.carbonKgCo2e,
                    )}
                    {" "}
                    (
                    {formatPercent(
                      item.sharePercent,
                    )}
                    )
                  </dd>
                </div>
              ),
            )
          ) : (
            <div>
              <dt>
                분석 데이터
              </dt>

              <dd>
                아직 없음
              </dd>
            </div>
          )}
        </dl>
      </details>


      <details className="edit-details">
        <summary>
          입력한 계획 확인
        </summary>

        <dl>
          <div>
            <dt>
              행사 유형
            </dt>

            <dd>
              {plan.activityType ?? "-"}
            </dd>
          </div>

          <div>
            <dt>
              목적지
            </dt>

            <dd>
              {plan.destination ?? "-"}
            </dd>
          </div>

          <div>
            <dt>
              참가 인원
            </dt>

            <dd>
              {plan.participantCount
                ? `${plan.participantCount}명`
                : "-"}
            </dd>
          </div>

          <div>
            <dt>
              행사 기간
            </dt>

            <dd>
              {plan.durationDays
                ? `${plan.durationDays}일`
                : "-"}
            </dd>
          </div>

          <div>
            <dt>
              이동수단
            </dt>

            <dd>
              {plan.transport ?? "-"}
            </dd>
          </div>

          <div>
            <dt>
              왕복 거리
            </dt>

            <dd>
              {plan.roundTripDistanceKm != null
                ? `${plan.roundTripDistanceKm}km`
                : "-"}
            </dd>
          </div>

          <div>
            <dt>
              식사 계획
            </dt>

            <dd>
              {plan.mealPlan ?? "-"}
            </dd>
          </div>

          <div>
            <dt>
              숙박 계획
            </dt>

            <dd>
              {plan.lodgingPlan ?? "-"}
            </dd>
          </div>

          <div>
            <dt>
              물품·소모품
            </dt>

            <dd>
              {plan.suppliesPlan ?? "-"}
            </dd>
          </div>

          <div>
            <dt>
              예산
            </dt>

            <dd>
              {plan.budgetKrw != null
                ? `${plan.budgetKrw.toLocaleString()}원`
                : "-"}
            </dd>
          </div>
        </dl>
      </details>


      {result?.recommendationReason && (
        <p className="small">
          {result.recommendationReason}
        </p>
      )}


      {result?.disclaimer && (
        <p className="small">
          {result.disclaimer}
        </p>
      )}


      <div className="actions">
        <button
          type="button"
          className="secondary back"
          onClick={onBack}
        >
          이전
        </button>

        <button
          type="button"
          className="primary"
          onClick={onNext}
          disabled={
            !result
            || result.alternatives.length === 0
          }
        >
          대안 비교하기
          <span>
            →
          </span>
        </button>
      </div>
    </section>
  );
}


export default ResultPage;