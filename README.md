# Route-Finding Web App

A Flask-based route-finding application that calculates and visualizes the optimal path between a source and destination based on user-selected transport mode (walking, biking, driving, or bus). It provides travel time estimates and route visualization using OpenStreetMap data.


## Features

- **Multi-Mode Routing**: Choose between walking, biking, driving, and bus modes.
- **Interactive Map Visualization**: Visualize the route on an interactive map.
- **Travel Distance and Time Calculation**: Get real-time travel distance and estimated time based on selected transport mode.

## Project Structure

![Screenshot 2025-05-24 095314](https://github.com/user-attachments/assets/149dbb6d-4182-4546-8c00-061ce20bfa5b)


---

## Setup and Installation

```markdown
## Setup and Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/route-finding-web-app.git
    ```
2. Navigate to the project directory:
    ```bash
    cd route-finding-web-app
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the Flask application:
    ```bash
    python app.py
    ```

5. Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000) to use the app.
```

## Example Code

```python
from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
import osmnx as ox
import networkx as nx
import folium

app = Flask(__name__)
geolocator = Nominatim(user_agent="route_finder_app")

@app.route('/get-route', methods=['POST'])
def get_route():
    # Fetch source, destination, and mode from request
    # Compute route, time, and distance
    # Generate map with Folium
    pass
```

## Usage

1. Enter the source and destination locations.
2. Select the mode of transportation: walking, biking, driving, or bus.
3. Click "Submit" to view the optimal route, travel distance, and estimated time.


## Technologies Used

- **Flask**: Backend framework for handling HTTP requests
- **Geopy**: For geolocation lookup of addresses
- **OSMNX**: For accessing OpenStreetMap data and building graphs
- **NetworkX**: For shortest path algorithms
- **Folium**: For interactive map visualizations


![image](https://github.com/user-attachments/assets/e0b7dc13-fb19-4eba-96d2-e728f6273f2c)





