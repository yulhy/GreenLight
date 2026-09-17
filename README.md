# GreenMate MVP

GreenMate는 MT, OT 등 소규모 단체활동 계획을 AI와의 자연어 대화로 수집하고, 현재 계획의 탄소배출량과 비용을 계산하여 현실적으로 실행 가능한 저탄소 대안을 추천하는 서비스다.

이번 24시간 오프라인 해커톤 MVP는 **단체 이동형 활동(MT/OT)** 하나의 시나리오를 처음부터 끝까지 실제로 작동시키는 데 집중한다. 권장 시연은 **학생 30명의 가평 1박 2일 MT**이다.

## MVP 목표와 원칙

1. AI 대화로 활동계획을 수집하고 구조화한다.
2. Python 계산 모듈이 CSV 데이터에서 탄소배출량과 비용을 계산한다.
3. Hotspot을 찾아 동일 카테고리 내의 대안을 탐색한다.
4. Python 규칙으로 예산, 인원, 거리, 접근성, 변경 불가 조건을 검증한다.
5. 조건을 통과한 대안 A/B/C를 비교하고 LLM이 최종 추천 이유를 설명한다.

탄소배출량과 비용 수치는 LLM이 만들지 않는다. LLM은 대화, 정보 추출, 누락 정보 질문, 정성적 선호 해석, 추천 이유 설명만 맡는다. 수치 계산과 명확한 제약조건 검증은 Python이 담당한다.

## MVP 범위

### 지원 활동

- 우선 지원: 대학 MT, OT 등 단체 이동형 활동
- 확장 가능한 활동: 체험학습, 야유회, 축제 부스

### 계산 카테고리

- 이동수단: 승합차, 전세버스, 기차, 시외버스
- 식사: 소고기, 돼지고기, 닭고기, 저탄소 식단
- 숙박: 시연에 필요한 최소 숙박 선택지
- 소모품: 일회용 식기, 다회용 식기

### 계산 및 추천 규칙

- Hotspot은 배출량 상위 2개 카테고리를 기본으로 선정한다.
- 3위 카테고리의 배출 비중이 전체의 10% 이상이면 Hotspot에 포함한다.
- 현재 선택과 같은 항목은 대안 후보에서 제외한다.
- 후보는 수용 인원, 이동 가능 거리, 목적지 접근성, 예산, 사용자 제외 항목을 통과해야 한다.
- 결과는 입력값과 등록된 배출계수에 기반한 추정치임을 화면에 표시한다.

## 심사 피드백 반영

- 데이터셋을 무작정 넓히기보다, 가평 MT 시나리오에서 신뢰도 있게 작동하는 최소 항목을 구축한다.
- 탄소배출계수와 비용 데이터는 출처, 기준연도, 계산 단위, 가정을 함께 기록한다.
- 범용 채팅 AI와의 차별점은 계산과 규칙 검증이 분리된 의사결정 파이프라인이라는 점이다.
- 현재안, 대안 A/B/C, 감축률, 비용 차이, 조건 충족 여부를 같은 화면에서 비교한다.

## 프로젝트 구조

| 구분 | 기술 | 역할 |
| --- | --- | --- |
| Frontend | React, TypeScript, Vite | 대화와 결과 비교 화면 |
| Styling | Tailwind CSS | 빠르고 일관된 반응형 UI |
| Backend | Python, FastAPI | LLM 연동 및 계산 API |
| Data processing | Pandas | CSV 데이터 조회와 처리 |
| Validation | Pydantic | API와 활동계획 데이터 검증 |
| AI | LLM API | 대화, 정보 구조화, 추천 이유 생성 |
| Data | CSV | 탄소배출계수, 비용, 조건 관리 |
| Charts | Recharts | 배출 비중 및 대안 비교 시각화 |
| Testing | Pytest | 계산과 규칙 필터 테스트 |
| Development | Git, GitHub, VS Code, dotenv | 협업, 버전관리, 환경변수 관리 |

