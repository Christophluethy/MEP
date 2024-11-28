# User Interface mit PyQt

import matplotlib.pyplot as plt
from src.ifc_handler import load_ifc, get_rooms

def plot_room_data():
    file_path = r"C:\\Users\\clu\\OneDrive - Hochschule Luzern\\HS24\\DT_Programm\\DT_Project\\IFC-Auswertung\\data\\FUT-ARM-31.ifc"
    model = load_ifc(file_path)
    
    if model:
        rooms = get_rooms(model)
        
        room_names = [room['Name'] for room in rooms]
        room_areas = [room['Fläche (m²)'] for room in rooms]
        room_heights = [room['Raumhöhe (m)'] for room in rooms]
        window_areas = [room['Fensterfläche (m²)'] for room in rooms]
        
        # Erstelle eine Figur mit Subplots
        fig, axs = plt.subplots(3, 1, figsize=(10, 15))
        
        # Plot für die Raumfläche
        axs[0].bar(room_names, room_areas, color='blue')
        axs[0].set_title('Raumfläche (m²)')
        axs[0].set_xlabel('Raum')
        axs[0].set_ylabel('Fläche (m²)')
        axs[0].tick_params(axis='x', rotation=90)
        
        # Plot für die Raumhöhe
        axs[1].bar(room_names, room_heights, color='green')
        axs[1].set_title('Raumhöhe (m)')
        axs[1].set_xlabel('Raum')
        axs[1].set_ylabel('Raumhöhe (m)')
        axs[1].tick_params(axis='x', rotation=90)
        
        # Plot für die Fensterfläche
        axs[2].bar(room_names, window_areas, color='orange')
        axs[2].set_title('Fensterfläche (m²)')
        axs[2].set_xlabel('Raum')
        axs[2].set_ylabel('Fensterfläche (m²)')
        axs[2].tick_params(axis='x', rotation=90)
        
        # Layout anpassen und Anzeigen
        plt.tight_layout()
        plt.show()
    else:
        print("Fehler: IFC-Datei konnte nicht geladen werden.")

# Aufruf der Visualisierungsfunktion
plot_room_data()
