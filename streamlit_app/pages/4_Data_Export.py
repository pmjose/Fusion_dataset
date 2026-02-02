import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Data Export | Fusion", page_icon="logo.jpg", layout="wide")

st.logo("logo.jpg")

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
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
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
    
    .config-card {
        animation: fadeInUp 0.6s ease-out 0.2s backwards;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    .config-card:hover {
        box-shadow: 0 8px 30px rgba(30, 58, 95, 0.1);
    }
    .config-title {
        color: #1E3A5F;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 1rem 0;
        animation: fadeInUp 0.6s ease-out 0.3s backwards;
    }
    .summary-card {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .summary-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(30, 58, 95, 0.1);
        border-color: #0891B2;
    }
    .summary-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1E3A5F;
        margin: 0;
    }
    .summary-label {
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 0.25rem;
    }
    
    .enterprise-cta {
        animation: fadeInUp 0.6s ease-out 0.5s backwards;
        background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-top: 2rem;
        position: relative;
        overflow: hidden;
    }
    .enterprise-cta::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }
    .enterprise-cta h3 {
        color: white;
        margin: 0 0 0.75rem 0;
        font-size: 1.3rem;
        font-weight: 700;
        position: relative;
        z-index: 1;
    }
    .enterprise-cta p {
        color: rgba(255,255,255,0.9);
        margin: 0;
        font-size: 0.95rem;
        position: relative;
        z-index: 1;
        line-height: 1.6;
    }
    
    .terms-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fef9c3 100%);
        border: 1px solid #f59e0b;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
    }
    .terms-box p {
        color: #92400e;
        font-size: 0.9rem;
        margin: 0;
        line-height: 1.5;
    }
    
    .export-success {
        animation: pulse 2s ease-in-out infinite;
    }
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
    genders = session.sql("SELECT DISTINCT GENDER FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    sub_types = session.sql("SELECT DISTINCT SUBSCRIPTION_TYPE FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    dates = session.sql("SELECT MIN(DATE) as MIN_DATE, MAX(DATE) as MAX_DATE FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA").to_pandas()
    return cities, nationalities, age_groups, genders, sub_types, dates

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

cities_df, nationalities_df, age_groups_df, genders_df, sub_types_df, dates_df = get_filter_options()
min_date = dates_df['MIN_DATE'].iloc[0]
max_date = dates_df['MAX_DATE'].iloc[0]

st.html("""
<div class="section-header">
    <h3>⚙️ Configure Data Package</h3>
    <div class="section-line"></div>
</div>
""")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("**📍 Geographic & Temporal**")
        
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
        st.markdown("**👤 Demographic Filters**")
        
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
        
        col_g, col_s = st.columns(2)
        with col_g:
            selected_genders = st.multiselect(
                "Gender",
                options=genders_df['GENDER'].tolist(),
                default=[]
            )
        with col_s:
            selected_sub_types = st.multiselect(
                "Subscription",
                options=sub_types_df['SUBSCRIPTION_TYPE'].tolist(),
                default=[]
            )

record_count = get_record_count(
    selected_cities, selected_nationalities, selected_age_groups,
    selected_genders, selected_sub_types, date_range
)

st.html("""
<div class="section-header">
    <h3>📊 Package Summary</h3>
    <div class="section-line"></div>
</div>
""")

cities_label = ", ".join(selected_cities) if selected_cities else "All Cities"
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Records", f"{record_count:,}", border=True)
with col2:
    st.metric("Coverage", cities_label[:30] + "..." if len(cities_label) > 30 else cities_label, border=True)
with col3:
    st.metric("Date Range", f"{date_range[0]} → {date_range[1]}", border=True)

st.html("""
<div class="section-header">
    <h3>👁️ Sample Preview</h3>
    <div class="section-line"></div>
</div>
""")

with st.container(border=True):
    sample_df = get_sample_data(
        selected_cities, selected_nationalities, selected_age_groups,
        selected_genders, selected_sub_types, date_range
    )
    st.dataframe(
        sample_df,
        use_container_width=True,
        height=250,
        hide_index=True,
        column_config={
            "AVG_STAYING_DURATION_MIN": st.column_config.NumberColumn(
                "Avg Duration (min)",
                format="%.1f"
            ),
            "DATE": st.column_config.DateColumn("Date"),
        }
    )
    st.caption("Showing first 100 records as preview")

st.html("""
<div class="section-header">
    <h3>📥 Export Data</h3>
    <div class="section-line"></div>
</div>
""")

with st.container(border=True):
    st.html("""
    <div class="terms-box">
        <p>⚠️ <strong>Data Usage Terms:</strong> This data is for analytical purposes only. 
        Redistribution or resale is prohibited. Data must not be used for individual identification.</p>
    </div>
    """)
    
    terms_accepted = st.checkbox(
        "I agree to the data usage terms",
        help="You must accept the terms to proceed with export"
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
            if st.button("Prepare Export", type="primary", icon=":material/download:", use_container_width=True):
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
                        icon=":material/file_download:",
                        use_container_width=True
                    )
                    
                    st.success(f"Export ready! {len(export_df):,} records prepared for download.", icon="✅")
    else:
        st.info("Please accept the data usage terms to proceed with export.", icon="ℹ️")

st.html("""
<div class="enterprise-cta">
    <h3>🏢 Need Full Dataset Access?</h3>
    <p>For enterprise data sharing with unlimited records and real-time access,<br/>
    contact our sales team to set up a Snowflake Data Share or Marketplace listing.</p>
</div>
""")
