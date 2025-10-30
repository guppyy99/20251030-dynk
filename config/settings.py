"""설정 파일 관리"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 네이버 API
    naver_client_id: str
    naver_client_secret: str
    
    # Google Gemini API
    gemini_api_key: str
    
    # 데이터베이스
    database_path: str = "data/trends.db"
    
    # Streamlit 설정
    streamlit_server_port: int = 8501
    streamlit_server_address: str = "0.0.0.0"
    
    # Railway 포트 (환경 변수에서 읽기)
    @property
    def port(self) -> int:
        """Railway에서 자동 할당된 포트 사용"""
        import os
        return int(os.environ.get("PORT", self.streamlit_server_port))
    
    # API Rate Limiting
    naver_api_rate_limit: int = 30  # 분당 호출 수
    gemini_api_rate_limit: int = 15  # 분당 호출 수
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 전역 설정 인스턴스
settings = Settings()

