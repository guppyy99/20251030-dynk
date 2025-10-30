FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 데이터 디렉토리 생성
RUN mkdir -p data

# 포트 노출 (Railway가 자동으로 할당)
EXPOSE 8501

# Streamlit 실행 (Railway PORT 환경 변수 사용)
CMD python -m streamlit run src/dashboard/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true