## 디렉터리 구조

```text
greenmate/
├─ frontend/
│  ├─ src/
│  │  ├─ components/
│  │  │  ├─ .gitkeep
│  │  │  ├─ ChatMessage.tsx
│  │  │  ├─ ComparisonTable.tsx
│  │  │  ├─ EmissionChart.tsx
│  │  │  └─ PlanSummary.tsx
│  │  ├─ pages/
│  │  │  ├─ .gitkeep
│  │  │  ├─ ChatPage.tsx
│  │  │  └─ ResultPage.tsx
│  │  ├─ hooks/
│  │  │  ├─ .gitkeep
│  │  │  └─ hook.ts
│  │  ├─ services/
│  │  │  ├─ .gitkeep
│  │  │  └─ api.ts
│  │  ├─ types/
│  │  │  ├─ .gitkeep
│  │  │  └─ plan.ts
│  │  ├─ utils/
│  │  │  └─.gitkeep
│  │  ├─ App.tsx
│  │  └─ main.tsx
│  ├─ public/
│  │  └─ .gitkeep
│  ├─ package.json
│  └─ vite.config.ts
├─ backend/
│  ├─ app/
│  │  ├─ api/
│  │  ├─ __init__.py
│  │  ├─ routes
│  │  │  ├─ __init__.py
│  │  │  ├─ .gitkeep
│  │  │  ├─ chat.py
│  │  │  └─ plans.py
│  │  ├─ core/
│  │  │  ├─ __init__.py
│  │  │  └─ .gitkeep
│  │  ├─ models/
│  │  │  ├─ __init__.py
│  │  │  └─ .gitkeep
│  │  ├─ schemas/
│  │  │  ├─ __init__.py
│  │  │  ├─ plan.py
│  │  │  └─ .gitkeep
│  │  ├─ services/
│  │  │  ├─ __init__.py
│  │  │  ├─ analyzer.py
│  │  │  ├─ calculator.py
│  │  │  ├─ llm_service.py
│  │  │  ├─ recommendation_service.py
│  │  │  └─ .gitkeep
│  │  ├─ rules/
│  │  │  ├─ __init__.py
│  │  │  ├─ feasibility.py
│  │  │  └─ .gitkeep
│  │  ├─ repositories/
│  │  │  ├─ .gitkeep
│  │  │  ├─ catalog_repository.py
│  │  │  └─ __init__.py
│  │  ├─ data/
│  │  │  ├─ .gitkeep
│  │  │  └─ catalog.csv
│  │  ├─ __init__.py
│  │  └─ main.py
│  ├─ tests/
│  │  ├─ __init__.py
│  │  ├─ .gitkeep
│  │  ├─ test_calculator.py
│  │  └─ test_feasibility.py
│  ├─ requirements.txt
│  └─ .env.example
├─ docs/
│  ├─ data-sources.md
│  ├─ ai-behavior.md
│  ├─ api-contract.md
│  ├─ architecture.md
│  ├─ bussiness-rules.md
│  ├─ data-dictionary.md
│  ├─ decisions.md
│  ├─ project-overview.md
│  ├─ requirements.md
│  ├─ testing.md
│  ├─ ui-flow.md
│  └─ demo-scenario.md
├─ .gitignore
├─ Agents.md
└─ README.md
```

## 계층 역할

