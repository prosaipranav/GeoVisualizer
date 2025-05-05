import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import random
from folium.plugins import MarkerCluster

st.set_page_config(page_title="GeoVisualizer", page_icon="🌍", layout="wide")
st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem;
            padding-bottom: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
    </style>
""", unsafe_allow_html=True)

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("""
    <style>
    .center-title {
        font-size: 100px;
        font-weight: bold;
        text-align: center;
        color: #31333F;
    }
    </style>
    <h1 class="center-title">🌍 GeoVisualizer 🌍</h1>
""", unsafe_allow_html=True)

def generate_random_data(num_points, lat_min, lat_max, lon_min, lon_max):
    latitudes = [random.uniform(lat_min, lat_max) for _ in range(num_points)]
    longitudes = [random.uniform(lon_min, lon_max) for _ in range(num_points)]
    return pd.DataFrame({'latitude': latitudes, 'longitude': longitudes})

def create_styled_map(data, zoom_start=10):
    center_lat = data['latitude'].mean()
    center_lon = data['longitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start, tiles="OpenStreetMap")
    colors = ['#e6194b', '#3cb44b', '#ffe119', '#0082c8', '#f58231', '#911eb4',
              '#46f0f0', '#f032e6', '#d2f53c', '#fabebe', '#008080', '#e6beff',
              '#aa6e28', '#fffad4', '#800000', '#aaffc3', '#808000', '#ffb300',
              '#803e75', '#ff8e00']
    cluster = MarkerCluster().add_to(m)
    for index, row in data.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        color = colors[index % len(colors)]
        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            fill_color=color,
            color=color,
            fill_opacity=0.7,
            popup=f"<b>Latitude:</b> {lat:.4f}<br><b>Longitude:</b> {lon:.4f}",
            tooltip="Click for details",
        ).add_to(cluster)
    return m

def main():
    st.title("Geospatial Data Visualization App")

    st.sidebar.header("Data Options")
    num_points = st.sidebar.slider("Number of Data Points:", 10, 500, 100)
    lat_min = st.sidebar.slider("Minimum Latitude:", -90.0, 90.0, 10.0)
    lat_max = st.sidebar.slider("Maximum Latitude:", -90.0, 90.0, 20.0)
    lon_min = st.sidebar.slider("Minimum Longitude:", -180.0, 180.0, 70.0)
    lon_max = st.sidebar.slider("Maximum Longitude:", -180.0, 180.0, 80.0)
    zoom_level = st.sidebar.slider("Initial Zoom Level:", 1, 20, 4)

    st.sidebar.markdown(f"**Lat Range:** {lat_min} to {lat_max}")
    st.sidebar.markdown(f"**Lon Range:** {lon_min} to {lon_max}")

    if lat_max <= lat_min or lon_max <= lon_min:
        st.error("Make sure that maximum values are greater than minimum values.")
        return

    if "data" not in st.session_state or st.sidebar.button("Generate New Data"):
        st.session_state.data = generate_random_data(num_points, lat_min, lat_max, lon_min, lon_max)

    data = st.session_state.data

    st.subheader("Data Sample")
    st.dataframe(data.head())

    st.download_button("Download Data as CSV", data.to_csv(index=False), "geodata.csv", "text/csv")

    st.markdown("""
        This app generates and visualizes random geospatial data on an interactive map.  
        Use the sidebar to control the number of data points and the range of latitudes and longitudes.  
        Hover over the markers for coordinate details, and click to see more information.
    """)
    st.subheader("Geospatial Map")
    m = create_styled_map(data, zoom_start=zoom_level)
    st_folium(m, width=800, height=600)

if __name__ == "__main__":
    main()
