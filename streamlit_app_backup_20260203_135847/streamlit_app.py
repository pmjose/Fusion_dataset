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
       SIDEBAR STYLING
       ========================================= */
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #0f172a 100%) !important;
        border-right: 1px solid rgba(8, 145, 178, 0.2) !important;
    }
    
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .st-emotion-cache-1rtdyuf,
    [data-testid="stSidebarNavItems"] span,
    [data-testid="stSidebarNav"] span,
    section[data-testid="stSidebar"] span {
        color: #ffffff !important;
        opacity: 1 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stLogo"] img {
        border-radius: 12px !important;
        padding: 8px !important;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] a {
        color: #ffffff !important;
        font-weight: 500 !important;
        padding: 0.75rem 1rem !important;
        border-radius: 10px !important;
        margin: 0.25rem 0.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] a:hover {
        background: linear-gradient(135deg, rgba(8, 145, 178, 0.2) 0%, rgba(30, 58, 95, 0.3) 100%) !important;
        color: #ffffff !important;
        transform: translateX(4px);
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

st.subheader("Data Product Catalog", anchor=False)
st.caption("Aligned with TM Forum GB1086 Data Product Lifecycle Management (DPLM) v1.0")

offerings = [
    {
        "icon": ":material/store:",
        "title": "Retail Mobility Insights",
        "desc": "Site selection, foot traffic, competitor benchmarking",
        "type": "Consumer-Aligned",
        "status": "Published"
    },
    {
        "icon": ":material/account_balance:",
        "title": "Urban Planning Analytics", 
        "desc": "Infrastructure planning, smart city, population density",
        "type": "Consumer-Aligned",
        "status": "Published"
    },
    {
        "icon": ":material/flight:",
        "title": "Tourism Flow Data",
        "desc": "Visitor flows, destination analytics, seasonal patterns",
        "type": "Source-Aligned",
        "status": "Published"
    },
    {
        "icon": ":material/directions_bus:",
        "title": "Transport Patterns",
        "desc": "Commuter patterns, route optimization, peak hours",
        "type": "Knowledge-Aligned",
        "status": "Draft"
    }
]

cols = st.columns(4)
for i, offer in enumerate(offerings):
    with cols[i]:
        with st.container(border=True):
            st.markdown(f"### {offer['icon']}")
            st.markdown(f"**{offer['title']}**")
            st.caption(offer['desc'])
            status_color = "#22c55e" if offer['status'] == "Published" else "#f59e0b"
            st.html(f'<span style="background:{status_color};color:white;padding:2px 8px;border-radius:10px;font-size:0.7rem;">{offer["status"]}</span> <span style="background:#64748b;color:white;padding:2px 8px;border-radius:10px;font-size:0.7rem;">{offer["type"]}</span>')

st.subheader("Data Product Specification", anchor=False)
st.caption("Following DATSIS principles: Discoverable, Addressable, Trustworthy, Self-describing, Interoperable, Secure")

st.html("""
<table class="insight-table">
    <thead>
        <tr>
            <th>Attribute</th>
            <th>Details</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Domain Owner</strong></td>
            <td>Telco Mobility Analytics Team</td>
        </tr>
        <tr>
            <td><strong>Data Contract</strong></td>
            <td>SLA: 99.5% uptime | Freshness: Hourly refresh | Quality: >98% completeness</td>
        </tr>
        <tr>
            <td><strong>Access Patterns</strong></td>
            <td>SQL (Snowflake), REST API, Streamlit Dashboard</td>
        </tr>
        <tr>
            <td><strong>Lineage</strong></td>
            <td>STC + Mobily + Zain raw feeds → Anonymization → Aggregation → H3 Hexagons</td>
        </tr>
        <tr>
            <td><strong>Version</strong></td>
            <td>v1.0.0 (Jan 2026) | Lifecycle: Published</td>
        </tr>
    </tbody>
</table>
""")

with st.expander("Data Product Types (TM Forum DPLM)"):
    st.markdown("""
    | Type | Description |
    |------|-------------|
    | **Source-Aligned** | Raw data with minimal transformation, preserves fidelity to source systems |
    | **Consumer-Aligned** | Optimized for specific use cases, aggregated and enriched for direct consumption |
    | **Knowledge-Aligned** | Semantic models and knowledge graphs for AI/ML reasoning |
    | **Standard-Aligned** | Conforms to TM Forum SID/ODA standards for cross-operator interoperability |
    """)

st.caption("Navigate using the sidebar to explore data, view analytics, visualize maps, or export data packages.")

with st.sidebar:
    st.caption("Data sourced from STC, Mobily, and Zain mobility networks. All data is anonymized and aggregated.")
