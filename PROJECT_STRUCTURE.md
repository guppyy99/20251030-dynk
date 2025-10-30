# 한국 검색 트렌드 분석 대시보드 - 프로젝트 구조

```
.
├── config/                    # 설정 파일
│   ├── __init__.py
│   └── settings.py           # 환경 변수 및 설정 관리 (Pydantic)
│
├── src/                       # 소스 코드
│   ├── __init__.py
│   ├── database/             # 데이터베이스 관련
│   │   ├── __init__.py
│   │   └── init_db.py       # DuckDB 초기화 및 스키마 생성
│   │
│   ├── data/                 # 데이터 소스 통합
│   │   ├── __init__.py
│   │   ├── naver_api.py     # 네이버 데이터랩 API 클라이언트
│   │   └── gemini_api.py    # Google Gemini API 클라이언트 (키워드 확장)
│   │
│   ├── etl/                  # 데이터 수집 및 변환
│   │   ├── __init__.py
│   │   └── collect_trends.py # 트렌드 데이터 수집 ETL
│   │
│   ├── utils/                # 유틸리티 함수
│   │   ├── __init__.py
│   │   └── holidays.py      # 한국 공휴일 처리
│   │
│   └── dashboard/            # 대시보드 앱
│       ├── __init__.py
│       └── streamlit_app.py  # Streamlit 메인 앱
│
├── scripts/                   # 실행 스크립트
│   ├── __init__.py
│   └── collect_data.py       # 데이터 수집 스크립트
│
├── data/                      # 데이터 저장 디렉토리 (gitignore)
│   └── trends.db             # DuckDB 데이터베이스
│
├── requirements.txt           # Python 의존성
├── Dockerfile                # Docker 이미지 빌드 설정
├── railway.json              # Railway 배포 설정
├── .env.example              # 환경 변수 예제
├── .gitignore                # Git 제외 파일
├── README.md                 # 프로젝트 문서
├── RAILWAY_DEPLOY.md         # Railway 배포 가이드
└── prd.md                    # 제품 요구사항 문서

```

## 주요 컴포넌트 설명

### 1. 데이터 소스
- **네이버 데이터랩 API**: 검색 트렌드 데이터 수집 (무료, 일 1,000회)
- **Google Gemini API**: AI 기반 키워드 확장 (무료 티어)

### 2. 데이터 저장
- **DuckDB**: 고성능 분석용 데이터베이스
- 테이블: `search_trends`, `keyword_expansions`, `franchise_events`

### 3. 대시보드
- **Streamlit**: 웹 기반 대시보드
- 시계열 차트, 히트맵 달력, 통계 분석

### 4. 배포
- **Railway**: Docker 기반 자동 배포
- 환경 변수 기반 설정 관리

