import pandas as pd
import folium
from folium.plugins import HeatMap

# Load data
coords = pd.read_csv("city_coordinates.csv")
preds = pd.read_csv("city_predictions.csv")
df = pd.merge(coords, preds, on="city")

# Create base map
india_map = folium.Map(location=[22.5, 79.0], zoom_start=5)

# -------------------------------
# Marker Layer (City Risk Markers)
# -------------------------------
marker_layer = folium.FeatureGroup(name="City Risk Markers")

def risk_color(risk):
    if risk == "High":
        return "red"
    elif risk == "Medium":
        return "orange"
    else:
        return "green"

for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5 + row["flood_probability"] * 10,
        color=risk_color(row["risk_level"]),
        fill=True,
        fill_color=risk_color(row["risk_level"]),
        fill_opacity=0.7,
        popup=folium.Popup(
            f"""
            <b>{row['city']}</b><br>
            Flood Probability: <b>{row['flood_probability']}</b><br>
            Risk Level: <b>{row['risk_level']}</b>
            """,
            max_width=250
        )
    ).add_to(marker_layer)

marker_layer.add_to(india_map)

# -------------------------------
# Heatmap Layer (Risk Intensity)
# -------------------------------
heatmap_layer = folium.FeatureGroup(name="Flood Risk Heatmap")

heat_data = [
    [row["latitude"], row["longitude"], row["flood_probability"]]
    for _, row in df.iterrows()
]

HeatMap(
    heat_data,
    radius=25,
    blur=15,
    min_opacity=0.3
).add_to(heatmap_layer)

heatmap_layer.add_to(india_map)

# -------------------------------
# Legend
# -------------------------------
legend_html = """
<div style="
position: fixed;
bottom: 50px;
left: 50px;
width: 180px;
background-color: white;
border: 2px solid grey;
z-index: 9999;
font-size: 14px;
padding: 10px;
">
<b>Flood Risk Levels</b><br><br>
<span style="color:red;">●</span> High Risk<br>
<span style="color:orange;">●</span> Medium Risk<br>
<span style="color:green;">●</span> Low Risk
</div>
"""

india_map.get_root().html.add_child(folium.Element(legend_html))

# -------------------------------
# Layer Toggle Control
# -------------------------------
folium.LayerControl(collapsed=False).add_to(india_map)

# Save map
india_map.save("flood_risk_map.html")
print("Toggle-enabled map saved as flood_risk_map.html")