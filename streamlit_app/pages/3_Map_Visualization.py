import streamlit as st
import pydeck as pdk
import h3
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Map Visualization | Fusion", page_icon="logo.jpg", layout="wide")

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
    
    map_style = st.selectbox(
        "Map style",
        options=["Dark", "Light", "Satellite"],
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
    
    map_styles = {
        "Dark": "mapbox://styles/mapbox/dark-v10",
        "Light": "mapbox://styles/mapbox/light-v10",
        "Satellite": "mapbox://styles/mapbox/satellite-streets-v11"
    }
    
    layer = pdk.Layer(
        "H3HexagonLayer",
        hex_df,
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        get_hexagon="HEXAGON_ID",
        get_fill_color=["color_r", "color_g", "color_b", "opacity"],
        get_line_color=[255, 255, 255, 50],
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
        map_style=map_styles[map_style],
        tooltip={
            "html": """
                <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; padding: 8px;">
                    <div style="font-weight: 600; margin-bottom: 4px;">📍 Hexagon Details</div>
                    <div><b>Traffic:</b> {TRAFFIC_COUNT}</div>
                    <div><b>Avg Dwell:</b> {AVG_DWELL:.1f} min</div>
                </div>
            """,
            "style": {
                "backgroundColor": "#1E3A5F",
                "color": "white",
                "borderRadius": "12px",
                "padding": "0",
                "boxShadow": "0 4px 20px rgba(0,0,0,0.3)"
            }
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
