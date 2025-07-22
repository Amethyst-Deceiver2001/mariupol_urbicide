import osmnx as ox

G = ox.graph_from_place('Mariupol, Ukraine', network_type='drive')
nodes, edges = ox.graph_to_gdfs(G)
edges.to_file('data/raw/osm/mariupol_streets.geojson', driver='GeoJSON')