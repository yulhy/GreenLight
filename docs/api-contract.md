
# GreenMate API 계약서

## 1. 공통 규칙

### Base URL

```text
http://localhost:8000
```

### Content-Type

```text
application/json
```

### 공통 오류 응답

```json
{
  "detail": "오류 설명"
}
```

## 2. GET /api/health

### 목적

서버 상태 확인.

### 응답 예시

```json
{
  "status": "ok"
}
```

## 3. POST /api/chat

### 목적

사용자와 AI의 대화를 처리하고
행사 계획 초안을 구조화한다.

### Request example

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

### 필드 정의

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| conversation | array | YES | 대화 메시지 목록 |
| conversation[].role | string | YES | user 또는 assistant |
| conversation[].content | string | YES | 메시지 내용 |
| currentPlan | object/null | NO | 현재까지 구조화된 계획 |

### Response example

```json
{
  "assistantMessage": "왕복 이동거리와 현재 계획한 이동수단을 알려주세요.",
  "missingFields": [
    "roundTripDistanceKm",
    "transport"
  ],
  "planDraft": {
    "activityType": "MT",
    "destination": "가평",
    "participantCount": 30
  },
  "isReadyToAnalyze": false
}
```

### 동작 규칙

- 누락 필드가 있으면 질문한다.
- 정보가 충분하면 isReadyToAnalyze를 true로 설정할 수 있다.
- 계획 초안은 사용자가 확인할 수 있어야 한다.
- AI가 추정한 값은 사용자 입력값과 구분한다.

## 4. POST /api/plans/analyze

### 목적

행사 계획의 현재안과 저탄소 대안을 분석한다.

### Request example

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
    {
      "category": "transport",
      "itemId": "van",
      "quantity": 3
    },
    {
      "category": "food",
      "itemId": "beef_meal",
      "quantity": 60
    },
    {
      "category": "lodging",
      "itemId": "pension",
      "quantity": 30
    },
    {
      "category": "tableware",
      "itemId": "disposable",
      "quantity": 60
    }
  ]
}
```

### Response example

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
  "hotspots": [
    "transport",
    "food"
  ],
  "alternatives": [
    {
      "id": "A",
      "name": "최소 변경안",
      "changedCategories": [
        "transport"
      ],
      "totalCarbonKgCo2e": 340.0,
      "totalCostKrw": 2850000,
      "carbonReductionPercent": 19.1,
      "costDifferenceKrw": 50000,
      "constraintsSatisfied": true
    }
  ],
  "recommendedAlternativeId": "B",
  "recommendationReason": "예산 조건과 이동 편의성을 고려한 대안입니다.",
  "disclaimer": "결과는 입력값과 등록된 배출계수에 기반한 추정치입니다."
}
```

## 5. GET /api/catalog/categories

### 목적

지원하는 카테고리 목록 조회.

### 응답 예시

```json
{
  "categories": [
    "transport",
    "food",
    "lodging",
    "tableware"
  ]
}
```

## 6. GET /api/catalog/items

### Query Parameters

| 파라미터 | 타입 | 설명 |
|---|---|---|
| category | string | 조회할 카테고리 |

### 응답 규칙

- 등록된 카탈로그 항목만 반환한다.
- 존재하지 않는 카테고리는 오류 처리한다.
- 각 항목의 ID는 고유해야 한다.

## 7. API 변경 규칙

- 기존 필드명을 임의로 변경하지 않는다.
- 필드를 변경하면 이 문서를 먼저 수정한다.
- 프론트엔드 타입과 백엔드 스키마를 함께 수정한다.
- Breaking Change는 팀원에게 공유한다.
- 응답에 새로운 필드를 추가할 때 기존 클라이언트가 깨지지 않는지 확인한다.
