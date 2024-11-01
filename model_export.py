import rhino3dm

def export_to_3dm(model_data):
    model = rhino3dm.File3dm()
    
    # Beispiel: Hinzufügen von Daten aus model_data zum 3D-Modell
    # Terrain und Gebäude hinzufügen
    # Hier kannst du eine echte 3D-Modellstruktur aus den Daten aufbauen

    # Platzhalter-Beispiel
    for elevation in model_data["terrain"]:
        # Terrain-Verarbeitung und -Hinzufügen
        pass

    for building in model_data["buildings"]:
        # Gebäude-Verarbeitung und -Hinzufügen
        pass

    model.Write("output.3dm")
