import streamlit as st
import altair as alt
import pandas as pd
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Analytics Dashboard | Fusion", page_icon=":material/bar_chart:", layout="wide")

st.logo("logo.jpg")

# =============================================================================
# FUSION BRAND COLORS
# =============================================================================
FUSION_BLUE = "#1E3A5F"
FUSION_TEAL = "#0891B2"
FUSION_GOLD = "#D4AF37"
FUSION_LIGHT = "#F0F9FF"

# =============================================================================
# GLOBAL STYLES & ANIMATIONS
# =============================================================================
st.html("""
<style>
    /* Animation Keyframes */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes countUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes barGrow {
        from { transform: scaleX(0); }
        to { transform: scaleX(1); }
    }
    
    /* Page Header */
    .page-header {
        background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 50%, #1E3A5F 100%);
        background-size: 200% 200%;
        animation: gradientFlow 8s ease infinite, fadeInUp 0.6s ease-out;
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(30, 58, 95, 0.3);
    }
    .page-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        pointer-events: none;
    }
    .page-header h1 { 
        margin: 0; 
        font-size: 2rem; 
        font-weight: 700;
        position: relative;
        z-index: 1;
    }
    .page-header p { 
        margin: 0.5rem 0 0 0; 
        opacity: 0.9; 
        font-size: 1rem;
        position: relative;
        z-index: 1;
    }
    .header-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-top: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2rem 0 1rem 0;
        animation: slideInLeft 0.5s ease-out backwards;
    }
    .section-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    .section-icon.trends { background: linear-gradient(135deg, #0891B2, #06B6D4); }
    .section-icon.demo { background: linear-gradient(135deg, #8B5CF6, #A78BFA); }
    .section-icon.dwell { background: linear-gradient(135deg, #D4AF37, #F59E0B); }
    .section-icon.od { background: linear-gradient(135deg, #10B981, #34D399); }
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1E3A5F;
        margin: 0;
    }
    .section-line {
        flex: 1;
        height: 2px;
        background: linear-gradient(90deg, #e2e8f0 0%, transparent 100%);
        border-radius: 1px;
    }
    
    /* Metrics Cards */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    @media (max-width: 900px) {
        .metrics-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 500px) {
        .metrics-grid { grid-template-columns: 1fr; }
    }
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
        animation: scaleIn 0.5s ease-out backwards;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(30, 58, 95, 0.12);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        border-radius: 16px 16px 0 0;
    }
    .metric-card.records::before { background: linear-gradient(90deg, #1E3A5F, #0891B2); }
    .metric-card.hexagons::before { background: linear-gradient(90deg, #8B5CF6, #A78BFA); }
    .metric-card.dwell::before { background: linear-gradient(90deg, #D4AF37, #F59E0B); }
    .metric-card.nations::before { background: linear-gradient(90deg, #10B981, #34D399); }
    
    .metric-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .metric-card.records .metric-icon { background: linear-gradient(135deg, rgba(30, 58, 95, 0.1), rgba(8, 145, 178, 0.1)); }
    .metric-card.hexagons .metric-icon { background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(167, 139, 250, 0.1)); }
    .metric-card.dwell .metric-icon { background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(245, 158, 11, 0.1)); }
    .metric-card.nations .metric-icon { background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(52, 211, 153, 0.1)); }
    
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 0.25rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E3A5F;
        animation: countUp 0.8s ease-out backwards;
    }
    .metric-card:nth-child(1) { animation-delay: 0.1s; }
    .metric-card:nth-child(1) .metric-value { animation-delay: 0.3s; }
    .metric-card:nth-child(2) { animation-delay: 0.2s; }
    .metric-card:nth-child(2) .metric-value { animation-delay: 0.4s; }
    .metric-card:nth-child(3) { animation-delay: 0.3s; }
    .metric-card:nth-child(3) .metric-value { animation-delay: 0.5s; }
    .metric-card:nth-child(4) { animation-delay: 0.4s; }
    .metric-card:nth-child(4) .metric-value { animation-delay: 0.6s; }
    
    /* Chart Cards */
    .chart-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        animation: fadeInUp 0.6s ease-out backwards;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .chart-card:hover {
        box-shadow: 0 8px 25px rgba(30, 58, 95, 0.1);
    }
    .chart-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #1E3A5F, #0891B2, #D4AF37);
        border-radius: 16px 16px 0 0;
    }
    .chart-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #f1f5f9;
    }
    .chart-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        font-size: 1rem;
        color: #1E3A5F;
    }
    .chart-title-icon {
        width: 28px;
        height: 28px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
    }
    .chart-badge {
        font-size: 0.7rem;
        padding: 0.25rem 0.6rem;
        border-radius: 12px;
        font-weight: 500;
    }
    .chart-badge.live {
        background: linear-gradient(135deg, #10B981, #34D399);
        color: white;
    }
    .chart-badge.trend {
        background: linear-gradient(135deg, #0891B2, #06B6D4);
        color: white;
    }
    
    /* Animation delays for chart cards */
    .chart-col-1 .chart-card { animation-delay: 0.1s; }
    .chart-col-2 .chart-card { animation-delay: 0.2s; }
    .chart-col-3 .chart-card { animation-delay: 0.3s; }
    
    /* Data Table Styling */
    .data-table-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        animation: fadeInUp 0.6s ease-out backwards;
        animation-delay: 0.4s;
    }
    .data-table-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #10B981, #34D399);
        border-radius: 16px 16px 0 0;
    }
</style>
""")

