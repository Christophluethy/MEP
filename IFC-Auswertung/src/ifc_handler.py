import ifcopenshell

def load_ifc_data(file_path):
    ifc_file = ifcopenshell.open(file_path)

    raum_daten = {}

    for room in ifc_file.by_type("IfcSpace"):
        raum_name = room.Name
        found_area = False
        found_height = False
        found_classification = False
        found_building_id = False
        found_room_name = False
        area = None
        height = None
        classification = None
        building_id = None
        room_name = None
        apartment_id = raum_name[:-2]

        for rel in room.IsDefinedBy:
            if rel.is_a("IfcRelDefinesByProperties"):
                prop_def = rel.RelatingPropertyDefinition
                if prop_def.is_a("IfcPropertySet") and prop_def.Name == "Pset_Futuro":
                    for prop in prop_def.HasProperties:
                        if prop.Name == "Bodenfläche (Netto)":
                            if prop.is_a("IfcPropertySingleValue"):
                                try:
                                    area = float(prop.NominalValue.wrappedValue)
                                    found_area = True
                                except ValueError as e:
                                    print(f"Fehler beim Konvertieren der Fläche: {e}")
                        if prop.Name == "Höhe im Licht":
                            if prop.is_a("IfcPropertySingleValue"):
                                try:
                                    height = float(prop.NominalValue.wrappedValue)
                                    found_height = True
                                except ValueError as e:
                                    print(f"Fehler beim Konvertieren der Höhe: {e}")
                        if prop.Name == "Raumklassifikation":
                            if prop.is_a("IfcPropertySingleValue"):
                                try:
                                    classification = str(prop.NominalValue.wrappedValue)
                                    found_classification = True
                                except ValueError as e:
                                    print(f"Fehler beim Konvertieren der Raumklassifikation: {e}")
                        if prop.Name == "Gebäude-ID":
                            if prop.is_a("IfcPropertySingleValue"):
                                try:
                                    building_id = str(prop.NominalValue.wrappedValue)
                                    found_building_id = True
                                except ValueError as e:
                                    print(f"Fehler beim Konvertieren der Gebäude-ID: {e}")
                        if prop.Name == "Raumname":
                            if prop.is_a("IfcPropertySingleValue"):
                                try:
                                    room_name = str(prop.NominalValue.wrappedValue)
                                    found_room_name = True
                                except ValueError as e:
                                    print(f"Fehler beim Konvertieren des Raumnamens: {e}")

        if found_area or found_height or found_classification or found_building_id or found_room_name:
            raum_daten[raum_name] = {
                "Nettofläche": round(area, 2) if found_area else None,
                "Höhe im Licht": round(height, 2) if found_height else None,
                "Raumklassifikation": classification if found_classification else None,
                "Gebäude-ID": building_id if found_building_id else None,
                "Raumname": room_name if found_room_name else None,
                "Wohnung-ID": apartment_id
            }

    return raum_daten  # Gibt die Raumdaten zurück
