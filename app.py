import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 테마 및 레이아웃 설정
st.set_page_config(
    page_title="차세대 디스플레이 기술 분석 & 예측 플랫폼",
    page_icon="🔮",
    layout="wide"
)

# 2. 마스터 데이터셋 통합 구축
@st.cache_data
def load_all_data():
    # [이전 데이터 1] 디스플레이 기술 트렌드 (TFT, 기판, 레이저 등)
    tech_trend_data = {
        '구분': ['LTPS TFT', 'Oxide (IGZO) TFT', 'LTPO TFT', 'COE (Color Filter on Encapsulation)', 'Tandem OLED'],
        '주요 특징': [
            '고이동도, LTPS 기반 구동 소자 안정성 우수',
            '저누설 전류, 대면적 및 고해상도 최적화',
            'LTPS와 Oxide 결합, 가변 주사율 실현으로 소비전력 극소화',
            '편광판을 컬러필터로 대체하여 두께 감소 및 광효율 향상',
            '발광층을 2개 층으로 적층하여 수명 4배, 휘도 2배 향상'
        ],
        '핵심 공정/재료': [
            'ELA (Eximer Laser Annealing) 결정화 공정',
            '수소 제어 기술, Active 레이어 스퍼터링 공정',
            '복잡한 포토마스크 공정 (고비용 마스크 수 증가)',
            'Inkjet Printing 또는 Photo 공정 기반 CF 형성',
            '유기물 2중 적층용 CGL (Charge Generation Layer) 증착'
        ]
    }
    df_tech = pd.DataFrame(tech_trend_data)

    # [예측 데이터 A] 역사적 추이 + 2028년까지의 기술 지표 예측 데이터 (Macro Trend)
    macro_trend_data = {
        'Year': [2024, 2025, 2026, 2027, 2028],
        'Avg_Bezel_mm': [1.35, 1.10, 0.82, 0.55, 0.40],
        'Avg_Brightness_nits': [2300, 2750, 3100, 3450, 3800],
        'Tandem_OLED_Adoption_Rate_pct': [10, 35, 60, 80, 95],
        'UPC_Camera_Adoption_Rate_pct': [2, 8, 22, 50, 85]
    }
    df_macro = pd.DataFrame(macro_trend_data)

    # [예측 데이터 B] 폼팩터별 시장 세그먼트 전이 예측
    market_share_data = {
        'Year': [2024, 2025, 2026, 2027, 2028],
        'Bar_Phone_pct': [92, 85, 74, 62, 50],
        'Foldable_Bi_pct': [7, 12, 18, 23, 28],
        'Foldable_Tri_pct': [1, 3, 8, 15, 22]
    }
    df_share = pd.DataFrame(market_share_data)
    df_share_melted = df_share.melt(id_vars=['Year'], var_name='Form_Factor', value_name='Market_Share_pct')

    # [예측 데이터 C] 애플 특허 기반 역공학 로드맵
    patent_data = {
        '핵심 특허 기술명': [
            'Border Reduction Structure (BRC) 베젤 극소화',
            'Under-Display Dynamic Sensor Array (전면 풀스크린)',
            'Tandem OLED Stack Power Optimization (소자 적층 수명)',
            'Multi-Foldable Hinge & Display Wrinkle Control (주름 제어)',
            'Thin-Film Encapsulation (TFE) 두께 감소 및 투습 방지'
        ],
        '기술 분류': ['구조/디자인', '센서 통합', '화질/구동', '폼팩터 혁신', '재료/공정'],
        '핵심 분석 타깃 (Reverse Targeting)': ['회로 구부림 공정 마진', '패널 투과율 및 픽셀 피치 변형', '유기물 2개층 전류 밸런싱', 'UTG 응력 분산 및 복원력', '무기막/유기막 다층 박막 제어'],
        '양산 검토 연도': [2024, 2027, 2025, 2026, 2025],
        '현재 기술 성숙도': ['양산 적용 완료', '선행 R&D 및 시제품 검증', '소자 신뢰성 평가 중', '기구 설계 고도화 단계', '라인 인라인 공정 셋업 중'],
        '미래 제품군 로드맵 예측 인사이트': [
            'iPhone 16/17 시리즈에 순차 적용되어 제로 베젤(0.8mm) 달성 및 몰입감 극대화로 판매량 견인.',
            '카메라 홀이 완전히 사라지는 최초의 아이폰 전면 디스플레이 구현(2027년 플래그십 탑재 유력).',
            'iPad, MacBook 라인업에 이어 스마트폰 전 라인업으로 Tandem OLED 확산, 패널 단가 상승 요인.',
            '애플 최초의 폴더블/폴더블 패드 라인업 진입 신호탄. 주름 시인성을 극소화한 특수 두께 UTG 채택 예정.',
            '슬림형(Slim) 모델 라인업 구축을 위해 편광판을 제거하고 COE(Color Filter on Encapsulation) 공정 융합.'
        ]
    }
    df_patents = pd.DataFrame(patent_data)

    return df_tech, df_macro, df_share_melted, df_patents