# =============================================================================
# PAGE HEADER
# =============================================================================
st.html("""
<div class="page-header">
    <h1>Analytics Dashboard</h1>
    <p>Sellable insights from Saudi telco mobility data</p>
    <div class="header-badge">
        <span>📊</span>
        <span>Real-time analytics powered by Snowflake</span>
    </div>
</div>
""")

# =============================================================================
# DATA FUNCTIONS
# =============================================================================
@st.cache_data(ttl=600)
def get_cities():
    session = get_active_session()
    return session.sql("SELECT DISTINCT SUBSCRIBER_HOME_CITY FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()

@st.cache_data(ttl=600)
def get_hourly_traffic(cities):
    session = get_active_session()
    where_clause = ""
    if cities:
        city_list = "','".join(cities)
        where_clause = f"WHERE SUBSCRIBER_HOME_CITY IN ('{city_list}')"
    
    query = f"""
        SELECT HOUR, COUNT(*) as TRAFFIC_COUNT
        FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        {where_clause}
        GROUP BY HOUR
        ORDER BY HOUR
    """
    return session.sql(query).to_pandas()

@st.cache_data(ttl=600)
def get_daily_traffic(cities):
    session = get_active_session()
    where_clause = ""
    if cities:
        city_list = "','".join(cities)
        where_clause = f"WHERE SUBSCRIBER_HOME_CITY IN ('{city_list}')"
    
    query = f"""
        SELECT DATE, COUNT(*) as TRAFFIC_COUNT
        FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        {where_clause}
        GROUP BY DATE
        ORDER BY DATE
    """
    return session.sql(query).to_pandas()

@st.cache_data(ttl=600)
def get_nationality_breakdown(cities):
    session = get_active_session()
    where_clause = ""
    if cities:
        city_list = "','".join(cities)
        where_clause = f"WHERE SUBSCRIBER_HOME_CITY IN ('{city_list}')"
    
    query = f"""
        SELECT NATIONALITY, COUNT(*) as COUNT
        FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        {where_clause}
        GROUP BY NATIONALITY
        ORDER BY COUNT DESC
        LIMIT 10
    """
    return session.sql(query).to_pandas()

@st.cache_data(ttl=600)
def get_age_breakdown(cities):
    session = get_active_session()
    where_clause = ""
    if cities:
        city_list = "','".join(cities)
        where_clause = f"WHERE SUBSCRIBER_HOME_CITY IN ('{city_list}')"
    
    query = f"""
        SELECT AGE_GROUP, COUNT(*) as COUNT
        FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        {where_clause}
        GROUP BY AGE_GROUP
        ORDER BY AGE_GROUP
    """
    return session.sql(query).to_pandas()

@st.cache_data(ttl=600)
def get_gender_breakdown(cities):
    session = get_active_session()
    where_clause = ""
    if cities:
        city_list = "','".join(cities)
        where_clause = f"WHERE SUBSCRIBER_HOME_CITY IN ('{city_list}')"
    
    query = f"""
        SELECT GENDER, COUNT(*) as COUNT
        FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        {where_clause}
        GROUP BY GENDER
    """
    return session.sql(query).to_pandas()

@st.cache_data(ttl=600)
def get_subscription_breakdown(cities):
    session = get_active_session()
    where_clause = ""
    if cities:
        city_list = "','".join(cities)
        where_clause = f"WHERE SUBSCRIBER_HOME_CITY IN ('{city_list}')"
    
    query = f"""
        SELECT SUBSCRIPTION_TYPE, COUNT(*) as COUNT
        FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        {where_clause}
        GROUP BY SUBSCRIPTION_TYPE
    """
    return session.sql(query).to_pandas()

@st.cache_data(ttl=600)
def get_dwell_time_by_city():
    session = get_active_session()
    query = """
        SELECT SUBSCRIBER_HOME_CITY as CITY, 
               AVG(AVG_STAYING_DURATION_MIN) as AVG_DWELL_TIME,
               COUNT(*) as OBSERVATIONS
        FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        GROUP BY SUBSCRIBER_HOME_CITY
        ORDER BY AVG_DWELL_TIME DESC
    """
    return session.sql(query).to_pandas()

@st.cache_data(ttl=600)
def get_origin_destination(cities):
    session = get_active_session()
    where_clause = ""
    if cities:
        city_list = "','".join(cities)
        where_clause = f"WHERE SUBSCRIBER_HOME_CITY IN ('{city_list}')"
    
    query = f"""
        SELECT SUBSCRIBER_HOME_CITY as HOME_CITY, COUNT(*) as VISITORS
        FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        {where_clause}
        GROUP BY SUBSCRIBER_HOME_CITY
        ORDER BY VISITORS DESC
    """
    return session.sql(query).to_pandas()

@st.cache_data(ttl=600)
def get_summary_metrics(cities):
    session = get_active_session()
    where_clause = ""
    if cities:
        city_list = "','".join(cities)
        where_clause = f"WHERE SUBSCRIBER_HOME_CITY IN ('{city_list}')"
    
    query = f"""
        SELECT 
            COUNT(*) as TOTAL_RECORDS,
            COUNT(DISTINCT HEXAGON_ID) as UNIQUE_HEXAGONS,
            AVG(AVG_STAYING_DURATION_MIN) as AVG_DWELL,
            COUNT(DISTINCT NATIONALITY) as NATIONALITIES
        FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        {where_clause}
    """
    return session.sql(query).to_pandas()

# =============================================================================
# SIDEBAR FILTERS
# =============================================================================
cities_df = get_cities()

with st.sidebar:
    st.subheader(":material/filter_list: Filters", anchor=False)
    selected_cities = st.multiselect(
        "Filter by city",
        options=cities_df['SUBSCRIBER_HOME_CITY'].tolist(),
        default=[]
    )
    
    st.divider()
    st.caption("Data refreshes every 10 minutes")

# =============================================================================
# METRICS SECTION
# =============================================================================
metrics_df = get_summary_metrics(selected_cities)

st.html(f"""
<div class="metrics-grid">
    <div class="metric-card records">
        <div class="metric-icon">📊</div>
        <div class="metric-label">Total Records</div>
        <div class="metric-value">{metrics_df['TOTAL_RECORDS'].iloc[0]:,}</div>
    </div>
    <div class="metric-card hexagons">
        <div class="metric-icon">⬡</div>
        <div class="metric-label">Unique Hexagons</div>
        <div class="metric-value">{metrics_df['UNIQUE_HEXAGONS'].iloc[0]:,}</div>
    </div>
    <div class="metric-card dwell">
        <div class="metric-icon">⏱️</div>
        <div class="metric-label">Avg Dwell Time</div>
        <div class="metric-value">{metrics_df['AVG_DWELL'].iloc[0]:.1f} min</div>
    </div>
    <div class="metric-card nations">
        <div class="metric-icon">🌍</div>
        <div class="metric-label">Nationalities</div>
        <div class="metric-value">{metrics_df['NATIONALITIES'].iloc[0]}</div>
    </div>
</div>
""")

# =============================================================================
# FOOT TRAFFIC TRENDS
# =============================================================================
st.html("""
<div class="section-header" style="animation-delay: 0.2s;">
    <div class="section-icon trends">📈</div>
    <h2 class="section-title">Foot Traffic Trends</h2>
    <div class="section-line"></div>
</div>
""")

col1, col2 = st.columns(2)

with col1:
    st.html('<div class="chart-col-1">')
    hourly_df = get_hourly_traffic(selected_cities)
    
    # Create gradient area chart for hourly traffic
    hourly_chart = alt.Chart(hourly_df).mark_bar(
        cornerRadiusTopLeft=4,
        cornerRadiusTopRight=4,
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='#0891B2', offset=0),
                alt.GradientStop(color='#1E3A5F', offset=1)
            ],
            x1=1, x2=1, y1=1, y2=0
        )
    ).encode(
        x=alt.X('HOUR:O', axis=alt.Axis(
            title='Hour of Day',
            labelAngle=0,
            labelFontSize=11,
            titleFontSize=12,
            titleFontWeight='bold',
            titleColor='#64748b'
        )),
        y=alt.Y('TRAFFIC_COUNT:Q', axis=alt.Axis(
            title='Traffic Count',
            grid=True,
            gridOpacity=0.3,
            labelFontSize=11,
            titleFontSize=12,
            titleFontWeight='bold',
            titleColor='#64748b',
            format=',.0f'
        )),
        tooltip=[
            alt.Tooltip('HOUR:O', title='Hour'),
            alt.Tooltip('TRAFFIC_COUNT:Q', title='Traffic', format=',')
        ]
    ).properties(height=280)
    
    st.html("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">
                <div class="chart-title-icon" style="background: linear-gradient(135deg, #0891B2, #06B6D4);">🕐</div>
                Hourly Traffic Pattern
            </div>
            <span class="chart-badge live">Live</span>
        </div>
    </div>
    """)
    st.altair_chart(hourly_chart, use_container_width=True)
    st.html('</div>')

with col2:
    st.html('<div class="chart-col-2">')
    daily_df = get_daily_traffic(selected_cities)
    
    # Create area chart with line for daily traffic
    daily_area = alt.Chart(daily_df).mark_area(
        line={'color': FUSION_BLUE, 'strokeWidth': 3},
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='rgba(30, 58, 95, 0.4)', offset=0),
                alt.GradientStop(color='rgba(30, 58, 95, 0.05)', offset=1)
            ],
            x1=1, x2=1, y1=1, y2=0
        )
    ).encode(
        x=alt.X('DATE:T', axis=alt.Axis(
            title='Date',
            labelAngle=-45,
            labelFontSize=10,
            titleFontSize=12,
            titleFontWeight='bold',
            titleColor='#64748b',
            format='%b %d'
        )),
        y=alt.Y('TRAFFIC_COUNT:Q', axis=alt.Axis(
            title='Traffic Count',
            grid=True,
            gridOpacity=0.3,
            labelFontSize=11,
            titleFontSize=12,
            titleFontWeight='bold',
            titleColor='#64748b',
            format=',.0f'
        )),
        tooltip=[
            alt.Tooltip('DATE:T', title='Date', format='%B %d, %Y'),
            alt.Tooltip('TRAFFIC_COUNT:Q', title='Traffic', format=',')
        ]
    ).properties(height=280)
    
    daily_points = alt.Chart(daily_df).mark_circle(size=60, color=FUSION_TEAL).encode(
        x='DATE:T',
        y='TRAFFIC_COUNT:Q'
    )
    
    st.html("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">
                <div class="chart-title-icon" style="background: linear-gradient(135deg, #1E3A5F, #334155);">📅</div>
                Daily Traffic Trend
            </div>
            <span class="chart-badge trend">Trend</span>
        </div>
    </div>
    """)
    st.altair_chart(daily_area + daily_points, use_container_width=True)
    st.html('</div>')

