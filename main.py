from map_interface import select_points_on_map
from swisstopo_api import fetch_elevation_data, fetch_building_data
from data_processing import process_data_for_model
from model_export import export_to_3dm



def main():
    # Schritt 1: Auswahl der Punkte auf der Karte
    points = select_points_on_map()


bbox = {
        "minx": min(p[1] for p in points),
        "miny": min(p[0] for p in points),
        "maxx": max(p[1] for p in points),
        "maxy": max(p[0] for p in points)
    }

elevation_data = fetch_elevation_data(bbox)
building_data = fetch_building_data(bbox)

model_data = process_data_for_model(elevation_data, building_data)

export_to_3dm(model_data)
    print("3D-Modell erfolgreich exportiert als output.3dm")


if __name__ == "__main__":
    main()