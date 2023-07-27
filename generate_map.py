import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Load the data from both the training and classified sets
data_training = pd.read_csv('poi_training.csv')
data_classified = pd.read_csv('poi_classified.csv')

# Combine the data from both sets
data = pd.concat([data_training, data_classified], ignore_index=True)

# Center the map on the United States (where all POIs are located)
map_center = [39.8283, -98.5795]

# Create the map
mymap = folium.Map(location=map_center, zoom_start=5)

# Color each point of interest differently
type_colors = {
    'National Battlefield': 'gray',
    'National Battlefield Site': 'lightblue',
    'National Heritage Site': 'purple',
    'National Historic Park': 'pink',
    'National Historic Reserve': 'lightred',
    'National Historic Trail': 'green',
    'National Lakeshore': 'orange',
    'National Memorial': 'beige',
    'National Military Park': 'cadetblue',
    'National Monument': 'black',
    'National Park': 'blue',
    'National Preserve': 'darkgreen',
    'National Recreation Area': 'red',
    'National Recreational River': 'white',
    'National River': 'darkred',
    'National Scenic River': 'darkblue',
    'National Scenic Trail': 'darkpurple',
    'National Seashore': 'lightgreen',
    'Other': 'lightgray',
    'Park': 'gray',
    'Parkway': 'lightblue'
}

# Create a MarkerCluster group for efficient rendering of multiple markers
marker_cluster = MarkerCluster().add_to(mymap)

# Loop through the data and add markers
for idx, row in data.iterrows():
    name = row['name']
    latitude = row['latitude']
    longitude = row['longitude']
    poi_type = row['type']

    # Get the color for the type
    color = type_colors.get(poi_type, 'gray')

    # Add the marker to the MarkerCluster group
    folium.Marker(
        location=[latitude, longitude],
        popup=name,
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(marker_cluster)

# Save the map to an HTML file
mymap.save('poi_map.html')
