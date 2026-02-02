import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Data Explorer | Fusion", page_icon="logo.jpg", layout="wide")

st.logo("logo.jpg")

st.html("""
<style>
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
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
    
    .metrics-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.6s ease-out 0.2s backwards;
    }
    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(30, 58, 95, 0.1);
        border-color: #0891B2;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E3A5F;
        margin: 0;
    }
    .metric-value.highlight {
        background: linear-gradient(135deg, #0891B2, #1E3A5F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .metric-label {
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 0.25rem;
    }
    
    .filter-section {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        animation: slideInRight 0.5s ease-out;
    }
    .filter-title {
        color: #1E3A5F;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .data-container {
        animation: fadeInUp 0.6s ease-out;
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    .loading-pulse {
        animation: pulse 1.5s ease-in-out infinite;
    }
</style>
""")

st.html("""
<div class="page-header">
    <h1>Data Explorer</h1>
    <p>Browse and filter Saudi telco mobility data</p>
</div>
""")

@st.cache_data(ttl=600)
def get_filter_options():
    session = get_active_session()
    cities = session.sql("SELECT DISTINCT SUBSCRIBER_HOME_CITY FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    nationalities = session.sql("SELECT DISTINCT NATIONALITY FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    age_groups = session.sql("SELECT DISTINCT AGE_GROUP FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    genders = session.sql("SELECT DISTINCT GENDER FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    sub_types = session.sql("SELECT DISTINCT SUBSCRIPTION_TYPE FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    return cities, nationalities, age_groups, genders, sub_types

@st.cache_data(ttl=300)
def get_filtered_data(cities, nationalities, age_groups, genders, sub_types, hour_range, limit=10000):
    session = get_active_session()
    
    where_clauses = []
    if cities:
        city_list = "','".join(cities)
        where_clauses.append(f"SUBSCRIBER_HOME_CITY IN ('{city_list}')")
    if nationalities:
        nat_list = "','".join(nationalities)
        where_clauses.append(f"NATIONALITY IN ('{nat_list}')")
    if age_groups:
        age_list = "','".join(age_groups)
        where_clauses.append(f"AGE_GROUP IN ('{age_list}')")
    if genders:
        gender_list = "','".join(genders)
        where_clauses.append(f"GENDER IN ('{gender_list}')")
    if sub_types:
        sub_list = "','".join(sub_types)
        where_clauses.append(f"SUBSCRIPTION_TYPE IN ('{sub_list}')")
    
    where_clauses.append(f"HOUR BETWEEN {hour_range[0]} AND {hour_range[1]}")
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    query = f"""
        SELECT * FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        WHERE {where_sql}
        LIMIT {limit}
    """
    return session.sql(query).to_pandas()

@st.cache_data(ttl=300)
def get_record_count(cities, nationalities, age_groups, genders, sub_types, hour_range):
    session = get_active_session()
    
    where_clauses = []
    if cities:
        city_list = "','".join(cities)
        where_clauses.append(f"SUBSCRIBER_HOME_CITY IN ('{city_list}')")
    if nationalities:
        nat_list = "','".join(nationalities)
        where_clauses.append(f"NATIONALITY IN ('{nat_list}')")
    if age_groups:
        age_list = "','".join(age_groups)
        where_clauses.append(f"AGE_GROUP IN ('{age_list}')")
    if genders:
        gender_list = "','".join(genders)
        where_clauses.append(f"GENDER IN ('{gender_list}')")
    if sub_types:
        sub_list = "','".join(sub_types)
        where_clauses.append(f"SUBSCRIPTION_TYPE IN ('{sub_list}')")
    
    where_clauses.append(f"HOUR BETWEEN {hour_range[0]} AND {hour_range[1]}")
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    query = f"""
        SELECT COUNT(*) as cnt FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        WHERE {where_sql}
    """
    return session.sql(query).to_pandas()['CNT'].iloc[0]

cities_df, nationalities_df, age_groups_df, genders_df, sub_types_df = get_filter_options()

with st.sidebar:
    st.html("""
    <div style="color: #1E3A5F; font-weight: 600; font-size: 1rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
        <span style="font-size: 1.2rem;">🔍</span> Filters
    </div>
    """)
    
    selected_cities = st.multiselect(
        "Cities",
        options=cities_df['SUBSCRIBER_HOME_CITY'].tolist(),
        default=[]
    )
    
    selected_nationalities = st.multiselect(
        "Nationalities",
        options=nationalities_df['NATIONALITY'].tolist(),
        default=[]
    )
    
    selected_age_groups = st.multiselect(
        "Age groups",
        options=age_groups_df['AGE_GROUP'].tolist(),
        default=[]
    )
    
    selected_genders = st.multiselect(
        "Gender",
        options=genders_df['GENDER'].tolist(),
        default=[]
    )
    
    selected_sub_types = st.multiselect(
        "Subscription type",
        options=sub_types_df['SUBSCRIPTION_TYPE'].tolist(),
        default=[]
    )
    
    hour_range = st.slider(
        "Hour of day",
        min_value=0,
        max_value=23,
        value=(0, 23)
    )

record_count = get_record_count(
    selected_cities, selected_nationalities, selected_age_groups,
    selected_genders, selected_sub_types, hour_range
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Matching records", f"{record_count:,}", border=True)
with col2:
    filter_count = sum([
        len(selected_cities) > 0,
        len(selected_nationalities) > 0,
        len(selected_age_groups) > 0,
        len(selected_genders) > 0,
        len(selected_sub_types) > 0,
        hour_range != (0, 23)
    ])
    st.metric("Active filters", f"{filter_count}", border=True)
with col3:
    coverage = (record_count / 4245000) * 100
    st.metric("Data coverage", f"{coverage:.1f}%", border=True)

st.divider()

if st.button("Load Data", type="primary", icon=":material/table_view:", use_container_width=True):
    with st.spinner("Loading data..."):
        df = get_filtered_data(
            selected_cities, selected_nationalities, selected_age_groups,
            selected_genders, selected_sub_types, hour_range
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg dwell time", f"{df['AVG_STAYING_DURATION_MIN'].mean():.1f} min", border=True)
        with col2:
            st.metric("Unique hexagons", f"{df['HEXAGON_ID'].nunique():,}", border=True)
        with col3:
            st.metric("Rows loaded", f"{len(df):,}", border=True)
        
        st.dataframe(
            df,
            use_container_width=True,
            height=500,
            hide_index=True,
            column_config={
                "AVG_STAYING_DURATION_MIN": st.column_config.NumberColumn(
                    "Avg Duration (min)",
                    format="%.1f"
                ),
                "DATE": st.column_config.DateColumn("Date"),
                "HEXAGON_ID": st.column_config.TextColumn("Hexagon ID", width="medium")
            }
        )
