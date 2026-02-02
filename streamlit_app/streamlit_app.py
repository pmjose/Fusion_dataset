import streamlit as st

st.set_page_config(
    page_title="Fusion - Saudi Mobility Intelligence",
    page_icon="logo.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.logo("logo.jpg")

st.html("""
<style>
    /* Global animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 50%, #1E3A5F 100%);
        background-size: 200% 200%;
        animation: gradientFlow 8s ease infinite, fadeInUp 0.8s ease-out;
        padding: 2.5rem 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(30, 58, 95, 0.3);
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.5;
    }
    .hero-content {
        position: relative;
        z-index: 1;
    }
    .hero-title {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 20px rgba(0,0,0,0.2);
    }
    .hero-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin: 0.8rem 0 1.5rem 0;
        font-weight: 400;
    }
    .hero-badges {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        cursor: default;
    }
    .hero-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    .badge-stc { background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3); }
    .badge-mobily { background: rgba(8,145,178,0.4); color: white; border: 1px solid rgba(8,145,178,0.5); }
    .badge-zain { background: rgba(212,175,55,0.4); color: white; border: 1px solid rgba(212,175,55,0.5); }
    
    /* Stats grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
        animation: fadeInUp 0.8s ease-out 0.2s backwards;
    }
    .stat-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1E3A5F, #0891B2);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(30, 58, 95, 0.15);
        border-color: #0891B2;
    }
    .stat-card:hover::before {
        transform: scaleX(1);
    }
    .stat-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A5F;
        margin: 0;
        background: linear-gradient(135deg, #1E3A5F, #0891B2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stat-label {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 0.3rem;
        font-weight: 500;
    }
    
    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2.5rem 0 1.5rem 0;
        animation: slideInLeft 0.6s ease-out;
    }
    .section-header h2 {
        color: #1E3A5F;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
    }
    .section-line {
        flex: 1;
        height: 2px;
        background: linear-gradient(90deg, #e2e8f0, transparent);
        border-radius: 1px;
    }
    
    /* Offering cards */
    .offerings-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        animation: fadeInUp 0.8s ease-out 0.4s backwards;
    }
    .offering-card {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.8rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .offering-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #0891B2, #D4AF37);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    .offering-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(30, 58, 95, 0.12);
        border-color: transparent;
    }
    .offering-card:hover::after {
        transform: scaleX(1);
    }
    .offering-icon {
        width: 56px;
        height: 56px;
        background: linear-gradient(135deg, #1E3A5F, #0891B2);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: white;
    }
    .offering-title {
        color: #1E3A5F;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .offering-desc {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* Insights table */
    .insights-container {
        animation: fadeInUp 0.8s ease-out 0.6s backwards;
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    .insight-table {
        width: 100%;
        border-collapse: collapse;
    }
    .insight-table th {
        background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        text-align: left;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.02em;
    }
    .insight-table td {
        padding: 1.2rem 1.5rem;
        border-bottom: 1px solid #f1f5f9;
        transition: all 0.2s ease;
    }
    .insight-table tr:last-child td {
        border-bottom: none;
    }
    .insight-table tr:hover td {
        background: linear-gradient(90deg, #f8fafc, #ffffff);
        padding-left: 2rem;
    }
    .insight-category {
        color: #1E3A5F;
        font-weight: 600;
    }
    .insight-desc {
        color: #64748b;
    }
    
    /* Footer CTA */
    .footer-cta {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        text-align: center;
        margin-top: 2rem;
        animation: fadeIn 0.8s ease-out 0.8s backwards;
        border: 1px solid #e2e8f0;
    }
    .footer-cta p {
        color: #64748b;
        margin: 0;
        font-size: 0.95rem;
    }
    
    /* Responsive */
    @media (max-width: 1024px) {
        .stats-grid, .offerings-grid { grid-template-columns: repeat(2, 1fr); }
        .hero-title { font-size: 2.2rem; }
    }
    @media (max-width: 640px) {
        .stats-grid, .offerings-grid { grid-template-columns: 1fr; }
        .hero-section { padding: 1.5rem; }
        .hero-title { font-size: 1.8rem; }
    }
</style>
""")

st.html("""
<div class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">Fusion</h1>
        <p class="hero-subtitle">Saudi Arabia's Premier Mobility Intelligence Platform</p>
        <div class="hero-badges">
            <span class="hero-badge badge-stc">STC</span>
            <span class="hero-badge badge-mobily">Mobily</span>
            <span class="hero-badge badge-zain">Zain</span>
        </div>
    </div>
</div>
""")

st.html("""
<div class="stats-grid">
    <div class="stat-card">
        <p class="stat-value">4.2M+</p>
        <p class="stat-label">Total Records</p>
    </div>
    <div class="stat-card">
        <p class="stat-value">3</p>
        <p class="stat-label">Telco Providers</p>
    </div>
    <div class="stat-card">
        <p class="stat-value">13</p>
        <p class="stat-label">Cities Covered</p>
    </div>
    <div class="stat-card">
        <p class="stat-value">Jan '26</p>
        <p class="stat-label">Data Period</p>
    </div>
</div>
""")

st.html("""
<div class="section-header">
    <h2>Data Product Offerings</h2>
    <div class="section-line"></div>
</div>
""")

st.html("""
<div class="offerings-grid">
    <div class="offering-card">
        <div class="offering-icon">🏪</div>
        <div class="offering-title">Retail & Commercial</div>
        <div class="offering-desc">Site selection, foot traffic analysis, competitor benchmarking</div>
    </div>
    <div class="offering-card">
        <div class="offering-icon">🏛️</div>
        <div class="offering-title">Government & Urban Planning</div>
        <div class="offering-desc">Infrastructure planning, smart city initiatives, population density</div>
    </div>
    <div class="offering-card">
        <div class="offering-icon">✈️</div>
        <div class="offering-title">Tourism & Hospitality</div>
        <div class="offering-desc">Visitor flows, destination analytics, seasonal patterns</div>
    </div>
    <div class="offering-card">
        <div class="offering-icon">🚌</div>
        <div class="offering-title">Transportation</div>
        <div class="offering-desc">Commuter patterns, route optimization, peak hour analysis</div>
    </div>
</div>
""")

st.html("""
<div class="section-header">
    <h2>Available Insights</h2>
    <div class="section-line"></div>
</div>
""")

st.html("""
<div class="insights-container">
    <table class="insight-table">
        <thead>
            <tr>
                <th>Insight Category</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="insight-category">Foot Traffic Trends</td>
                <td class="insight-desc">Hourly and daily traffic patterns across locations</td>
            </tr>
            <tr>
                <td class="insight-category">Demographic Analysis</td>
                <td class="insight-desc">Nationality, age, and gender breakdowns</td>
            </tr>
            <tr>
                <td class="insight-category">Dwell Time Hotspots</td>
                <td class="insight-desc">Areas with highest visitor engagement</td>
            </tr>
            <tr>
                <td class="insight-category">Origin-Destination Flows</td>
                <td class="insight-desc">Cross-city movement patterns</td>
            </tr>
        </tbody>
    </table>
</div>
""")

st.html("""
<div class="footer-cta">
    <p>Navigate using the sidebar to explore data, view analytics, visualize maps, or export data packages.</p>
</div>
""")

with st.sidebar:
    st.caption("Data sourced from STC, Mobily, and Zain mobility networks. All data is anonymized and aggregated.")