# =============================================================================
# DEMOGRAPHIC ANALYSIS
# =============================================================================
st.html("""
<div class="section-header" style="animation-delay: 0.3s;">
    <div class="section-icon demo">👥</div>
    <h2 class="section-title">Demographic Analysis</h2>
    <div class="section-line"></div>
</div>
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.html('<div class="chart-col-1">')
    nat_df = get_nationality_breakdown(selected_cities)
    
    nat_chart = alt.Chart(nat_df).mark_bar(
        cornerRadiusTopRight=6,
        cornerRadiusBottomRight=6,
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='#0891B2', offset=0),
                alt.GradientStop(color='#06B6D4', offset=1)
            ],
            x1=0, x2=1, y1=0, y2=0
        )
    ).encode(
        y=alt.Y('NATIONALITY:N', axis=alt.Axis(
            title=None,
            labelFontSize=11
        ), sort='-x'),
        x=alt.X('COUNT:Q', axis=alt.Axis(
            title='Count',
            grid=True,
            gridOpacity=0.3,
            format=',.0f'
        )),
        tooltip=[
            alt.Tooltip('NATIONALITY:N', title='Nationality'),
            alt.Tooltip('COUNT:Q', title='Count', format=',')
        ]
    ).properties(height=300)
    
    st.html("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">
                <div class="chart-title-icon" style="background: linear-gradient(135deg, #0891B2, #06B6D4);">🌍</div>
                Top Nationalities
            </div>
        </div>
    </div>
    """)
    st.altair_chart(nat_chart, use_container_width=True)
    st.html('</div>')