df_tech, df_macro, df_share_melted, df_patents = load_all_data()

# 3. 레이아웃 헤더 및 타이틀
st.title("🔮 차세대 디스플레이 기술 분석 & 미래 예측 플랫폼")
st.markdown("본 플랫폼은 핵심 제조 공정 분석(이전 작업)과 미래 기술 트렌드 시뮬레이션(신규 작업)을 통합하여 설계되었습니다.")
st.markdown("---")

# 4. 전체 탭 레이아웃 구성
tab_main1, tab_main2 = st.tabs([
    "🔬 [이전 작업] 핵심 제조 공정 & 기술 트렌드 분석",
    "📊 [신규 작업] 미래 하드웨어 스펙 및 폼팩터 예측 시뮬레이터"
])

# ==================== 탭 1: 이전 작업 내용 (제조 공정 및 핵심 기술) ====================
with tab_main1:
    st.header("🕵️‍♂️ 디스플레이 핵심 기술 공정 및 특성 검토")
    st.markdown("차세대 패널에 적용되는 Backplane 원천 기술과 고효율 패널 공정의 특성을 비교 분석합니다.")
    
    # 1) 기존 분석 테이블 시각화
    st.subheader("💡 주요 백플레인 및 패널 공정 요약")
    st.dataframe(df_tech, use_container_width=True)
    
    # 2) 보충 인사이트 박스
    st.info("""
    📝 **R&D 공정 관점 핵심 요약:**
    * **LTPO TFT의 난제:** 뛰어난 전력 절감 효과를 내지만 LTPS와 Oxide를 복합 증착하므로 포토마스크 수가 급증하여 수율 관리가 어렵습니다.
    * **Oxide 수소 제어:** IGZO 채널 영역 내 잔류 수소(H) 함량 제어는 TFT 신뢰성 및 문턱전압($V_{th}$) 이동을 결정짓는 핵심 공정 제어 인자입니다.
    """)