| 경로 | 역할 |
| --- | --- |
| `frontend/src/pages/ChatPage.tsx` | 사용자 계획 입력과 AI 대화 흐름을 제공한다. |
| `frontend/src/pages/ResultPage.tsx` | 현재안, Hotspot, 대안, 최종 추천을 보여준다. |
| `frontend/src/components/ChatMessage.tsx` | 사용자와 AI의 대화 메시지를 표시한다. |
| `frontend/src/components/PlanSummary.tsx` | 구조화된 활동계획을 확인시킨다. |
| `frontend/src/components/ComparisonTable.tsx` | 현재안과 대안의 탄소, 비용, 감축률을 비교한다. |
| `frontend/src/components/EmissionChart.tsx` | 카테고리별 탄소배출 비중을 시각화한다. |
| `frontend/src/services/api.ts` | FastAPI 서버와의 HTTP 통신을 관리한다. |
| `frontend/src/types/plan.ts` | 활동계획과 분석 결과 타입을 정의한다. |
| `backend/app/main.py` | FastAPI 앱과 라우터를 등록한다. |
| `backend/app/api/routes/chat.py` | AI 대화와 구조화 API를 제공한다. |
| `backend/app/api/routes/plans.py` | 계획 분석과 추천 API를 제공한다. |
| `backend/app/schemas/plan.py` | 요청과 응답 데이터 모델을 정의한다. |
| `backend/app/services/llm_service.py` | LLM 호출, 누락 정보 질문, 구조화, 추천 설명을 담당한다. |
| `backend/app/services/calculator.py` | 탄소배출량과 비용을 계산한다. |
| `backend/app/services/analyzer.py` | 배출 비중과 Hotspot을 분석한다. |
| `backend/app/services/recommendation_service.py` | 대안 구성과 최종 추천 흐름을 조정한다. |
| `backend/app/rules/feasibility.py` | 인원, 거리, 예산, 접근성, 불가 조건을 검증한다. |
| `backend/app/repositories/catalog_repository.py` | CSV 카탈로그를 조회한다. |
| `backend/app/data/catalog.csv` | 탄소배출계수, 비용, 단위, 조건 데이터다. |
| `backend/tests/` | 계산과 후보 필터링을 검증한다. |
| `docs/data-sources.md` | 데이터 출처와 기준연도를 기록한다. |
| `docs/demo-scenario.md` | 해커톤 시연 입력과 기대 결과를 기록한다. |

## 환경 변수

| 환경 변수 | 예시 | 역할 |
| --- | --- | --- |
| `OPENAI_API_KEY` | `sk-...` | LLM API 인증 키 |
| `OPENAI_MODEL` | `gpt-5-mini` | 대화와 구조화, 추천 설명에 사용할 모델 |
| `BACKEND_HOST` | `0.0.0.0` | FastAPI 실행 호스트 |
| `BACKEND_PORT` | `8000` | FastAPI 실행 포트 |
| `FRONTEND_ORIGIN` | `http://localhost:5173` | CORS 허용 프론트엔드 주소 |
| `CATALOG_CSV_PATH` | `app/data/catalog.csv` | 탄소·비용 CSV 경로 |
| `APP_ENV` | `development` | 개발·배포 환경 구분 |
| `LOG_LEVEL` | `INFO` | 서버 로그 수준 |

`.env` 파일은 Git에 올리지 않고, `.env.example`에는 변수명만 제공한다.

## HTTP API

| 메서드 | 경로 | 설명 |
| --- | --- | --- |
| `GET` | `/api/health` | 서버 상태를 확인한다. |
| `POST` | `/api/chat` | AI 응답, 누락 정보, 구조화된 계획 초안을 반환한다. |
| `POST` | `/api/plans/analyze` | 현재안, Hotspot, 대안 A/B/C, 최종 추천을 계산한다. |
| `GET` | `/api/catalog/categories` | 지원 카테고리와 항목 목록을 조회한다. |
| `GET` | `/api/catalog/items` | 카테고리별 선택 가능 항목을 조회한다. |

## 요청 본문

### `POST /api/chat`

```json
{
  "conversation": [
    {
      "role": "user",
      "content": "학과 학생 30명이 가평으로 MT를 가려고 해요."
    }
  ],
  "currentPlan": {
    "activityType": "MT",
    "participantCount": 30
  }
}
```

### `POST /api/plans/analyze`