with col2:
    st.html('<div class="chart-col-2">')
    age_df = get_age_breakdown(selected_cities)
    
    age_chart = alt.Chart(age_df).mark_bar(
        cornerRadiusTopLeft=6,
        cornerRadiusTopRight=6,
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='#8B5CF6', offset=0),
                alt.GradientStop(color='#A78BFA', offset=1)
            ],
            x1=1, x2=1, y1=1, y2=0
        )
    ).encode(
        x=alt.X('AGE_GROUP:N', axis=alt.Axis(
            title='Age Group',
            labelAngle=-45,
            labelFontSize=10,
            titleFontSize=12,
            titleFontWeight='bold',
            titleColor='#64748b'
        ), sort=None),
        y=alt.Y('COUNT:Q', axis=alt.Axis(
            title='Count',
            grid=True,
            gridOpacity=0.3,
            format=',.0f'
        )),
        tooltip=[
            alt.Tooltip('AGE_GROUP:N', title='Age Group'),
            alt.Tooltip('COUNT:Q', title='Count', format=',')
        ]
    ).properties(height=300)
    
    st.html("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">
                <div class="chart-title-icon" style="background: linear-gradient(135deg, #8B5CF6, #A78BFA);">📊</div>
                Age Distribution
            </div>
        </div>
    </div>
    """)
    st.altair_chart(age_chart, use_container_width=True)
    st.html('</div>')

with col3:
    st.html('<div class="chart-col-3">')
    gender_df = get_gender_breakdown(selected_cities)
    
    # Create donut chart for gender
    gender_chart = alt.Chart(gender_df).mark_arc(
        innerRadius=50,
        outerRadius=90,
        cornerRadius=4
    ).encode(
        theta=alt.Theta('COUNT:Q'),
        color=alt.Color('GENDER:N', scale=alt.Scale(
            domain=gender_df['GENDER'].tolist(),
            range=['#1E3A5F', '#0891B2', '#D4AF37']
        ), legend=alt.Legend(
            title=None,
            orient='bottom',
            labelFontSize=11
        )),
        tooltip=[
            alt.Tooltip('GENDER:N', title='Gender'),
            alt.Tooltip('COUNT:Q', title='Count', format=',')
        ]
    ).properties(height=300)
    
    st.html("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">
                <div class="chart-title-icon" style="background: linear-gradient(135deg, #1E3A5F, #0891B2);">⚤</div>
                Gender Split
            </div>
        </div>
    </div>
    """)
    st.altair_chart(gender_chart, use_container_width=True)
    st.html('</div>')

