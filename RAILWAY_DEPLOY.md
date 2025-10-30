# Railway 배포 가이드

## 빠른 시작

### 1. GitHub 저장소 생성 및 푸시

```bash
git init
git add .
git commit -m "Initial commit: 한국 검색 트렌드 분석 대시보드"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Railway에서 프로젝트 생성

1. [Railway](https://railway.app) 접속 및 로그인
2. "New Project" 클릭
3. "Deploy from GitHub repo" 선택
4. GitHub 저장소 선택

### 3. 환경 변수 설정

Railway 대시보드에서 다음 환경 변수를 설정하세요:

- `NAVER_CLIENT_ID`: 네이버 데이터랩 API Client ID
- `NAVER_CLIENT_SECRET`: 네이버 데이터랩 API Client Secret
- `GEMINI_API_KEY`: Google Gemini API 키
- `DATABASE_PATH`: `data/trends.db` (기본값)

### 4. 배포 확인

Railway가 자동으로 빌드 및 배포합니다. 배포 완료 후 생성된 URL로 접속하세요.

## 트러블슈팅

### 포트 관련 문제

Railway는 `PORT` 환경 변수를 자동으로 할당합니다. Dockerfile과 railway.json에서 이를 사용하도록 설정되어 있습니다.

### 데이터베이스 경로

Railway의 파일 시스템은 일시적입니다. 영구 저장이 필요한 경우:
- Railway Volume을 사용하거나
- 외부 데이터베이스(Railway PostgreSQL 등)를 사용하세요

### 로그 확인

Railway 대시보드의 "Logs" 탭에서 애플리케이션 로그를 확인할 수 있습니다.

