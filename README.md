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
  - Total mortalities
  - Road vs. off‑road breakdown  
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
1. Adjust Sidebar Filters
Select year range, seasons, mortality sources, and demographic filters.

2. Explore the Maps
All Mortalities Map: Zoom, pan, and click clusters or markers to inspect individual events.

Regional Density: Switch between hexagon bins or heatmap to reveal hotspots.

3. Inspect Trends
Visualize counts over time, faceted by season and colored by source.

4. Survival Analysis
If lifelines is installed, view capture→release curves under the "Survival Curves" section.

5. Cluster Summary
Explore the most active DBSCAN clusters and their centroids.

6. Download Data
Click Download filtered dataset as CSV to export your current selection.
Use the tabs to access raw logs (Capture, Release, Management).

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
```bash

## 📁 Project Structure
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
Install everything with:
pip install -r requirements.txt

Used packages:
Streamlit – web app framework

pandas – data manipulation

pydeck – geospatial hex & cluster maps

folium – Leaflet maps & heatmaps

plotly.express – interactive charts

scikit-learn – DBSCAN clustering

lifelines – optional survival analysis
     
