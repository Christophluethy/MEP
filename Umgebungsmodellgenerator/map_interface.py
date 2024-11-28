import customtkinter as ctk
import tkintermapview
from kivy.garden.mapview import MapView, MarkerMap
map = MapView()

# GUI
root_tk = ctk.CTk()
root_tk.geometry("1000x600")
root_tk.title("Umgebungsmodell Generator")

# Darkmode
ctk.set_appearance_mode("dark")  # oder "light"

# Sidebar
sidebar = ctk.CTkFrame(root_tk, width=200)
sidebar.pack(side="left", fill="y")

# Modellausgabe-Button
def modellausgabe():
    print("Modellausgabe gestartet")

output_button = ctk.CTkButton(sidebar, text="Modellausgabe", command=modellausgabe)
output_button.pack(side="bottom", pady=20)

# Button zum Setzen eines Positionsmarkers in der Mitte der Karte
def set_center_marker():
    center_lat, center_lon = map_widget.get_position()
    center_marker = map_widget.set_marker(center_lat, center_lon, text=f"Punkt")
    print(f"Marker in der Mitte gesetzt bei Latitude: {center_lat:.5f}, Longitude: {center_lon:.5f}")

center_marker_button = ctk.CTkButton(sidebar, text="Marker in Kartenmitte setzen", command=set_center_marker)
center_marker_button.pack(pady=10)

# Karten-Widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
map_widget.pack(side="right", fill="both", expand=True)

# Startposition
map_widget.set_position(47.34904, 8.24261, zoom=15) #Villmergen

# Marker mit rechtem Mausklick hinzufügen

def add_marker_event(coords):
    print("Add marker:", coords)
    new_marker = map_widget.set_marker(coords[0], coords[1], text="Punkt")
    

map_widget.add_right_click_menu_command(label="Punkt hinzufügen",
                                        command=add_marker_event,
                                        pass_coords=True)


# Start
root_tk.mainloop()



