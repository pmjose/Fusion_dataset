import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Data Export | Fusion", page_icon=":material/download:", layout="wide")

st.logo("logo.jpg")

st.html("""
<style>
    /* SIDEBAR STYLING */
    @keyframes sidebarFadeIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 4px 15px rgba(8, 145, 178, 0.2); }
        50% { box-shadow: 0 4px 25px rgba(8, 145, 178, 0.4); }
    }
    @keyframes navItemSlide {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #0f172a 100%) !important;
        border-right: 1px solid rgba(8, 145, 178, 0.2) !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(ellipse at top left, rgba(8, 145, 178, 0.08) 0%, transparent 50%),
                    radial-gradient(ellipse at bottom right, rgba(212, 175, 55, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    [data-testid="stSidebar"] > div:first-child { position: relative; z-index: 1; }
    [data-testid="stSidebar"] [data-testid="stLogo"] { animation: sidebarFadeIn 0.5s ease-out; }
    [data-testid="stSidebar"] [data-testid="stLogo"] img {
        border-radius: 12px !important;
        padding: 8px !important;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
        animation: glowPulse 3s ease-in-out infinite;
    }
    [data-testid="stSidebar"] [data-testid="stLogo"] img:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 30px rgba(8, 145, 178, 0.4), 0 0 0 2px rgba(8, 145, 178, 0.3) !important;
    }
    [data-testid="stSidebar"] a {
        color: #ffffff !important;
        font-weight: 500 !important;
        padding: 0.75rem 1rem !important;
        border-radius: 10px !important;
        margin: 0.25rem 0.5rem !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
        animation: navItemSlide 0.4s ease-out backwards;
    }
    [data-testid="stSidebar"] a:nth-child(1) { animation-delay: 0.1s; }
    [data-testid="stSidebar"] a:nth-child(2) { animation-delay: 0.15s; }
    [data-testid="stSidebar"] a:nth-child(3) { animation-delay: 0.2s; }
    [data-testid="stSidebar"] a:nth-child(4) { animation-delay: 0.25s; }
    [data-testid="stSidebar"] a:nth-child(5) { animation-delay: 0.3s; }
    [data-testid="stSidebar"] a:nth-child(6) { animation-delay: 0.35s; }
    [data-testid="stSidebar"] a::before {
        content: '';
        position: absolute;
        left: 0; top: 0;
        height: 100%; width: 0;
        background: linear-gradient(90deg, rgba(8, 145, 178, 0.3), transparent);
        transition: width 0.3s ease;
        border-radius: 10px;
    }
    [data-testid="stSidebar"] a:hover {
        background: linear-gradient(135deg, rgba(8, 145, 178, 0.2) 0%, rgba(30, 58, 95, 0.3) 100%) !important;
        color: #ffffff !important;
        transform: translateX(4px);
    }
    [data-testid="stSidebar"] a:hover::before {
        width: 4px;
        background: linear-gradient(180deg, #0891B2, #D4AF37);
    }
    [data-testid="stSidebar"] a[aria-current="page"] {
        background: linear-gradient(135deg, rgba(8, 145, 178, 0.25) 0%, rgba(30, 58, 95, 0.4) 100%) !important;
        color: #ffffff !important;
        border-left: 3px solid #0891B2 !important;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown p { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #f1f5f9 !important; font-weight: 600 !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(8, 145, 178, 0.2) !important; margin: 1rem 0 !important; }
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(8, 145, 178, 0.3) !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div:hover,
    [data-testid="stSidebar"] .stMultiSelect > div > div:hover {
        border-color: #0891B2 !important;
        box-shadow: 0 0 0 2px rgba(8, 145, 178, 0.15) !important;
    }
    [data-testid="stSidebar"] .stCaption { color: #64748b !important; font-size: 0.75rem !important; }
    
    /* PAGE STYLING */
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
