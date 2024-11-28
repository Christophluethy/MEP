import requests

def get_area_data(lat_min, lat_max, lon_min, lon_max):
    # SwissTopo API URL (dies ist ein Platzhalter)
    url = "https://api.swisstopo.ch/"
    params = {
        "lat_min": lat_min,
        "lat_max": lat_max,
        "lon_min": lon_min,
        "lon_max": lon_max
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()  # Rückgabe der Geländedaten als JSON
    else:
        raise Exception("Fehler beim Abrufen der Daten von SwissTopo")
