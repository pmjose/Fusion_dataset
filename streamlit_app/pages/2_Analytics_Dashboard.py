import streamlit as st
import altair as alt
import pandas as pd
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Analytics Dashboard | Fusion", page_icon="logo.jpg", layout="wide")

st.logo("logo.jpg")

FUSION_BLUE = "#1E3A5F"
FUSION_TEAL = "#0891B2"
FUSION_GOLD = "#D4AF37"

st.html("""
<style>
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
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
        box-shadow: 0 10px 40px rgba(30, 58, 95, 0.25);
    }
    .page-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M20 20h20v20H20V20zM0 0h20v20H0V0z'/%3E%3C/g%3E%3C/svg%3E");
    }
    .page-header h1 { margin: 0; font-size: 2rem; font-weight: 700; position: relative; z-index: 1; }
    .page-header p { margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1rem; position: relative; z-index: 1; }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2rem 0 1rem 0;
        animation: slideIn 0.5s ease-out;
    }
    .section-header h3 {
        color: #1E3A5F;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0;
    }
    .section-line {
        flex: 1;
        height: 2px;
        background: linear-gradient(90deg, #e2e8f0, transparent);
    }
    
    .chart-container {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out backwards;
    }
    .chart-container:hover {
        box-shadow: 0 10px 30px rgba(30, 58, 95, 0.1);
        border-color: #0891B2;
    }
    .chart-title {
        color: #1E3A5F;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
        animation: fadeInUp 0.6s ease-out 0.1s backwards;
    }
    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #1E3A5F, #0891B2);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(30, 58, 95, 0.1);
    }
    .metric-card:hover::before {
        transform: scaleX(1);
    }
</style>
""")

st.html("""
<div class="page-header">
    <h1>Analytics Dashboard</h1>
    <p>Insights from Saudi telco mobility data</p>
</div>
""")

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

cities_df = get_cities()

with st.sidebar:
    st.html("""
    <div style="color: #1E3A5F; font-weight: 600; font-size: 1rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
        <span style="font-size: 1.2rem;">🎯</span> Filters
    </div>
    """)
    selected_cities = st.multiselect(
        "Filter by city",
        options=cities_df['SUBSCRIBER_HOME_CITY'].tolist(),
        default=[]
    )

metrics_df = get_summary_metrics(selected_cities)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Records", f"{metrics_df['TOTAL_RECORDS'].iloc[0]:,}", border=True)
with col2:
    st.metric("Unique Hexagons", f"{metrics_df['UNIQUE_HEXAGONS'].iloc[0]:,}", border=True)
with col3:
    st.metric("Avg Dwell Time", f"{metrics_df['AVG_DWELL'].iloc[0]:.1f} min", border=True)
with col4:
    st.metric("Nationalities", f"{metrics_df['NATIONALITIES'].iloc[0]}", border=True)

st.html("""
<div class="section-header">
    <h3>📈 Foot Traffic Trends</h3>
    <div class="section-line"></div>
</div>
""")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("**Hourly Traffic Pattern**")
        hourly_df = get_hourly_traffic(selected_cities)
        
        hourly_chart = alt.Chart(hourly_df).mark_bar(
            cornerRadiusTopLeft=6,
            cornerRadiusTopRight=6,
            color=FUSION_TEAL
        ).encode(
            x=alt.X('HOUR:O', 
                    axis=alt.Axis(title='Hour of Day', labelAngle=0, grid=False),
                    scale=alt.Scale(padding=0.1)),
            y=alt.Y('TRAFFIC_COUNT:Q', 
                    axis=alt.Axis(title='Traffic Count', grid=True, gridOpacity=0.3)),
            tooltip=[
                alt.Tooltip('HOUR:O', title='Hour'),
                alt.Tooltip('TRAFFIC_COUNT:Q', title='Traffic', format=',')
            ]
        ).properties(
            height=320
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            labelFontSize=11,
            titleFontSize=12,
            titleColor=FUSION_BLUE,
            labelColor='#64748b'
        )
        
        st.altair_chart(hourly_chart, use_container_width=True)

