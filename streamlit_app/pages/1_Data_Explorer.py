import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Data Explorer | Fusion", page_icon=":material/search:", layout="wide")

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
    return cities, nationalities, age_groups

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

cities_df, nationalities_df, age_groups_df = get_filter_options()

with st.sidebar:
    st.subheader(":material/filter_list: Filters", anchor=False)
    
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
        options=["Male", "Female"],
        default=[]
    )
    
    selected_sub_types = st.multiselect(
        "Subscription type",
        options=["Prepaid", "Postpaid"],
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

st.metric("Matching records", f"{record_count:,}", border=True)

if st.button("Load data", type="primary", icon=":material/download:"):
    with st.spinner("Loading data..."):
        df = get_filtered_data(
            selected_cities, selected_nationalities, selected_age_groups,
            selected_genders, selected_sub_types, hour_range
        )
        
        with st.container(border=True):
            st.dataframe(df, use_container_width=True, height=500, hide_index=True)
        
        with st.container(horizontal=True):
            st.metric("Avg dwell time", f"{df['AVG_STAYING_DURATION_MIN'].mean():.1f} min", border=True)
            st.metric("Unique hexagons", f"{df['HEXAGON_ID'].nunique():,}", border=True)
            st.metric("Rows displayed", f"{len(df):,}", border=True)
