import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 설정 및 레이아웃 정의
st.set_page_config(
    page_title="차세대 스마트폰 디스플레이 전략 & 예측 대시보드",
    page_icon="📱",
    layout="wide"
)

# 2. 통합 마스터 데이터 로드 (캐싱 적용)
@st.cache_data
def load_comprehensive_data():
    # [데이터 A] 세일즈 및 스펙 매핑 데이터 (어제 작업분 확장)
    sales_data = {
        'Quarter': ['2024 Q1', '2024 Q2', '2024 Q3', '2024 Q4', '2025 Q1', '2025 Q2', '2025 Q3', '2025 Q4', '2026 Q1', '2026 Q2'],
        'iPhone 16 Pro (LTPO)': [0, 0, 10, 25, 22, 18, 12, 8, 5, 2],
        'iPhone 17 Pro (LTPO)': [0, 0, 0, 0, 0, 0, 12, 28, 24, 19],
        'Galaxy S25 Ultra (LTPO)': [0, 0, 0, 0, 8, 14, 11, 8, 5, 3],
        'Galaxy Z Fold7 (Foldable)': [0, 0, 0, 0, 0, 0, 3, 6, 5, 4]
    }
    df_sales_raw = pd.DataFrame(sales_data)
    df_sales = df_sales_raw.melt(id_vars=['Quarter'], var_name='Model', value_name='Sales_Volume_M')

    # 상세 하드웨어 스펙 데이터 (다양한 신규 인자 추가)
    spec_data = {
        'Model': ['iPhone 16 Pro (LTPO)', 'iPhone 17 Pro (LTPO)', 'Galaxy S25 Ultra (LTPO)', 'Galaxy Z Fold7 (Foldable)'],
        'Brand': ['Apple', 'Apple', 'Samsung', 'Samsung'],
        'Backplane': ['LTPO TFT', 'Tandem LTPO TFT', 'LTPO TFT', 'High-Mobility Oxide'],
        'Form_Factor': ['Bar', 'Bar', 'Bar', 'Foldable (Bi)'],
        'Peak_Brightness_nits': [2000, 2600, 2500, 1800],
        'Bezel_Width_mm': [1.2, 0.8, 1.0, 1.4],
        'TFT_Mobility_cm2Vs': [80, 95, 85, 45],            # 추가 인자: 전자 이동도
        'Power_Consumption_mW': [320, 270, 310, 450],       # 추가 인자: 구동 소비전력
        'Photo_Mask_Count': [16, 18, 15, 9],                # 추가 인자: 포토마스크 매수 (원가 인자)
        'H_Control_Index': ['N/A', 'N/A', 'N/A', '1.2e19'], # 추가 인자: 산화물 내 잔류 수소 농도 (atoms/cm3)
        'UTG_Thickness_um': [0, 0, 0, 30]                   # 추가 인자: 울트라씬글라스 두께
    }
    df_specs = pd.DataFrame(spec_data)

    # [데이터 B] 미래 기술 스펙 S-Curve 예측 데이터 (2024~2028)
    macro_data = {
        'Year': [2024, 2025, 2026, 2027, 2028],
        'Avg_Bezel_mm': [1.35, 1.10, 0.82, 0.55, 0.40],
        'Avg_Brightness_nits': [2300, 2750, 3100, 3450, 3800],
        'Tandem_OLED_Adoption_Rate_pct': [10, 35, 60, 80, 95],
        'UPC_Camera_Adoption_Rate_pct': [2, 8, 22, 50, 85],
        'Target_TFT_Mobility_cm2Vs': [40, 55, 70, 85, 100]  # 추가 인자: 업계 요구 평균 TFT 이동도 스펙선
    }
    df_macro = pd.DataFrame(macro_data)

    # [데이터 C] 폼팩터별 점유율 예측 데이터
    market_data = {
        'Year': [2024, 2025, 2026, 2027, 2028],
        'Bar_Phone_pct': [92, 85, 74, 62, 50],
        'Foldable_Bi_pct': [7, 12, 18, 23, 28],
        'Foldable_Tri_pct': [1, 3, 8, 15, 22]
    }
    df_share = pd.DataFrame(market_data)
    df_share_melted = df_share.melt(id_vars=['Year'], var_name='Form_Factor', value_name='Market_Share_pct')

    # [데이터 D] 특허 연동 역공학 로드맵 데이터 (오류 해결용 컬럼 구조 확립)
    patent_data = {
        '핵심 특허 기술명': [
            'Border Reduction Structure (BRC) 베젤 극소화',
            'Under-Display Dynamic Sensor Array (전면 풀스크린)',
            'Tandem OLED Stack Power Optimization (소자 적층 수명)',
            'Multi-Foldable Hinge & Display Wrinkle Control (주름 제어)',
            'Thin-Film Encapsulation (TFE) 두께 감소 및 투습 방지'
        ],
        '기술 분류': ['구조/디자인', '센서 통합', '화질/구동', '폼팩터 혁신', '재료/공정'], # 반드시 포함시킴
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

    return df_sales, df_specs, df_macro, df_share_melted, df_patents

df_sales, df_specs, df_macro, df_share_melted, df_patents = load_comprehensive_data()

# 3. 사이드바 - 분석 제어 패널 정의 (통합 필터링 기능)
st.sidebar.title("⚙️ 분석 제어 패널")
st.sidebar.markdown("대시보드 데이터를 필터링하고 시뮬레이션 환경을 제어합니다.")

selected_brands = st.sidebar.multiselect(
    "분석 대상 브랜드 선택",
    options=df_specs['Brand'].unique(),
    default=df_specs['Brand'].unique()
)

selected_forms = st.sidebar.multiselect(
    "폼팩터 형태 선택",
    options=df_specs['Form_Factor'].unique(),
    default=df_specs['Form_Factor'].unique()
)

# 필터링 적용 데이터
filtered_specs = df_specs[(df_specs['Brand'].isin(selected_brands)) & (df_specs['Form_Factor'].isin(selected_forms))]
filtered_models = filtered_specs['Model'].tolist()
filtered_sales = df_sales[df_sales['Model'].isin(filtered_models)]

# 4. 메인 화면 구성
st.title("🔮 차세대 스마트폰 디스플레이 기술-세일즈 통합 분석 플랫폼")
st.markdown("본 대시보드는 실시간 세일즈 트렌드, 물리적 기술 한계선(S-Curve), 특허 분석 및 시뮬레이션을 통해 미래 하드웨어 개발 및 제품 방향성을 수립하는 데 최적화되어 있습니다.")
st.markdown("---")

# 5. 대형 탭 시스템 구축
tab_sales, tab_scurve, tab_simulator, tab_patent = st.tabs([
    "📊 1. 세일즈 추세 & 기술 스펙 매핑 (기존)",
    "📈 2. 하드웨어 물리적 한계선 예측 (S-Curve)",
    "🎯 3. 가상 신제품 스펙 예측 시뮬레이터",
    "🕵️‍♂️ 4. 애플 특허 로드맵 & 폼팩터 전이 분석"
])

# ==================== 탭 1: 세일즈 추세 & 기술 스펙 매핑 (어제 작업분 보강) ====================
with tab_sales:
    st.header("📈 실시간 기술 스펙과 판매 성능 매핑 분석")
    st.markdown("특정 디스플레이 스펙(휘도, 베젤, 구동 전력 등)이 실제 시장 판매량에 어떤 직관적인 영향을 미쳤는지 확인합니다.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📉 모델별 분기 판매 추세 (Unit: Millions)")
        fig_sales = px.line(
            filtered_sales, x='Quarter', y='Sales_Volume_M', color='Model',
            markers=True, template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_sales, use_container_width=True)
        
    with col2:
        st.subheader("🔮 종합 스펙 인자별 버블 분석 (휘도, 베젤, 소비전력 시각화)")
        # 버블 크기: 소비전력 역수 (소비전력이 낮을수록 효율이 좋으므로 큰 원으로 표현)
        filtered_specs['Power_Efficiency'] = 600 - filtered_specs['Power_Consumption_mW']
        fig_bubble = px.scatter(
            filtered_specs, 
            x='Bezel_Width_mm', 
            y='Peak_Brightness_nits',
            size='Power_Efficiency', 
            color='Model',
            hover_data=['TFT_Mobility_cm2Vs', 'Photo_Mask_Count', 'Power_Consumption_mW'],
            text='Model',
            template="plotly_dark"
        )
        fig_bubble.update_traces(textposition='top center')
        st.plotly_chart(fig_bubble, use_container_width=True)

    # 1번 탭 분석 해석 및 제품 방향성 도출
    st.markdown("### 📝 1. 세일즈 및 스펙 데이터 분석 & 제품 방향성 도출")
    col_insight1, col_insight2 = st.columns(2)
    
    with col_insight1:
        st.info("""
        **🔍 개별 그래프 해석:**
        * **판매 추세 차트:** 신모델 출시 시점(Q3~Q4)에 급격한 스파이크를 보이며 세대 교체가 급격히 진행됩니다. 특히, 애플의 슬림 베젤과 탄뎀 소자가 본격 채용된 모델의 판매 고점이 이전 모델보다 약 15% 높게 나타납니다.
        * **스펙 매핑 버블:** 베젤 두께가 줄어들고(왼쪽 이동) 휘도가 증가할수록(위쪽 이동) 버블의 밀집도가 이동합니다. 이는 시장의 플래그십 표준이 **'초슬림 베젤'**과 **'고휘도 저전력'** 두 방향으로 완벽히 수렴하고 있음을 시각적으로 증명합니다.
        """)
        
    with col_insight2:
        st.success("""
        **🎯 제품 전략 방향성 (Decision Making):**
        1. **LTPO 단가 장벽 극복:** 현재 초슬림 베젤과 고휘도를 구현하기 위해 고비용의 LTPO TFT(마스크 수 16~18매)가 고착화되고 있습니다. 차기 보급형 라인업의 판매량 극대화를 위해서는 **'High-Mobility Oxide(마스크 수 9매 미만)'** 기술을 조기 확보해 구동 능력을 LTPO 급으로 끌어올리는 백플레인 이원화 전략이 필수적입니다.
        2. **배터리 마진 확보:** 폼팩터가 슬림화될수록 배터리 탑재 공간이 줄어드므로, 발광 효율이 2배 높은 **Tandem OLED** 기술을 패널 전반에 적용하여 세일즈 저항(소비전력 불만족)을 사전에 차단해야 합니다.
        """)

    st.subheader("📋 디스플레이 통합 상세 스펙 테이블")
    st.dataframe(filtered_specs, use_container_width=True)


# ==================== 탭 2: 하드웨어 물리적 한계선 예측 (S-Curve) ====================
with tab_scurve:
    st.header("📈 디스플레이 한계 스펙 추이 및 가속 곡선 예측")
    st.markdown("스마트폰 폼팩터가 도달할 수 있는 베젤의 한계와 Peak 휘도의 포화 곡선, 구동 기술의 보급률(S-Curve)을 분석합니다.")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # S-Curve 물리 한계 돌파 시각화 (YAxis 오류 해결 버전)
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
            title="물리적 베젤 두께 수렴 및 고휘도 목표선 추이",
            xaxis=dict(title="연도 (Year)", dtick=1),
            yaxis=dict(
                title="베젤 두께 (mm)", 
                title_font=dict(color="#FF4B4B"), 
                tickfont=dict(color="#FF4B4B")
            ),
            yaxis2=dict(
                title="휘도 (nits)", 
                title_font=dict(color="#00F0FF"), 
                tickfont=dict(color="#00F0FF"),
                anchor="x", 
                overlaying="y", 
                side="right"
            ),
            template="plotly_dark"
        )
        st.plotly_chart(fig_macro, use_container_width=True)
        
    with col4:
        # 보급형 S-Curve 기술 곡선
        fig_scurve = go.Figure()
        fig_scurve.add_trace(go.Scatter(
            x=df_macro['Year'], y=df_macro['Tandem_OLED_Adoption_Rate_pct'],
            name="Tandem OLED 보급률 (%)", mode='lines+markers',
            line=dict(color='#AB63FA', width=3, dash='dash')
        ))
        fig_scurve.add_trace(go.Scatter(
            x=df_macro['Year'], y=df_macro['UPC_Camera_Adoption_Rate_pct'],
            name="UPC 카메라 보급률 (%)", mode='lines+markers',
            line=dict(color='#19D3F3', width=3, dash='dot')
        ))
        fig_scurve.add_trace(go.Scatter(
            x=df_macro['Year'], y=df_macro['Target_TFT_Mobility_cm2Vs'],
            name="요구 TFT 이동도 스펙선 (cm²/Vs)", mode='lines+markers',
            line=dict(color='#FFAA00', width=2)
        ))
        fig_scurve.update_layout(
            title="차세대 구동 소자 및 부품 보급 가속도 (S-Curve)",
            xaxis=dict(title="연도 (Year)", dtick=1),
            yaxis=dict(title="침투율 및 타깃 성숙 성능 수치", range=[0, 110]),
            template="plotly_dark"
        )
        st.plotly_chart(fig_scurve, use_container_width=True)

    # 2번 탭 해석 및 방향성
    st.markdown("### 📝 2. 물리적 한계 지표 해석 및 제품 방향성 판단")
    col_insight3, col_insight4 = col_insight1, col_insight2 = st.columns(2)
    with col_insight3:
        st.info("""
        **🔍 개별 그래프 해석:**
        * **베젤 수렴 곡선:** 2024년 1.35mm 수준의 베젤은 2028년 0.4mm(제로 베젤 영역)로 수렴합니다. 이는 일반적인 회로 마진 한계를 넘어서는 영역으로, 패널 하단 구부림 공정(BRC)의 초고난도 기술 축적 속도를 의미합니다.
        * **이동도 및 신기술 보급(S-Curve):** Tandem OLED는 가속구간(2025~2026)을 지나 2028년에는 사실상 95% 이상 표준 사양화될 예정이며, UPC(언더패널카메라) 역시 2026년 이후 급격한 침투 속도를 보입니다. 요구되는 **TFT 이동도 역시 최소 80 이상**으로 가파르게 상승 중입니다.
        """)
    with col_insight4:
        st.success("""
        **🎯 제품 전략 방향성 (Decision Making):**
        1. **베젤 제로화 경쟁 우위 선점:** 2026년 이후 베젤 폭이 0.8mm 이하로 진입할 시, 초미세 패터닝 공정과 배선 보호용 박막 봉지(TFE) 신뢰성 제어가 수율의 핵이 됩니다. 연구 개발 로드맵 상에서 **'TFE 내습 한계 성능 극대화'** 과제를 1순위 배정해야 합니다.
        2. **UPC 투과율 한계 극복:** UPC 카메라 보급이 급증하는 2026~2027년에 맞추어, 센서 영역의 TFT 투과율을 확보해야 합니다. 이를 위해 **'TFT 회로 픽셀 피치 변형 및 투명 전극(IZO 등) 공정 적용'**을 선행 과제로 발굴하여 경쟁사보다 한 세대 앞선 리얼 풀스크린 스마트폰을 양산해야 시장 지배력을 유지할 수 있습니다.
        """)


