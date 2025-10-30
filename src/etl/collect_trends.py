"""검색 트렌드 데이터 수집 ETL"""
import duckdb
from datetime import datetime, timedelta
from loguru import logger
from pathlib import Path
from typing import List
import pandas as pd

from config.settings import settings
from src.data.naver_api import NaverDataLabClient
from src.database.init_db import init_database


class TrendCollector:
    """트렌드 데이터 수집기"""
    
    def __init__(self):
        self.api_client = NaverDataLabClient()
        self.db_path = settings.database_path
        init_database()
    
    def collect_keyword_trends(
        self,
        keywords: List[str],
        start_date: str,
        end_date: str,
        device: str = "all",
        gender: str = "all"
    ):
        """
        키워드 트렌드 데이터 수집 및 저장
        
        Args:
            keywords: 키워드 리스트
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)
            device: 기기 타입
            gender: 성별
        """
        conn = duckdb.connect(self.db_path)
        
        try:
            # API 호출 (최대 5개씩 배치 처리)
            for i in range(0, len(keywords), 5):
                batch_keywords = keywords[i:i+5]
                
                try:
                    response = self.api_client.get_trend_data(
                        keywords=batch_keywords,
                        start_date=start_date,
                        end_date=end_date,
                        device=device,
                        gender=gender
                    )
                    
                    # 응답 데이터 파싱 및 저장
                    self._save_trend_data(conn, response, batch_keywords, device, gender)
                    
                except Exception as e:
                    logger.error(f"배치 처리 실패 ({batch_keywords}): {e}")
                    continue
            
            conn.close()
            logger.info(f"트렌드 데이터 수집 완료: {len(keywords)}개 키워드")
            
        except Exception as e:
            logger.error(f"데이터 수집 실패: {e}")
            conn.close()
            raise
    
    def _save_trend_data(
        self,
        conn: duckdb.DuckDBPyConnection,
        response: dict,
        keywords: List[str],
        device: str,
        gender: str
    ):
        """API 응답 데이터를 데이터베이스에 저장"""
        try:
            # 네이버 데이터랩 API 응답 구조 파싱
            if "results" in response:
                for result in response["results"]:
                    keyword_group = result.get("keywordGroup", [])
                    if keyword_group:
                        keyword = keyword_group[0]  # 첫 번째 키워드 사용
                    else:
                        # keywordGroup이 없으면 groupName 또는 title 사용
                        keyword = result.get("title", "") or (keywords[0] if keywords else "unknown")
                    
                    if not keyword:
                        continue
                    
                    data_list = result.get("data", [])
                    
                    for data_point in data_list:
                        date_str = data_point.get("period")
                        value = data_point.get("ratio", 0)
                        
                        if date_str and keyword:
                            # 중복 방지: ON CONFLICT 사용
                            conn.execute("""
                                INSERT INTO search_trends 
                                (keyword, date, value, device_type, gender, age_group)
                                VALUES (?, ?, ?, ?, ?, ?)
                                ON CONFLICT (keyword, date, device_type, gender, age_group) 
                                DO UPDATE SET value = EXCLUDED.value, collected_at = CURRENT_TIMESTAMP
                            """, [keyword, date_str, value, device, gender, "all"])
            
            conn.commit()
            logger.info(f"데이터 저장 완료: {len(keywords)}개 키워드")
            
        except Exception as e:
            logger.error(f"데이터 저장 실패: {e}")
            conn.rollback()
            raise
    
    def collect_historical_data(
        self,
        keywords: List[str],
        months: int = 12
    ):
        """과거 N개월 데이터 수집"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        # 월별로 나누어 수집 (API 부하 분산)
        current = start_date
        while current <= end_date:
            month_end = min(
                current.replace(day=28) + timedelta(days=4),
                end_date
            )
            
            self.collect_keyword_trends(
                keywords=keywords,
                start_date=current.strftime("%Y-%m-%d"),
                end_date=month_end.strftime("%Y-%m-%d")
            )
            
            current = month_end + timedelta(days=1)


if __name__ == "__main__":
    collector = TrendCollector()
    # 테스트용
    collector.collect_keyword_trends(
        keywords=["커피", "카페"],
        start_date="2024-01-01",
        end_date="2024-12-31"
    )

