import ifcopenshell

print(ifcopenshell.version)
model = ifcopenshell.file()

# file_path = "C:/Users/clu/OneDrive - Hochschule Luzern/HS24/DT_Programm/DT_Project/IFC-Auswertung/data/ifc_example.ifc"
file_path = "C:/Users/clu/OneDrive - Hochschule Luzern/HS24/DT_Programm/DT_Project/IFC-Auswertung/data/FUT-ARM-31.ifc"
ifc_file = ifcopenshell.open(file_path)




# Dictionary für Raumdaten erstellen
raum_daten = {}

for room in ifc_file.by_type("IfcSpace"):
    raum_name = room.Name  # Raumnamen (Raumnummer) als Key
    found_area = False  # Flag, um festzustellen, ob die Fläche gefunden wurde
    found_height = False  # Flag, um festzustellen, ob die Höhe gefunden wurde
    found_classification = False  # Flag, um festzustellen, ob die Raumklassifikation gefunden wurde
    found_building_id = False  # Flag, um festzustellen, ob die Gebäude-ID gefunden wurde
    found_room_name = False  # Flag, um festzustellen, ob der Raumname gefunden wurde
    area = None  # Variable für die Fläche
    height = None  # Variable für die Höhe
    classification = None  # Variable für die Raumklassifikation
    building_id = None  # Variable für die Gebäude-ID
    room_name = None  # Variable für den Raumname
    apartment_id = raum_name[:-2]  # Wohnung ableiten: Raumnummer ohne die letzten 2 Stellen

    for rel in room.IsDefinedBy:
        if rel.is_a("IfcRelDefinesByProperties"):
            prop_def = rel.RelatingPropertyDefinition
            if prop_def.is_a("IfcPropertySet") and prop_def.Name == "Pset_Futuro":
                for prop in prop_def.HasProperties:
                    # Extrahieren der Bodenfläche (Netto)
                    if prop.Name == "Bodenfläche (Netto)":
                        if prop.is_a("IfcPropertySingleValue"):
                            try:
                                area = float(prop.NominalValue.wrappedValue)
                                found_area = True
                            except ValueError as e:
                                print(f"    Fehler beim Konvertieren der Fläche: {e}")
                    
                    # Extrahieren der Höhe im Licht
                    if prop.Name == "Höhe im Licht":
                        if prop.is_a("IfcPropertySingleValue"):
                            try:
                                height = float(prop.NominalValue.wrappedValue)
                                found_height = True
                            except ValueError as e:
                                print(f"    Fehler beim Konvertieren der Höhe: {e}")
                    
                    # Extrahieren der Raumklassifikation
                    if prop.Name == "Raumklassifikation":
                        if prop.is_a("IfcPropertySingleValue"):
                            try:
                                classification = str(prop.NominalValue.wrappedValue)
                                found_classification = True
                            except ValueError as e:
                                print(f"    Fehler beim Konvertieren der Raumklassifikation: {e}")

                    # Extrahieren der Gebäude-ID
                    if prop.Name == "Gebäude-ID":
                        if prop.is_a("IfcPropertySingleValue"):
                            try:
                                building_id = str(prop.NominalValue.wrappedValue)
                                found_building_id = True
                            except ValueError as e:
                                print(f"    Fehler beim Konvertieren der Gebäude-ID: {e}")
                    
                    # Extrahieren des Raumnamens
                    if prop.Name == "Raumname":
                        if prop.is_a("IfcPropertySingleValue"):
                            try:
                                room_name = str(prop.NominalValue.wrappedValue)
                                found_room_name = True
                            except ValueError as e:
                                print(f"    Fehler beim Konvertieren des Raumnamens: {e}")
    
    # Dictionary-Eintrag für Raum mit Fläche, Höhe, Raumklassifikation, Gebäude-ID und Raumname (wenn gefunden)
    if found_area or found_height or found_classification or found_building_id or found_room_name:
        raum_daten[raum_name] = {
            "Nettofläche": round(area, 2) if found_area else None,
            "Höhe im Licht": round(height, 2) if found_height else None,
            "Raumklassifikation": classification if found_classification else None,
            "Gebäude-ID": building_id if found_building_id else None,
            "Raumname": room_name if found_room_name else None,
            "Wohnung-ID": apartment_id  # Wohnung ID speichern
        }


# Ausgabe des Dictionaries
for raum, eigenschaften in raum_daten.items():
    print(f"Raum: {raum}, Nettofläche: {eigenschaften['Nettofläche']} m², Höhe im Licht: {eigenschaften['Höhe im Licht']} m, Raumklassifikation: {eigenschaften['Raumklassifikation']}, Gebäude-ID: {eigenschaften['Gebäude-ID']}, Raumname: {eigenschaften['Raumname']}")



