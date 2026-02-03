import streamlit as st
import pydeck as pdk
import h3
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Map Visualization | Fusion", page_icon="logo.jpg", layout="wide")

st.logo("logo.jpg")

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
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 10px 40px rgba(30, 58, 95, 0.25); }
        50% { box-shadow: 0 10px 60px rgba(8, 145, 178, 0.35); }
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
    
    .map-container {
        animation: fadeInUp 0.6s ease-out 0.2s backwards;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(30, 58, 95, 0.15);
        border: 1px solid #e2e8f0;
    }
    
    .control-panel {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .legend-container {
        animation: fadeInUp 0.6s ease-out 0.3s backwards;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .legend-title {
        color: #1E3A5F;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.75rem;
    }
    .legend-gradient {
        height: 12px;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }
    .legend-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        color: #64748b;
    }
</style>
""")

st.html("""
<div class="page-header">
    <h1>Map Visualization</h1>
    <p>H3 hexagon visualization of foot traffic density</p>
</div>
""")

CITY_CENTERS = {
    "Riyadh": {"lat": 24.7136, "lon": 46.6753},
    "Jeddah": {"lat": 21.4858, "lon": 39.1925},
    "Mecca": {"lat": 21.3891, "lon": 39.8579},
    "Medina": {"lat": 24.5247, "lon": 39.5692},
    "Dammam": {"lat": 26.4207, "lon": 50.0888},
    "Khobar": {"lat": 26.2172, "lon": 50.1971},
    "Tabuk": {"lat": 28.3838, "lon": 36.5550},
    "Abha": {"lat": 18.2164, "lon": 42.5053},
    "Buraidah": {"lat": 26.3260, "lon": 43.9750},
    "Khamis Mushait": {"lat": 18.3093, "lon": 42.7294},
    "Hofuf": {"lat": 25.3648, "lon": 49.5870},
    "Taif": {"lat": 21.4373, "lon": 40.5127},
    "Najran": {"lat": 17.4933, "lon": 44.1277}
}

@st.cache_data(ttl=600)
def get_hexagon_data(city, hour):
    session = get_active_session()
    
    where_clauses = [f"HOUR = {hour}"]
    if city != "All Cities":
        where_clauses.append(f"SUBSCRIBER_HOME_CITY = '{city}'")
    
    where_sql = " AND ".join(where_clauses)
    
    query = f"""
        SELECT HEXAGON_ID, 
               COUNT(*) as TRAFFIC_COUNT,
               AVG(AVG_STAYING_DURATION_MIN) as AVG_DWELL
        FROM FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA
        WHERE {where_sql}
        GROUP BY HEXAGON_ID
        ORDER BY TRAFFIC_COUNT DESC
        LIMIT 5000
    """
    return session.sql(query).to_pandas()

def h3_to_lat_lon(h3_index):
    try:
        lat, lon = h3.cell_to_latlng(h3_index)
        return lat, lon
    except Exception:
        try:
            lat, lon = h3.h3_to_geo(h3_index)
            return lat, lon
        except Exception:
            return None, None

with st.sidebar:
    st.html("""
    <div style="color: #1E3A5F; font-weight: 600; font-size: 1rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
        <span style="font-size: 1.2rem;">🗺️</span> Map Controls
    </div>
    """)
    
    selected_city = st.selectbox(
        "Focus city",
        options=["All Cities"] + list(CITY_CENTERS.keys()),
        index=1
    )
    
    selected_hour = st.slider(
        "Hour of day",
        min_value=0,
        max_value=23,
        value=12,
        help="Filter data by hour of the day"
    )
    
    time_label = "AM" if selected_hour < 12 else "PM"
    display_hour = selected_hour if selected_hour <= 12 else selected_hour - 12
    if display_hour == 0:
        display_hour = 12
    st.caption(f"Currently showing: **{display_hour}:00 {time_label}**")
    
    st.divider()
    
    color_scale = st.selectbox(
        "Color scale",
        options=["Traffic Density", "Dwell Time"],
        index=0
    )

with st.spinner("Loading hexagon data..."):
    hex_df = get_hexagon_data(selected_city, selected_hour)

if len(hex_df) > 0:
    coords = hex_df['HEXAGON_ID'].apply(h3_to_lat_lon)
    hex_df['lat'] = coords.apply(lambda x: x[0])
    hex_df['lon'] = coords.apply(lambda x: x[1])
    hex_df = hex_df.dropna(subset=['lat', 'lon'])
    
    max_traffic = hex_df['TRAFFIC_COUNT'].max()
    hex_df['normalized'] = hex_df['TRAFFIC_COUNT'] / max_traffic
    
    if color_scale == "Traffic Density":
        hex_df['color_r'] = (hex_df['normalized'] * 8 + (1 - hex_df['normalized']) * 30).astype(int)
        hex_df['color_g'] = (hex_df['normalized'] * 145 + (1 - hex_df['normalized']) * 58).astype(int)
        hex_df['color_b'] = (hex_df['normalized'] * 178 + (1 - hex_df['normalized']) * 95).astype(int)
        hex_df['opacity'] = (hex_df['normalized'] * 200 + 55).astype(int)
        legend_colors = "linear-gradient(90deg, #1E3A5F, #0891B2)"
        legend_label_low = "Low Traffic"
        legend_label_high = "High Traffic"
    else:
        max_dwell = hex_df['AVG_DWELL'].max()
        hex_df['dwell_norm'] = hex_df['AVG_DWELL'] / max_dwell
        hex_df['color_r'] = 212
        hex_df['color_g'] = (hex_df['dwell_norm'] * 175 + (1 - hex_df['dwell_norm']) * 100).astype(int)
        hex_df['color_b'] = (hex_df['dwell_norm'] * 55 + (1 - hex_df['dwell_norm']) * 30).astype(int)
        hex_df['opacity'] = (hex_df['dwell_norm'] * 200 + 55).astype(int)
        legend_colors = "linear-gradient(90deg, #D46420, #D4AF37)"
        legend_label_low = "Short Dwell"
        legend_label_high = "Long Dwell"
    
    if selected_city != "All Cities" and selected_city in CITY_CENTERS:
        center = CITY_CENTERS[selected_city]
        view_lat, view_lon = center["lat"], center["lon"]
        zoom = 11
    else:
        view_lat = hex_df['lat'].mean()
        view_lon = hex_df['lon'].mean()
        zoom = 6
    
    layer = pdk.Layer(
        "H3HexagonLayer",
        hex_df,
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        get_hexagon="HEXAGON_ID",
        get_fill_color=["color_r", "color_g", "color_b", "opacity"],
        get_line_color=[30, 58, 95, 100],
        line_width_min_pixels=1
    )
    
    view_state = pdk.ViewState(
        latitude=view_lat,
        longitude=view_lon,
        zoom=zoom,
        pitch=0
    )
    
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "html": "<b>Traffic:</b> {TRAFFIC_COUNT}<br/><b>Avg Dwell:</b> {AVG_DWELL:.1f} min",
            "style": {"backgroundColor": "#1E3A5F", "color": "white", "borderRadius": "8px", "padding": "8px"}
        }
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Hexagons Displayed", f"{len(hex_df):,}", border=True)
    with col2:
        st.metric("Total Traffic", f"{hex_df['TRAFFIC_COUNT'].sum():,}", border=True)
    with col3:
        st.metric("Avg Dwell Time", f"{hex_df['AVG_DWELL'].mean():.1f} min", border=True)
    
    with st.container(border=True):
        st.pydeck_chart(deck, use_container_width=True, height=550)
    
    st.html(f"""
    <div class="legend-container">
        <div class="legend-title">Color Legend</div>
        <div class="legend-gradient" style="background: {legend_colors};"></div>
        <div class="legend-labels">
            <span>{legend_label_low}</span>
            <span>{legend_label_high}</span>
        </div>
    </div>
    """)
    
    st.caption("H3 Resolution 9 hexagons (~174m edge length). Zoom and pan to explore different areas.")
    
else:
    st.warning("No data available for the selected filters. Try adjusting the city or hour.", icon="⚠️")
