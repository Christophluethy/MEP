import requests

def fetch_elevation_data(bbox):
    elevations = []
    # Beispielweise rufe Punkte im Grid ab
    for lng in range(int(bbox["minx"]), int(bbox["maxx"]), 100):  # Schrittweite anpassen
        for lat in range(int(bbox["miny"]), int(bbox["maxy"]), 100):
            url = f"https://api3.geo.admin.ch/rest/services/height?easting={lng}&northing={lat}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                elevations.append(data['height'])
            else:
                print("Fehler bei Höhenabfrage:", response.status_code)
    return elevations

def fetch_building_data(bbox):
    wfs_url = "https://wfs.swisstopo.admin.ch"
    params = {
        "SERVICE": "WFS",
        "VERSION": "2.0.0",
        "REQUEST": "GetFeature",
        "TYPENAME": "swissbuildings3d",
        "BBOX": f"{bbox['minx']},{bbox['miny']},{bbox['maxx']},{bbox['maxy']}"
    }
    response = requests.get(wfs_url, params=params)
    if response.status_code == 200:
        return response.text  # XML-Daten
    else:
        print("Fehler bei Gebäudedatenabfrage:", response.status_code)
        return None
