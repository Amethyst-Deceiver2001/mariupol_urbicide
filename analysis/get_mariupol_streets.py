import os
BASE_DIR = os.environ.get("PROJECT_ROOT", os.path.dirname(os.path.abspath(__file__)))
import osmnx as ox

G = ox.graph_from_place('Mariupol, Ukraine', network_type='drive')
nodes, edges = ox.graph_to_gdfs(G)
edges.to_file(os.path.join(BASE_DIR, "data", "raw", "osm", "mariupol_streets.geojson"), driver="GeoJSON")