```json
{
  "activityType": "MT",
  "destination": "가평",
  "participantCount": 30,
  "roundTripDistanceKm": 200,
  "budgetKrw": 3000000,
  "preferences": {
    "maxAdditionalCostKrw": 50000,
    "avoidItems": ["기차"],
    "priority": "convenience"
  },
  "selections": [
    { "category": "transport", "itemId": "van", "quantity": 3 },
    { "category": "food", "itemId": "beef_meal", "quantity": 60 },
    { "category": "lodging", "itemId": "pension", "quantity": 30 },
    { "category": "tableware", "itemId": "disposable", "quantity": 60 }
  ]
}
```

## 응답

### `POST /api/chat`

```json
{
  "assistantMessage": "왕복 이동거리와 현재 계획한 이동수단을 알려주세요.",
  "missingFields": ["roundTripDistanceKm", "transport"],
  "planDraft": {
    "activityType": "MT",
    "destination": "가평",
    "participantCount": 30
  },
  "isReadyToAnalyze": false
}
```

### `POST /api/plans/analyze`

```json
{
  "currentPlan": {
    "totalCarbonKgCo2e": 420.5,
    "totalCostKrw": 2800000,
    "breakdown": [
      {
        "category": "transport",
        "carbonKgCo2e": 210.2,
        "sharePercent": 50.0
      }
    ]
  },
  "hotspots": ["transport", "food"],
  "alternatives": [
    {
      "id": "A",
      "name": "최소 변경안",
      "changedCategories": ["transport"],
      "totalCarbonKgCo2e": 340.0,
      "totalCostKrw": 2850000,
      "carbonReductionPercent": 19.1,
      "costDifferenceKrw": 50000,
      "constraintsSatisfied": true
    }
  ],
  "recommendedAlternativeId": "B",
  "recommendationReason": "대안 B는 예산 조건을 만족하면서 탄소배출량을 줄이고 이동 편의성도 유지합니다.",
  "disclaimer": "결과는 입력값과 등록된 배출계수에 기반한 추정치입니다."
}
```

## 데이터셋 기준

`catalog.csv`의 각 항목은 아래 정보를 포함한다.

| 필드 | 역할 |
| --- | --- |
| `category` | 항목 카테고리 |
| `item_id` | 코드에서 사용할 고유 식별자 |
| `item_name` | 화면에 표시할 항목명 |
| `carbon_factor` | 탄소배출계수 |
| `unit` | 계산 단위 |
| `reference_cost_krw` | 참고 비용 |
| `capacity_or_condition` | 수용 인원 또는 적용 조건 |
| `source` | 데이터 출처명 |
| `source_url` | 원문 링크 |
| `reference_year` | 기준연도 |
| `assumption` | 계산에 사용한 가정 |

## 실행

### 사전 준비

- Node.js 20 이상
- Python 3.11 이상
- LLM API 키
- 탄소·비용 데이터 CSV

### 백엔드 실행

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

### 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

브라우저에서 `http://localhost:5173`으로 접속한다.

## 해커톤 시연 흐름

1. 사용자가 학생 30명의 가평 1박 2일 MT 계획을 입력한다.
2. AI가 이동수단, 거리, 식사, 숙박, 소모품, 예산, 불가 조건을 질문한다.
3. 사용자가 구조화된 계획을 확인하고 분석을 실행한다.
4. 현재안의 총 탄소배출량, 비용, Hotspot을 확인한다.
5. 대안 A/B/C의 탄소감축률, 비용 차이, 조건 충족 여부를 비교한다.
6. AI가 가장 현실적인 대안과 추천 이유를 제시한다.

## MVP에서 제외하는 항목

- 로그인, 회원가입, 활동계획 저장
- 실시간 지도, 교통, 숙박 가격 API 연동
- 예약과 결제
- 모든 활동 유형과 세부 탄소 항목 지원
- 누적 탄소감축 대시보드
- 사용자 채택 이력을 활용한 개인화 추천
