# Plan: Restore AI Predictions Graphs

## Problem
The AI Predictions tab was consolidated into a simplified dropdown + text format, removing all the Plotly visualizations that existed before.

## Original Content (from backup)
The backup at [2_Analytics_Dashboard.py](streamlit_app_backup_20260203_135847/pages/2_Analytics_Dashboard.py) contains 6 rich industry sections with charts:

| Industry | Chart Type | Description |
|----------|------------|-------------|
| Tourism & Hospitality | Bar Chart | Visitor nationality vs average dwell time |
| Transport & Logistics | Sankey Diagram | Commuter flow between origins/destinations |
| Financial Services | Dual Gauge | Fraud detection accuracy + Risk scoring |
| Advertising & Media | Treemap | Customer segments by size and value |
| Forecasting | Line Chart | 30-day mobility forecast with confidence bands |
| Vision 2030 | Cards | NEOM, Qiddiya, Red Sea Project alignment |

## Solution
Replace the current simplified AI tab (lines 337-478) with the original rich content from the backup file.

## Files to Modify
- [streamlit_app/pages/2_Analytics_Dashboard.py](streamlit_app/pages/2_Analytics_Dashboard.py) - Replace tab_ai content

## Implementation Steps

1. **Extract original AI tab content** from backup (approximately lines 1200-1800)
2. **Replace current tab_ai section** (lines 337-478) with original content
3. **Deploy to Snowflake** via PUT command
