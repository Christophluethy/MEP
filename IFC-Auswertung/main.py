# Hauptskript zum Starten des Programms

from src.ifc_handler import load_ifc, get_rooms

if __name__ == "__main__":
    # Beispielpfad zu einer IFC-Datei
    file_path = r"C:\\Users\\clu\\OneDrive - Hochschule Luzern\\HS24\\DT_Programm\\DT_Project\\IFC-Auswertung\\data\\FUT-ARM-31.ifc"
    model = load_ifc(file_path)

    if model:
        print("IFC-Modell erfolgreich geladen.")
        
        # Räume extrahieren
        rooms = get_rooms(model)
        print(f"\nGefundene Räume: {len(rooms)}")
        
        # Räume mit erweiterten Daten ausgeben
        for room in rooms:
            print(f"Raum: {room['Name']}")
            print(f"  Fläche: {room['Fläche (m²)']}")
            print(f"  Raumhöhe: {room['Raumhöhe (m)']}")  # Der korrekte Schlüssel
            print(f"  Fensterfläche: {room['Fensterfläche (m²)']}")
            print()
    else:
        print("Fehler: IFC-Datei konnte nicht geladen werden.")