with col2:
    with st.container(border=True):
        st.markdown("**Daily Traffic Trend**")
        daily_df = get_daily_traffic(selected_cities)
        
        daily_chart = alt.Chart(daily_df).mark_area(
            line={'color': FUSION_BLUE, 'strokeWidth': 2},
            color=alt.Gradient(
                gradient='linear',
                stops=[
                    alt.GradientStop(color='rgba(30, 58, 95, 0.4)', offset=0),
                    alt.GradientStop(color='rgba(30, 58, 95, 0.05)', offset=1)
                ],
                x1=1, x2=1, y1=1, y2=0
            )
        ).encode(
            x=alt.X('DATE:T', 
                    axis=alt.Axis(title='Date', format='%b %d', grid=False)),
            y=alt.Y('TRAFFIC_COUNT:Q', 
                    axis=alt.Axis(title='Traffic Count', grid=True, gridOpacity=0.3)),
            tooltip=[
                alt.Tooltip('DATE:T', title='Date', format='%B %d, %Y'),
                alt.Tooltip('TRAFFIC_COUNT:Q', title='Traffic', format=',')
            ]
        ).properties(
            height=320
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            labelFontSize=11,
            titleFontSize=12,
            titleColor=FUSION_BLUE,
            labelColor='#64748b'
        )
        
        st.altair_chart(daily_chart, use_container_width=True)

st.html("""
<div class="section-header">
    <h3>👥 Demographic Analysis</h3>
    <div class="section-line"></div>
</div>
""")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("**Top Nationalities**")
        nat_df = get_nationality_breakdown(selected_cities)
        
        nat_chart = alt.Chart(nat_df).mark_bar(
            cornerRadiusTopRight=6,
            cornerRadiusBottomRight=6,
            color=FUSION_TEAL
        ).encode(
            x=alt.X('COUNT:Q', 
                    axis=alt.Axis(title='Count', grid=True, gridOpacity=0.3)),
            y=alt.Y('NATIONALITY:N', 
                    axis=alt.Axis(title=None, grid=False),
                    sort='-x'),
            tooltip=[
                alt.Tooltip('NATIONALITY:N', title='Nationality'),
                alt.Tooltip('COUNT:Q', title='Count', format=',')
            ]
        ).properties(
            height=320
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            labelFontSize=11,
            titleFontSize=12,
            titleColor=FUSION_BLUE,
            labelColor='#64748b'
        )
        
        st.altair_chart(nat_chart, use_container_width=True)

with col2:
    with st.container(border=True):
        st.markdown("**Age Distribution**")
        age_df = get_age_breakdown(selected_cities)
        
        age_chart = alt.Chart(age_df).mark_bar(
            cornerRadiusTopLeft=6,
            cornerRadiusTopRight=6,
            color=FUSION_BLUE
        ).encode(
            x=alt.X('AGE_GROUP:N', 
                    axis=alt.Axis(title='Age Group', labelAngle=-45, grid=False),
                    sort=['18-24', '25-34', '35-44', '45-54', '55-64', '65+']),
            y=alt.Y('COUNT:Q', 
                    axis=alt.Axis(title='Count', grid=True, gridOpacity=0.3)),
            tooltip=[
                alt.Tooltip('AGE_GROUP:N', title='Age Group'),
                alt.Tooltip('COUNT:Q', title='Count', format=',')
            ]
        ).properties(
            height=320
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            labelFontSize=11,
            titleFontSize=12,
            titleColor=FUSION_BLUE,
            labelColor='#64748b'
        )
        
        st.altair_chart(age_chart, use_container_width=True)

