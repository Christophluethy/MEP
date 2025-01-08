import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from ifc_handler import load_ifc_data

# Globale Variable für raum_daten
raum_daten = {}

# Funktion zum Erstellen des GUI
def create_gui():
    # Root-Fenster erstellen
    root = ctk.CTk()
    root.title("Raumdaten Anzeige")
    root.geometry("900x600") 
    root.iconbitmap("C:\\Users\\clu\\OneDrive - Hochschule Luzern\\HS24\\DT_Programm\\DT_Project\\IFC-Auswertung\\src\\favicon.ico") 

    # Hintergrund des Fensters auf Weiß setzen
    root.configure(fg_color="antique white")

    # Schriftgröße definieren
    font_size = 16
    font = ("Helvetica", font_size)

    # Titel hinzufügen
    title_label = ctk.CTkLabel(root, text="Raumübersicht", font=("Helvetica", font_size + 4, "bold"), text_color="black")

    title_label.pack(pady=10)

    # Dropdown für Wohnungsauswahl erstellen
    selected_apartment = tk.StringVar()
    apartments = ["Alle Wohnungen"]  # Standardwert als erstes Element

    dropdown = ttk.Combobox(root, textvariable=selected_apartment, values=apartments,
                            state="readonly", font=font)
    dropdown.pack(pady=10)
    dropdown.set("Alle Wohnungen")  # Standardwert setzen

    # Frame für die Raumdetails
    details_frame = ctk.CTkFrame(root, fg_color="white")  # Hintergrund auf Weiß setzen
    details_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Spalten definieren
    columns = ["Raum-ID", "Raumname", "Nettofläche (m²)", "Höhe im Licht (m)", "Raumklassifikation", "Gebäude-ID", "Bodenbelag", "Wandbekleidung"]
    visible_columns = set(columns)  # Anfangs sind alle Spalten sichtbar

    # Treeview für die Raumdetails
    details_tree = ttk.Treeview(details_frame, columns=columns, show="headings", height=12)
    details_tree.pack(fill="both", expand=True)

    # Setze die Schriftgröße für Treeview
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", font_size))
    style.configure("Treeview.Heading", font=("Helvetica", font_size + 2, "bold"))
    style.configure("Treeview", rowheight=30)  # Zeilenhöhe erhöhen

    for col in columns:
        details_tree.heading(col, text=col, anchor="w", command=lambda c=col: toggle_column(c))
        details_tree.column(col, width=200, anchor="w")

    export_button = ctk.CTkButton(root, text="Exportieren nach Excel",
                                  command=lambda: export_to_excel(details_tree, visible_columns), font=font, text_color="black", fg_color="navajo white")
    export_button.pack(pady=10)

    # Funktion, um Raumdetails zu laden
    def load_apartment_details(event=None):
        selected = selected_apartment.get()

        for item in details_tree.get_children():
            details_tree.delete(item)

        total_area = 0  # Variable für die Gesamtfläche

        if selected == "Alle Wohnungen":
            for raum_name, eigenschaften in sorted(raum_daten.items()):
                values = [
                    raum_name,
                    eigenschaften["Raumname"],
                    eigenschaften["Nettofläche"],
                    eigenschaften["Höhe im Licht"],
                    eigenschaften["Raumklassifikation"],
                    eigenschaften["Gebäude-ID"],
                    eigenschaften["Bodenbelag"],
                    eigenschaften["Wandbekleidung"]
                ]
                filtered_values = [val if col in visible_columns else "" for col, val in zip(columns, values)]
                details_tree.insert("", "end", values=filtered_values)
                if eigenschaften["Nettofläche"] is not None:
                    total_area += eigenschaften["Nettofläche"]
        else:
            for raum_name, eigenschaften in sorted(raum_daten.items()):
                if eigenschaften["Wohnung-ID"] == selected:
                    values = [
                        raum_name,
                        eigenschaften["Raumname"],
                        eigenschaften["Nettofläche"],
                        eigenschaften["Höhe im Licht"],
                        eigenschaften["Raumklassifikation"],
                        eigenschaften["Gebäude-ID"],
                        eigenschaften["Bodenbelag"],
                        eigenschaften["Wandbekleidung"]
                    ]
                    filtered_values = [val if col in visible_columns else "" for col, val in zip(columns, values)]
                    details_tree.insert("", "end", values=filtered_values)
                    if eigenschaften["Nettofläche"] is not None:
                        total_area += eigenschaften["Nettofläche"]

        # Leere Zeile hinzufügen
        details_tree.insert("", "end", values=("", "", "", "", "", "", "", ""))

        # Gesamtfläche als letzte Zeile hinzufügen
        details_tree.insert("", "end", values=("Nettowohnfläche (m²)", "", round(total_area, 2), "", "", "", "", ""), tags=("total",))

        # Formatierung für Gesamtfläche
        details_tree.tag_configure("total", font=("Helvetica", font_size, "bold"), background="#e0e0e0")

        apply_alternate_row_colors()

    dropdown.bind("<<ComboboxSelected>>", load_apartment_details)

    # Funktion, um IFC-Datei zu laden
    def load_ifc_file():
        global raum_daten  # Benutzen der globalen raum_daten-Variable
        # Öffnet ein Dialogfenster, um die Datei auszuwählen
        file_path = filedialog.askopenfilename(title="IFC-Datei auswählen", filetypes=[("IFC-Dateien", "*.ifc")])

        if file_path:
            # Wenn eine Datei ausgewählt wurde, dann die IFC-Datei laden
            print(f"Datei ausgewählt: {file_path}")
            raum_daten = load_ifc_data(file_path)  # IFC-Daten laden und zurückbekommen

            # Dropdown mit den Wohnungen aktualisieren
            apartments = sorted(set([eigenschaften["Wohnung-ID"] for eigenschaften in raum_daten.values()]))
            apartments.insert(0, "Alle Wohnungen")  # "Alle Wohnungen" als erste Option hinzufügen
            dropdown['values'] = apartments  # Dropdown mit neuen Werten füllen
            dropdown.set("Alle Wohnungen")  # Standardwert setzen

            # Funktion zum Laden der Rauminformationen erneut aufrufen
            load_apartment_details()  # Details neu laden (mit den geladenen Daten)
        else:
            print("Keine Datei ausgewählt.")

    load_button = ctk.CTkButton(root, text="IFC-Datei laden", command=load_ifc_file, font=font, text_color="black", fg_color="navajo white")
    load_button.pack(pady=10)

    # Funktion zum Umschalten der Sichtbarkeit einer Spalte
    def toggle_column(column):
        nonlocal visible_columns
        if column in visible_columns:
            visible_columns.remove(column)
        else:
            visible_columns.add(column)
        load_apartment_details()  # Die Details neu laden, um die geänderte Sichtbarkeit zu berücksichtigen

    # Diagramm anzeigen/ausblenden
    diagram_canvas = None  # Canvas-Referenz speichern

    def toggle_diagram():
        nonlocal diagram_canvas
        if diagram_canvas:
            diagram_canvas.get_tk_widget().destroy()
            diagram_canvas = None
        else:
            show_diagram()

    def show_diagram():
        nonlocal diagram_canvas

        # Wohnung filtern
        selected = selected_apartment.get()
        labels = []
        values = []

        for raum, eigenschaften in raum_daten.items():
            if selected == "Alle Wohnungen" or eigenschaften["Wohnung-ID"] == selected:
                if eigenschaften["Nettofläche"] is not None:
                    labels.append(eigenschaften["Raumname"])  # Raumname statt Raum-ID
                    values.append(eigenschaften["Nettofläche"])

        if not labels:  # Keine Daten für Diagramm
            return

        # Matplotlib-Figure erstellen
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(labels, values, color="bisque")
        ax.set_title(f"Nettofläche für {'alle Wohnungen' if selected == 'Alle Wohnungen' else selected}",
                     fontsize=16, weight="bold")
        ax.set_xlabel("Raumname", fontsize=15, weight="bold")
        ax.set_ylabel("Nettofläche (m²)", fontsize=15, weight="bold")
        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
        fig.tight_layout()

        # Diagramm in GUI einbetten
        diagram_canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = diagram_canvas.get_tk_widget()
        canvas_widget.pack(pady=10, fill="both", expand=True)

        # Diagramm rendern
        diagram_canvas.draw()

    diagram_button = ctk.CTkButton(root, text="Diagramm", command=toggle_diagram, font=font, text_color="black", fg_color="navajo white")
    diagram_button.pack(pady=10)

    # Sauberes Schließen des Fensters
    def on_close():
        nonlocal diagram_canvas
        if diagram_canvas:
            diagram_canvas.get_tk_widget().destroy()
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)  # Event-Handler für das Schließen des Fensters

    # GUI starten
    root.mainloop()

def export_to_excel(tree, visible_columns):
    data = []
    for item in tree.get_children():
        values = tree.item(item)["values"]
        # Nur Werte der sichtbaren Spalten exportieren
        filtered_values = [val for col, val in zip(tree["columns"], values) if col in visible_columns]
        data.append(filtered_values)

    columns = [col for col in tree["columns"] if col in visible_columns]

    df = pd.DataFrame(data, columns=columns)
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel-Dateien", "*.xlsx")])

    if file_path:
        df.to_excel(file_path, index=False, engine='openpyxl')
        print(f"Daten wurden in '{file_path}' exportiert.")
    else:
        print("Export abgebrochen.")

def apply_alternate_row_colors():
    for i, item in enumerate(details_tree.get_children()):
        if i % 2 == 0:  # Für gerade Zeilen
            details_tree.item(item, tags=("even",))
        else:  # Für ungerade Zeilen
            details_tree.item(item, tags=("odd",))

    details_tree.tag_configure("even", background="#f2f2f2")
    details_tree.tag_configure("odd", background="#ffffff")

# GUI starten
create_gui()
