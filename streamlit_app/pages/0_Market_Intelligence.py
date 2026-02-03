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
    /* =========================================
       SIDEBAR STYLING
       ========================================= */
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
        color: #e2e8f0 !important;
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
    
    /* =========================================
       ANIMATIONS
       ========================================= */
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
        padding: 1.75rem;
        margin-bottom: 1rem;
        animation: fadeInUp 0.6s ease-out;
        transition: all 0.3s ease;
    }
    .intro-card:hover {
        box-shadow: 0 10px 40px rgba(30, 58, 95, 0.1);
        transform: translateY(-2px);
    }
    
    .questions-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-top: 1.5rem;
    }
    @media (max-width: 768px) {
        .questions-grid { grid-template-columns: 1fr; }
    }
    .question-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        animation: fadeInUp 0.6s ease-out backwards;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .question-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #0891B2, #1E3A5F);
        border-radius: 4px 0 0 4px;
        transition: width 0.3s ease;
    }
    .question-card:hover {
        transform: translateY(-4px) translateX(4px);
        box-shadow: 0 12px 30px rgba(30, 58, 95, 0.12);
        border-color: #0891B2;
    }
    .question-card:hover::before {
        width: 6px;
    }
    .question-card .q-icon {
        font-size: 1.5rem;
        margin-bottom: 0.75rem;
        display: inline-block;
        animation: bounce 2s ease-in-out infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-4px); }
    }
    .question-card .q-title {
        color: #1E3A5F;
        font-weight: 700;
        font-size: 1rem;
        margin: 0 0 0.5rem 0;
        line-height: 1.4;
    }
    .question-card .q-desc {
        color: #64748b;
        font-size: 0.9rem;
        margin: 0;
        line-height: 1.6;
    }
    .question-card .q-arrow {
        position: absolute;
        bottom: 1rem;
        right: 1rem;
        color: #0891B2;
        font-size: 1.2rem;
        opacity: 0;
        transform: translateX(-10px);
        transition: all 0.3s ease;
    }
    .question-card:hover .q-arrow {
        opacity: 1;
        transform: translateX(0);
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
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
    }
    .stat-highlight .label {
        font-size: 0.85rem;
        opacity: 0.9;
        margin-top: 0.3rem;
    }
    
    .shift-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
        animation: fadeInUp 0.6s ease-out backwards;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .shift-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1E3A5F, #0891B2);
    }
    .shift-card:hover {
        border-color: #0891B2;
        box-shadow: 0 10px 30px rgba(30, 58, 95, 0.12);
        transform: translateY(-3px);
    }
    .shift-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #1E3A5F, #0891B2);
        color: white;
        border-radius: 50%;
        font-weight: 700;
        font-size: 0.9rem;
        margin-bottom: 0.75rem;
    }
    .shift-title {
        color: #1E3A5F;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
    }
    .shift-desc {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .shift-example {
        background: #f8fafc;
        border-radius: 8px;
        padding: 0.75rem;
        margin-top: 0.75rem;
        font-size: 0.8rem;
        color: #64748b;
        border-left: 3px solid #D4AF37;
    }
    
    .buyer-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        animation: fadeInUp 0.5s ease-out backwards;
        transition: all 0.3s ease;
    }
    .buyer-card:hover {
        border-color: #0891B2;
        box-shadow: 0 8px 25px rgba(30, 58, 95, 0.1);
    }
    .buyer-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .buyer-title {
        color: #1E3A5F;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.3rem;
    }
    .buyer-uses {
        color: #64748b;
        font-size: 0.8rem;
        line-height: 1.5;
    }
    
    .pricing-model {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: left;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out backwards;
        height: 100%;
    }
    .pricing-model:hover {
        border-color: #0891B2;
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(30, 58, 95, 0.12);
    }
    .pricing-model.recommended {
        border-color: #0891B2;
        background: linear-gradient(180deg, #f0fdfa 0%, #ffffff 100%);
    }
    .pricing-icon {
        font-size: 1.8rem;
        margin-bottom: 0.75rem;
    }
    .pricing-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .pricing-desc {
        color: #64748b;
        font-size: 0.85rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    .pricing-details {
        background: #f8fafc;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 0.8rem;
        color: #64748b;
    }
    .pricing-tag {
        display: inline-block;
        background: #0891B2;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    .distribution-option {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        animation: fadeInUp 0.6s ease-out backwards;
        transition: all 0.3s ease;
        height: 100%;
    }
    .distribution-option:hover {
        border-color: #0891B2;
        box-shadow: 0 10px 30px rgba(30, 58, 95, 0.1);
        transform: translateY(-3px);
    }
    .distribution-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #1E3A5F, #0891B2);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .distribution-title {
        font-size: 1rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .distribution-desc {
        color: #64748b;
        font-size: 0.85rem;
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
    .distribution-tag.warning {
        background: #fef3c7;
        color: #92400e;
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
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    .ksa-highlight {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 4px solid #10B981;
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }
    .ksa-highlight p {
        color: #065f46;
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    .source-ref {
        color: #94a3b8;
        font-size: 0.75rem;
        font-style: italic;
        margin-top: 0.5rem;
    }
    
    .position-box {
        background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 100%);
        border-radius: 12px;
        padding: 1.25rem;
        color: white;
        margin-top: 1rem;
    }
    .position-box p {
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .position-box strong {
        color: #D4AF37;
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
        <h3>📌 About This Dashboard</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <p style="color: #64748b; font-size: 1rem; line-height: 1.7; margin-bottom: 0.5rem;">
        This Market Intelligence dashboard addresses <strong style="color: #1E3A5F;">key strategic questions from Fusion</strong> 
        about telco data monetization. Each tab provides research, market data, and actionable insights.
    </p>
    
    <div class="questions-grid">
        <div class="question-card" style="animation-delay: 0.1s;">
            <div class="q-icon">📈</div>
            <p class="q-title">What is the telco data product trend?</p>
            <p class="q-desc">Three major shifts: from raw data to privacy-safe insights, from one-off deals to marketplaces, and AI-native use on governed products.</p>
            <span class="q-arrow">→</span>
        </div>
        <div class="question-card" style="animation-delay: 0.2s;">
            <div class="q-icon">🎯</div>
            <p class="q-title">What is the market demand for telco data products?</p>
            <p class="q-desc">Multi-billion dollar market with strong demand from public sector, retail, transport, financial services, and advertising verticals.</p>
            <span class="q-arrow">→</span>
        </div>
        <div class="question-card" style="animation-delay: 0.3s;">
            <div class="q-icon">💰</div>
            <p class="q-title">Is there a reference pricing model?</p>
            <p class="q-desc">A pricing toolbox: subscription/recurring licenses, usage-based/API-metered, flat licenses, freemium tiers, and outcome/revenue-share models.</p>
            <span class="q-arrow">→</span>
        </div>
        <div class="question-card" style="animation-delay: 0.4s;">
            <div class="q-icon">🌐</div>
            <p class="q-title">How to expose data to consumers without a Snowflake account?</p>
            <p class="q-desc">Multiple options: Reader accounts, "Powered-by Fusion" portals, REST APIs, Clean Rooms, and file exports—all with Snowflake as the governed backend.</p>
            <span class="q-arrow">→</span>
        </div>
    </div>
    """)
    
    st.html("""
    <div class="section-header">
        <h3>🇸🇦 Saudi Arabia Context: Vision 2030 & National Data Strategy</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.html("""
        <div class="intro-card">
            <h4 style="color: #1E3A5F; margin-top: 0;">SDAIA & National Strategy for Data & AI</h4>
            <p style="color: #64748b; line-height: 1.7; margin-bottom: 1rem;">
                The Saudi Data & AI Authority (SDAIA) drives the Kingdom's data agenda. Approved by King Salman 
                in July 2020, the National Strategy for Data & AI follows a phased approach:
            </p>
            <ul style="color: #64748b; line-height: 1.8; margin: 0; padding-left: 1.25rem;">
                <li><strong>2021 (National Enabler)</strong> — Address urgent national needs aligned with Vision 2030</li>
                <li><strong>2025 (Specialist)</strong> — Build foundations for competitive advantage in key domains</li>
                <li><strong>2030 (Industry Leader)</strong> — Compete internationally as a leading data & AI economy</li>
            </ul>
            <p class="source-ref">Source: sdaia.gov.sa</p>
        </div>
        """)
        
        st.html("""
        <div class="ksa-highlight">
            <p>🇸🇦 <strong>Vision 2030 Integration:</strong> Of the 96 goals in Saudi Vision 2030, 
            <strong>66 direct and indirect goals</strong> are related to data and AI. SDAIA has established 
            440+ data-sharing services in the Digital Data Marketplace and integrated 370+ government systems 
            in the National Data Catalog.</p>
        </div>
        """)
    
    with col2:
        st.html("""
        <div class="stat-highlight" style="margin-bottom: 1rem;">
            <p class="value">Top 15</p>
            <p class="label">AI Global Ranking Target</p>
        </div>
        """)
        st.html("""
        <div class="stat-highlight" style="background: linear-gradient(135deg, #0891B2 0%, #10B981 100%); margin-bottom: 1rem;">
            <p class="value">20,000+</p>
            <p class="label">Data & AI Specialists Goal</p>
        </div>
        """)
        st.html("""
        <div class="stat-highlight" style="background: linear-gradient(135deg, #D4AF37 0%, #F59E0B 100%);">
            <p class="value">440+</p>
            <p class="label">Data Sharing Services</p>
        </div>
        """)
    
    st.html("""
    <div class="section-header">
        <h3>🏗️ Giga-Projects & Smart City Opportunity</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    
    giga_projects = [
        {"icon": "🌆", "name": "NEOM", "desc": "Cognitive city spanning 26,500 km², partnered with SDAIA for AI research"},
        {"icon": "🏙️", "name": "THE LINE", "desc": "Zero-carbon city requiring real-time mobility and density analytics"},
        {"icon": "🏭", "name": "Oxagon", "desc": "Industrial hub 'Powering Data' with advanced logistics needs"},
        {"icon": "🎿", "name": "Trojena", "desc": "Mountain tourism destination requiring visitor flow analytics"}
    ]
    
    for col, proj in zip([col1, col2, col3, col4], giga_projects):
        with col:
            with st.container(border=True):
                st.markdown(f"### {proj['icon']}")
                st.markdown(f"**{proj['name']}**")
                st.caption(proj['desc'])
    
    st.caption("Source: neom.com, pif.gov.sa")

# =============================================================================
# TAB 2: TELCO DATA PRODUCT TRENDS
# =============================================================================
with tab_trends:
    st.html("""
    <div class="section-header">
        <h3>🔄 Three Big Shifts in Telco Data Products</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.html("""
        <div class="shift-card" style="animation-delay: 0.1s;">
            <div class="shift-number">1</div>
            <div class="shift-title">From Raw Data to Privacy-Safe Insight Products</div>
            <div class="shift-desc">
                Operators are moving away from selling raw CDR/location feeds toward curated, anonymized 
                insight products: mobility & footfall, network quality, IoT/5G telemetry, fraud/risk signals, 
                customer intent, and more.
            </div>
            <div class="shift-example">
                <strong>Example:</strong> "Digital nervous system" products for cities—real-time density, 
                surge prediction, and recommended actions for transport, energy, and public safety packaged 
                as data products, not raw network logs.
            </div>
        </div>
        """)
    
    with col2:
        st.html("""
        <div class="shift-card" style="animation-delay: 0.2s;">
            <div class="shift-number">2</div>
            <div class="shift-title">From One-Off Deals to Marketplaces & Platforms</div>
            <div class="shift-desc">
                Telcos increasingly publish their data products through data marketplaces and clean rooms, 
                so partners (cities, retailers, banks, advertisers) can subscribe to governed feeds and run 
                their own analytics without ever seeing raw subscriber identifiers.
            </div>
            <div class="shift-example">
                <strong>Key principle:</strong> "This is not about selling raw telco data, it's about a 
                trusted collaboration platform for insights."
            </div>
        </div>
        """)
    
    with col3:
        st.html("""
        <div class="shift-card" style="animation-delay: 0.3s;">
            <div class="shift-number">3</div>
            <div class="shift-title">AI-Native / Agentic Use on Governed Products</div>
            <div class="shift-desc">
                The next wave is AI/agent-assist on top of these data products: call-center intent detection, 
                agent assist, network ops copilots—all using the same governed products with masking and 
                row-level policies.
            </div>
            <div class="shift-example">
                <strong>The pattern:</strong> Build reusable, policy-attached telco data products once; 
                reuse them across dashboards, AI, and partner use cases.
            </div>
        </div>
        """)
    
    st.html("""
    <div class="position-box">
        <p><strong>Position Fusion as:</strong> "We want to build a catalog of governed telco data products 
        (mobility, network, CX, IoT) that can power AI and analytics for government and ecosystem partners."</p>
    </div>
    """)
    
    st.html("""
    <div class="section-header">
        <h3>📊 Data Product Categories</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    products_data = pd.DataFrame({
        'Category': ['Mobility & Footfall', 'Audience Segments', 'Network Quality', 'Fraud & Risk Signals', 'IoT / 5G Telemetry', 'Customer Intent'],
        'Maturity': [95, 85, 80, 75, 70, 65],
        'Privacy': ['Aggregated', 'Cohort-based', 'Aggregated', 'Scored', 'Device-level', 'Inferred'],
        'Icon': ['📍', '👥', '📶', '🛡️', '📡', '🎯']
    })
    
    st.html("""
    <style>
        .product-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 1rem 0;
        }
        @media (max-width: 768px) {
            .product-grid { grid-template-columns: repeat(2, 1fr); }
        }
        .product-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.25rem;
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.5s ease-out backwards;
            transition: all 0.3s ease;
        }
        .product-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(30, 58, 95, 0.12);
            border-color: #0891B2;
        }
        .product-card .card-icon {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
        }
        .product-card .card-name {
            color: #1E3A5F;
            font-weight: 700;
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
        }
        .product-card .card-privacy {
            display: inline-block;
            background: #f0fdfa;
            color: #0891B2;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }
        .product-card .progress-bar {
            background: #e2e8f0;
            border-radius: 6px;
            height: 8px;
            overflow: hidden;
        }
        .product-card .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #1E3A5F, #0891B2);
            border-radius: 6px;
            transition: width 1s ease-out;
        }
        .product-card .maturity-label {
            display: flex;
            justify-content: space-between;
            margin-top: 0.4rem;
            font-size: 0.75rem;
            color: #64748b;
        }
    </style>
    
    <div class="product-grid">
        <div class="product-card" style="animation-delay: 0.1s;">
            <div class="card-icon">📍</div>
            <div class="card-name">Mobility & Footfall</div>
            <div class="card-privacy">Aggregated</div>
            <div class="progress-bar"><div class="progress-fill" style="width: 95%;"></div></div>
            <div class="maturity-label"><span>Maturity</span><span>95%</span></div>
        </div>
        <div class="product-card" style="animation-delay: 0.15s;">
            <div class="card-icon">👥</div>
            <div class="card-name">Audience Segments</div>
            <div class="card-privacy">Cohort-based</div>
            <div class="progress-bar"><div class="progress-fill" style="width: 85%;"></div></div>
            <div class="maturity-label"><span>Maturity</span><span>85%</span></div>
        </div>
        <div class="product-card" style="animation-delay: 0.2s;">
            <div class="card-icon">📶</div>
            <div class="card-name">Network Quality</div>
            <div class="card-privacy">Aggregated</div>
            <div class="progress-bar"><div class="progress-fill" style="width: 80%;"></div></div>
            <div class="maturity-label"><span>Maturity</span><span>80%</span></div>
        </div>
        <div class="product-card" style="animation-delay: 0.25s;">
            <div class="card-icon">🛡️</div>
            <div class="card-name">Fraud & Risk Signals</div>
            <div class="card-privacy">Scored</div>
            <div class="progress-bar"><div class="progress-fill" style="width: 75%;"></div></div>
            <div class="maturity-label"><span>Maturity</span><span>75%</span></div>
        </div>
        <div class="product-card" style="animation-delay: 0.3s;">
            <div class="card-icon">📡</div>
            <div class="card-name">IoT / 5G Telemetry</div>
            <div class="card-privacy">Device-level</div>
            <div class="progress-bar"><div class="progress-fill" style="width: 70%;"></div></div>
            <div class="maturity-label"><span>Maturity</span><span>70%</span></div>
        </div>
        <div class="product-card" style="animation-delay: 0.35s;">
            <div class="card-icon">🎯</div>
            <div class="card-name">Customer Intent</div>
            <div class="card-privacy">Inferred</div>
            <div class="progress-bar"><div class="progress-fill" style="width: 65%;"></div></div>
            <div class="maturity-label"><span>Maturity</span><span>65%</span></div>
        </div>
    </div>
    """)
    
    st.html("""
    <div class="section-header">
        <h3>🇸🇦 KSA Alignment</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <div class="ksa-highlight">
        <p>🇸🇦 <strong>Saudi Opportunity:</strong> The SDAIA-NEOM partnership (September 2024) explicitly 
        targets AI and data innovation for cognitive city development. Fusion's mobility, network, and 
        CX data products directly align with giga-project needs for real-time density analytics, surge 
        prediction, and infrastructure planning.</p>
    </div>
    """)
    
    # TM Forum Section
    st.html("""
    <div class="section-header">
        <h3>📚 TM Forum Industry Guidance</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.markdown("""
    **TM Forum**, the global industry association for digital business, provides comprehensive guidance 
    on telco data monetization through its Open Digital Framework and research publications.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("**📘 IG1138: External Data Monetization Guide**")
            st.markdown("""
            TM Forum's flagship guide for CSP data monetization covers:
            
            - **Regulations & Compliance** — Privacy requirements by jurisdiction
            - **Privacy Techniques** — Anonymization, aggregation, differential privacy
            - **10 Monetization Use Cases** across Health, Transportation, Finance/Fraud, 
              Advertising, Site Planning, and Tourism
            - **Revenue Conversion** — Moving from data assets to commercial products
            """)
            st.caption("Source: TM Forum IG1138 R15.5.1")
        
        with st.container(border=True):
            st.markdown("**🔄 ODA Monetization Engine**")
            st.markdown("""
            TM Forum's Open Digital Architecture (ODA) provides a standards-based platform to:
            
            - **Unify fragmented data** across legacy and modern systems
            - **Apply governance & automation** frameworks consistently
            - **Convert data assets** into revenue-generating services
            - **Enable secure data movement** via TM Forum-certified APIs 
              (TMF620, TMF622, TMF638-642)
            """)
            st.caption("Source: TM Forum ODA Catalyst, 2024")
    
    with col2:
        with st.container(border=True):
            st.markdown("**🏪 Digital Marketplace Model**")
            st.markdown("""
            TM Forum research highlights **digital marketplaces** as the primary channel 
            for data monetization:
            
            - **Self-service discovery** — Partners find and subscribe to data products
            - **Micro-segmentation** — Target specific demographics geographically
            - **5G data explosion** — Mobile data usage projected to reach 56GB/smartphone by 2029
            - **IoT scale** — 55.7 billion IoT devices estimated by 2025
            """)
            st.caption("Source: TM Forum Inform, 'How telcos can monetize data through digital marketplaces'")
        
        with st.container(border=True):
            st.markdown("**⚠️ The Monetization Gap**")
            st.markdown("""
            TM Forum research identifies a critical challenge:
            
            > *"While CSPs possess vast data assets and have invested heavily in big data platforms, 
            most haven't achieved tangible ROI."*
            
            **Key barriers:** Legacy IT silos, fragmented data, lack of governance, 
            and inability to package data as consumable products.
            
            **Solution:** Move from static data collection to **dynamic intelligence exchange** 
            using governed, API-accessible data products.
            """)
            st.caption("Source: TM Forum IG1138")
    
    st.html("""
    <div class="key-insight">
        <p>💡 <strong>TM Forum Recommendation:</strong> CSPs should pursue <strong>external data monetization</strong> 
        (selling insights to third parties) alongside internal use cases to significantly increase revenue. 
        The shift is from being <strong>data custodians</strong> to <strong>digital service orchestrators</strong>.</p>
    </div>
    """)
    
    # TM Forum Use Cases
    st.html("""
    <div class="section-header">
        <h3>🎯 TM Forum Use Case Framework</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    tmf_use_cases = pd.DataFrame({
        'Vertical': ['🏥 Health', '🚗 Transportation', '🏦 Finance/Fraud', '📣 Advertising', '📍 Site Planning', '✈️ Tourism'],
        'Data Products': [
            'Population health patterns, mobility for outbreak tracking',
            'Traffic flow, commuter patterns, route optimization',
            'Fraud detection signals, credit risk scoring, geo-behavior',
            'Audience segments, campaign measurement, attribution',
            'Footfall analytics, catchment analysis, location scoring',
            'Visitor flows, origin-destination, seasonal patterns'
        ],
        'Privacy Model': ['Aggregated', 'Aggregated', 'Scored/Anonymized', 'Cohort-based', 'Aggregated', 'Aggregated']
    })
    
    with st.container(border=True):
        st.dataframe(
            tmf_use_cases,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Vertical": st.column_config.TextColumn("Industry Vertical", width="medium"),
                "Data Products": st.column_config.TextColumn("Example Data Products", width="large"),
                "Privacy Model": st.column_config.TextColumn("Privacy Model", width="medium")
            }
        )
    
    st.caption("Source: TM Forum IG1138 — Introductory Guide to External Data Monetization")

# =============================================================================
# TAB 3: MARKET DEMAND
# =============================================================================
with tab_demand:
    st.html("""
    <div class="section-header">
        <h3>📊 Market Size & Growth</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <style>
        @keyframes numberPop {
            0% { transform: scale(0.5); opacity: 0; }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); opacity: 1; }
        }
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        .market-stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.25rem;
            margin-bottom: 1rem;
        }
        @media (max-width: 768px) {
            .market-stats-grid { grid-template-columns: 1fr; }
        }
        .market-stat-card {
            border-radius: 16px;
            padding: 1.75rem 1.5rem;
            text-align: center;
            position: relative;
            overflow: hidden;
            animation: slideUp 0.6s ease-out backwards;
        }
        .market-stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            background-size: 200% 100%;
            animation: shimmer 3s ease-in-out infinite;
        }
        .market-stat-card.blue {
            background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 100%);
        }
        .market-stat-card.teal {
            background: linear-gradient(135deg, #0891B2 0%, #10B981 100%);
        }
        .market-stat-card.gold {
            background: linear-gradient(135deg, #D4AF37 0%, #F59E0B 100%);
        }
        .market-stat-card .stat-value {
            font-size: 2.8rem;
            font-weight: 800;
            color: white;
            margin: 0;
            position: relative;
            z-index: 1;
            animation: numberPop 0.8s ease-out backwards;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        .market-stat-card .stat-label {
            font-size: 0.9rem;
            color: rgba(255,255,255,0.9);
            margin-top: 0.5rem;
            position: relative;
            z-index: 1;
        }
        .market-stat-card .stat-source {
            font-size: 0.7rem;
            color: rgba(255,255,255,0.6);
            margin-top: 0.75rem;
            position: relative;
            z-index: 1;
            font-style: italic;
        }
    </style>
    
    <div class="market-stats-grid">
        <div class="market-stat-card blue" style="animation-delay: 0.1s;">
            <p class="stat-value" style="animation-delay: 0.3s;">~$5.3B</p>
            <p class="stat-label">Global Market 2024</p>
            <p class="stat-source">Precedence Research, 2024</p>
        </div>
        <div class="market-stat-card teal" style="animation-delay: 0.2s;">
            <p class="stat-value" style="animation-delay: 0.4s;">$14.9B</p>
            <p class="stat-label">Projected by 2029</p>
            <p class="stat-source">Market Research Future</p>
        </div>
        <div class="market-stat-card gold" style="animation-delay: 0.3s;">
            <p class="stat-value" style="animation-delay: 0.5s;">~24%</p>
            <p class="stat-label">CAGR Growth Rate</p>
            <p class="stat-source">Industry Consensus</p>
        </div>
    </div>
    """)
    
    st.html("""
    <div class="key-insight">
        <p>💡 <strong>Message:</strong> "This is now a multi-billion-dollar, high-growth segment, not an experiment."</p>
    </div>
    """)
    
    # Market growth chart
    market_data = pd.DataFrame({
        'Year': [2024, 2025, 2026, 2027, 2028, 2029],
        'Market Size ($B)': [5.3, 6.6, 8.2, 10.2, 12.5, 14.9],
        'Type': ['Actual'] + ['Projected'] * 5
    })
    
    st.html("""
    <style>
        @keyframes chartReveal {
            from { 
                clip-path: inset(0 100% 0 0);
                opacity: 0.5;
            }
            to { 
                clip-path: inset(0 0 0 0);
                opacity: 1;
            }
        }
        @keyframes pulseGlow {
            0%, 100% { box-shadow: 0 4px 20px rgba(8, 145, 178, 0.1); }
            50% { box-shadow: 0 4px 30px rgba(8, 145, 178, 0.25); }
        }
        .chart-container {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            animation: fadeInUp 0.6s ease-out, pulseGlow 3s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }
        .chart-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #1E3A5F, #0891B2, #D4AF37);
            border-radius: 16px 16px 0 0;
        }
        .chart-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #1E3A5F;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .chart-title-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #0891B2, #1E3A5F);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
        }
        .chart-subtitle {
            font-size: 0.85rem;
            color: #64748b;
            margin-bottom: 1rem;
        }
        .chart-wrapper {
            animation: chartReveal 1.5s ease-out 0.3s backwards;
        }
        .chart-sources {
            margin-top: 1rem;
            padding-top: 0.75rem;
            border-top: 1px solid #e2e8f0;
            font-size: 0.75rem;
            color: #94a3b8;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .chart-sources::before {
            content: '📊';
        }
        .growth-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            background: linear-gradient(135deg, #10B981, #34D399);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-left: auto;
            animation: pulse 2s ease-in-out infinite;
        }
    </style>
    <div class="chart-container">
        <div style="display: flex; align-items: center;">
            <div class="chart-title">
                <div class="chart-title-icon">📈</div>
                Global Telco Data Monetization Market Trajectory
            </div>
            <span class="growth-badge">↑ ~24% CAGR</span>
        </div>
        <div class="chart-subtitle">Projected growth from $5.3B (2024) to $14.9B (2029)</div>
    </div>
    """)
    
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
            alt.Tooltip('Market Size ($B):Q', title='Market Size', format='$,.1f')
        ]
    ).properties(height=300)
    
    points = alt.Chart(market_data).mark_circle(size=100, color=FUSION_TEAL).encode(
        x='Year:O',
        y='Market Size ($B):Q'
    )
    
    st.altair_chart(market_chart + points, use_container_width=True)
    
    st.html("""
    <div class="chart-sources">
        Sources: Precedence Research, Market Research Future, Mordor Intelligence — Telecom Data Monetization Market Reports 2024
    </div>
    """)
    
    st.html("""
    <div class="section-header">
        <h3>🎯 Who is Buying What?</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <style>
        .use-case-container {
            margin: 1.5rem 0;
        }
        .industry-section {
            margin-bottom: 2rem;
            animation: fadeInUp 0.6s ease-out backwards;
        }
        .industry-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #e2e8f0;
        }
        .industry-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #1E3A5F, #0891B2);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        .industry-name {
            font-size: 1.1rem;
            font-weight: 700;
            color: #1E3A5F;
            margin: 0;
        }
        .industry-tag {
            background: #f0fdfa;
            color: #0891B2;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-left: auto;
        }
        .industry-tag.hot {
            background: #fef3c7;
            color: #d97706;
        }
        .use-cases-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 0.75rem;
        }
        .use-case-chip {
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 0.875rem 1rem;
            display: flex;
            align-items: flex-start;
            gap: 0.6rem;
            transition: all 0.3s ease;
            animation: fadeInUp 0.4s ease-out backwards;
        }
        .use-case-chip:hover {
            border-color: #0891B2;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(30, 58, 95, 0.1);
        }
        .use-case-chip .chip-icon {
            font-size: 1.2rem;
            flex-shrink: 0;
        }
        .use-case-chip .chip-content {
            flex: 1;
        }
        .use-case-chip .chip-title {
            font-weight: 600;
            font-size: 0.85rem;
            color: #1E3A5F;
            margin-bottom: 0.2rem;
        }
        .use-case-chip .chip-desc {
            font-size: 0.75rem;
            color: #64748b;
            line-height: 1.4;
        }
    </style>
    
    <div class="use-case-container">
        <!-- Government & Smart Cities -->
        <div class="industry-section" style="animation-delay: 0.1s;">
            <div class="industry-header">
                <div class="industry-icon">🏛️</div>
                <h4 class="industry-name">Government & Smart Cities</h4>
                <span class="industry-tag hot">High Priority for KSA</span>
            </div>
            <div class="use-cases-grid">
                <div class="use-case-chip" style="animation-delay: 0.15s;">
                    <span class="chip-icon">📊</span>
                    <div class="chip-content">
                        <div class="chip-title">Population Analytics</div>
                        <div class="chip-desc">Real-time density, demographic distribution</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.2s;">
                    <span class="chip-icon">🚨</span>
                    <div class="chip-content">
                        <div class="chip-title">Emergency Response</div>
                        <div class="chip-desc">Crowd surge prediction, evacuation planning</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.25s;">
                    <span class="chip-icon">🏗️</span>
                    <div class="chip-content">
                        <div class="chip-title">Infrastructure Planning</div>
                        <div class="chip-desc">Transport routes, utility demand forecasting</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.3s;">
                    <span class="chip-icon">🎉</span>
                    <div class="chip-content">
                        <div class="chip-title">Event Management</div>
                        <div class="chip-desc">Crowd flow, capacity optimization</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Retail & Real Estate -->
        <div class="industry-section" style="animation-delay: 0.2s;">
            <div class="industry-header">
                <div class="industry-icon">🏪</div>
                <h4 class="industry-name">Retail & Real Estate</h4>
                <span class="industry-tag">High Demand</span>
            </div>
            <div class="use-cases-grid">
                <div class="use-case-chip" style="animation-delay: 0.25s;">
                    <span class="chip-icon">📍</span>
                    <div class="chip-content">
                        <div class="chip-title">Site Selection</div>
                        <div class="chip-desc">Optimal store/branch locations</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.3s;">
                    <span class="chip-icon">👣</span>
                    <div class="chip-content">
                        <div class="chip-title">Foot Traffic Analysis</div>
                        <div class="chip-desc">Hourly/daily visitor patterns</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.35s;">
                    <span class="chip-icon">🎯</span>
                    <div class="chip-content">
                        <div class="chip-title">Catchment Analysis</div>
                        <div class="chip-desc">Trade area, customer origin</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.4s;">
                    <span class="chip-icon">⚔️</span>
                    <div class="chip-content">
                        <div class="chip-title">Competitive Intel</div>
                        <div class="chip-desc">Competitor foot traffic benchmarking</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Tourism & Hospitality -->
        <div class="industry-section" style="animation-delay: 0.3s;">
            <div class="industry-header">
                <div class="industry-icon">✈️</div>
                <h4 class="industry-name">Tourism & Hospitality</h4>
                <span class="industry-tag hot">Growing Fast</span>
            </div>
            <div class="use-cases-grid">
                <div class="use-case-chip" style="animation-delay: 0.35s;">
                    <span class="chip-icon">🗺️</span>
                    <div class="chip-content">
                        <div class="chip-title">Visitor Flow Mapping</div>
                        <div class="chip-desc">Tourist routes, attraction popularity</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.4s;">
                    <span class="chip-icon">🌍</span>
                    <div class="chip-content">
                        <div class="chip-title">Origin-Destination</div>
                        <div class="chip-desc">Where visitors come from</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.45s;">
                    <span class="chip-icon">📅</span>
                    <div class="chip-content">
                        <div class="chip-title">Seasonal Patterns</div>
                        <div class="chip-desc">Peak periods, trend forecasting</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.5s;">
                    <span class="chip-icon">⏱️</span>
                    <div class="chip-content">
                        <div class="chip-title">Dwell Time Hotspots</div>
                        <div class="chip-desc">High-engagement areas</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Transport & Logistics -->
        <div class="industry-section" style="animation-delay: 0.4s;">
            <div class="industry-header">
                <div class="industry-icon">🚌</div>
                <h4 class="industry-name">Transport & Logistics</h4>
                <span class="industry-tag">Steady Demand</span>
            </div>
            <div class="use-cases-grid">
                <div class="use-case-chip" style="animation-delay: 0.45s;">
                    <span class="chip-icon">🛤️</span>
                    <div class="chip-content">
                        <div class="chip-title">Route Optimization</div>
                        <div class="chip-desc">Delivery efficiency, traffic patterns</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.5s;">
                    <span class="chip-icon">🚇</span>
                    <div class="chip-content">
                        <div class="chip-title">Commuter Analysis</div>
                        <div class="chip-desc">Peak hours, corridor demand</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.55s;">
                    <span class="chip-icon">✈️</span>
                    <div class="chip-content">
                        <div class="chip-title">Hub Capacity</div>
                        <div class="chip-desc">Airport/station planning</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.6s;">
                    <span class="chip-icon">📦</span>
                    <div class="chip-content">
                        <div class="chip-title">Last-Mile Insights</div>
                        <div class="chip-desc">Delivery zone optimization</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Financial Services -->
        <div class="industry-section" style="animation-delay: 0.5s;">
            <div class="industry-header">
                <div class="industry-icon">🏦</div>
                <h4 class="industry-name">Financial Services & Insurance</h4>
                <span class="industry-tag">Emerging</span>
            </div>
            <div class="use-cases-grid">
                <div class="use-case-chip" style="animation-delay: 0.55s;">
                    <span class="chip-icon">🛡️</span>
                    <div class="chip-content">
                        <div class="chip-title">Fraud Detection</div>
                        <div class="chip-desc">Location-based anomaly signals</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.6s;">
                    <span class="chip-icon">📋</span>
                    <div class="chip-content">
                        <div class="chip-title">Risk Scoring</div>
                        <div class="chip-desc">Geo-behavior for underwriting</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.65s;">
                    <span class="chip-icon">🏧</span>
                    <div class="chip-content">
                        <div class="chip-title">Branch Network</div>
                        <div class="chip-desc">ATM/branch placement optimization</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.7s;">
                    <span class="chip-icon">💳</span>
                    <div class="chip-content">
                        <div class="chip-title">Credit Signals</div>
                        <div class="chip-desc">Alternative data for thin-file customers</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Advertising & Media -->
        <div class="industry-section" style="animation-delay: 0.6s;">
            <div class="industry-header">
                <div class="industry-icon">📣</div>
                <h4 class="industry-name">Advertising & Media</h4>
                <span class="industry-tag">Privacy-First</span>
            </div>
            <div class="use-cases-grid">
                <div class="use-case-chip" style="animation-delay: 0.65s;">
                    <span class="chip-icon">👥</span>
                    <div class="chip-content">
                        <div class="chip-title">Audience Segments</div>
                        <div class="chip-desc">Privacy-safe cohorts for targeting</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.7s;">
                    <span class="chip-icon">📺</span>
                    <div class="chip-content">
                        <div class="chip-title">OOH Measurement</div>
                        <div class="chip-desc">Billboard/screen exposure analytics</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.75s;">
                    <span class="chip-icon">📈</span>
                    <div class="chip-content">
                        <div class="chip-title">Attribution</div>
                        <div class="chip-desc">Ad exposure to store visit</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.8s;">
                    <span class="chip-icon">🎯</span>
                    <div class="chip-content">
                        <div class="chip-title">Campaign Measurement</div>
                        <div class="chip-desc">Reach, frequency, uplift</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """)
    
    st.html("""
    <div class="section-header">
        <h3>📱 How They Prefer to Consume</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <div class="intro-card">
        <p style="color: #64748b; line-height: 1.7; margin: 0;">
            TM Forum and market research show telcos moving to <strong>digital marketplaces and platforms</strong> 
            where enterprises can self-service discover, subscribe, and integrate telco data products rather 
            than bespoke one-offs. The shift is from custom integrations to standardized, governed data products 
            with clear APIs and SLAs.
        </p>
    </div>
    """)
    
    st.html("""
    <div class="position-box">
        <p><strong>For Fusion:</strong> "We see strong demand from governments, banks, and retailers for exactly 
        the kinds of mobility, network and identity-adjacent signals Fusion already has—as long as we deliver 
        them as <strong>governed products, not raw feeds</strong>."</p>
    </div>
    """)

# =============================================================================
# TAB 4: PRICING MODELS
# =============================================================================
with tab_pricing:
    st.html("""
    <div class="section-header">
        <h3>🧰 The Pricing Toolbox</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.markdown("""
    There's no single global tariff sheet, but there are clear patterns. Here's the pricing toolbox 
    telcos use for data products:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.html("""
        <div class="pricing-model recommended" style="animation-delay: 0.1s; margin-bottom: 1rem;">
            <div class="pricing-tag">MOST COMMON</div>
            <div class="pricing-icon">🔄</div>
            <div class="pricing-name">Subscription / Recurring Licenses</div>
            <div class="pricing-desc">
                Monthly/annual subscription per data product + geography + freshness 
                (e.g., Riyadh daily mobility insights, KSA-wide weekly, GCC regional).
            </div>
            <div class="pricing-details">
                Often tiered by volume, history window, SLA, and number of users/use-cases. 
                Core revenue stream for real-time and historical insight feeds.
            </div>
        </div>
        """)
        
        st.html("""
        <div class="pricing-model" style="animation-delay: 0.3s; margin-bottom: 1rem;">
            <div class="pricing-icon">📁</div>
            <div class="pricing-name">Flat Licenses for Static/Historical Data</div>
            <div class="pricing-desc">
                One-off or annual license for historic archives (e.g., 3 years of aggregated mobility).
            </div>
            <div class="pricing-details">
                Often used for consulting, strategy projects, and model training. Lower recurring 
                revenue but good for market entry.
            </div>
        </div>
        """)
        
        st.html("""
        <div class="pricing-model" style="animation-delay: 0.5s;">
            <div class="pricing-icon">🎯</div>
            <div class="pricing-name">Outcome / Revenue-Share Models</div>
            <div class="pricing-desc">
                For advertising, insurance, or retail uplift, some telcos use rev-share or 
                success-based fees with partners.
            </div>
            <div class="pricing-details">
                Especially for "Powered-by-[Telco]" white-label platforms and APIs. Aligns 
                incentives but requires strong measurement.
            </div>
        </div>
        """)
    
    with col2:
        st.html("""
        <div class="pricing-model recommended" style="animation-delay: 0.2s; margin-bottom: 1rem;">
            <div class="pricing-tag">SCALABLE</div>
            <div class="pricing-icon">📊</div>
            <div class="pricing-name">Usage-Based / API-Metered</div>
            <div class="pricing-desc">
                Pay-per-API call, per 1k queries, or per 1k records scored (for prediction services).
            </div>
            <div class="pricing-details">
                Market studies highlight license fee, pay-per-use, and subscription as the main 
                commercial models. Great for developer adoption and variable workloads.
            </div>
        </div>
        """)
        
        st.html("""
        <div class="pricing-model" style="animation-delay: 0.4s;">
            <div class="pricing-icon">🎁</div>
            <div class="pricing-name">Freemium / Trial Tiers via Marketplaces</div>
            <div class="pricing-desc">
                Provide sample/low-granularity datasets for free; charge for higher resolution, 
                more history, or custom segments.
            </div>
            <div class="pricing-details">
                Trials, paid POCs, and usage-based experiments are standard practice for data 
                products. Reduces friction for new customers.
            </div>
        </div>
        """)
    
    st.html("""
    <div class="section-header">
        <h3>💡 Pricing Recommendation for Fusion</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <div class="position-box">
        <p><strong>Recommended approach:</strong> "Globally we see subscription for core data products, 
        usage-based for APIs and predictions, and rev-share where we co-create services with partners. 
        We'd recommend starting simple (<strong>tiered subscription + usage-based API</strong>) and then 
        adding outcome-based pricing where we have strong partners like banks or ad platforms."</p>
    </div>
    """)
    
    st.html("""
    <div class="section-header">
        <h3>📋 Pricing Dimensions</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <style>
        .dimensions-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin: 1rem 0;
        }
        @media (max-width: 900px) {
            .dimensions-grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 500px) {
            .dimensions-grid { grid-template-columns: 1fr; }
        }
        .dimension-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.5s ease-out backwards;
            transition: all 0.3s ease;
        }
        .dimension-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(30, 58, 95, 0.12);
            border-color: #0891B2;
        }
        .dimension-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            border-radius: 16px 16px 0 0;
        }
        .dimension-card.geo::before { background: linear-gradient(90deg, #1E3A5F, #0891B2); }
        .dimension-card.fresh::before { background: linear-gradient(90deg, #10B981, #34D399); }
        .dimension-card.volume::before { background: linear-gradient(90deg, #8B5CF6, #A78BFA); }
        .dimension-card.history::before { background: linear-gradient(90deg, #D4AF37, #F59E0B); }
        
        .dimension-header {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin-bottom: 1rem;
        }
        .dimension-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
        }
        .dimension-card.geo .dimension-icon { background: linear-gradient(135deg, #1E3A5F, #0891B2); }
        .dimension-card.fresh .dimension-icon { background: linear-gradient(135deg, #10B981, #34D399); }
        .dimension-card.volume .dimension-icon { background: linear-gradient(135deg, #8B5CF6, #A78BFA); }
        .dimension-card.history .dimension-icon { background: linear-gradient(135deg, #D4AF37, #F59E0B); }
        
        .dimension-name {
            font-weight: 700;
            font-size: 1rem;
            color: #1E3A5F;
        }
        .dimension-items {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        .dimension-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 0.75rem;
            background: #f8fafc;
            border-radius: 8px;
            font-size: 0.85rem;
            color: #475569;
            transition: all 0.2s ease;
        }
        .dimension-item:hover {
            background: #f0fdfa;
            color: #0891B2;
            transform: translateX(4px);
        }
        .dimension-item .item-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            flex-shrink: 0;
        }
        .dimension-card.geo .item-dot { background: #0891B2; }
        .dimension-card.fresh .item-dot { background: #10B981; }
        .dimension-card.volume .item-dot { background: #8B5CF6; }
        .dimension-card.history .item-dot { background: #D4AF37; }
    </style>
    
    <div class="dimensions-grid">
        <div class="dimension-card geo" style="animation-delay: 0.1s;">
            <div class="dimension-header">
                <div class="dimension-icon">🌍</div>
                <span class="dimension-name">Geography</span>
            </div>
            <div class="dimension-items">
                <div class="dimension-item"><span class="item-dot"></span>City-level</div>
                <div class="dimension-item"><span class="item-dot"></span>National (KSA)</div>
                <div class="dimension-item"><span class="item-dot"></span>Regional (GCC)</div>
                <div class="dimension-item"><span class="item-dot"></span>Custom zones</div>
            </div>
        </div>
        <div class="dimension-card fresh" style="animation-delay: 0.2s;">
            <div class="dimension-header">
                <div class="dimension-icon">⚡</div>
                <span class="dimension-name">Freshness</span>
            </div>
            <div class="dimension-items">
                <div class="dimension-item"><span class="item-dot"></span>Real-time</div>
                <div class="dimension-item"><span class="item-dot"></span>Hourly</div>
                <div class="dimension-item"><span class="item-dot"></span>Daily</div>
                <div class="dimension-item"><span class="item-dot"></span>Weekly / Monthly</div>
            </div>
        </div>
        <div class="dimension-card volume" style="animation-delay: 0.3s;">
            <div class="dimension-header">
                <div class="dimension-icon">📊</div>
                <span class="dimension-name">Volume</span>
            </div>
            <div class="dimension-items">
                <div class="dimension-item"><span class="item-dot"></span>Record count</div>
                <div class="dimension-item"><span class="item-dot"></span>Query limits</div>
                <div class="dimension-item"><span class="item-dot"></span>API calls/month</div>
                <div class="dimension-item"><span class="item-dot"></span>User seats</div>
            </div>
        </div>
        <div class="dimension-card history" style="animation-delay: 0.4s;">
            <div class="dimension-header">
                <div class="dimension-icon">📅</div>
                <span class="dimension-name">History</span>
            </div>
            <div class="dimension-items">
                <div class="dimension-item"><span class="item-dot"></span>30 days rolling</div>
                <div class="dimension-item"><span class="item-dot"></span>1 year archive</div>
                <div class="dimension-item"><span class="item-dot"></span>3+ years deep</div>
                <div class="dimension-item"><span class="item-dot"></span>Custom range</div>
            </div>
        </div>
    </div>
    """)

# =============================================================================
# TAB 5: DATA DISTRIBUTION
# =============================================================================
with tab_distribution:
    st.html("""
    <div class="section-header">
        <h3>🌐 Reaching Consumers Without a Snowflake Account</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.markdown("""
    All options use **Snowflake as Fusion's platform** but abstract it from the end consumer. 
    Here's the menu of distribution options with the specific Snowflake features that enable each:
    """)
    
    # Option 1: Reader Accounts
    with st.container(border=True):
        col_icon, col_content = st.columns([1, 11])
        with col_icon:
            st.html("""<div class="distribution-icon">👤</div>""")
        with col_content:
            st.markdown("### Reader-Style Access")
            st.markdown("""
            Fusion hosts the data in Snowflake and provisions governed, read-only endpoints for 
            agencies or enterprises. The consumer doesn't need their own Snowflake contract; 
            Fusion controls the account, roles, policies, and pays for compute.
            """)
        
        st.html("""<div class="distribution-tag">Best for: Government entities who want dashboards/SQL</div>""")
        
        st.markdown("**Snowflake Features:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - **Reader Accounts** — Managed accounts Fusion creates for consumers; no separate Snowflake contract needed
            - **Resource Monitors** — Set compute budgets per consumer to control costs
            - **Network Policies** — Restrict access by IP range for security
            """)
        with col2:
            st.markdown("""
            - **Role-Based Access Control (RBAC)** — Fine-grained permissions per user/group
            - **Object Tagging** — Classify data sensitivity for governance
            - **Query History & Access History** — Full audit trail of who accessed what
            """)
    
    # Option 2: Streamlit Apps / Portals
    with st.container(border=True):
        col_icon, col_content = st.columns([1, 11])
        with col_icon:
            st.html("""<div class="distribution-icon">📱</div>""")
        with col_content:
            st.markdown("### \"Powered-by Fusion\" Applications & Portals")
            st.markdown("""
            Build web or mobile apps (e.g., city operations dashboard, tourism insights portal, 
            government analytics cockpit) where Snowflake is the backend and the user only sees 
            Fusion's UI. For KSA, this could be a "Fusion Data Exchange Portal" with SSO.
            """)
        
        st.html("""<div class="distribution-tag">Best for: Business users and ministries</div>""")
        
        st.markdown("**Snowflake Features:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - **Streamlit in Snowflake** — Build and host Python apps directly in Snowflake; no external infra needed
            - **Snowflake Native Apps** — Package apps + data as installable products consumers run in their account
            - **Snowsight Dashboards** — No-code dashboards with filters, charts, and sharing
            """)
        with col2:
            st.markdown("""
            - **OAuth / SAML SSO** — Integrate with ministry identity providers (Azure AD, Okta, etc.)
            - **Row Access Policies** — Each ministry sees only their entitled data automatically
            - **Secure Views** — Expose curated datasets without revealing underlying tables
            """)
    
    # Option 3: APIs
    with st.container(border=True):
        col_icon, col_content = st.columns([1, 11])
        with col_icon:
            st.html("""<div class="distribution-icon">🔌</div>""")
        with col_content:
            st.markdown("### APIs and Services on Top of Snowflake")
            st.markdown("""
            Expose REST/GraphQL APIs for queries like "give me today's footfall by district" or 
            "score this list of locations", implemented via services that query Snowflake. 
            API usage (pay-per-call) is a core revenue stream.
            """)
        
        st.html("""<div class="distribution-tag">Best for: Developers and system integrations</div>""")
        
        st.markdown("**Snowflake Features:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - **Snowflake REST API** — Native SQL API for programmatic access with OAuth/key-pair auth
            - **Snowpark Container Services** — Deploy custom API containers (FastAPI, Flask) inside Snowflake
            - **External Functions** — Call external ML models or services from SQL
            """)
        with col2:
            st.markdown("""
            - **Snowflake Connector for Python/Java/.NET** — Native drivers for any backend
            - **Usage Metering** — Track API calls per consumer for billing
            - **Warehouse Auto-Suspend/Resume** — Pay only when queries run
            """)
    
    # Option 4: Clean Rooms
    with st.container(border=True):
        col_icon, col_content = st.columns([1, 11])
        with col_icon:
            st.html("""<div class="distribution-icon">🔒</div>""")
        with col_content:
            st.markdown("### Clean Rooms for Joint Analysis")
            st.markdown("""
            Use Snowflake Clean Rooms so government agencies can run approved queries that join 
            their data with Fusion's, without ever exchanging raw PII. Access can be via their 
            tools or a simple front-end; governed products with row/masking policies attached.
            """)
        
        st.html("""<div class="distribution-tag">Best for: Privacy-sensitive joint analytics</div>""")
        
        st.markdown("**Snowflake Features:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - **Snowflake Data Clean Rooms** — Pre-built templates for secure overlap analysis, attribution, lookalikes
            - **Secure Data Sharing** — Share live data without copying; consumer queries Fusion's tables in-place
            - **Differential Privacy** — Add statistical noise to prevent re-identification
            """)
        with col2:
            st.markdown("""
            - **Dynamic Data Masking** — Mask PII columns based on consumer role (e.g., show city but hide exact lat/lon)
            - **Aggregation Policies** — Enforce minimum group sizes (e.g., no results with <100 people)
            - **Projection Policies** — Control which columns each consumer can select
            """)
    
    # Option 5: File Exports
    with st.container(border=True):
        col_icon, col_content = st.columns([1, 11])
        with col_icon:
            st.html("""<div class="distribution-icon">📁</div>""")
        with col_content:
            st.markdown("### Files / Object-Store Exports")
            st.markdown("""
            If a specific agency can only consume files (CSV/Parquet in S3/Blob), Fusion can 
            schedule governed exports from Snowflake. This is the least powerful option 
            (no live data, harder to govern/audit).
            """)
        
        st.html("""<div class="distribution-tag warning">Fallback option — limited governance</div>""")
        
        st.markdown("**Snowflake Features:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - **COPY INTO (Unload)** — Export query results to S3, Azure Blob, or GCS in CSV/Parquet/JSON
            - **Tasks & Streams** — Schedule automated exports on data changes or time intervals
            - **External Stages** — Managed connection to cloud storage with encryption
            """)
        with col2:
            st.markdown("""
            - **Storage Integration** — Secure, credential-free access to cloud buckets
            - **Data Retention Policies** — Auto-delete old exports after N days
            - **File Format Options** — Compression (gzip, snappy), partitioning, headers
            """)
    
    st.html("""
    <div class="section-header">
        <h3>📋 Distribution Method Comparison</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    comparison_data = pd.DataFrame({
        'Method': ['Reader Accounts', 'Streamlit / Native Apps', 'REST APIs', 'Clean Rooms', 'File Exports'],
        'Snowflake Feature': ['Reader Accounts + RBAC', 'Streamlit in Snowflake', 'Snowpark Container Services', 'Data Clean Rooms', 'COPY INTO + Tasks'],
        'Consumer Needs': ['Browser only', 'Browser + SSO', 'Developer skills', 'Analyst skills', 'File handling'],
        'Live Data': ['✓', '✓', '✓', '✓', '✗'],
        'Governance': ['High', 'High', 'High', 'Very High', 'Low'],
        'Best For': ['Govt dashboards', 'Ministry portals', 'System integration', 'Joint analytics', 'Legacy systems']
    })
    
    with st.container(border=True):
        st.dataframe(
            comparison_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Method": st.column_config.TextColumn("Distribution Method", width="medium"),
                "Snowflake Feature": st.column_config.TextColumn("Key Snowflake Feature", width="large"),
                "Consumer Needs": st.column_config.TextColumn("Consumer Needs"),
                "Live Data": st.column_config.TextColumn("Live"),
                "Governance": st.column_config.TextColumn("Governance"),
                "Best For": st.column_config.TextColumn("Best For", width="medium")
            }
        )
    
    st.html("""
    <div class="section-header">
        <h3>🏗️ Snowflake Governance Stack</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.markdown("These governance features apply across **all** distribution methods:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("**🔐 Access Control**")
            st.caption("• Role-Based Access Control (RBAC)")
            st.caption("• Row Access Policies")
            st.caption("• Column-Level Security")
            st.caption("• Network Policies (IP allowlists)")
            st.caption("• Multi-Factor Authentication")
    
    with col2:
        with st.container(border=True):
            st.markdown("**🛡️ Data Protection**")
            st.caption("• Dynamic Data Masking")
            st.caption("• Aggregation Policies")
            st.caption("• Projection Policies")
            st.caption("• Secure Views")
            st.caption("• End-to-End Encryption")
    
    with col3:
        with st.container(border=True):
            st.markdown("**📊 Audit & Compliance**")
            st.caption("• Query History (90 days)")
            st.caption("• Access History")
            st.caption("• Object Tagging & Classification")
            st.caption("• Data Lineage (Horizon)")
            st.caption("• SOC 2 / ISO 27001 / GDPR")
    
    st.html("""
    <div class="key-insight">
        <p>💡 <strong>Recommendation:</strong> For maximum reach, combine <strong>Streamlit Apps</strong> 
        (for government self-service), <strong>Snowpark Container Services APIs</strong> (for developer integrations), and 
        <strong>Clean Rooms</strong> (for privacy-sensitive joint analytics with ministries). 
        This covers 90%+ of potential KSA customer segments while maintaining full data governance.</p>
    </div>
    """)
    
    st.html("""
    <div class="position-box">
        <p><strong>For KSA Government:</strong> Position as a "Fusion Data Exchange Portal" built with 
        <strong>Streamlit in Snowflake</strong>, integrated with ministry SSO via <strong>SAML/OAuth</strong>, 
        where each ministry only sees entitled data via <strong>Row Access Policies</strong>. 
        Snowflake stays invisible; Fusion delivers governed insights through a trusted, branded experience.</p>
    </div>
    """)