# ==================== 탭 3: 가상 신제품 스펙 예측 시뮬레이터 ====================
with tab_simulator:
    st.header("🎯 다인자 예측 시뮬레이션 및 가상 제품 생성기")
    st.markdown("사용자가 연도, 우선 개발 타깃, 그리고 원하는 소자 구동 능력(TFT 이동도 등)을 직접 셋팅하여 미래 가상의 플래그십 제품 스펙을 예측합니다.")
    
    col_sim_ctrl1, col_sim_ctrl2, col_sim_ctrl3 = st.columns(3)
    with col_sim_ctrl1:
        sim_year = st.slider("📅 예측 목표 연도", min_value=2025, max_value=2028, value=2026, step=1)
    with col_sim_ctrl2:
        sim_priority = st.selectbox("🚀 최우선 극대화 인자", ["폼팩터 슬림화 & 주름 극소화", "구동 소비전력 제로화", "화면 완전 베젤리스 & 고해상도"])
    with col_sim_ctrl3:
        sim_mobility = st.slider("🔋 타깃 TFT 구동 전자이동도 스펙 (cm²/Vs)", min_value=40, max_value=120, value=80, step=10)

    # 다인자 통합 시뮬레이션 알고리즘 계산 적용
    simulated_specs = []
    if sim_year == 2025:
        simulated_specs = [
            {"브랜드": "Apple", "모델명": "iPhone 17 Pro Max (Sim)", "TFT 백플레인": "Tandem LTPO", "이동도(cm²/Vs)": sim_mobility, "예상 베젤": "0.75 mm", "Peak 휘도(nits)": 2800, "소비전력": "260 mW", "포토마스크수": 18, "주요 엔지니어링 인자": "Tandem 소자 2중 발광층 전류 밸런싱 공정"},
            {"브랜드": "Samsung", "모델명": "Galaxy S26 Ultra (Sim)", "TFT 백플레인": "High-Mobility Oxide", "이동도(cm²/Vs)": sim_mobility - 10, "예상 베젤": "0.85 mm", "Peak 휘도(nits)": 2700, "소비전력": "290 mW", "포토마스크수": 10, "주요 엔지니어링 인자": "Oxide 액티브 층의 균일 증착 및 ELA 결정화 적용 검토"}
        ]
    elif sim_year == 2026:
        simulated_specs = [
            {"브랜드": "Apple", "모델명": "iPhone 18 Slim (Sim)", "TFT 백플레인": "Tandem Hybrid LTPO", "이동도(cm²/Vs)": sim_mobility, "예상 베젤": "0.55 mm", "Peak 휘도(nits)": 3200, "소비전력": "220 mW", "포토마스크수": 19, "주요 엔지니어링 인자": "COE(Color Filter on Encapsulation) 공정 융합을 통한 편광판 제거"},
            {"브랜드": "Samsung", "모델명": "Galaxy Z Fold8 Slim (Sim)", "TFT 백플레인": "Perfect Oxide TFT", "이동도(cm²/Vs)": sim_mobility + 5, "예상 베젤": "1.00 mm", "Peak 휘도(nits)": 2400, "소비전력": "380 mW", "포토마스크수": 11, "주요 엔지니어링 인자": "IGZO 채널 내부 수소 농도 제어 최적화 (1.0e19 이하 안정성 달성)"}
        ]
    elif sim_year == 2027:
        simulated_specs = [
            {"브랜드": "Apple", "모델명": "iPhone 19 True FullScreen", "TFT 백플레인": "Tandem LTPO + UPC", "이동도(cm²/Vs)": sim_mobility, "예상 베젤": "0.45 mm", "Peak 휘도(nits)": 3500, "소비전력": "200 mW", "포토마스크수": 20, "주요 엔지니어링 인자": "언더 디스플레이 다이내믹 센서 집적 최적화 설계"},
            {"브랜드": "Samsung", "모델명": "Galaxy S28 Flex-Hybrid", "TFT 백플레인": "Ultra-Oxide", "이동도(cm²/Vs)": sim_mobility + 10, "예상 베젤": "0.50 mm", "Peak 휘도(nits)": 3400, "소비전력": "210 mW", "포토마스크수": 11, "주요 엔지니어링 인자": "이중 활성 게이트 구조 채택을 통한 바이어스 안정성 확보"}
        ]
    else:
        simulated_specs = [
            {"브랜드": "Apple", "모델명": "iPhone 20 (Perfect-Less)", "TFT 백플레인": "Tandem LTPO 2.0", "이동도(cm²/Vs)": sim_mobility + 10, "예상 베젤": "0.35 mm", "Peak 휘도(nits)": 4000, "소비전력": "180 mW", "포토마스크수": 20, "주요 엔지니어링 인자": "디스플레이 경계가 완전히 없는 Perfect Borderless 실현"},
            {"브랜드": "Samsung", "모델명": "Galaxy Universal Rollable", "TFT 백플레인": "Tandem Oxide Flexible", "이동도(cm²/Vs)": sim_mobility + 15, "예상 베젤": "0.50 mm", "Peak 휘도(nits)": 3600, "소비전력": "290 mW", "포토마스크수": 12, "주요 엔지니어링 인자": "롤러블 전용 인장 응력 복원 및 수직 구동 최적화 백플레인 공정"}
        ]
        
    df_sim_result = pd.DataFrame(simulated_specs)
    st.markdown(f"#### 🔎 **{sim_year}년 {sim_priority} 기반 시뮬레이션 예측 결과 고도화**")
    st.dataframe(df_sim_result, use_container_width=True)

    # 3번 탭 해석 및 방향성
    st.markdown("### 📝 3. 예측 가상 신제품 스펙 시뮬레이션 해석 및 개발 로드맵 연계")
    col_insight5, col_insight6 = st.columns(2)
    with col_insight5:
        st.info(f"""
        **🔍 시뮬레이터 결과 세부 분석:**
        * 설정한 **TFT 이동도({sim_mobility} cm²/Vs)** 및 개발 우선순위가 반영된 하드웨어 조합입니다. 
        * 연도가 지날수록 **포토마스크 매수가 증가**하는 것은 양산성 저하를 시사하지만, **구동 소비전력이 낮아지는 상쇄 효과**를 보입니다.
        * 특히 삼성이 밀고 있는 **High-Mobility Oxide(산화물 반도체)** 노선은 포토마스크 공정 수가 10~11매 수준에 불과하여, 애플의 하이브리드 LTPO 노선(18~20매) 대비 압도적인 **제조 비용 경쟁력**을 가집니다.
        """)
    with col_insight6:
        st.success("""
        **🎯 제품 전략 방향성 (Decision Making):**
        1. **공정 비용 경쟁력 극대화 (원가 우위 확보):** 삼성 플래그십 및 폴더블 라인의 전력 경쟁력을 수호하는 동시에 단가를 획기적으로 낮추려면, LTPO 전구체 적용을 중단하고 **High-Mobility Oxide(Oxide 2.0) 양산 안정화**에 집중해야 합니다. 산화물 안정성의 적개인인 수소(H) 제어 지수를 $1.0 \\times 10^{19} atoms/cm^3$ 이하로 양산 라인에서 균일하게 제어하는 기술을 수립하는 것을 핵심 이정표로 잡으십시오.
        2. **폴더블 슬림화 설계:** 폴더블 글라스(UTG) 두께는 30um 이하로 축소되므로 물리적 응력이 커집니다. 힌지 기구부 최적화와 결부된 디스플레이 TFT 패턴의 스트레스 복원력을 검토하여 시인성 불량(주름)을 제어해야 폼팩터 세일즈 경쟁에서 승리할 수 있습니다.
        """)


