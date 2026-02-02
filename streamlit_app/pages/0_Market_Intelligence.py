import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title="Market Intelligence | Fusion", page_icon="logo.jpg", layout="wide")

st.logo("logo.jpg")

FUSION_BLUE = "#1E3A5F"
FUSION_TEAL = "#0891B2"
FUSION_GOLD = "#D4AF37"
FUSION_GREEN = "#10B981"
FUSION_PURPLE = "#8B5CF6"

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
    @keyframes countUp {
        from { opacity: 0; transform: scale(0.5); }
        to { opacity: 1; transform: scale(1); }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
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
        top: 0; left: 0; right: 0; bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M20 20h20v20H20V20zM0 0h20v20H0V0z'/%3E%3C/g%3E%3C/svg%3E");
    }
    .page-header h1 { margin: 0; font-size: 2rem; font-weight: 700; position: relative; z-index: 1; }
    .page-header p { margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1rem; position: relative; z-index: 1; }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 1.5rem 0 1rem 0;
        animation: slideIn 0.5s ease-out;
    }
    .section-header h3 {
        color: #1E3A5F;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0;
    }
    .section-line {
        flex: 1;
        height: 2px;
        background: linear-gradient(90deg, #e2e8f0, transparent);
    }
    
    .intro-card {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.6s ease-out;
        transition: all 0.3s ease;
    }
    .intro-card:hover {
        box-shadow: 0 10px 40px rgba(30, 58, 95, 0.1);
        transform: translateY(-2px);
    }
    
    .stat-highlight {
        background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 100%);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        color: white;
        text-align: center;
        animation: fadeInUp 0.6s ease-out, countUp 0.8s ease-out;
        transition: all 0.3s ease;
    }
    .stat-highlight:hover {
        transform: scale(1.02);
        box-shadow: 0 15px 40px rgba(30, 58, 95, 0.3);
    }
    .stat-highlight .value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
    }
    .stat-highlight .label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.3rem;
    }
    
    .trend-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        animation: fadeInUp 0.6s ease-out backwards;
        transition: all 0.3s ease;
    }
    .trend-card:hover {
        border-color: #0891B2;
        box-shadow: 0 8px 25px rgba(30, 58, 95, 0.1);
    }
    
    .pricing-tier {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out backwards;
        position: relative;
        overflow: hidden;
    }
    .pricing-tier:hover {
        border-color: #0891B2;
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(30, 58, 95, 0.15);
    }
    .pricing-tier.featured {
        border-color: #0891B2;
        background: linear-gradient(180deg, #f0fdfa 0%, #ffffff 100%);
    }
    .pricing-tier.featured::before {
        content: 'POPULAR';
        position: absolute;
        top: 12px;
        right: -30px;
        background: #0891B2;
        color: white;
        padding: 0.25rem 2rem;
        font-size: 0.7rem;
        font-weight: 600;
        transform: rotate(45deg);
    }
    .pricing-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .pricing-price {
        font-size: 2rem;
        font-weight: 800;
        color: #0891B2;
        margin: 0.5rem 0;
    }
    .pricing-price span {
        font-size: 0.9rem;
        font-weight: 400;
        color: #64748b;
    }
    .pricing-features {
        text-align: left;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }
    .pricing-feature {
        color: #64748b;
        font-size: 0.9rem;
        padding: 0.4rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .pricing-feature::before {
        content: '✓';
        color: #10B981;
        font-weight: 600;
    }
    
    .distribution-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        animation: fadeInUp 0.6s ease-out backwards;
        transition: all 0.3s ease;
        height: 100%;
    }
    .distribution-card:hover {
        border-color: #0891B2;
        box-shadow: 0 10px 30px rgba(30, 58, 95, 0.1);
        transform: translateY(-3px);
    }
    .distribution-icon {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #1E3A5F, #0891B2);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    .distribution-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .distribution-desc {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .distribution-tag {
        display: inline-block;
        background: #f0fdfa;
        color: #0891B2;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 1rem;
    }
    
    .key-insight {
        background: linear-gradient(135deg, #fef3c7 0%, #fef9c3 100%);
        border-left: 4px solid #D4AF37;
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }
    .key-insight p {
        color: #92400e;
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .source-citation {
        color: #94a3b8;
        font-size: 0.75rem;
        font-style: italic;
        margin-top: 0.5rem;
    }
</style>
""")

st.html("""
<div class="page-header">
    <h1>Market Intelligence</h1>
    <p>Understanding the telco data monetization landscape</p>
</div>
""")

tab_intro, tab_trends, tab_demand, tab_pricing, tab_distribution = st.tabs([
    "📋 Intro",
    "📈 Data Product Trends",
    "🎯 Market Demand",
    "💰 Pricing Models",
    "🌐 Data Distribution"
])

# =============================================================================
# TAB 1: INTRO
# =============================================================================
with tab_intro:
    st.html("""
    <div class="section-header">
        <h3>🚀 The Telco Data Monetization Opportunity</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.html("""
        <div class="intro-card">
            <h4 style="color: #1E3A5F; margin-top: 0;">Why Telco Data?</h4>
            <p style="color: #64748b; line-height: 1.8;">
                Telecommunications companies sit on one of the most valuable data assets in the digital economy: 
                <strong>real-time, privacy-compliant mobility intelligence</strong>. With billions of devices 
                connecting daily, telcos capture anonymized movement patterns, demographic insights, and 
                behavioral signals that power critical business decisions across industries.
            </p>
            <p style="color: #64748b; line-height: 1.8; margin-bottom: 0;">
                <strong>Fusion</strong> aggregates data from Saudi Arabia's three major telco providers—STC, Mobily, 
                and Zain—creating a comprehensive view of mobility patterns across the Kingdom. This unified 
                dataset enables unprecedented insights for retail, government, tourism, and transportation sectors.
            </p>
        </div>
        """)
        
        st.html("""
        <div class="key-insight">
            <p>💡 <strong>Key Insight:</strong> Telco data monetization is projected to become a $15B+ 
            global market by 2028, with mobility and location intelligence leading the growth.</p>
        </div>
        """)
    
    with col2:
        st.html("""
        <div class="stat-highlight" style="margin-bottom: 1rem;">
            <p class="value">$15B+</p>
            <p class="label">Global Market by 2028</p>
        </div>
        """)
        st.html("""
        <div class="stat-highlight" style="background: linear-gradient(135deg, #0891B2 0%, #10B981 100%); margin-bottom: 1rem;">
            <p class="value">25%</p>
            <p class="label">Annual Growth Rate</p>
        </div>
        """)
        st.html("""
        <div class="stat-highlight" style="background: linear-gradient(135deg, #D4AF37 0%, #F59E0B 100%);">
            <p class="value">4.2M+</p>
            <p class="label">Fusion Records</p>
        </div>
        """)
    
    st.html("""
    <div class="section-header">
        <h3>🎯 Target Industries</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    
    industries = [
        {"icon": "🏪", "name": "Retail & Commercial", "use": "Site selection, competitive analysis, foot traffic"},
        {"icon": "🏛️", "name": "Government", "use": "Urban planning, infrastructure, smart cities"},
        {"icon": "✈️", "name": "Tourism", "use": "Visitor flows, destination analytics, seasonality"},
        {"icon": "🚌", "name": "Transportation", "use": "Route optimization, commuter patterns, peak hours"}
    ]
    
    for col, ind in zip([col1, col2, col3, col4], industries):
        with col:
            with st.container(border=True):
                st.markdown(f"### {ind['icon']}")
                st.markdown(f"**{ind['name']}**")
                st.caption(ind['use'])

# =============================================================================
# TAB 2: TELCO DATA PRODUCT TRENDS
# =============================================================================
with tab_trends:
    st.html("""
    <div class="section-header">
        <h3>📊 Global Telco Data Product Evolution</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    # Market Growth Chart
    market_data = pd.DataFrame({
        'Year': [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028],
        'Market Size ($B)': [4.2, 5.1, 6.3, 7.8, 9.5, 11.2, 12.8, 14.1, 15.5],
        'Type': ['Historical'] * 5 + ['Projected'] * 4
    })
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.container(border=True):
            st.markdown("**Global Telco Data Monetization Market Size**")
            
            market_chart = alt.Chart(market_data).mark_area(
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
                x=alt.X('Year:O', axis=alt.Axis(title='Year', labelAngle=0)),
                y=alt.Y('Market Size ($B):Q', axis=alt.Axis(title='Market Size ($ Billion)', grid=True, gridOpacity=0.3)),
                tooltip=[
                    alt.Tooltip('Year:O', title='Year'),
                    alt.Tooltip('Market Size ($B):Q', title='Market Size', format='$.1f'),
                    alt.Tooltip('Type:N', title='Status')
                ]
            ).properties(height=350)
            
            # Add points
            points = alt.Chart(market_data).mark_circle(size=80, color=FUSION_TEAL).encode(
                x='Year:O',
                y='Market Size ($B):Q'
            )
            
            st.altair_chart(market_chart + points, use_container_width=True)
            st.caption("Source: Industry analyst reports, 2024")
    
    with col2:
        st.html("""
        <div class="trend-card" style="animation-delay: 0.1s; margin-bottom: 1rem;">
            <h4 style="color: #1E3A5F; margin: 0 0 0.5rem 0; font-size: 1rem;">📱 Mobility Data</h4>
            <p style="color: #64748b; font-size: 0.85rem; margin: 0; line-height: 1.5;">
                Leading segment with 40% market share. High demand for foot traffic and movement patterns.
            </p>
        </div>
        """)
        st.html("""
        <div class="trend-card" style="animation-delay: 0.2s; margin-bottom: 1rem;">
            <h4 style="color: #1E3A5F; margin: 0 0 0.5rem 0; font-size: 1rem;">👥 Demographic Insights</h4>
            <p style="color: #64748b; font-size: 0.85rem; margin: 0; line-height: 1.5;">
                Growing 30% YoY. Age, nationality, and behavioral segmentation driving value.
            </p>
        </div>
        """)
        st.html("""
        <div class="trend-card" style="animation-delay: 0.3s;">
            <h4 style="color: #1E3A5F; margin: 0 0 0.5rem 0; font-size: 1rem;">📍 Location Intelligence</h4>
            <p style="color: #64748b; font-size: 0.85rem; margin: 0; line-height: 1.5;">
                H3 hexagon-based analytics emerging as industry standard for spatial analysis.
            </p>
        </div>
        """)
    
    st.html("""
    <div class="section-header">
        <h3>🔥 Key Product Trends in 2026</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    trends_data = pd.DataFrame({
        'Trend': ['Real-time Analytics', 'Privacy-First Design', 'AI/ML Integration', 'Cross-Industry Bundles', 'Self-Service Platforms'],
        'Adoption': [85, 92, 78, 65, 88],
        'Growth': ['+35%', '+45%', '+52%', '+28%', '+40%']
    })
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.container(border=True):
            st.markdown("**Trend Adoption Rate Among Telcos**")
            
            trend_chart = alt.Chart(trends_data).mark_bar(
                cornerRadiusTopRight=8,
                cornerRadiusBottomRight=8
            ).encode(
                x=alt.X('Adoption:Q', axis=alt.Axis(title='Adoption Rate (%)', grid=True, gridOpacity=0.3), scale=alt.Scale(domain=[0, 100])),
                y=alt.Y('Trend:N', axis=alt.Axis(title=None), sort='-x'),
                color=alt.Color('Adoption:Q', scale=alt.Scale(scheme='teals'), legend=None),
                tooltip=[
                    alt.Tooltip('Trend:N', title='Trend'),
                    alt.Tooltip('Adoption:Q', title='Adoption', format='.0f'),
                    alt.Tooltip('Growth:N', title='YoY Growth')
                ]
            ).properties(height=280)
            
            st.altair_chart(trend_chart, use_container_width=True)
    
    with col2:
        with st.container(border=True):
            st.markdown("**YoY Growth by Trend**")
            st.dataframe(
                trends_data,
                use_container_width=True,
                hide_index=True,
                height=280,
                column_config={
                    "Trend": st.column_config.TextColumn("Trend", width="large"),
                    "Adoption": st.column_config.ProgressColumn("Adoption %", format="%d%%", min_value=0, max_value=100),
                    "Growth": st.column_config.TextColumn("YoY Growth", width="small")
                }
            )

# =============================================================================
# TAB 3: MARKET DEMAND
# =============================================================================
with tab_demand:
    st.html("""
    <div class="section-header">
        <h3>🎯 Who's Buying Telco Data Products?</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    # Industry demand data
    demand_data = pd.DataFrame({
        'Industry': ['Retail & E-commerce', 'Real Estate', 'Government', 'Financial Services', 'Tourism & Hospitality', 'Transportation', 'Healthcare', 'Advertising'],
        'Demand Score': [92, 88, 85, 78, 82, 75, 65, 70],
        'Spend ($M)': [2.8, 2.4, 2.1, 1.9, 1.7, 1.5, 1.2, 1.4]
    })
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        with st.container(border=True):
            st.markdown("**Industry Demand for Telco Data Products**")
            
            demand_chart = alt.Chart(demand_data).mark_bar(
                cornerRadiusTopLeft=8,
                cornerRadiusTopRight=8
            ).encode(
                x=alt.X('Industry:N', axis=alt.Axis(title=None, labelAngle=-45), sort='-y'),
                y=alt.Y('Demand Score:Q', axis=alt.Axis(title='Demand Score (0-100)', grid=True, gridOpacity=0.3)),
                color=alt.Color('Demand Score:Q', 
                               scale=alt.Scale(domain=[60, 95], range=[FUSION_BLUE, FUSION_TEAL]),
                               legend=None),
                tooltip=[
                    alt.Tooltip('Industry:N', title='Industry'),
                    alt.Tooltip('Demand Score:Q', title='Demand Score'),
                    alt.Tooltip('Spend ($M):Q', title='Avg Annual Spend', format='$,.1f')
                ]
            ).properties(height=350)
            
            st.altair_chart(demand_chart, use_container_width=True)
    
    with col2:
        st.html("""
        <div class="stat-highlight" style="margin-bottom: 1rem;">
            <p class="value">92%</p>
            <p class="label">Retail Demand Score</p>
        </div>
        """)
        st.html("""
        <div class="stat-highlight" style="background: linear-gradient(135deg, #0891B2 0%, #10B981 100%); margin-bottom: 1rem;">
            <p class="value">$2.8M</p>
            <p class="label">Avg Retail Annual Spend</p>
        </div>
        """)
        
        st.html("""
        <div class="key-insight">
            <p>💡 <strong>Saudi Market:</strong> Vision 2030 initiatives are driving unprecedented 
            demand for mobility data in urban planning, tourism, and retail sectors.</p>
        </div>
        """)
    
    st.html("""
    <div class="section-header">
        <h3>📊 Use Case Demand Analysis</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    use_cases = pd.DataFrame({
        'Use Case': ['Site Selection', 'Foot Traffic Analysis', 'Customer Segmentation', 'Urban Planning', 'Tourism Analytics', 'Competitive Intelligence', 'Route Optimization', 'Event Impact Analysis'],
        'Priority': ['High', 'High', 'High', 'Medium', 'High', 'Medium', 'Medium', 'Low'],
        'Buyers': [85, 92, 78, 65, 72, 68, 55, 45]
    })
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        with st.container(border=True):
            st.markdown("**🏪 Site Selection**")
            st.metric("Buyer Interest", "85%", "+12% YoY")
            st.caption("Retail chains, restaurants, banks selecting optimal locations")
    
    with col2:
        with st.container(border=True):
            st.markdown("**👣 Foot Traffic**")
            st.metric("Buyer Interest", "92%", "+18% YoY")
            st.caption("Most requested use case across all industries")
    
    with col3:
        with st.container(border=True):
            st.markdown("**👥 Segmentation**")
            st.metric("Buyer Interest", "78%", "+22% YoY")
            st.caption("Demographics, behavior patterns, customer profiling")
    
    with col4:
        with st.container(border=True):
            st.markdown("**✈️ Tourism**")
            st.metric("Buyer Interest", "72%", "+35% YoY")
            st.caption("Fastest growing segment, especially in Saudi Arabia")

# =============================================================================
# TAB 4: PRICING MODELS
# =============================================================================
with tab_pricing:
    st.html("""
    <div class="section-header">
        <h3>💰 Reference Pricing Models for Telco Data Products</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.markdown("""
    Telco data products are typically priced using one or more of these models. The right model depends on 
    your data's uniqueness, refresh frequency, and target customer segment.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.html("""
        <div class="pricing-tier">
            <div class="pricing-name">Subscription</div>
            <div class="pricing-price">$5-50K<span>/month</span></div>
            <p style="color: #64748b; font-size: 0.85rem;">Recurring access to data feeds</p>
            <div class="pricing-features">
                <div class="pricing-feature">Monthly/quarterly refresh</div>
                <div class="pricing-feature">API or file delivery</div>
                <div class="pricing-feature">Standard SLAs</div>
                <div class="pricing-feature">Volume-based tiers</div>
            </div>
        </div>
        """)
    
    with col2:
        st.html("""
        <div class="pricing-tier featured">
            <div class="pricing-name">Usage-Based</div>
            <div class="pricing-price">$0.01-0.10<span>/query</span></div>
            <p style="color: #64748b; font-size: 0.85rem;">Pay-per-use consumption model</p>
            <div class="pricing-features">
                <div class="pricing-feature">Real-time or near real-time</div>
                <div class="pricing-feature">Snowflake Data Cloud</div>
                <div class="pricing-feature">Compute costs passed through</div>
                <div class="pricing-feature">Scalable with demand</div>
            </div>
        </div>
        """)
    
    with col3:
        st.html("""
        <div class="pricing-tier">
            <div class="pricing-name">Enterprise License</div>
            <div class="pricing-price">$100-500K<span>/year</span></div>
            <p style="color: #64748b; font-size: 0.85rem;">Unlimited access agreements</p>
            <div class="pricing-features">
                <div class="pricing-feature">Full dataset access</div>
                <div class="pricing-feature">Custom integrations</div>
                <div class="pricing-feature">Dedicated support</div>
                <div class="pricing-feature">Co-marketing rights</div>
            </div>
        </div>
        """)
    
    st.html("""
    <div class="section-header">
        <h3>📈 Pricing Benchmarks by Data Type</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    pricing_data = pd.DataFrame({
        'Data Type': ['Raw Mobility', 'Aggregated Insights', 'Real-time Feeds', 'Historical Archives', 'Custom Reports'],
        'Low ($K/mo)': [5, 10, 25, 2, 15],
        'Mid ($K/mo)': [15, 25, 50, 8, 35],
        'High ($K/mo)': [50, 75, 150, 25, 100]
    })
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.container(border=True):
            st.markdown("**Monthly Pricing Ranges by Data Type**")
            
            # Reshape for Altair
            pricing_melted = pricing_data.melt(
                id_vars=['Data Type'],
                value_vars=['Low ($K/mo)', 'Mid ($K/mo)', 'High ($K/mo)'],
                var_name='Tier',
                value_name='Price'
            )
            
            pricing_chart = alt.Chart(pricing_melted).mark_bar(
                cornerRadiusTopLeft=4,
                cornerRadiusTopRight=4
            ).encode(
                x=alt.X('Data Type:N', axis=alt.Axis(title=None, labelAngle=-45)),
                y=alt.Y('Price:Q', axis=alt.Axis(title='Price ($K/month)', grid=True, gridOpacity=0.3)),
                color=alt.Color('Tier:N', 
                               scale=alt.Scale(domain=['Low ($K/mo)', 'Mid ($K/mo)', 'High ($K/mo)'],
                                              range=['#94a3b8', FUSION_TEAL, FUSION_BLUE]),
                               legend=alt.Legend(title='Tier', orient='bottom')),
                xOffset='Tier:N',
                tooltip=[
                    alt.Tooltip('Data Type:N', title='Data Type'),
                    alt.Tooltip('Tier:N', title='Tier'),
                    alt.Tooltip('Price:Q', title='Price ($K/mo)', format=',.0f')
                ]
            ).properties(height=320)
            
            st.altair_chart(pricing_chart, use_container_width=True)
    
    with col2:
        st.html("""
        <div class="key-insight">
            <p>💡 <strong>Pricing Tip:</strong> Start with aggregated insights at mid-tier pricing. 
            Premium pricing applies when data is exclusive, real-time, or covers unique geographies.</p>
        </div>
        """)
        
        with st.container(border=True):
            st.markdown("**Price Multipliers**")
            st.markdown("""
            - **Exclusivity**: 2-3x premium
            - **Real-time**: 3-5x vs batch
            - **Saudi/GCC**: 1.5x global avg
            - **Custom enrichment**: +25-50%
            """)

# =============================================================================
# TAB 5: DATA DISTRIBUTION
# =============================================================================
with tab_distribution:
    st.html("""
    <div class="section-header">
        <h3>🌐 Reaching Customers Without Snowflake Accounts</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.markdown("""
    While Snowflake Data Sharing provides the most seamless experience for Snowflake customers, 
    there are multiple ways to expose telco data products to a broader audience.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.html("""
        <div class="distribution-card" style="animation-delay: 0.1s;">
            <div class="distribution-icon">🏪</div>
            <div class="distribution-title">Snowflake Marketplace</div>
            <div class="distribution-desc">
                List your data product on Snowflake Marketplace for discovery by 10,000+ organizations. 
                Supports both free trials and paid listings. Customers get instant access without data movement.
            </div>
            <div class="distribution-tag">Recommended for Snowflake Users</div>
        </div>
        """)
    
    with col2:
        st.html("""
        <div class="distribution-card" style="animation-delay: 0.2s;">
            <div class="distribution-icon">🔌</div>
            <div class="distribution-title">REST API</div>
            <div class="distribution-desc">
                Expose data via Snowflake's REST API or external API gateway. Customers query data 
                programmatically without needing a Snowflake account. Ideal for real-time integrations.
            </div>
            <div class="distribution-tag">Best for Developers</div>
        </div>
        """)
    
    with col3:
        st.html("""
        <div class="distribution-card" style="animation-delay: 0.3s;">
            <div class="distribution-icon">📱</div>
            <div class="distribution-title">Streamlit Apps</div>
            <div class="distribution-desc">
                Build interactive web apps (like this one!) that let customers explore, visualize, and 
                export data without any technical setup. Hosted on Snowflake with built-in security.
            </div>
            <div class="distribution-tag">Best for Self-Service</div>
        </div>
        """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.html("""
        <div class="distribution-card" style="animation-delay: 0.4s;">
            <div class="distribution-icon">📊</div>
            <div class="distribution-title">BI Tool Connectors</div>
            <div class="distribution-desc">
                Connect Power BI, Tableau, or Looker directly to Snowflake. Customers use familiar tools 
                while you maintain data governance. Native connectors available for all major platforms.
            </div>
            <div class="distribution-tag">Enterprise Friendly</div>
        </div>
        """)
    
    with col2:
        st.html("""
        <div class="distribution-card" style="animation-delay: 0.5s;">
            <div class="distribution-icon">📦</div>
            <div class="distribution-title">Data Exports</div>
            <div class="distribution-desc">
                Generate CSV, Parquet, or JSON exports for customers who prefer file-based delivery. 
                Can be automated via Snowflake tasks and delivered to cloud storage (S3, GCS, Azure).
            </div>
            <div class="distribution-tag">Universal Compatibility</div>
        </div>
        """)
    
    with col3:
        st.html("""
        <div class="distribution-card" style="animation-delay: 0.6s;">
            <div class="distribution-icon">🔄</div>
            <div class="distribution-title">Reader Accounts</div>
            <div class="distribution-desc">
                Create managed Snowflake Reader Accounts for non-Snowflake customers. They get full 
                Snowflake query capabilities with costs billed to your account. Best for high-value clients.
            </div>
            <div class="distribution-tag">Full Snowflake Experience</div>
        </div>
        """)
    
    st.html("""
    <div class="section-header">
        <h3>📋 Distribution Method Comparison</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    comparison_data = pd.DataFrame({
        'Method': ['Snowflake Marketplace', 'REST API', 'Streamlit Apps', 'BI Connectors', 'Data Exports', 'Reader Accounts'],
        'Setup Effort': ['Low', 'Medium', 'Low', 'Low', 'Low', 'Medium'],
        'Customer Tech Required': ['Snowflake', 'Any', 'Browser', 'BI Tool', 'Any', 'Browser'],
        'Real-time': ['✓', '✓', '✓', '✓', '✗', '✓'],
        'Governance': ['High', 'High', 'High', 'Medium', 'Low', 'High'],
        'Best For': ['Snowflake users', 'Developers', 'Business users', 'Analysts', 'Legacy systems', 'Premium clients']
    })
    
    with st.container(border=True):
        st.dataframe(
            comparison_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Method": st.column_config.TextColumn("Distribution Method", width="large"),
                "Setup Effort": st.column_config.TextColumn("Setup Effort"),
                "Customer Tech Required": st.column_config.TextColumn("Customer Needs"),
                "Real-time": st.column_config.TextColumn("Real-time"),
                "Governance": st.column_config.TextColumn("Governance"),
                "Best For": st.column_config.TextColumn("Best For", width="medium")
            }
        )
    
    st.html("""
    <div class="key-insight">
        <p>💡 <strong>Recommendation:</strong> For maximum reach, combine Snowflake Marketplace (for data-savvy customers), 
        Streamlit Apps (for self-service exploration), and REST APIs (for developer integrations). 
        This covers 90%+ of potential customer segments.</p>
    </div>
    """)
