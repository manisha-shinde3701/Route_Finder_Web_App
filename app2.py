from flask import Flask, render_template, request, jsonify
from geopy.geocoders import Nominatim
import osmnx as ox
import networkx as nx
import folium

app = Flask(__name__)
geolocator = Nominatim(user_agent="route_finder_app")

@app.route('/')
def index():
    return render_template('index2.html')  # Render the frontend

@app.route('/get-route', methods=['POST'])
def get_route():
    try:
        data = request.json
        source = data.get("source")
        destination = data.get("destination")
        mode = data.get("mode")  # Mode can be 'walk', 'bike', 'drive', 'bus'

        if not source or not destination or not mode:
            return jsonify({"error": "Source, destination, and mode are required."}), 400

        # Geocode source and destination
        source_location = geolocator.geocode(source)
        destination_location = geolocator.geocode(destination)

        if not source_location or not destination_location:
            return jsonify({"error": "Could not locate one or both locations."}), 400

        # Determine OSM network type
        network_type = "drive" if mode == "bus" else mode

        # Set a dynamic bounding box
        north = max(source_location.latitude, destination_location.latitude) + 0.1
        south = min(source_location.latitude, destination_location.latitude) - 0.02
        east = max(source_location.longitude, destination_location.longitude) + 0.1
        west = min(source_location.longitude, destination_location.longitude) - 0.02

        # Fetch the graph for the specific mode
        G = ox.graph_from_bbox(north, south, east, west, network_type=network_type)

        # Find nearest nodes
        orig_node = ox.distance.nearest_nodes(G, source_location.longitude, source_location.latitude)
        dest_node = ox.distance.nearest_nodes(G, destination_location.longitude, destination_location.latitude)

        # Calculate the shortest path and its total distance
        shortest_path = nx.shortest_path(G, orig_node, dest_node, weight='length')
        total_distance = nx.shortest_path_length(G, orig_node, dest_node, weight='length')  # in meters

        if not shortest_path:
            return jsonify({"error": f"No route found for mode: {mode}."}), 400

        # Estimate time based on average speeds (meters/second)
        average_speeds = {
            "walk": 1.4,   # ~5 km/h
            "bike": 4.1,   # ~15 km/h
            "drive": 13.9,  # ~50 km/h
            "bus": 7.0     # ~25 km/h (assumed for bus)
        }
        travel_time = total_distance / average_speeds[mode]  # in seconds

        # Convert time to hours, minutes, and seconds
        travel_time_hours = int(travel_time // 3600)
        travel_time_minutes = int((travel_time % 3600) // 60)
        travel_time_seconds = int(travel_time % 60)

        # Generate map visualization
        path_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]
        m = folium.Map(location=[(source_location.latitude + destination_location.latitude) / 2,
                                 (source_location.longitude + destination_location.longitude) / 2],
                       zoom_start=15)
        line_style = "dotted" if mode == "walk" else "solid"
        folium.PolyLine(locations=path_coords, color="blue", weight=5, opacity=0.7, dash_array="5, 5" if line_style == "dotted" else None).add_to(m)

        # Add source and destination markers
        folium.Marker([source_location.latitude, source_location.longitude],
                      popup=f"Source: {source}", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker([destination_location.latitude, destination_location.longitude],
                      popup=f"Destination: {destination}", icon=folium.Icon(color="red")).add_to(m)

        return jsonify({
            "route_found": True,
            "total_distance": round(total_distance / 1000, 2),  # Convert to kilometers
            "travel_time": f"{travel_time_hours} hours {travel_time_minutes} minutes {travel_time_seconds} seconds",
            "map_html": m._repr_html_()
        })

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
