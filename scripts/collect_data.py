"""데이터 수집 스크립트"""
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.etl.collect_trends import TrendCollector
from loguru import logger


def main():
    """메인 실행 함수"""
    # 수집할 키워드 리스트 (환경 변수나 설정 파일에서 가져올 수 있음)
    keywords = [
        "커피",
        "카페",
        "스타벅스",
        "이디야",
        "카페베네"
    ]
    
    collector = TrendCollector()
    
    # 최근 12개월 데이터 수집
    collector.collect_historical_data(
        keywords=keywords,
        months=12
    )
    
    logger.info("데이터 수집 완료")


if __name__ == "__main__":
    main()

