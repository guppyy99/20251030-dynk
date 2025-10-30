# 한국 검색 트렌드 분석 대시보드

네이버 데이터랩 API와 Google Gemini API를 활용한 무료 검색 트렌드 분석 대시보드입니다.

## 주요 기능

- 📊 네이버 데이터랩 API 기반 검색 트렌드 분석
- 🔍 Google Gemini API를 활용한 키워드 확장
- 📅 연간 히트맵 달력 시각화
- 🗓️ 한국 공휴일 데이터 통합
- 🚀 Railway를 통한 간편한 배포

## 기술 스택

- **Backend**: Python 3.11
- **Database**: DuckDB
- **Dashboard**: Streamlit
- **Visualization**: Plotly, plotly-calplot
- **API**: 네이버 데이터랩 API, Google Gemini API
- **Deployment**: Railway

## 설치 및 설정

### 1. 저장소 클론

```bash
git clone <repository-url>
cd 20251030-dynk
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.env.example`을 참고하여 `.env` 파일을 생성하세요:

```bash
cp .env.example .env
```

`.env` 파일에 다음 정보를 입력:

```env
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret
GEMINI_API_KEY=your_gemini_api_key
DATABASE_PATH=data/trends.db
```

### 5. API 키 발급

#### 네이버 데이터랩 API
1. [developers.naver.com](https://developers.naver.com) 접속
2. 애플리케이션 등록
3. "데이터랩(검색어 트렌드)" API 선택
4. Client ID와 Client Secret 발급

#### Google Gemini API
1. [Google AI Studio](https://makersuite.google.com/app/apikey) 접속
2. API 키 생성 (무료 티어 사용 가능)

### 6. 데이터베이스 초기화

```bash
python -m src.database.init_db
```

### 7. 로컬 실행

```bash
streamlit run src/dashboard/streamlit_app.py
```

브라우저에서 http://localhost:8501 접속

## Railway 배포

### 1. Railway 계정 생성 및 프로젝트 생성

1. [Railway](https://railway.app) 접속 및 로그인
2. "New Project" 클릭
3. "Deploy from GitHub repo" 선택
4. GitHub 저장소 연결

### 2. 환경 변수 설정

Railway 대시보드에서 환경 변수 설정:

- `NAVER_CLIENT_ID`
- `NAVER_CLIENT_SECRET`
- `GEMINI_API_KEY`
- `DATABASE_PATH` (선택사항, 기본값: `data/trends.db`)

### 3. 자동 배포

GitHub에 푸시하면 Railway가 자동으로 빌드 및 배포합니다.

## 프로젝트 구조

```
.
├── config/
│   └── settings.py          # 설정 관리
├── src/
│   ├── database/
│   │   └── init_db.py       # 데이터베이스 초기화
│   ├── data/
│   │   ├── naver_api.py     # 네이버 API 클라이언트
│   │   └── gemini_api.py    # Gemini API 클라이언트
│   ├── etl/
│   │   └── collect_trends.py # 데이터 수집 ETL
│   ├── utils/
│   │   └── holidays.py      # 공휴일 유틸리티
│   └── dashboard/
│       └── streamlit_app.py # Streamlit 대시보드
├── scripts/
│   └── collect_data.py      # 데이터 수집 스크립트
├── data/                    # 데이터 저장 디렉토리
├── requirements.txt         # Python 의존성
├── Dockerfile              # Docker 설정
├── railway.json            # Railway 설정
└── README.md               # 프로젝트 문서
```

## 사용 방법

### 데이터 수집

1. 대시보드 사이드바에서 "데이터 수집" 섹션 사용
2. 또는 스크립트 실행:
```bash
python scripts/collect_data.py
```

### 키워드 확장

1. 사이드바에서 "키워드 확장" 섹션 사용
2. 시드 키워드 입력 후 "키워드 확장" 버튼 클릭
3. 생성된 키워드로 데이터 수집 가능

### 트렌드 분석

1. 사이드바에서 분석할 키워드 선택
2. 날짜 범위 설정
3. 시계열 차트, 히트맵, 통계 분석 탭에서 결과 확인

## 라이선스

MIT License

## 참고 자료

- [네이버 데이터랩 API 문서](https://developers.naver.com/docs/datalab/)
- [Google Gemini API 문서](https://ai.google.dev/docs)
- [Streamlit 문서](https://docs.streamlit.io)
- [Railway 문서](https://docs.railway.app)

