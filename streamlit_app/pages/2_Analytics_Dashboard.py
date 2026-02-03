import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Analytics Dashboard | Fusion", page_icon=":material/bar_chart:", layout="wide")

st.logo("logo.jpg")

st.html("""
<style>
    .page-header {
        background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 100%);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .page-header h1 { margin: 0; font-size: 1.8rem; }
    .page-header p { margin: 0.3rem 0 0 0; opacity: 0.9; font-size: 0.95rem; }
    .section-title {
        color: #1E3A5F;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
</style>
""")

st.html("""
<div class="page-header">
    <h1>Analytics Dashboard</h1>
    <p>Sellable insights from Saudi telco mobility data</p>
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

cities_df = get_cities()

with st.sidebar:
    st.subheader(":material/filter_list: Filters", anchor=False)
    selected_cities = st.multiselect(
        "Filter by city",
        options=cities_df['SUBSCRIBER_HOME_CITY'].tolist(),
        default=[]
    )

metrics_df = get_summary_metrics(selected_cities)
with st.container(horizontal=True):
    st.metric("Total records", f"{metrics_df['TOTAL_RECORDS'].iloc[0]:,}", border=True)
    st.metric("Unique hexagons", f"{metrics_df['UNIQUE_HEXAGONS'].iloc[0]:,}", border=True)
    st.metric("Avg dwell time", f"{metrics_df['AVG_DWELL'].iloc[0]:.1f} min", border=True)
    st.metric("Nationalities", f"{metrics_df['NATIONALITIES'].iloc[0]}", border=True)

st.subheader(":material/trending_up: Foot traffic trends", anchor=False)
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("**Hourly traffic pattern**")
        hourly_df = get_hourly_traffic(selected_cities)
        st.bar_chart(hourly_df, x='HOUR', y='TRAFFIC_COUNT', color="#0891B2", height=300)

with col2:
    with st.container(border=True):
        st.markdown("**Daily traffic trend**")
        daily_df = get_daily_traffic(selected_cities)
        st.line_chart(daily_df, x='DATE', y='TRAFFIC_COUNT', color="#1E3A5F", height=300)

st.subheader(":material/groups: Demographic analysis", anchor=False)
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("**Top nationalities**")
        nat_df = get_nationality_breakdown(selected_cities)
        st.bar_chart(nat_df, x='NATIONALITY', y='COUNT', color="#0891B2", horizontal=True, height=300)

with col2:
    with st.container(border=True):
        st.markdown("**Age distribution**")
        age_df = get_age_breakdown(selected_cities)
        st.bar_chart(age_df, x='AGE_GROUP', y='COUNT', color="#1E3A5F", height=300)

with col3:
    with st.container(border=True):
        st.markdown("**Gender split**")
        gender_df = get_gender_breakdown(selected_cities)
        st.bar_chart(gender_df, x='GENDER', y='COUNT', color="#0891B2", height=300)

st.subheader(":material/schedule: Dwell time hotspots", anchor=False)
with st.container(border=True):
    st.markdown("**Average dwell time by city (minutes)**")
    dwell_df = get_dwell_time_by_city()
    st.bar_chart(dwell_df, x='CITY', y='AVG_DWELL_TIME', color="#D4AF37", height=300)

st.subheader(":material/swap_horiz: Origin-destination analysis", anchor=False)
with st.container(border=True):
    st.markdown("**Visitor distribution by home city**")
    od_df = get_origin_destination(selected_cities)
    st.dataframe(od_df, use_container_width=True, hide_index=True, height=300)
