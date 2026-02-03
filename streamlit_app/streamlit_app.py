import streamlit as st

st.set_page_config(
    page_title="Fusion - Saudi Mobility Intelligence",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.logo("logo.jpg")

FUSION_BLUE = "#1E3A5F"
FUSION_TEAL = "#0891B2"
FUSION_GOLD = "#D4AF37"

st.html("""
<style>
    /* =========================================
       SIDEBAR STYLING & ANIMATIONS
       ========================================= */
    
    /* Animation Keyframes */
    @keyframes sidebarFadeIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes logoFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-3px); }
    }
    @keyframes navItemSlide {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 4px 15px rgba(8, 145, 178, 0.2); }
        50% { box-shadow: 0 4px 25px rgba(8, 145, 178, 0.4); }
    }
    
    /* Sidebar Container */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #0f172a 100%) !important;
        border-right: 1px solid rgba(8, 145, 178, 0.2) !important;
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(ellipse at top left, rgba(8, 145, 178, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at bottom right, rgba(212, 175, 55, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        position: relative;
        z-index: 1;
    }
    
    /* Logo Styling */
    [data-testid="stSidebar"] [data-testid="stLogo"] {
        animation: sidebarFadeIn 0.5s ease-out;
    }
    
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
    
    /* Navigation Links */
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
        left: 0;
        top: 0;
        height: 100%;
        width: 0;
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
    
    /* Active Navigation State */
    [data-testid="stSidebar"] a[aria-current="page"],
    [data-testid="stSidebar"] a.active {
        background: linear-gradient(135deg, rgba(8, 145, 178, 0.25) 0%, rgba(30, 58, 95, 0.4) 100%) !important;
        color: #ffffff !important;
        border-left: 3px solid #0891B2 !important;
    }
    
    /* Sidebar Text & Labels */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown p {
        color: #cbd5e1 !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar Divider */
    [data-testid="stSidebar"] hr {
        border-color: rgba(8, 145, 178, 0.2) !important;
        margin: 1rem 0 !important;
    }
    
    /* Sidebar Inputs */
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
    
    /* Custom Scrollbar for Sidebar */
    [data-testid="stSidebar"]::-webkit-scrollbar {
        width: 6px;
    }
    [data-testid="stSidebar"]::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
    }
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #0891B2, #1E3A5F);
        border-radius: 3px;
    }
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #0891B2, #0891B2);
    }
    
    /* Sidebar Caption */
    [data-testid="stSidebar"] .stCaption {
        color: #64748b !important;
        font-size: 0.75rem !important;
    }
    
    /* =========================================
       MAIN PAGE STYLES
       ========================================= */
    
    .fusion-header {
        background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .fusion-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    .fusion-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    .partner-badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        color: white;
        font-size: 0.85rem;
        margin: 0.3rem 0.3rem 0 0;
    }
    .offering-card {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.2rem;
        height: 100%;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .offering-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .offering-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .offering-title {
        color: #1E3A5F;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.3rem;
    }
    .offering-desc {
        color: #64748b;
        font-size: 0.85rem;
        line-height: 1.4;
    }
    .insight-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
    }
    .insight-table th {
        background: #1E3A5F;
        color: white;
        padding: 0.8rem 1rem;
        text-align: left;
        font-weight: 500;
    }
    .insight-table th:first-child { border-radius: 8px 0 0 0; }
    .insight-table th:last-child { border-radius: 0 8px 0 0; }
    .insight-table td {
        padding: 0.8rem 1rem;
        border-bottom: 1px solid #e2e8f0;
    }
    .insight-table tr:last-child td:first-child { border-radius: 0 0 0 8px; }
    .insight-table tr:last-child td:last-child { border-radius: 0 0 8px 0; }
    .insight-table tr:hover td { background: #f8fafc; }
</style>
""")

st.html("""
<div style="padding-top: 0.5rem;">
    <h1 style="color: #1E3A5F; margin: 0; font-size: 2.2rem;">Fusion</h1>
    <p style="color: #64748b; margin: 0.2rem 0 0.5rem 0;">Saudi Arabia's Premier Mobility Intelligence Platform</p>
    <span style="background: #1E3A5F; color: white; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; margin-right: 0.3rem;">STC</span>
    <span style="background: #0891B2; color: white; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; margin-right: 0.3rem;">Mobily</span>
    <span style="background: #D4AF37; color: white; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem;">Zain</span>
</div>
""")

st.markdown("""
Aggregating anonymized mobility data from Saudi Arabia's three major 
telecommunications providers, enabling powerful location-based analytics across the Kingdom.
""")

with st.container(horizontal=True):
    st.metric("Total records", "4.2M+", border=True)
    st.metric("Telco providers", "3", border=True)
    st.metric("Cities covered", "13", border=True)
    st.metric("Date range", "Jan 2026", border=True)

st.subheader("Data product offerings", anchor=False)

offerings = [
    {
        "icon": ":material/store:",
        "title": "Retail & Commercial",
        "desc": "Site selection, foot traffic analysis, competitor benchmarking"
    },
    {
        "icon": ":material/account_balance:",
        "title": "Government & Urban Planning", 
        "desc": "Infrastructure planning, smart city initiatives, population density"
    },
    {
        "icon": ":material/flight:",
        "title": "Tourism & Hospitality",
        "desc": "Visitor flows, destination analytics, seasonal patterns"
    },
    {
        "icon": ":material/directions_bus:",
        "title": "Transportation",
        "desc": "Commuter patterns, route optimization, peak hour analysis"
    }
]

cols = st.columns(4)
for i, offer in enumerate(offerings):
    with cols[i]:
        with st.container(border=True):
            st.markdown(f"### {offer['icon']}")
            st.markdown(f"**{offer['title']}**")
            st.caption(offer['desc'])

st.subheader("Available insights", anchor=False)

st.html("""
<table class="insight-table">
    <thead>
        <tr>
            <th>Insight Category</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Foot Traffic Trends</strong></td>
            <td>Hourly and daily traffic patterns across locations</td>
        </tr>
        <tr>
            <td><strong>Demographic Analysis</strong></td>
            <td>Nationality, age, and gender breakdowns</td>
        </tr>
        <tr>
            <td><strong>Dwell Time Hotspots</strong></td>
            <td>Areas with highest visitor engagement</td>
        </tr>
        <tr>
            <td><strong>Origin-Destination Flows</strong></td>
            <td>Cross-city movement patterns</td>
        </tr>
    </tbody>
</table>
""")

st.caption("Navigate using the sidebar to explore data, view analytics, visualize maps, or export data packages.")

with st.sidebar:
    st.caption("Data sourced from STC, Mobily, and Zain mobility networks. All data is anonymized and aggregated.")
