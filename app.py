import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.express as px
import pydeck as pdk
from sklearn.cluster import DBSCAN
from sklearn.ensemble import RandomForestClassifier

# 1. Page config
st.set_page_config(page_title="Bear‑Risk Dashboard", layout="wide")

# 2. Load & cache data
@st.cache_data
def load_all_data():
    # point at our repo’s data/ folder
    D = Path(__file__).parent / "data"

    road    = pd.read_csv(D / "Road_Mortality.csv",    parse_dates=["ReportDate"])
    nonroad = pd.read_csv(D / "Non_Road_Mortality.csv", parse_dates=["ReportDate"])
    capture = pd.read_csv(D / "Capture.csv",          parse_dates=["ReportDate"])
    release = pd.read_csv(D / "Release.csv",          parse_dates=["ReportDate"])
    manage  = pd.read_csv(D / "Management.csv")  # no dates here

    # combine and compute derived columns
    mort = pd.concat([
        road.assign(Source="Road"),
        nonroad.assign(Source="Off-Road")
    ], ignore_index=True)
    mort["Year"]   = mort.ReportDate.dt.year
    mort["Month"]  = mort.ReportDate.dt.month
    mort["Season"] = mort.Month.map({
        12: "Winter", 1: "Winter", 2: "Winter",
         3: "Spring", 4: "Spring", 5: "Spring",
         6: "Summer", 7: "Summer", 8: "Summer",
         9: "Fall",  10: "Fall",  11: "Fall"
    })

    capture["Year"] = capture.ReportDate.dt.year
    release["Year"] = release.ReportDate.dt.year

    return mort, capture, release, manage

# now call it
mort, capture, release, manage = load_all_data()

# 3. Sidebar filters
st.sidebar.header("Filters")
min_y, max_y = 1979, int(mort.Year.max())
start_year = st.sidebar.number_input("Start Year", min_y, max_y, min_y)
end_year   = st.sidebar.number_input("End Year",   min_y, max_y, max_y)
if start_year > end_year:
    st.sidebar.error("Start Year ≤ End Year")
st.sidebar.multiselect("Season", ["Winter","Spring","Summer","Fall"], default=["Winter","Spring","Summer","Fall"])
sources = st.sidebar.multiselect("Mortality source", ["Road","Off-Road"], default=["Road","Off-Road"])
regions = mort.Region.dropna().unique().tolist()
chosen_regions = st.sidebar.multiselect("Region", regions, default=regions)
sexes = mort.Sex.dropna().unique().tolist()
chosen_sexes = st.sidebar.multiselect("Sex", sexes, default=sexes)
ages = mort.AgeClass.dropna().unique().tolist()
chosen_ages = st.sidebar.multiselect("Age Class", ages, default=ages)
wmin, wmax = int(mort.Weight.min()), int(mort.Weight.max())
low_w  = st.sidebar.number_input("Min Weight (kg)", wmin, wmax, wmin)
high_w = st.sidebar.number_input("Max Weight (kg)", wmin, wmax, wmax)
if low_w > high_w:
    st.sidebar.error("Min Weight ≤ Max Weight")
mask = (
    mort.Year.between(start_year, end_year) &
    mort.Source.isin(sources) &
    mort.Region.isin(chosen_regions) &
    mort.Sex.isin(chosen_sexes) &
    mort.AgeClass.isin(chosen_ages) &
    mort.Weight.between(low_w, high_w)
)
filtered = mort[mask]

# 4. Key metrics
st.markdown("## 📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Mortalities", len(filtered))
col2.metric("Road Mortalities", len(filtered[filtered.Source=="Road"]))
col3.metric("Off‑Road Mortalities", len(filtered[filtered.Source=="Off-Road"]))

# 5. All mortalities map w/ clustering & popups
st.markdown("### All Mortalities Map")
m_all = folium.Map(
    location=[filtered.Latitude.mean(), filtered.Longitude.mean()],
    zoom_start=6,
    control_scale=True,
    zoom_control=True,
    prefer_canvas=True
)

# create a cluster group
from folium.plugins import MarkerCluster
cluster = MarkerCluster(name="Bear events").add_to(m_all)

# define your two‐color palette
palette = {"Road":"#0072B2","Off-Road":"#D55E00"}

# add each point to the cluster, with a popup
for _, r in filtered.iterrows():
    popup = (
        f"<b>BearID:</b> {r.BearID}<br>"
        f"<b>Date:</b> {r.ReportDate.date()}<br>"
        f"<b>Source:</b> {r.Source}"
    )
    folium.CircleMarker(
        [r.Latitude, r.Longitude],
        radius=4,
        color=palette[r.Source],
        fill=True,
        fill_opacity=0.7,
        popup=popup
    ).add_to(cluster)

# add a little legend
legend_html = """
 <div style="
   position: fixed; bottom: 50px; left: 50px;
   background: white; padding: 5px; border:2px solid grey;
   z-index:9999;
 ">
   <i style="background:#0072B2;width:10px;height:10px;display:inline-block;"></i>
      Road
   <i style="background:#D55E00;width:10px;height:10px;display:inline-block;"></i>
      Off‑Road
 </div>
"""
m_all.get_root().html.add_child(folium.Element(legend_html))