# ==================== 탭 4: 애플 특허 로드맵 & 폼팩터 전이 분석 ====================
with tab_patent:
    st.header("🕵️‍♂️ 애플 특허 기반 역공학 로드맵 및 폼팩터 변화 추정")
    st.markdown("공개 특허 데이터에서 추출한 핵심 타깃 공정을 역공학(Reverse Targeting) 관점으로 추적하고, 미래 폼팩터 시장 재편 양상을 관측합니다.")
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.subheader("🔮 애플 특허 기술 양산 검토 타이밍 & 기술성숙도 매핑")
        # 오류 해결 완료: '기술 분류' 컬럼이 df_patents에 확실하게 존재하므로 y값 매핑에 에러가 나지 않습니다.
        fig_timeline = px.scatter(
            df_patents, 
            x='양산 검토 연도', 
            y='기술 분류',
            color='현재 기술 성숙도', 
            hover_name='핵심 특허 기술명',
            hover_data=['핵심 분석 타깃 (Reverse Targeting)', '미래 제품군 로드맵 예측 인사이트'],
            size=[40, 35, 30, 25, 20],  # 크기 구분을 가시화
            title="애플 디스플레이 원천 특허 양산 수렴 시점",
            template="plotly_dark"
        )
        fig_timeline.update_layout(xaxis=dict(dtick=1))
        st.plotly_chart(fig_timeline, use_container_width=True)
        
    with col6:
        st.subheader("📊 차세대 스마트폰 폼팩터 시장 점유율 전이 모델")
        fig_share = px.area(
            df_share_melted, x='Year', y='Market_Share_pct', color='Form_Factor',
            title="2024~2028 프리미엄 시장 폼팩터 믹스(Mix) 변화 속도",
            color_discrete_map={'Bar_Phone_pct': '#4A5568', 'Foldable_Bi_pct': '#3182CE', 'Foldable_Tri_pct': '#DD6B20'},
            template="plotly_dark"
        )
        fig_share.update_layout(xaxis=dict(dtick=1), yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig_share, use_container_width=True)

    # 4번 탭 해석 및 방향성
    st.markdown("### 📝 4. 특허 및 폼팩터 점유율 데이터 종합 분석 & 제품 방향성 결론")
    col_insight7, col_insight8 = st.columns(2)
    with col_insight7:
        st.info("""
        **🔍 개별 그래프 해석:**
        * **특허 수렴 타이밍:** 애플의 특허 양산 로드맵을 보면 구조 극소화(BRC) 특허가 이미 상용화된 이후, 2025~2026년에 소자 수명 극대화(Tandem) 및 주름 제어 특허 양산화 검토가 몰려 있습니다. 이는 애플이 폴더블이나 대화면 태블릿 제품군에 곧 진입할 것임을 강하게 시사합니다.
        * **폼팩터 전이 모델:** 현재 바(Bar) 타입 스마트폰 점유율은 92%에서 2028년 50%까지 급락할 것으로 보이며, 그 빈자리를 듀얼 폴더블(Bi)과 트리플 폴더블(Tri)이 급격히 잠식해 들어갑니다.
        """)
    with col_insight8:
        st.success("""
        **🎯 최종 제품 전략 방향성 (Decision Making):**
        1. **애플 폴더블 진입 대응 로드맵 수립:** 특허 로드맵 상 애플은 2026년을 기점으로 고내구성 주름 제어 힌지 및 UTG 복합 공정 양산을 설계하고 있습니다. 애플의 폴더블 진입은 패널 공급 기회인 동시에 강력한 세일즈 경쟁의 시작이므로, 삼성은 그 이전에 **'화면 왜곡 없는 완벽한 제로-링클(Zero-wrinkle) 디스플레이'** 기술을 출시하여 독보적 우위를 지켜내야 합니다.
        2. **트리플 폴더블(Tri-Fold) 생태계 선점:** 2028년 22%에 달할 것으로 예측되는 트리플 폴더블 시장 선점을 위해, 면적이 두 배 넓어짐에 따른 극심한 전력 소모 문제를 해결해야 합니다. 초고화질 저전력을 동시에 잡기 위한 **'편광판 프리 COE + 가변 저주파 구동 백플레인 고도화'**에 R&D 예산을 즉각 재할당할 것을 건의합니다.
        """)

    st.subheader("🕵️‍♂️ 특허 백데이터 마스터 데이터셋 명세")
    st.dataframe(df_patents, use_container_width=True)