with col3:
    with st.container(border=True):
        st.markdown("**Gender & Subscription Split**")
        
        gender_df = get_gender_breakdown(selected_cities)
        sub_df = get_subscription_breakdown(selected_cities)
        
        gender_chart = alt.Chart(gender_df).mark_arc(
            innerRadius=50,
            outerRadius=80,
            stroke='white',
            strokeWidth=2
        ).encode(
            theta=alt.Theta('COUNT:Q'),
            color=alt.Color('GENDER:N', 
                           scale=alt.Scale(domain=['Male', 'Female'], 
                                          range=[FUSION_BLUE, FUSION_TEAL]),
                           legend=alt.Legend(title='Gender', orient='bottom')),
            tooltip=[
                alt.Tooltip('GENDER:N', title='Gender'),
                alt.Tooltip('COUNT:Q', title='Count', format=',')
            ]
        ).properties(
            height=150,
            title=alt.TitleParams(text='Gender', fontSize=12, color=FUSION_BLUE)
        )
        
        sub_chart = alt.Chart(sub_df).mark_arc(
            innerRadius=50,
            outerRadius=80,
            stroke='white',
            strokeWidth=2
        ).encode(
            theta=alt.Theta('COUNT:Q'),
            color=alt.Color('SUBSCRIPTION_TYPE:N', 
                           scale=alt.Scale(domain=['Prepaid', 'Postpaid'], 
                                          range=[FUSION_GOLD, FUSION_BLUE]),
                           legend=alt.Legend(title='Type', orient='bottom')),
            tooltip=[
                alt.Tooltip('SUBSCRIPTION_TYPE:N', title='Type'),
                alt.Tooltip('COUNT:Q', title='Count', format=',')
            ]
        ).properties(
            height=150,
            title=alt.TitleParams(text='Subscription', fontSize=12, color=FUSION_BLUE)
        )
        
        combined = alt.vconcat(gender_chart, sub_chart).configure_view(strokeWidth=0)
        st.altair_chart(combined, use_container_width=True)

st.html("""
<div class="section-header">
    <h3>⏱️ Dwell Time Analysis</h3>
    <div class="section-line"></div>
</div>
""")

with st.container(border=True):
    st.markdown("**Average Dwell Time by City**")
    dwell_df = get_dwell_time_by_city()
    
    dwell_chart = alt.Chart(dwell_df).mark_bar(
        cornerRadiusTopLeft=6,
        cornerRadiusTopRight=6
    ).encode(
        x=alt.X('CITY:N', 
                axis=alt.Axis(title='City', labelAngle=-45, grid=False),
                sort='-y'),
        y=alt.Y('AVG_DWELL_TIME:Q', 
                axis=alt.Axis(title='Average Dwell Time (minutes)', grid=True, gridOpacity=0.3)),
        color=alt.Color('AVG_DWELL_TIME:Q',
                       scale=alt.Scale(scheme='teals'),
                       legend=None),
        tooltip=[
            alt.Tooltip('CITY:N', title='City'),
            alt.Tooltip('AVG_DWELL_TIME:Q', title='Avg Dwell Time', format='.1f'),
            alt.Tooltip('OBSERVATIONS:Q', title='Observations', format=',')
        ]
    ).properties(
        height=350
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        labelFontSize=11,
        titleFontSize=12,
        titleColor=FUSION_BLUE,
        labelColor='#64748b'
    )
    
    st.altair_chart(dwell_chart, use_container_width=True)

st.html("""
<div class="section-header">
    <h3>🔄 Visitor Distribution</h3>
    <div class="section-line"></div>
</div>
""")

with st.container(border=True):
    st.markdown("**Visitor Distribution by Home City**")
    od_df = get_origin_destination(selected_cities)
    st.dataframe(
        od_df,
        use_container_width=True,
        hide_index=True,
        height=300,
        column_config={
            "HOME_CITY": st.column_config.TextColumn("Home City", width="medium"),
            "VISITORS": st.column_config.ProgressColumn(
                "Visitors",
                format="%d",
                min_value=0,
                max_value=int(od_df['VISITORS'].max())
            )
        }
    )
