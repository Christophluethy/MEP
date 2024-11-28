# Funktionen zum Laden und Verarbeiten von IFC-Dateien

import ifcopenshell

def load_ifc(file_path):
    """
    Läd eine IFC-Datei und gibt das Modell zurück.
    """
    try:
        model = ifcopenshell.open(file_path)
        print(f"IFC-Datei erfolgreich geladen: {file_path}")
        return model
    except Exception as e:
        print(f"Fehler beim Laden der IFC-Datei: {e}")
        return None
        
def get_rooms(model):
    """
    Extrahiert Räume (IfcSpace-Objekte) aus dem IFC-Modell und gibt ihre Eigenschaften zurück.
    """
    spaces = model.by_type("IfcSpace")
    rooms = []

    for space in spaces:
        # Raumname
        name = space.Name if space.Name else "Unbenannt"

        # Versuche, die Fläche zu extrahieren
        gross_area = None
        for rel in space.IsDefinedBy:
            if rel.is_a("IfcRelDefinesByProperties"):
                properties = rel.RelatingPropertyDefinition
                if properties.is_a("IfcElementQuantity"):
                    for quantity in properties.Quantities:
                        if quantity.is_a("IfcQuantityArea") and quantity.Name == "GrossFloorArea":
                            gross_area = quantity.AreaValue

        # Raumhöhe (falls vorhanden), andernfalls auf "Nicht definiert" setzen
        height = "Nicht definiert"
        for rel in space.IsDefinedBy:
            if rel.is_a("IfcRelDefinesByProperties"):
                properties = rel.RelatingPropertyDefinition
                if properties.is_a("IfcElementQuantity"):
                    for quantity in properties.Quantities:
                        if quantity.is_a("IfcQuantityLength") and quantity.Name == "Height":
                            height = quantity.LengthValue  # Wenn gefunden, Wert setzen

        # Fensterflächen (falls vorhanden)
        window_area = 0
        for window in model.by_type("IfcWindow"):
            if window.ContainedInStructure:  # Wenn das Fenster im Raum enthalten ist
                window_area += window.OverallHeight * window.OverallWidth  # Fensterfläche berechnen

        rooms.append({
            "Name": name,
            "Fläche (m²)": gross_area if gross_area else "Nicht definiert",
            "Raumhöhe (m)": height,  # Raumhöhe jetzt immer gesetzt
            "Fensterfläche (m²)": window_area if window_area else "Nicht definiert"
        })

    return rooms









# Testfunktion
if __name__ == "__main__":
    # Beispielpfad zu einer IFC-Datei (anpassen)
    file_path = "C:\\Users\\clu\\OneDrive - Hochschule Luzern\\HS24\\DT_Programm\\DT_Project\\IFC-Auswertung\\data\\FUT-ARM-31.ifc"

    model = load_ifc(file_path)

    if model:
        print("IFC-Modell geladen:", model)
    else:
        print("Das Modell konnte nicht geladen werden.")


