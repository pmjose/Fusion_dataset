import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import h3
import os

np.random.seed(42)

ROWS_PER_TELCO = 1_415_000  # ~99MB per file

TELCOS = ['STC', 'Mobily', 'Zain']

NATIONALITIES = {
    'Saudi': 0.62,
    'Indian': 0.10,
    'Pakistani': 0.06,
    'Egyptian': 0.05,
    'Filipino': 0.04,
    'Bangladeshi': 0.03,
    'Yemeni': 0.02,
    'Sudanese': 0.02,
    'Syrian': 0.02,
    'Jordanian': 0.01,
    'Other': 0.03
}

GENDER = {'Male': 0.65, 'Female': 0.35}

AGE_GROUPS = {
    '18-24': 0.20,
    '25-34': 0.30,
    '35-44': 0.25,
    '45-54': 0.15,
    '55+': 0.10
}

SUBSCRIPTION = {'Prepaid': 0.62, 'Postpaid': 0.38}

CITIES = {
    'Riyadh': {'lat': 24.7136, 'lon': 46.6753, 'weight': 0.30},
    'Jeddah': {'lat': 21.4858, 'lon': 39.1925, 'weight': 0.20},
    'Mecca': {'lat': 21.3891, 'lon': 39.8579, 'weight': 0.10},
    'Medina': {'lat': 24.5247, 'lon': 39.5692, 'weight': 0.08},
    'Dammam': {'lat': 26.4207, 'lon': 50.0888, 'weight': 0.08},
    'Khobar': {'lat': 26.2172, 'lon': 50.1971, 'weight': 0.05},
    'Tabuk': {'lat': 28.3838, 'lon': 36.5550, 'weight': 0.04},
    'Abha': {'lat': 18.2164, 'lon': 42.5053, 'weight': 0.03},
    'Buraidah': {'lat': 26.3260, 'lon': 43.9750, 'weight': 0.03},
    'Khamis Mushait': {'lat': 18.3000, 'lon': 42.7333, 'weight': 0.03},
    'Hofuf': {'lat': 25.3648, 'lon': 49.5855, 'weight': 0.02},
    'Taif': {'lat': 21.2703, 'lon': 40.4158, 'weight': 0.02},
    'Najran': {'lat': 17.4917, 'lon': 44.1322, 'weight': 0.02}
}

def weighted_choice(choices_dict, n):
    items = list(choices_dict.keys())
    weights = list(choices_dict.values())
    return np.random.choice(items, size=n, p=weights)

def generate_telco_file(telco_name, num_records):
    print(f"\nGenerating {telco_name} data ({num_records:,} records)...")
    
    nationality = weighted_choice(NATIONALITIES, num_records)
    gender = weighted_choice(GENDER, num_records)
    age_group = weighted_choice(AGE_GROUPS, num_records)
    subscription_type = weighted_choice(SUBSCRIPTION, num_records)
    home_city = weighted_choice({k: v['weight'] for k, v in CITIES.items()}, num_records)
    
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 1, 31)
    date_range = (end_date - start_date).days + 1
    dates = [start_date + timedelta(days=np.random.randint(0, date_range)) for _ in range(num_records)]
    
    hour_probs = [
        0.01, 0.01, 0.01, 0.01, 0.02, 0.03,
        0.04, 0.06, 0.07, 0.07, 0.07, 0.07,
        0.06, 0.06, 0.06, 0.06, 0.06, 0.06,
        0.05, 0.05, 0.04, 0.03, 0.02, 0.02
    ]
    hour_probs = [p / sum(hour_probs) for p in hour_probs]
    hours = np.random.choice(range(24), size=num_records, p=hour_probs)
    
    avg_duration = np.clip(np.random.exponential(scale=30, size=num_records), 5, 480).round(1)
    
    print(f"  Generating H3 hexagon IDs...")
    h3_ids = []
    for city in home_city:
        city_info = CITIES[city]
        lat, lon = city_info['lat'], city_info['lon']
        lat_offset = np.random.normal(0, 0.08)
        lon_offset = np.random.normal(0, 0.08)
        h3_id = h3.latlng_to_cell(lat + lat_offset, lon + lon_offset, 9)
        h3_ids.append(h3_id)
    
    df = pd.DataFrame({
        'hexagon_id': h3_ids,
        'hour': hours,
        'date': dates,
        'avg_staying_duration_min': avg_duration,
        'subscription_type': subscription_type,
        'nationality': nationality,
        'gender': gender,
        'age_group': age_group,
        'subscriber_home_city': home_city
    })
    
    df['date'] = pd.to_datetime(df['date']).dt.date
    df = df.sort_values(['date', 'hour']).reset_index(drop=True)
    
    filename = f'saudi_telco_{telco_name.lower()}_jan2026.csv'
    df.to_csv(filename, index=False)
    
    size_mb = os.path.getsize(filename) / (1024 * 1024)
    print(f"  Saved: {filename} ({size_mb:.1f} MB)")
    
    return filename, len(df), size_mb

# Remove old files
for f in ['saudi_telco_mobility_data.csv', 'saudi_telco_mobility_data_part1.csv', 'saudi_telco_mobility_data_part2.csv']:
    if os.path.exists(f):
        os.remove(f)
        print(f"Removed old file: {f}")

print("="*50)
print("GENERATING SAUDI TELCO DATASETS - JANUARY 2026")
print("="*50)

results = []
for telco in TELCOS:
    filename, rows, size = generate_telco_file(telco, ROWS_PER_TELCO)
    results.append((telco, filename, rows, size))

print("\n" + "="*50)
print("SUMMARY")
print("="*50)
for telco, filename, rows, size in results:
    print(f"{telco:8} | {filename:40} | {rows:,} rows | {size:.1f} MB")
print("="*50)
total_rows = sum(r[2] for r in results)
total_size = sum(r[3] for r in results)
print(f"{'TOTAL':8} | {'':40} | {total_rows:,} rows | {total_size:.1f} MB")
