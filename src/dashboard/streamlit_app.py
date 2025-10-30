"""Streamlit 대시보드 메인 앱"""
import streamlit as st
import duckdb
import pandas as pd
import plotly.graph_objects as go
from plotly_calplot import calplot
from datetime import datetime, date, timedelta
from typing import List
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from src.utils.holidays import get_holiday_dict, get_holiday_name
from src.data.gemini_api import GeminiKeywordExpander
from src.etl.collect_trends import TrendCollector
import os

# Railway 환경 변수 포트 설정
if "PORT" in os.environ:
    os.environ["STREAMLIT_SERVER_PORT"] = os.environ["PORT"]

# 페이지 설정
st.set_page_config(
    page_title="한국 검색 트렌드 분석 대시보드",
    page_icon="📊",
    layout="wide"
)

# 제목
st.title("📊 한국 검색 트렌드 분석 대시보드")
st.markdown("네이버 데이터랩 API 기반 검색 트렌드 분석")

# 데이터베이스 연결
@st.cache_resource
def get_db_connection():
    """데이터베이스 연결 캐싱"""
    # 데이터베이스가 없으면 초기화
    from src.database.init_db import init_database
    init_database()
    return duckdb.connect(settings.database_path)


# 사이드바
with st.sidebar:
    st.header("설정")
    
    # 키워드 선택
    st.subheader("키워드 분석")
    
    # 데이터베이스에서 기존 키워드 목록 가져오기
    conn = get_db_connection()
    existing_keywords = conn.execute("""
        SELECT DISTINCT keyword 
        FROM search_trends 
        ORDER BY keyword
    """).fetchdf()
    
    if not existing_keywords.empty:
        selected_keywords = st.multiselect(
            "분석할 키워드 선택",
            options=existing_keywords["keyword"].tolist(),
            default=existing_keywords["keyword"].tolist()[:3] if len(existing_keywords) >= 3 else existing_keywords["keyword"].tolist()
        )
    else:
        selected_keywords = []
        st.info("데이터가 없습니다. 먼저 데이터를 수집해주세요.")
    
    # 날짜 범위 선택
    st.subheader("기간 선택")
    date_range = st.date_input(
        "날짜 범위",
        value=[date.today() - timedelta(days=365), date.today()],
        min_value=date(2016, 1, 1),
        max_value=date.today()
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date.today() - timedelta(days=365)
    
    # 키워드 확장
    st.subheader("키워드 확장")
    seed_keyword = st.text_input("시드 키워드 입력")
    if st.button("키워드 확장") and seed_keyword:
        with st.spinner("키워드 확장 중..."):
            expander = GeminiKeywordExpander()
            expanded = expander.expand_keywords(seed_keyword, target_count=10)
            
            if expanded:
                st.success(f"{len(expanded)}개 키워드 생성됨")
                for kw in expanded:
                    st.write(f"- **{kw['keyword']}** ({kw['intent']})")
                
                # 데이터 수집 옵션
                if st.button("이 키워드들로 데이터 수집"):
                    collector = TrendCollector()
                    keywords_to_collect = [kw['keyword'] for kw in expanded]
                    collector.collect_keyword_trends(
                        keywords=keywords_to_collect,
                        start_date=start_date.strftime("%Y-%m-%d"),
                        end_date=end_date.strftime("%Y-%m-%d")
                    )
                    st.success("데이터 수집 완료!")
                    st.rerun()
    
    # 새 데이터 수집
    st.subheader("데이터 수집")
    new_keywords = st.text_input("수집할 키워드 (쉼표로 구분)")
    if st.button("데이터 수집 시작") and new_keywords:
        keyword_list = [k.strip() for k in new_keywords.split(",")]
        with st.spinner("데이터 수집 중..."):
            collector = TrendCollector()
            collector.collect_keyword_trends(
                keywords=keyword_list,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d")
            )
            st.success("데이터 수집 완료!")
            st.rerun()


# 메인 대시보드
if selected_keywords and len(date_range) == 2:
    conn = get_db_connection()
    
    # 데이터 조회
    placeholders = ",".join(["?"] * len(selected_keywords))
    query = f"""
        SELECT keyword, date, value
        FROM search_trends
        WHERE keyword IN ({placeholders})
        AND date BETWEEN ? AND ?
        ORDER BY date, keyword
    """
    
    params = selected_keywords + [
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    ]
    
    df = conn.execute(query, params).fetchdf()
    
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        
        # 탭 구성
        tab1, tab2, tab3 = st.tabs(["📈 시계열 차트", "🔥 히트맵 달력", "📊 통계 분석"])
        
        with tab1:
            st.subheader("검색 트렌드 시계열")
            
            # Plotly 라인 차트
            fig = go.Figure()
            
            for keyword in selected_keywords:
                keyword_df = df[df['keyword'] == keyword]
                fig.add_trace(go.Scatter(
                    x=keyword_df['date'],
                    y=keyword_df['value'],
                    mode='lines+markers',
                    name=keyword,
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                title="검색 트렌드 시계열",
                xaxis_title="날짜",
                yaxis_title="검색량 (상대 지수)",
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("연간 히트맵 달력")
            
            # 연도별 히트맵
            for year in range(start_date.year, end_date.year + 1):
                year_df = df[df['date'].dt.year == year].copy()
                
                if not year_df.empty:
                    # 키워드별 히트맵
                    for keyword in selected_keywords:
                        keyword_year_df = year_df[year_df['keyword'] == keyword].copy()
                        
                        if not keyword_year_df.empty:
                            st.markdown(f"### {keyword} - {year}년")
                            
                            # 히트맵용 데이터 준비
                            heatmap_df = keyword_year_df[['date', 'value']].copy()
                            heatmap_df.columns = ['date', 'value']
                            
                            # 공휴일 정보 추가
                            holiday_dict = get_holiday_dict(year)
                            
                            try:
                                fig = calplot(
                                    heatmap_df,
                                    x='date',
                                    y='value',
                                    dark_theme=False,
                                    years_as_title=True,
                                    colorscale='YlOrRd'
                                )
                                
                                fig.update_layout(
                                    title=f"{keyword} 검색 트렌드 히트맵",
                                    height=400
                                )
                                
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as e:
                                st.error(f"히트맵 생성 실패: {e}")
        
        with tab3:
            st.subheader("통계 분석")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("분석 키워드 수", len(selected_keywords))
            
            with col2:
                total_records = len(df)
                st.metric("총 데이터 포인트", f"{total_records:,}")
            
            with col3:
                avg_value = df['value'].mean()
                st.metric("평균 검색 지수", f"{avg_value:.1f}")
            
            with col4:
                max_value = df['value'].max()
                max_date = df[df['value'] == max_value]['date'].iloc[0]
                st.metric("최고 검색일", max_date.strftime("%Y-%m-%d"))
            
            # 키워드별 요약 통계
            st.subheader("키워드별 요약")
            summary = df.groupby('keyword').agg({
                'value': ['mean', 'max', 'min', 'std']
            }).round(2)
            summary.columns = ['평균', '최대', '최소', '표준편차']
            st.dataframe(summary)
            
            # 주간/월간 트렌드 분석
            st.subheader("주간 트렌드")
            df['week'] = df['date'].dt.to_period('W')
            weekly_trend = df.groupby(['keyword', 'week'])['value'].mean().reset_index()
            
            fig_weekly = go.Figure()
            for keyword in selected_keywords:
                kw_data = weekly_trend[weekly_trend['keyword'] == keyword]
                fig_weekly.add_trace(go.Scatter(
                    x=kw_data['week'].astype(str),
                    y=kw_data['value'],
                    mode='lines+markers',
                    name=keyword
                ))
            
            fig_weekly.update_layout(
                title="주간 평균 검색 트렌드",
                xaxis_title="주",
                yaxis_title="평균 검색 지수",
                height=400
            )
            st.plotly_chart(fig_weekly, use_container_width=True)
    
    else:
        st.warning("선택한 기간에 데이터가 없습니다.")
else:
    st.info("👈 사이드바에서 키워드를 선택하고 날짜 범위를 설정해주세요.")


# 푸터
st.markdown("---")
st.markdown("**한국 검색 트렌드 분석 대시보드** | 네이버 데이터랩 API 기반")

