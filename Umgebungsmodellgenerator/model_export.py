import ifcopenshell  # Beispiel mit ifcopenshell

def export_to_ifc(data, filename="output.ifc"):
    # Beispiel für das Erstellen einer IFC-Datei
    ifc = ifcopenshell.file()
    # Erstelle IFC-Objekte und füge sie der Datei hinzu
    # Dies ist ein einfaches Beispiel, du musst den IFC-Datentyp erstellen und befüllen
    ifc.write(filename)
    print(f"IFC-Datei gespeichert: {filename}")
