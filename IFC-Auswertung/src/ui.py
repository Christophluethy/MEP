import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from ifc_handler import raum_daten


# Funktion zum Erstellen des GUI
def create_gui(raum_daten):
    # Root-Fenster erstellen
    root = ctk.CTk()
    root.title("Raumdaten Anzeige")
    root.geometry("900x600")  # Fenstergröße anpassen

    # Schriftgröße definieren
    font_size = 16
    font = ("Helvetica", font_size)

    # Titel hinzufügen
    title_label = ctk.CTkLabel(root, text="Raumübersicht", font=("Helvetica", font_size + 4, "bold"))
    title_label.pack(pady=10)

    # Dropdown für Wohnungsauswahl erstellen
    selected_apartment = tk.StringVar()
    apartments = sorted(set([eigenschaften["Wohnung-ID"] for eigenschaften in raum_daten.values()]))

    dropdown = ttk.Combobox(root, textvariable=selected_apartment, values=["Alle Wohnungen"] + apartments,
                            state="readonly", font=font)
    dropdown.pack(pady=10)
    dropdown.set("Wähle eine Wohnung aus")

    # Frame für die Raumdetails
    details_frame = ctk.CTkFrame(root)
    details_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Treeview für die Raumdetails
    columns = ["Raum-ID", "Raumname", "Nettofläche (m²)", "Höhe im Licht (m)", "Raumklassifikation", "Gebäude-ID"]
    details_tree = ttk.Treeview(details_frame, columns=columns, show="headings", height=12)
    details_tree.pack(fill="both", expand=True)

    for col in columns:
        details_tree.heading(col, text=col, anchor="w")
        details_tree.column(col, width=200, anchor="w")

    # Schriftgröße für Treeview-Tabelle anpassen
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", font_size))
    style.configure("Treeview.Heading", font=("Helvetica", font_size + 2, "bold"))

    def apply_alternate_row_colors():
        for i, item in enumerate(details_tree.get_children()):
            if i % 2 == 0:
                details_tree.item(item, tags=("even",))
            else:
                details_tree.item(item, tags=("odd",))

        details_tree.tag_configure("even", background="#f0f0f0")
        details_tree.tag_configure("odd", background="white")

    export_button = ctk.CTkButton(root, text="Exportieren nach Excel",
                                  command=lambda: export_to_excel(details_tree), font=font)
    export_button.pack(pady=10)

    # Funktion, um Raumdetails zu laden
    def load_apartment_details(event=None):
        selected = selected_apartment.get()

        for item in details_tree.get_children():
            details_tree.delete(item)

        if selected == "Alle Wohnungen":
            for raum_name, eigenschaften in sorted(raum_daten.items()):
                details_tree.insert("", "end", values=(
                    raum_name,
                    eigenschaften["Raumname"],
                    eigenschaften["Nettofläche"],
                    eigenschaften["Höhe im Licht"],
                    eigenschaften["Raumklassifikation"],
                    eigenschaften["Gebäude-ID"]
                ))
        else:
            for raum_name, eigenschaften in sorted(raum_daten.items()):
                if eigenschaften["Wohnung-ID"] == selected:
                    details_tree.insert("", "end", values=(
                        raum_name,
                        eigenschaften["Raumname"],
                        eigenschaften["Nettofläche"],
                        eigenschaften["Höhe im Licht"],
                        eigenschaften["Raumklassifikation"],
                        eigenschaften["Gebäude-ID"]
                    ))
        apply_alternate_row_colors()

    dropdown.bind("<<ComboboxSelected>>", load_apartment_details)

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
                    labels.append(raum)
                    values.append(eigenschaften["Nettofläche"])

        if not labels:  # Keine Daten für Diagramm
            return

        # Matplotlib-Figure erstellen
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(labels, values, color="skyblue")
        ax.set_title(f"Nettofläche für {'alle Wohnungen' if selected == 'Alle Wohnungen' else selected}",
                     fontsize=16, weight="bold")
        ax.set_xlabel("Raum-ID", fontsize=12)
        ax.set_ylabel("Nettofläche (m²)", fontsize=12)
        ax.tick_params(axis='x', rotation=45, labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        fig.tight_layout()

        # Diagramm in GUI einbetten
        diagram_canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = diagram_canvas.get_tk_widget()
        canvas_widget.pack(pady=10, fill="both", expand=True)

        # Diagramm rendern
        diagram_canvas.draw()

    diagram_button = ctk.CTkButton(root, text="Diagramm", command=toggle_diagram, font=font)
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


def export_to_excel(tree):
    data = []
    for item in tree.get_children():
        data.append(tree.item(item)["values"])

    columns = [tree.heading(col)["text"] for col in tree["columns"]]

    df = pd.DataFrame(data, columns=columns)
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel-Dateien", "*.xlsx")])

    if file_path:
        df.to_excel(file_path, index=False, engine='openpyxl')
        print(f"Daten wurden in '{file_path}' exportiert.")
    else:
        print("Export abgebrochen.")


# GUI starten
create_gui(raum_daten)
