


import tkinter as tk
import customtkinter as ctk
from map_interface2 import MapInterface
from swisstopo_api import get_area_data
from model_export import export_to_ifc

# Hauptanwendungsklasse
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Umgebungsmodell Tool")

        # Konfiguration für das Design
        ctk.set_appearance_mode("System")  # Dunkel oder hell je nach System
        ctk.set_default_color_theme("blue")  # Farbthema anpassen

        # Layout der Anwendung
        self.setup_layout()

    def setup_layout(self):
        # Frame für die Sidebar auf der linken Seite
        sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=10)
        sidebar_frame.grid(row=0, column=0, padx=10, pady=10)

        # Knopf zum Auswählen von Koordinaten
        self.select_button = ctk.CTkButton(sidebar_frame, text="Koordinaten auswählen", command=self.select_coordinates)
        self.select_button.pack(pady=10)

        # Knopf für den Export als IFC
        self.export_button = ctk.CTkButton(sidebar_frame, text="Als IFC exportieren", command=self.export_ifc)
        self.export_button.pack(pady=10)

        # Frame für die Karte
        map_frame = ctk.CTkFrame(self.root, width=800, height=600, corner_radius=10)
        map_frame.grid(row=0, column=1, padx=10, pady=10)

        # Karte als interaktive Map
        self.map_interface = MapInterface(map_frame)
        
    def select_coordinates(self):
        # Funktionalität zum Auswählen von Koordinaten
        print("Koordinaten auswählen wurde geklickt.")
        # Hier kannst du die Interaktivität mit der Karte und das Speichern der Koordinaten implementieren

    def export_ifc(self):
        # Exportiere die ausgewählten Koordinaten als IFC
        print("Exportiere als IFC...")
        # Hier implementierst du die Logik, um die exportierten Daten zu verarbeiten und zu speichern.

# Tkinter Fenster
if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()

