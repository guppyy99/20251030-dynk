"""한국 공휴일 데이터 처리"""
import holidays
from datetime import datetime, date
from typing import Dict, List
import pandas as pd


def get_korean_holidays(year: int) -> pd.DataFrame:
    """한국 공휴일 데이터 조회"""
    kr_holidays = holidays.KR(years=year)
    
    holiday_list = []
    for holiday_date, holiday_name in kr_holidays.items():
        holiday_list.append({
            "date": holiday_date,
            "name": holiday_name,
            "is_holiday": True
        })
    
    return pd.DataFrame(holiday_list)


def get_holiday_dict(year: int) -> Dict[date, str]:
    """공휴일 딕셔너리 반환"""
    kr_holidays = holidays.KR(years=year)
    return {date_obj: name for date_obj, name in kr_holidays.items()}


def is_holiday(check_date: date) -> bool:
    """특정 날짜가 공휴일인지 확인"""
    kr_holidays = holidays.KR(years=check_date.year)
    return check_date in kr_holidays


def get_holiday_name(check_date: date) -> str:
    """특정 날짜의 공휴일 이름 반환"""
    kr_holidays = holidays.KR(years=check_date.year)
    return kr_holidays.get(check_date, "")

