# Datenanalyse und Berechnung von Flächen, Höhen etc.

from src.ifc_handler import load_ifc

model = load_ifc("C:\Users\clu\OneDrive - Hochschule Luzern\HS24\DT_Programm\DT_Project\IFC-Auswertung\data\FUT-ARM-31.ifc")
print("IFC-Datei erfolgreich geladen:", model)
