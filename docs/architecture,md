
# GreenMate 시스템 아키텍처

## 1. 전체 구조

```text
사용자
  |
  v
React Frontend
  |
  | HTTP / JSON
  v
FastAPI Backend
  |
  +--> Chat Service
  |      |
  |      v
  |    LLM API
  |
  +--> Plan Validation
  |
  +--> Calculator
  |      |
  |      v
  |    Catalog Repository
  |      |
  |      v
  |    catalog.csv
  |
  +--> Hotspot Analyzer
  |
  +--> Recommendation Service
  |
  v
분석 결과 JSON
  |
  v
React Result Page
```

## 2. 계층별 책임

### Frontend

담당:

- 사용자 입력
- AI 채팅 UI
- 계획 확인 화면
- 분석 실행
- 결과 비교 화면
- 차트와 표 렌더링

금지:

- 탄소배출량 직접 계산
- 비용 직접 계산
- API 키 보관
- 서버의 추천 규칙 재구현

### Backend API

담당:

- HTTP 요청 처리
- 요청 데이터 검증
- 서비스 호출
- 응답 데이터 직렬화
- 오류 처리

### LLM Service

담당:

- 자연어 대화
- 정보 추출
- 누락 정보 질문
- 사용자 선호 해석
- 추천 이유 설명

금지:

- 탄소배출량 임의 계산
- 비용 임의 생성
- 카탈로그에 없는 수치 생성

### Calculator

담당:

- 카탈로그 조회
- 카테고리별 탄소배출량 계산
- 카테고리별 비용 계산
- 전체 합계 계산

### Analyzer

담당:

- 카테고리별 배출량 분석
- 배출 비중 계산
- Hotspot 선정

### Recommendation Service

담당:

- Hotspot 기반 변경 대상 선정
- 후보 대안 조회
- 제약조건 검증
- 대안 A/B/C 구성
- 추천에 필요한 결과 조합

### Feasibility Rules

담당:

- 예산 검증
- 참가 인원 검증
- 수용 인원 검증
- 이동거리 검증
- 접근성 검증
- 사용자 제외 항목 검증

## 3. 의존성 규칙

- UI는 API를 통해서만 백엔드와 통신한다.
- API 라우터는 계산 세부 로직을 직접 구현하지 않는다.
- 계산 모듈은 LLM에 의존하지 않는다.
- 카탈로그 조회는 Repository를 통해 수행한다.
- 추천 서비스는 계산기와 규칙 검증 모듈을 사용한다.
- 데이터 출처 정보는 카탈로그와 함께 관리한다.

## 4. 데이터 흐름

### 계획 수집

1. 사용자가 자연어 입력
2. Frontend가 /api/chat 호출
3. LLM Service가 정보 추출
4. 누락 정보 확인
5. 구조화된 Plan 반환
6. Frontend가 계획 초안 표시

### 분석 실행

1. 사용자가 계획 확인
2. Frontend가 /api/plans/analyze 호출
3. Backend가 Plan 검증
4. Catalog Repository가 데이터 조회
5. Calculator가 현재안 계산
6. Analyzer가 Hotspot 분석
7. Recommendation Service가 대안 구성
8. Feasibility Rules가 후보 검증
9. LLM Service가 추천 이유 생성
10. 분석 결과 반환

## 5. 구현 시 주의사항

- 계산 모듈은 독립적으로 테스트 가능해야 한다.
- API 응답 스키마는 프론트엔드와 일치해야 한다.
- 모든 카테고리의 단위를 명확하게 정의한다.
- 데이터가 부족한 경우 오류 또는 확인 필요 상태를 반환한다.
- 실제 외부 API 연동은 MVP 범위에 포함하지 않는다.
