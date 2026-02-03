import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
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
    .insight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1rem;
    }
    .insight-card h3 { margin: 0 0 0.5rem 0; font-size: 1.1rem; }
    .insight-card p { margin: 0; opacity: 0.9; font-size: 0.9rem; }
    .insight-metric {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
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

tab_overview, tab_demographics, tab_insights = st.tabs(["📊 Overview", "👥 Demographics", "✨ Insights"])

with tab_overview:
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

with tab_demographics:
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

with tab_insights:
    
    @st.cache_data(ttl=600)
    def get_hourly_by_city():
        session = get_active_session()
        query = """
            SELECT SUBSCRIBER_HOME_CITY as CITY, HOUR, COUNT(*) as TRAFFIC
            FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
            GROUP BY SUBSCRIBER_HOME_CITY, HOUR
            ORDER BY SUBSCRIBER_HOME_CITY, HOUR
        """
        return session.sql(query).to_pandas()

    @st.cache_data(ttl=600)
    def get_age_by_nationality():
        session = get_active_session()
        query = """
            SELECT NATIONALITY, AGE_GROUP, COUNT(*) as COUNT
            FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
            GROUP BY NATIONALITY, AGE_GROUP
            ORDER BY COUNT DESC
        """
        return session.sql(query).to_pandas()
    
    @st.cache_data(ttl=600)
    def get_dwell_by_hour():
        session = get_active_session()
        query = """
            SELECT HOUR, AVG(AVG_STAYING_DURATION_MIN) as AVG_DWELL, COUNT(*) as VISITS
            FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
            GROUP BY HOUR
            ORDER BY HOUR
        """
        return session.sql(query).to_pandas()
    
    @st.cache_data(ttl=600)
    def get_city_nationality_matrix():
        session = get_active_session()
        query = """
            SELECT SUBSCRIBER_HOME_CITY as CITY, NATIONALITY, COUNT(*) as COUNT
            FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
            GROUP BY SUBSCRIBER_HOME_CITY, NATIONALITY
            ORDER BY COUNT DESC
        """
        return session.sql(query).to_pandas()
    
    @st.cache_data(ttl=600)
    def get_daily_by_city():
        session = get_active_session()
        query = """
            SELECT DATE, SUBSCRIBER_HOME_CITY as CITY, COUNT(*) as TRAFFIC
            FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
            GROUP BY DATE, SUBSCRIBER_HOME_CITY
            ORDER BY DATE, SUBSCRIBER_HOME_CITY
        """
        return session.sql(query).to_pandas()

    st.subheader("✨ AI-Powered Mobility Insights", anchor=False)
    st.caption("Animated visualizations revealing hidden patterns in Saudi mobility data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("**🌊 City Traffic Rhythms**")
            st.caption("Watch how each city pulses throughout the day")
            hourly_city_df = get_hourly_by_city()
            
            fig = px.line(
                hourly_city_df, 
                x='HOUR', 
                y='TRAFFIC', 
                color='CITY',
                markers=True,
                line_shape='spline',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis_title="Hour of Day",
                yaxis_title="Foot Traffic",
                hovermode="x unified"
            )
            fig.update_traces(
                hovertemplate="<b>%{y:,.0f}</b> visits<extra></extra>"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        with st.container(border=True):
            st.markdown("**🎯 Dwell Time vs Activity**")
            st.caption("The engagement-traffic relationship by hour")
            dwell_hour_df = get_dwell_by_hour()
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(
                    x=dwell_hour_df['HOUR'],
                    y=dwell_hour_df['VISITS'],
                    name="Traffic Volume",
                    marker_color='rgba(8, 145, 178, 0.6)',
                    hovertemplate="<b>%{y:,.0f}</b> visits<extra></extra>"
                ),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(
                    x=dwell_hour_df['HOUR'],
                    y=dwell_hour_df['AVG_DWELL'],
                    name="Avg Dwell Time",
                    line=dict(color='#D4AF37', width=3),
                    mode='lines+markers',
                    marker=dict(size=8),
                    hovertemplate="<b>%{y:.1f}</b> min<extra></extra>"
                ),
                secondary_y=True,
            )
            
            fig.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode="x unified"
            )
            fig.update_xaxes(title_text="Hour of Day")
            fig.update_yaxes(title_text="Traffic Volume", secondary_y=False)
            fig.update_yaxes(title_text="Dwell Time (min)", secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)
    
    with st.container(border=True):
        st.markdown("**🔥 Nationality-City Heatmap**")
        st.caption("Where different nationalities concentrate across Saudi cities")
        
        matrix_df = get_city_nationality_matrix()
        pivot_df = matrix_df.pivot_table(index='NATIONALITY', columns='CITY', values='COUNT', fill_value=0)
        top_nationalities = matrix_df.groupby('NATIONALITY')['COUNT'].sum().nlargest(10).index
        pivot_df = pivot_df.loc[pivot_df.index.isin(top_nationalities)]
        
        fig = px.imshow(
            pivot_df,
            labels=dict(x="City", y="Nationality", color="Visitors"),
            color_continuous_scale="Viridis",
            aspect="auto"
        )
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=30, b=20),
        )
        fig.update_traces(
            hovertemplate="<b>%{y}</b> in <b>%{x}</b><br>%{z:,.0f} visitors<extra></extra>"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("**🥧 Age-Nationality Distribution**")
            st.caption("Demographic breakdown by visitor origin")
            
            age_nat_df = get_age_by_nationality()
            top_5_nat = age_nat_df.groupby('NATIONALITY')['COUNT'].sum().nlargest(5).index
            filtered_df = age_nat_df[age_nat_df['NATIONALITY'].isin(top_5_nat)]
            
            fig = px.sunburst(
                filtered_df,
                path=['NATIONALITY', 'AGE_GROUP'],
                values='COUNT',
                color='NATIONALITY',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=30, b=20),
            )
            fig.update_traces(
                hovertemplate="<b>%{label}</b><br>%{value:,.0f} visitors<br>%{percentParent:.1%} of parent<extra></extra>"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        with st.container(border=True):
            st.markdown("**📈 Cumulative Traffic Growth**")
            st.caption("Animated view of daily traffic accumulation by city")
            
            daily_city_df = get_daily_by_city()
            daily_city_df['DATE'] = pd.to_datetime(daily_city_df['DATE'])
            daily_city_df = daily_city_df.sort_values(['CITY', 'DATE'])
            daily_city_df['CUMULATIVE'] = daily_city_df.groupby('CITY')['TRAFFIC'].cumsum()
            
            fig = px.area(
                daily_city_df,
                x='DATE',
                y='CUMULATIVE',
                color='CITY',
                line_group='CITY',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis_title="Date",
                yaxis_title="Cumulative Visitors",
                hovermode="x unified"
            )
            fig.update_traces(
                hovertemplate="<b>%{y:,.0f}</b> total<extra></extra>"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with st.container(border=True):
        st.markdown("**🏙️ City Performance Radar**")
        st.caption("Multi-dimensional comparison of city mobility metrics")
        
        dwell_df = get_dwell_time_by_city()
        hourly_city_df = get_hourly_by_city()
        
        city_metrics = hourly_city_df.groupby('CITY').agg({
            'TRAFFIC': ['sum', 'mean', 'std']
        }).reset_index()
        city_metrics.columns = ['CITY', 'TOTAL_TRAFFIC', 'AVG_HOURLY', 'VOLATILITY']
        city_metrics = city_metrics.merge(dwell_df[['CITY', 'AVG_DWELL_TIME']], on='CITY', how='left')
        
        for col in ['TOTAL_TRAFFIC', 'AVG_HOURLY', 'VOLATILITY', 'AVG_DWELL_TIME']:
            max_val = city_metrics[col].max()
            if max_val > 0:
                city_metrics[f'{col}_NORM'] = city_metrics[col] / max_val * 100
            else:
                city_metrics[f'{col}_NORM'] = 0
        
        categories = ['Total Traffic', 'Avg Hourly', 'Pattern Stability', 'Engagement']
        
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set2
        for idx, row in city_metrics.iterrows():
            stability = 100 - row['VOLATILITY_NORM'] if row['VOLATILITY_NORM'] > 0 else 100
            fig.add_trace(go.Scatterpolar(
                r=[row['TOTAL_TRAFFIC_NORM'], row['AVG_HOURLY_NORM'], stability, row['AVG_DWELL_TIME_NORM']],
                theta=categories,
                fill='toself',
                name=row['CITY'],
                line_color=colors[idx % len(colors)],
                opacity=0.7
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=True,
            height=450,
            margin=dict(l=80, r=80, t=40, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.html("""
    <div class="insight-card">
        <h3>💡 Key Insight: Peak Hour Opportunity</h3>
        <p>Traffic peaks at different hours across cities, creating opportunities for time-based dynamic pricing and targeted campaigns. 
        Cities with high dwell times but lower traffic represent engagement opportunities.</p>
    </div>
    """)
