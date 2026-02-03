import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Data Export | Fusion", page_icon=":material/download:", layout="wide")

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
    .enterprise-cta {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 2px solid #0891B2;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
    }
    .enterprise-cta h3 { color: #1E3A5F; margin: 0 0 0.5rem 0; }
    .enterprise-cta p { color: #64748b; margin: 0; }
</style>
""")

st.html("""
<div class="page-header">
    <h1>Data Export</h1>
    <p>Select and download mobility data packages</p>
</div>
""")

@st.cache_data(ttl=600)
def get_filter_options():
    session = get_active_session()
    cities = session.sql("SELECT DISTINCT SUBSCRIBER_HOME_CITY FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    nationalities = session.sql("SELECT DISTINCT NATIONALITY FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    age_groups = session.sql("SELECT DISTINCT AGE_GROUP FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    dates = session.sql("SELECT MIN(DATE) as MIN_DATE, MAX(DATE) as MAX_DATE FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA").to_pandas()
    return cities, nationalities, age_groups, dates

@st.cache_data(ttl=300)
def get_record_count(cities, nationalities, age_groups, genders, sub_types, date_range):
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
    if date_range:
        where_clauses.append(f"DATE BETWEEN '{date_range[0]}' AND '{date_range[1]}'")
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    query = f"""
        SELECT COUNT(*) as cnt FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        WHERE {where_sql}
    """
    return session.sql(query).to_pandas()['CNT'].iloc[0]

@st.cache_data(ttl=300)
def get_sample_data(cities, nationalities, age_groups, genders, sub_types, date_range, limit=100):
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
    if date_range:
        where_clauses.append(f"DATE BETWEEN '{date_range[0]}' AND '{date_range[1]}'")
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    query = f"""
        SELECT * FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        WHERE {where_sql}
        LIMIT {limit}
    """
    return session.sql(query).to_pandas()

@st.cache_data(ttl=60)
def get_export_data(cities, nationalities, age_groups, genders, sub_types, date_range, limit=100000):
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
    if date_range:
        where_clauses.append(f"DATE BETWEEN '{date_range[0]}' AND '{date_range[1]}'")
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    query = f"""
        SELECT * FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        WHERE {where_sql}
        LIMIT {limit}
    """
    return session.sql(query).to_pandas()

cities_df, nationalities_df, age_groups_df, dates_df = get_filter_options()
min_date = dates_df['MIN_DATE'].iloc[0]
max_date = dates_df['MAX_DATE'].iloc[0]



st.subheader(":material/settings: Configure data package", anchor=False)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("**:material/location_on: Geographic & Temporal**")
        
        selected_cities = st.multiselect(
            "Cities",
            options=cities_df['SUBSCRIBER_HOME_CITY'].tolist(),
            default=[],
            help="Leave empty for all cities"
        )
        
        date_range = st.date_input(
            "Date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

with col2:
    with st.container(border=True):
        st.markdown("**:material/person: Demographic filters**")
        
        selected_nationalities = st.multiselect(
            "Nationalities",
            options=nationalities_df['NATIONALITY'].tolist(),
            default=[],
            help="Leave empty for all nationalities"
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

record_count = get_record_count(
    selected_cities, selected_nationalities, selected_age_groups,
    selected_genders, selected_sub_types, date_range
)

st.subheader(":material/summarize: Data package summary", anchor=False)

cities_label = ", ".join(selected_cities) if selected_cities else "All Cities"
with st.container(horizontal=True):
    st.metric("Total records", f"{record_count:,}", border=True)
    st.metric("Coverage", cities_label[:25] + "..." if len(cities_label) > 25 else cities_label, border=True)
    st.metric("Date range", f"{date_range[0]} to {date_range[1]}", border=True)

st.subheader(":material/preview: Sample preview", anchor=False)
with st.container(border=True):
    sample_df = get_sample_data(
        selected_cities, selected_nationalities, selected_age_groups,
        selected_genders, selected_sub_types, date_range
    )
    st.dataframe(sample_df, use_container_width=True, height=250, hide_index=True)
    st.caption("Showing first 100 records as preview")

st.subheader(":material/file_download: Export data", anchor=False)

with st.container(border=True):
    terms_accepted = st.checkbox(
        "I agree to the data usage terms",
        help="This data is for analytical purposes only. Redistribution or resale is prohibited. Data must not be used for individual identification."
    )

    if terms_accepted:
        col1, col2 = st.columns([1, 2])
        with col1:
            export_limit = st.selectbox(
                "Export limit",
                options=[10000, 50000, 100000],
                index=0,
                help="Maximum records per export"
            )
        
        with col2:
            if st.button("Prepare export", type="primary", icon=":material/download:", use_container_width=True):
                with st.spinner("Preparing data export..."):
                    export_df = get_export_data(
                        selected_cities, selected_nationalities, selected_age_groups,
                        selected_genders, selected_sub_types, date_range, limit=export_limit
                    )
                    
                    csv_data = export_df.to_csv(index=False)
                    
                    st.download_button(
                        label=f"Download CSV ({len(export_df):,} records)",
                        data=csv_data,
                        file_name="fusion_mobility_export.csv",
                        mime="text/csv",
                        icon=":material/download:",
                        use_container_width=True
                    )
                    
                    st.success(f"Export ready! {len(export_df):,} records prepared for download.", icon=":material/check_circle:")
    else:
        st.caption("Please accept the data usage terms to proceed with export.")

st.html("""
<div class="enterprise-cta">
    <h3>:material/business: Need full dataset access?</h3>
    <p>For enterprise data sharing with unlimited records and real-time access,<br/>
    contact our sales team to set up a Snowflake Data Share or Marketplace listing.</p>
</div>
""")
