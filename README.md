# 🐻 Bear‑Risk Dashboard

An **interactive Streamlit** dashboard for exploring Black Bear mortality and capture/release data in Florida.  
Filter by time, season, source, region, sex, age class, and weight, then visualize trends, hotspots, and survival curves.

---

## 📺 Live Demo

[➡️ View the live dashboard](https://bear-dashboard-m3enxgrtonf3xobvkpnknp.streamlit.app/)

---

## 🚀 Features

- **Sidebar Filters**  
  - **Start / End Year** (1979–2023)  
  - **Season** (Winter, Spring, Summer, Fall)  
  - **Mortality Source** (Road, Off‑Road)  
  - **Region**, **Sex**, **Age Class**, **Weight Range**  
- **Key Metrics**  
  - Total mortalities, road vs. off‑road breakdown  
- **All Mortalities Map**  
  - Marker clustering with popup details (date, region, cause, weight, etc.)  
- **Regional Density**  
  - Hexagon binning (default) or heatmap view toggle  
- **Monthly Trends**  
  - Time‑series line charts by season & source  
- **Capture → Release Survival Curves**  
  - Kaplan‑Meier analysis (requires `lifelines`)  
- **Top Clusters Summary**  
  - DBSCAN cluster counts & centroids  
- **Downloadable Data**  
  - Export filtered mortalities as CSV  
  - Raw capture, release, and management logs with download buttons  

---
## 📝 How To Use
Adjust Sidebar Filters

Choose the year range, seasons, mortality sources, and demographic attributes.

Explore the Maps

All Mortalities Map: Zoom, pan, and click clusters/markers to inspect individual events.

Regional Density: Switch between hexagon bins or heatmap to reveal hotspots.

Inspect Trends

Monthly Trends: View counts over time, faceted by season and colored by source.

Survival Analysis

If lifelines is installed, see capture→release curves under “Capture→Release Survival Curves.”

Cluster Summary

Check which geographic clusters have the highest counts and view their centroids.

Download Data

Click Download filtered dataset as CSV to export your current selection.

Expand “Capture log,” “Release log,” or “Management” tabs to view/download raw tables.

## 🔧 Installation & Setup

```bash
# 1. Clone the repo
git clone https://github.com/ehorne31/bear-dashboard.git
cd bear-dashboard

# 2. Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Place your data
# Create a `data/` folder in the repo root and copy the six CSVs there:
# bear-dashboard/
# ├── data/
# │   ├── Road_Mortality.csv
# │   ├── Non_Road_Mortality.csv
# │   ├── Capture.csv
# │   ├── Release.csv
# │   ├── Management.csv
# │   └── Calls.csv
# ├── app.py
# └── requirements.txt

# 5. Run the dashboard locally
streamlit run app.py

## 📁 Project Structure
bear-dashboard/
...
├── app.py             # Streamlit application script
├── requirements.txt   # Python package list
├── data/              
│   ├── Road_Mortality.csv
│   ├── Non_Road_Mortality.csv
│   ├── Capture.csv
│   ├── Release.csv
│   ├── Management.csv
│   └── Calls.csv
└── README.md

## 📦 Dependencies
Streamlit — web app framework

pandas — data manipulation

pydeck — hexagon & cluster maps

folium — leaflet maps & heatmaps

plotly.express — line charts

scikit-learn — DBSCAN clustering

lifelines — optional survival analysis

Install via:

pip install -r requirements.txt
     