# render it
st_folium(m_all, width="100%", height=350)

# 6. Regional Density (Hexagon Layer)
st.markdown("### Regional Density (Hexagon Layer)")

# Build the layer off of the already‑filtered data
hex_layer = pdk.Layer(
    "HexagonLayer",
    data=filtered[["Latitude", "Longitude"]],
    get_position=["Longitude", "Latitude"],
    radius=7000,
    opacity=0.5,
    elevation_scale=30,
    extruded=True,
    # light‑safe yellow→orange fill
    get_fill_color=[255, 200, 50, 150],
)

view_state = pdk.ViewState(
    latitude=filtered.Latitude.mean(),
    longitude=filtered.Longitude.mean(),
    zoom=6,
    pitch=40,
)

st.pydeck_chart(
    pdk.Deck(
        layers=[hex_layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v10",
        tooltip={"text": "Count: {elevationValue}"},
    )
)

st.markdown(
    "**Hexagon density legend**  \n"
    "- 🟡 Low density  \n"
    "- 🟠 Medium density  \n"
    "- 🔴 High density"
)

# 7. Monthly Trends by Season & Source
st.markdown("### Monthly Trends by Season & Source")
df_ts = filtered.groupby([pd.Grouper(key="ReportDate", freq="M"), "Season", "Source"]).size().reset_index(name="Count")
fig = px.line(df_ts, x="ReportDate", y="Count", color="Source", facet_col="Season", facet_col_wrap=2)
fig.update_layout(
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="white", font_color="white"),
    height=400
)
st.plotly_chart(fig, use_container_width=True)

# 8. Remove survival and skip

# 9. Top Clusters Summary
st.markdown("### Top Clusters Summary")
coords = filtered[["Latitude","Longitude"]].to_numpy()
filtered["Cluster"] = DBSCAN(eps=0.02, min_samples=5).fit_predict(coords)
summary = (filtered[filtered.Cluster>=0].groupby("Cluster").size().rename("Count")).nlargest(3).to_frame()
summary["CentroidLat"] = summary.index.map(lambda c: filtered[filtered.Cluster==c].Latitude.mean())
summary["CentroidLon"] = summary.index.map(lambda c: filtered[filtered.Cluster==c].Longitude.mean())
st.table(summary)

top_n = 3
cluster_sizes = (
    filtered[filtered.Cluster >= 0]
    .groupby("Cluster")
    .size()
    .nlargest(top_n)
)
cluster_info = (
    filtered[filtered.Cluster.isin(cluster_sizes.index)]
    .groupby("Cluster")
    .agg(Count=("Cluster","size"),
         Lat      =("Latitude","mean"),
         Lon      =("Longitude","mean"))
    .loc[cluster_sizes.index]
)

# let user pick one
chosen_cluster = st.selectbox(
    "🔍 Zoom to cluster", 
    options=[f"#{c}" for c in cluster_info.index],
    format_func=lambda s: f"{s} ({cluster_info.loc[int(s[1:]),'Count']} events)"
)

if chosen_cluster:
    c = int(chosen_cluster[1:])
    centroid = cluster_info.loc[c, ["Lat","Lon"]].to_list()
    m_all = folium.Map(location=centroid, zoom_start=10)
    # draw all points in grey
    for _, r in filtered.iterrows():
        folium.CircleMarker(
            [r.Latitude, r.Longitude],
            radius=2,
            color="#888",
            fill=True,
            fill_opacity=0.3
        ).add_to(m_all)
    # overlay cluster c in its color
    for _, r in filtered[filtered.Cluster==c].iterrows():
        folium.CircleMarker(
            [r.Latitude, r.Longitude],
            radius=4,
            color=palette[r.Source],
            fill=True
        ).add_to(m_all)

    # re‑attach legend HTML as before…
    m_all.get_root().html.add_child(folium.Element(legend_html))
    st_folium(m_all, width="100%", height=300)

# 10. Download filtered data
st.markdown("### Download Filtered Data")
st.download_button("📥 Download filtered dataset as CSV", data=filtered.to_csv(index=False), file_name="filtered.csv", mime="text/csv")

# 11. Persistence tables
tab2, tab3, tab4 = st.tabs(["Capture log","Release log","Management"])
with tab2:
    with st.expander("👁️ View raw capture records"):
        st.dataframe(capture)
        st.download_button("📥 Download capture CSV", capture.to_csv(index=False), "capture.csv")
with tab3:
    with st.expander("👁️ View raw release records"):
        st.dataframe(release)
        st.download_button("📥 Download release CSV", release.to_csv(index=False), "release.csv")
with tab4:
    with st.expander("👁️ View raw management records"):
        st.dataframe(manage)
        st.download_button("📥 Download management CSV", manage.to_csv(index=False), "management.csv")

# 12. Mortality Heatmap
st.markdown("### Mortality Heatmap")
hmap = folium.Map(location=[filtered.Latitude.mean(), filtered.Longitude.mean()], zoom_start=6)
HeatMap(filtered[["Latitude","Longitude"]].values.tolist(), radius=15).add_to(hmap)
st_folium(hmap, width="100%", height=300)