# =============================================================================
# SUBSCRIPTION TYPE
# =============================================================================
col1, col2 = st.columns(2)

with col1:
    sub_df = get_subscription_breakdown(selected_cities)
    
    sub_chart = alt.Chart(sub_df).mark_arc(
        innerRadius=50,
        outerRadius=90,
        cornerRadius=4
    ).encode(
        theta=alt.Theta('COUNT:Q'),
        color=alt.Color('SUBSCRIPTION_TYPE:N', scale=alt.Scale(
            range=['#10B981', '#34D399', '#6EE7B7', '#A7F3D0']
        ), legend=alt.Legend(
            title=None,
            orient='bottom',
            labelFontSize=11
        )),
        tooltip=[
            alt.Tooltip('SUBSCRIPTION_TYPE:N', title='Type'),
            alt.Tooltip('COUNT:Q', title='Count', format=',')
        ]
    ).properties(height=280)
    
    st.html("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">
                <div class="chart-title-icon" style="background: linear-gradient(135deg, #10B981, #34D399);">📱</div>
                Subscription Types
            </div>
        </div>
    </div>
    """)
    st.altair_chart(sub_chart, use_container_width=True)

# =============================================================================
# DWELL TIME ANALYSIS
# =============================================================================
st.html("""
<div class="section-header" style="animation-delay: 0.4s;">
    <div class="section-icon dwell">⏱️</div>
    <h2 class="section-title">Dwell Time Hotspots</h2>
    <div class="section-line"></div>
</div>
""")

dwell_df = get_dwell_time_by_city()

dwell_chart = alt.Chart(dwell_df).mark_bar(
    cornerRadiusTopLeft=6,
    cornerRadiusTopRight=6
).encode(
    x=alt.X('CITY:N', axis=alt.Axis(
        title='City',
        labelAngle=-45,
        labelFontSize=10,
        titleFontSize=12,
        titleFontWeight='bold',
        titleColor='#64748b'
    ), sort='-y'),
    y=alt.Y('AVG_DWELL_TIME:Q', axis=alt.Axis(
        title='Average Dwell Time (minutes)',
        grid=True,
        gridOpacity=0.3,
        titleFontSize=12,
        titleFontWeight='bold',
        titleColor='#64748b'
    )),
    color=alt.Color('AVG_DWELL_TIME:Q', scale=alt.Scale(
        scheme='goldorange'
    ), legend=None),
    tooltip=[
        alt.Tooltip('CITY:N', title='City'),
        alt.Tooltip('AVG_DWELL_TIME:Q', title='Avg Dwell Time', format='.1f'),
        alt.Tooltip('OBSERVATIONS:Q', title='Observations', format=',')
    ]
).properties(height=350)

st.html("""
<div class="chart-card">
    <div class="chart-header">
        <div class="chart-title">
            <div class="chart-title-icon" style="background: linear-gradient(135deg, #D4AF37, #F59E0B);">📍</div>
            Average Dwell Time by City
        </div>
        <span class="chart-badge" style="background: linear-gradient(135deg, #D4AF37, #F59E0B); color: white;">Minutes</span>
    </div>
</div>
""")
st.altair_chart(dwell_chart, use_container_width=True)

# =============================================================================
# ORIGIN-DESTINATION
# =============================================================================
st.html("""
<div class="section-header" style="animation-delay: 0.5s;">
    <div class="section-icon od">🔄</div>
    <h2 class="section-title">Origin-Destination Analysis</h2>
    <div class="section-line"></div>
</div>
""")

od_df = get_origin_destination(selected_cities)

st.html("""
<div class="chart-card">
    <div class="chart-header">
        <div class="chart-title">
            <div class="chart-title-icon" style="background: linear-gradient(135deg, #10B981, #34D399);">🏠</div>
            Visitor Distribution by Home City
        </div>
    </div>
</div>
""")

st.dataframe(
    od_df,
    use_container_width=True,
    hide_index=True,
    height=300,
    column_config={
        "HOME_CITY": st.column_config.TextColumn("Home City", width="medium"),
        "VISITORS": st.column_config.NumberColumn("Visitors", format="%d", width="small")
    }
)
