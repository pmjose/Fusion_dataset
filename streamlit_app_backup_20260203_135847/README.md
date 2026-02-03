# Fusion - Saudi Mobility Intelligence Platform

A Streamlit in Snowflake app for monetizing Saudi telco mobility data.

## Features

- **Data Explorer**: Browse and filter 4.2M+ mobility records
- **Analytics Dashboard**: Sellable insights (traffic trends, demographics, dwell time)
- **Map Visualization**: PyDeck H3 hexagon visualization of foot traffic
- **Data Export**: Self-service data package downloads

## Data Source

- **Table**: `FUSION_TELCO.MOBILITY_DATA.TELCO_MOBILITY_DATA`
- **Records**: 4,245,000
- **Sources**: STC, Mobily, Zain (Saudi telcos)
- **Period**: January 2026

## Deployment to Snowflake

### 1. Create Stage

```sql
CREATE STAGE IF NOT EXISTS FUSION_TELCO.MOBILITY_DATA.STREAMLIT_STAGE
  DIRECTORY = (ENABLE = TRUE);
```

### 2. Upload Files

```sql
PUT file:///path/to/streamlit_app/streamlit_app.py @FUSION_TELCO.MOBILITY_DATA.STREAMLIT_STAGE OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file:///path/to/streamlit_app/environment.yml @FUSION_TELCO.MOBILITY_DATA.STREAMLIT_STAGE OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file:///path/to/streamlit_app/pages/1_Data_Explorer.py @FUSION_TELCO.MOBILITY_DATA.STREAMLIT_STAGE/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file:///path/to/streamlit_app/pages/2_Analytics_Dashboard.py @FUSION_TELCO.MOBILITY_DATA.STREAMLIT_STAGE/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file:///path/to/streamlit_app/pages/3_Map_Visualization.py @FUSION_TELCO.MOBILITY_DATA.STREAMLIT_STAGE/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file:///path/to/streamlit_app/pages/4_Data_Export.py @FUSION_TELCO.MOBILITY_DATA.STREAMLIT_STAGE/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
```

### 3. Create Streamlit App

```sql
CREATE OR REPLACE STREAMLIT FUSION_TELCO.MOBILITY_DATA.FUSION_APP
  ROOT_LOCATION = '@FUSION_TELCO.MOBILITY_DATA.STREAMLIT_STAGE'
  MAIN_FILE = 'streamlit_app.py'
  QUERY_WAREHOUSE = 'COMPUTE_WH';
```

### 4. Grant Access

```sql
GRANT USAGE ON STREAMLIT FUSION_TELCO.MOBILITY_DATA.FUSION_APP TO ROLE <role_name>;
```

## File Structure

```
streamlit_app/
├── streamlit_app.py          # Main entry point
├── pages/
│   ├── 1_Data_Explorer.py    # Data browsing and filtering
│   ├── 2_Analytics_Dashboard.py  # Charts and insights
│   ├── 3_Map_Visualization.py    # H3 hexagon maps
│   └── 4_Data_Export.py      # Data export/purchase
├── environment.yml           # Snowflake dependencies
└── README.md
```

## Target Users

- Retail & Commercial: Site selection, foot traffic analysis
- Government & Urban Planning: Infrastructure, smart city initiatives
- Tourism & Hospitality: Visitor flows, destination analytics
- Transportation: Commuter patterns, route optimization
