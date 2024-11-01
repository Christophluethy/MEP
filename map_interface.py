import folium
from ipywidgets import Output
from IPython.display import display

def select_points_on_map():
    # Initialisierung der Karte
    m = folium.Map(location=[46.8, 8.2], zoom_start=8)
    points = []

    # Funktion für das Hinzufügen von Punkten
    def on_click(event):
        lat, lon = event.latlng
        points.append((lat, lon))
        folium.Marker([lat, lon]).add_to(m)

    # Karte anzeigen
    out = Output()
    with out:
        display(m)
    out

    return points
