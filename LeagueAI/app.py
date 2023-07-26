import tkinter as tk
import json
from tkinter import ttk
from PIL import Image, ImageTk

champion_path = 'champion.json'
with open(champion_path, 'r') as f:
    data = json.load(f)

champions = []
for index, (champion_id, champion_info) in enumerate(data['data'].items()):
    champions.append(champion_info['id'])

icon_photos = []
team_index = 0


def on_button_click():
    print("Klicked")


def on_icon_click(name):
    if len(picked1) == 5:
        picked2.append(name)
        team2.clear()
        build_team2()
    else:
        picked1.append(name)
        team1.clear()
        build_team1()



def show_icons():
    # Liste, um die PhotoImage-Instanzen zu speichern
    for i, champ in enumerate(champions):
        icon_image = Image.open(f"champion/{champ}.png")
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_photos.append(icon_photo)  # Füge die PhotoImage-Instanz zur Liste hinzu

        # Erstelle ein Label für das Icon
        icon_label = ttk.Label(inner_frame, image=icon_photo)
        icon_label.grid(row=i // 5, column=i % 5, padx=5, pady=5)  # Verwende ein Grid-Layout

        # Erstelle eine Schaltfläche mit dem Icon als Hintergrund
        icon_button = ttk.Button(inner_frame, image=icon_photo, command=lambda name=champ: on_icon_click(name))
        icon_button.grid(row=i // 5, column=i % 5, padx=5, pady=5)  # Verwende ein Grid-Layout


def resize(event):
    canvas.config(scrollregion=canvas.bbox(tk.ALL))
    canvas.itemconfig(inner_frame_id, width=event.width)


def build_team1():
    for i,pick in enumerate(picked1):
        extra_icon_image = Image.open(f"champion/{pick}.png")
        extra_icon_photo = ImageTk.PhotoImage(extra_icon_image)
        team1.append(extra_icon_photo)

        # Erstelle ein Label für das zusätzliche Icon
        extra_icon_label = ttk.Label(extra_icons_frame, image=extra_icon_photo)
        extra_icon_label.grid(row=i // 5, column=i % 5, padx=5, pady=5)
        extra_icon_label.pack(pady=5)  # Platzieren Sie das zusätzliche Icon mit Abstand


def build_team2():
    for i in picked2:
        extra_icon_image = Image.open(f"champion/{i}.png")
        extra_icon_photo = ImageTk.PhotoImage(extra_icon_image)
        team2.append(extra_icon_photo)

        # Erstelle ein Label für das zusätzliche Icon
        extra_icon_label = ttk.Label(extra_icons_frame, image=extra_icon_photo)
        extra_icon_label.pack(pady=5)  # Platzieren Sie das zusätzliche Icon mit Abstand


# Erstelle ein Tkinter-Fenster
window = tk.Tk()
window.title("Champion Icons")
window.geometry("600x400")  # Größe des Fensters (Breite x Höhe)

# Füge ein Frame hinzu, um die Scrollbar und das Canvas zu enthalten
frame = ttk.Frame(window)
frame.pack(fill=tk.BOTH, expand=True)

# Füge eine Scrollbar hinzu
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Erstelle ein Canvas, das die Scrollbar steuert
canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Konfiguriere die Scrollbar, um das Canvas zu steuern
scrollbar.config(command=canvas.yview)

# Erstelle ein Frame im Canvas, um die Icons zu platzieren
inner_frame = tk.Frame(canvas)
inner_frame_id = canvas.create_window((0, 0), window=inner_frame, anchor=tk.NW)

# Zeige die Icons
show_icons()

# Binden des Events für die Größenänderung des Canvas
canvas.bind("<Configure>", resize)

extra_icons_frame = ttk.Frame(window)
extra_icons_frame.pack(side=tk.LEFT, fill=tk.Y)

picked1 = []
team1 = []
build_team1()


extra_icons_frame = ttk.Frame(window)
extra_icons_frame.pack(side=tk.LEFT, fill=tk.Y)

picked2 = []
team2 = []
build_team2()

# Starte die Tkinter-Schleife
window.mainloop()