# ==================== 탭 2: 신규 예측 및 시뮬레이터 내용 ====================
with tab_main2:
    st.header("🎯 미래 디스플레이 트렌드 및 가상 제품 예측")
    
    # 세부 서브 탭 분리
    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        "📈 하드웨어 스펙 한계선 예측 (2024~2028)",
        "🎯 미래 가상 신제품 스펙 시뮬레이터",
        "📊 차세대 폼팩터 시장 점유율 전이 모델"
    ])

    # 서브탭 1: 스펙 한계선
    with sub_tab1:
        st.subheader("⚙️ 주요 기술 스펙의 연도별 수렴 및 보급 예측 (S-Curve)")
        col1, col2 = st.columns(2)
        with col1:
            fig_macro = go.Figure()
            fig_macro.add_trace(go.Scatter(
                x=df_macro['Year'], y=df_macro['Avg_Bezel_mm'],
                name="평균 베젤 두께 (mm)", mode='lines+markers',
                line=dict(color='#FF4B4B', width=3)
            ))
            fig_macro.add_trace(go.Scatter(
                x=df_macro['Year'], y=df_macro['Avg_Brightness_nits'],
                name="평균 피크 휘도 (nits)", mode='lines+markers',
                line=dict(color='#00F0FF', width=3), yaxis="y2"
            ))
            fig_macro.update_layout(
                title="물리적 베젤 한계 돌파 및 휘도 상승 예측 곡선",
                xaxis=dict(title="연도 (Year)", dtick=1),
                yaxis=dict(title=dict(text="베젤 두께 (mm)", font=dict(color="#FF4B4B")), tickfont=dict(color="#FF4B4B")),
                yaxis2=dict(title=dict(text="휘도 (nits)", font=dict(color="#00F0FF")), tickfont=dict(color="#00F0FF"), anchor="x", overlaying="y", side="right"),
                template="plotly_dark"
            )
            st.plotly_chart(fig_macro, use_container_width=True)

        with col2:
            fig_scurve = go.Figure()
            fig_scurve.add_trace(go.Scatter(
                x=df_macro['Year'], y=df_macro['Tandem_OLED_Adoption_Rate_pct'],
                name="Tandem OLED 침투율 (%)", mode='lines+markers',
                line=dict(color='#AB63FA', width=3, dash='dash')
            ))
            fig_scurve.add_trace(go.Scatter(
                x=df_macro['Year'], y=df_macro['UPC_Camera_Adoption_Rate_pct'],
                name="UPC(언더패널카메라) 침투율 (%)", mode='lines+markers',
                line=dict(color='#19D3F3', width=3, dash='dot')
            ))
            fig_scurve.update_layout(
                title="차세대 디스플레이 핵심 구동 기술 보급 곡선 (S-Curve)",
                xaxis=dict(title="연도 (Year)", dtick=1),
                yaxis=dict(title="시장 보급률 (Penetration %)", range=[0, 100]),
                template="plotly_dark"
            )
            st.plotly_chart(fig_scurve, use_container_width=True)

    # 서브탭 2: 예측 시뮬레이터
    with sub_tab2:
        st.subheader("🎯 특허 기반 차세대 신제품 스펙 예측 시뮬레이터")
        col_ctrl1, col_ctrl2 = st.columns(2)
        with col_ctrl1:
            target_year = st.slider("🎯 예측 타깃 연도 선택", min_value=2025, max_value=2028, value=2026, step=1)
        with col_ctrl2:
            tech_priority = st.selectbox("🚀 우선 개발 집중 기술", ["폼팩터 극대화 (슬림/폴더블)", "배터리 세이빙 (소비전력 극소화)", "디자인 혁신 (제로베젤/UPC)"])

        predicted_specs = []
        if target_year == 2025:
            predicted_specs = [
                {"모델명": "iPhone 17 Pro Max", "TFT 백플레인": "Tandem LTPO", "예상 베젤": "0.8 mm", "화면 비중": "93.5%", "소비전력": "290 mW", "핵심 기술": "Tandem 2-Stack + BRC 제로베젤"},
                {"모델명": "Galaxy S26 Ultra", "TFT 백플레인": "High-Mobility Oxide", "예상 베젤": "0.9 mm", "화면 비중": "92.8%", "소비전력": "310 mW", "핵심 기술": "COE(편광판 제거) 적용"},
                {"모델명": "Apple Fold Slim 1st", "TFT 백플레인": "LTPO Oxide", "예상 베젤": "1.3 mm", "화면 비중": "89.5%", "소비전력": "420 mW", "핵심 기술": "초박형 가변 UTG 구조"}
            ]
        elif target_year == 2026:
            predicted_specs = [
                {"모델명": "iPhone 18 Ultra (Slim)", "TFT 백플레인": "Tandem LTPO (Slim)", "예상 베젤": "0.6 mm", "화면 비중": "94.8%", "소비전력": "250 mW", "핵심 기술": "COE + 편광판 프리 하이브리드 LTPO"},
                {"모델명": "Galaxy S27 Ultra (UPC)", "TFT 백플레인": "Oxide + UPC TFT", "예상 베젤": "0.7 mm", "화면 비중": "95.2%", "소비전력": "280 mW", "핵심 기술": "완전한 언더디스플레이 센서 적용"},
                {"모델명": "Apple Rollable / Tri-fold", "TFT 백플레인": "Tandem Oxide", "예상 베젤": "1.1 mm", "화면 비중": "93.0%", "소비전력": "510 mW", "핵심 기술": "스트레스 복원 무주름 복합 재료 패널"}
            ]
        elif target_year == 2027:
            predicted_specs = [
                {"모델명": "iPhone 19 Pro (True FullScreen)", "TFT 백플레인": "Tandem LTPO + UPC", "예상 베젤": "0.45 mm", "화면 비중": "96.5%", "소비전력": "220 mW", "핵심 기술": "다이내믹 센서 언더패널 통합"},
                {"모델명": "Galaxy S28 Ultra (Ultra-Oxide)", "TFT 백플레인": "Ultra-Mobility Oxide", "예상 베젤": "0.5 mm", "화면 비중": "96.0%", "소비전력": "240 mW", "핵심 기술": "TFT 소자 수소 제어 및 결정화 공정"},
                {"모델명": "Apple Foldable 2nd (Slim)", "TFT 백플레인": "Tandem LTPO", "예상 베젤": "0.8 mm", "화면 비중": "92.5%", "소비전력": "380 mW", "핵심 기술": "주름 차폐 복합 구조 힌지 시스템"}
            ]
        else:
            predicted_specs = [
                {"모델명": "iPhone 20 (Ultimate FullScreen)", "TFT 백플레인": "Tandem LTPO 2.0", "예상 베젤": "0.35 mm", "화면 비중": "98.2%", "소비전력": "180 mW", "핵심 기술": "완전 무경계(Bezel-less) 디스플레이 구현"},
                {"모델명": "Galaxy S29 Ultra", "TFT 백플레인": "Perfect Crystalline Oxide", "예상 베젤": "0.4 mm", "화면 비중": "97.8%", "소비전력": "195 mW", "핵심 기술": "초고속 구동 및 발광 소자 신재료 결합"},
                {"모델명": "Universal Fold-Roll Hybrid", "TFT 백플레인": "Tandem LTPO Elastic", "예상 베젤": "0.6 mm", "화면 비중": "95.5%", "소비전력": "320 mW", "핵심 기술": "신축성(Stretchable) 플렉서블 힌지 프리 구조"}
            ]
        df_predict_table = pd.DataFrame(predicted_specs)
        st.markdown(f"#### 🔎 **{target_year}년 {tech_priority} 기반 시뮬레이션 결과**")
        st.dataframe(df_predict_table, use_container_width=True)

    # 서브탭 3: 시장 점유율 예측 및 특허 데이터
    with sub_tab3:
        st.subheader("📊 차세대 스마트폰 폼팩터 믹스(Mix) 예측 및 시장 점유율 전이")
        fig_share = px.area(
            df_share_melted, x='Year', y='Market_Share_pct', color='Form_Factor',
            title="2024년 ~ 2028년 프리미엄 라인업 폼팩터별 시장 비중 예측 (% 수렴)",
            color_discrete_map={'Bar_Phone_pct': '#4A5568', 'Foldable_Bi_pct': '#3182CE', 'Foldable_Tri_pct': '#DD6B20'},
            template="plotly_dark"
        )
        fig_share.update_layout(xaxis=dict(title="연도 (Year)", dtick=1), yaxis=dict(title="시장 점유율 비중 (%)", range=[0, 100]))
        st.plotly_chart(fig_share, use_container_width=True)

        st.markdown("---")
        st.subheader("🕵️‍♂️ 예측 모델링 연동용 애플 핵심 특허 백데이터 확인")
        st.dataframe(df_patents, use_container_width=True)
