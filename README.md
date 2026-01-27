# Saudi Arabia Telco Mobility Dataset

## Overview

This dataset supports **Fusion**, a platform that aggregates anonymized mobility data from Saudi Arabia's three major telecommunications providers (STC, Mobily, and Zain). The data enables analysis of population movement patterns, urban planning insights, and location-based analytics across the Kingdom.

### Use Cases
- **Urban Planning**: Analyze foot traffic and population density across cities
- **Retail & Commercial**: Identify high-traffic areas for site selection
- **Transportation**: Understand commuter patterns and peak travel times
- **Tourism**: Track visitor flows to destinations like Mecca and Medina
- **Government**: Support smart city initiatives and infrastructure planning

### Data Ingestion Context
Each telco provides daily data exports containing subscriber mobility observations aggregated at the H3 hexagon level. This synthetic dataset mimics that ingestion pipeline for demonstration purposes.

## Files

| File | Telco | Records | Size |
|------|-------|---------|------|
| `saudi_telco_stc_jan2026.csv` | STC | 1,415,000 | 92 MB |
| `saudi_telco_mobily_jan2026.csv` | Mobily | 1,415,000 | 92 MB |
| `saudi_telco_zain_jan2026.csv` | Zain | 1,415,000 | 92 MB |
| **Total** | | **4,245,000** | **276 MB** |

## Date Range

January 1-31, 2026

## Schema

| Field | Type | Description |
|-------|------|-------------|
| `hexagon_id` | STRING | Uber H3 geospatial index (resolution 9, ~174m hexagons) |
| `hour` | INT | Hour of day (0-23) |
| `date` | DATE | Observation date (YYYY-MM-DD) |
| `avg_staying_duration_min` | FLOAT | Average time subscribers spent in hexagon (minutes) |
| `subscription_type` | STRING | Mobile plan type (Prepaid, Postpaid) |
| `nationality` | STRING | Subscriber nationality |
| `gender` | STRING | Subscriber gender (Male, Female) |
| `age_group` | STRING | Age bracket (18-24, 25-34, 35-44, 45-54, 55+) |
| `subscriber_home_city` | STRING | Subscriber's registered home city |

## Data Distributions

### Nationality
| Nationality | Percentage |
|-------------|------------|
| Saudi | 62% |
| Indian | 10% |
| Pakistani | 6% |
| Egyptian | 5% |
| Filipino | 4% |
| Bangladeshi | 3% |
| Yemeni | 2% |
| Sudanese | 2% |
| Syrian | 2% |
| Jordanian | 1% |
| Other | 3% |

### Gender
| Gender | Percentage |
|--------|------------|
| Male | 65% |
| Female | 35% |

### Age Group
| Age Group | Percentage |
|-----------|------------|
| 18-24 | 20% |
| 25-34 | 30% |
| 35-44 | 25% |
| 45-54 | 15% |
| 55+ | 10% |

### Subscription Type
| Type | Percentage |
|------|------------|
| Prepaid | 62% |
| Postpaid | 38% |

### Cities
| City | Percentage |
|------|------------|
| Riyadh | 30% |
| Jeddah | 20% |
| Mecca | 10% |
| Medina | 8% |
| Dammam | 8% |
| Khobar | 5% |
| Tabuk | 4% |
| Abha | 3% |
| Buraidah | 3% |
| Khamis Mushait | 3% |
| Hofuf | 2% |
| Taif | 2% |
| Najran | 2% |

### Average Staying Duration
- Min: 5 minutes
- Max: ~480 minutes
- Mean: ~30 minutes
- Distribution: Exponential (realistic for mobility data)

## H3 Geospatial Index

- Resolution: 9
- Hexagon edge length: ~174 meters
- Coverage: Urban areas of listed Saudi cities
- Coordinates are randomly distributed around city centers with Gaussian offset (std=0.08 degrees)

### Hexagon Verification

All H3 hexagon IDs are real and decode to actual Saudi Arabia coordinates:

| City | Hexagon ID | Decoded Lat | Decoded Lon | Status |
|------|------------|-------------|-------------|--------|
| Jeddah | 8953a955817ffff | 21.4854 | 39.2528 | ✓ Valid |
| Riyadh | 89537369303ffff | 24.7365 | 46.6364 | ✓ Valid |
| Khamis Mushait | 8952021b473ffff | 18.3096 | 42.6805 | ✓ Valid |
| Medina | 8953110e1cfffff | 24.5460 | 39.5549 | ✓ Valid |
| Taif | 89523447477ffff | 21.2768 | 40.4023 | ✓ Valid |

Hexagons can be plotted on a map and will display realistic Saudi locations matching their assigned cities.

## Saudi Telco Market Context

| Provider | Market Share |
|----------|--------------|
| STC (Saudi Telecom Company) | ~48% |
| Mobily (Etihad Etisalat) | ~28% |
| Zain Saudi Arabia | ~24% |

## Usage

```sql
-- Example: Load into Snowflake
CREATE OR REPLACE TABLE TELCO_MOBILITY_DATA (
    hexagon_id VARCHAR,
    hour INTEGER,
    date DATE,
    avg_staying_duration_min FLOAT,
    subscription_type VARCHAR,
    nationality VARCHAR,
    gender VARCHAR,
    age_group VARCHAR,
    subscriber_home_city VARCHAR
);

-- Load from stage
COPY INTO TELCO_MOBILITY_DATA FROM @my_stage/saudi_telco_stc_jan2026.csv
FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1);
```

## Generation Script

Dataset generated using `generate_telco_data.py` with realistic demographic distributions based on Saudi Arabia census and telecom market data.
