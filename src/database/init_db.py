"""DuckDB 데이터베이스 초기화"""
import duckdb
from pathlib import Path
from loguru import logger
from config.settings import settings


def init_database():
    """데이터베이스 및 테이블 초기화"""
    # 데이터 디렉토리 생성
    db_path = Path(settings.database_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # DuckDB 연결
    conn = duckdb.connect(str(db_path))
    
    # 검색 트렌드 테이블
    conn.execute("""
        CREATE TABLE IF NOT EXISTS search_trends (
            id INTEGER PRIMARY KEY,
            keyword VARCHAR NOT NULL,
            date DATE NOT NULL,
            value INTEGER NOT NULL,
            device_type VARCHAR DEFAULT 'all',  -- 'pc', 'mobile', 'all'
            gender VARCHAR DEFAULT 'all',  -- 'm', 'f', 'all'
            age_group VARCHAR DEFAULT 'all',  -- '10', '20', '30', '40', '50', '60', 'all'
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(keyword, date, device_type, gender, age_group)
        )
    """)
    
    # 키워드 확장 테이블
    conn.execute("""
        CREATE TABLE IF NOT EXISTS keyword_expansions (
            id INTEGER PRIMARY KEY,
            seed_keyword VARCHAR NOT NULL,
            expanded_keyword VARCHAR NOT NULL,
            search_intent VARCHAR,  -- 'informational', 'navigational', 'transactional'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(seed_keyword, expanded_keyword)
        )
    """)
    
    # 이벤트 크롤링 테이블 (선택적)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS franchise_events (
            id INTEGER PRIMARY KEY,
            brand VARCHAR NOT NULL,
            event_title VARCHAR NOT NULL,
            event_url VARCHAR,
            start_date DATE,
            end_date DATE,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 인덱스 생성
    conn.execute("CREATE INDEX IF NOT EXISTS idx_keyword_date ON search_trends(keyword, date)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_expanded_keyword ON keyword_expansions(seed_keyword)")
    
    conn.close()
    logger.info(f"데이터베이스 초기화 완료: {settings.database_path}")


if __name__ == "__main__":
    init_database()

