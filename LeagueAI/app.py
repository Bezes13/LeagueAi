import tkinter as tk
import json
from tkinter import ttk
from PIL import Image, ImageTk
from keras.models import load_model
import numpy as np

critic = load_model('model.h5')
champion_path = 'champion.json'
with open(champion_path, 'r') as f:
    data = json.load(f)

champions = []
champion_dic = {}

for index, (champion_id, champion_info) in enumerate(data['data'].items()):
    champions.append(champion_info['id'])
    champion_dic[champion_info['id']] = index

icon_photos = []
icon_buttons = []
filtered_champions = champions[:]
team_index = 0
picked_champs_teamA = []
picked_champs_teamB = []


def calculate_winner():
    data = []
    team1 = [champion_dic[champ] for champ in picked_champs_teamA]
    team2 = [champion_dic[champ] for champ in picked_champs_teamB]
    data.append([team1, team2])
    onehot = np.eye(len(champions), dtype='float32')[data]

    team_data = np.zeros((1, 2, 5, len(champions)))
    team_data[:, :, :, 0] = 0.0  # Fill with empty space

    team_data[:, :2, :5, :] = onehot
    value = critic.predict(team_data)
    value = value[0][0]
    print(value)
    chance = (value - 0.5)
    if chance > 0:
        result_label.config(text=f"Team A wins more likely with a chance {round((chance * 2) * 100)}%")
    else:
        result_label.config(text=f"Team B wins more likely with a chance {round((chance * -2) * 100)}%")


def empty_a():
    picked_champs_teamA.clear()
    update_selected_champions_label_team_a()


def empty_b():
    picked_champs_teamB.clear()
    update_selected_champions_label_team_b()


def on_icon_click(name):
    if len(picked_champs_teamA) < 5:
        picked_champs_teamA.append(name)
        update_selected_champions_label_team_a()
        return

    if len(picked_champs_teamB) < 5:
        picked_champs_teamB.append(name)
        update_selected_champions_label_team_b()


def update_selected_champions_label_team_a():
    selected_champions_label.config(text="Team A : " + (", ".join(picked_champs_teamA)))


def update_selected_champions_label_team_b():
    selected_champions_label1.config(text="Team B : " + (", ".join(picked_champs_teamB)))


def show_icons():
    icon_photos.clear()
    for button in icon_buttons:
        button.destroy()
    icon_buttons.clear()
    # Liste, um die PhotoImage-Instanzen zu speichern
    for i, champ in enumerate(filtered_champions):
        icon_image = Image.open(f"champion/{champ}.png")
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_photos.append(icon_photo)  # Füge die PhotoImage-Instanz zur Liste hinzu

        # Erstelle eine Schaltfläche mit dem Icon als Hintergrund
        icon_button = ttk.Button(inner_frame, image=icon_photo, command=lambda name=champ: on_icon_click(name))
        icon_button.grid(row=i // 5, column=i % 5, padx=5, pady=5)  # Verwende ein Grid-Layout
        icon_buttons.append(icon_button)


def filter_champions(search_word):
    filtered = []
    for champ in champions:
        if str(champ).lower().startswith(search_word.lower()):
            filtered.append(champ)

    return filtered


def on_search_changed(a, b, c):
    search_word = search_var.get()
    global filtered_champions
    filtered_champions = filter_champions(search_word)
    show_icons()


def resize(event):
    canvas.config(scrollregion=canvas.bbox(tk.ALL))
    canvas.itemconfig(inner_frame_id, width=event.width)


# Erstelle ein Tkinter-Fenster
window = tk.Tk()
window.title("League Criticer")
window.geometry("1000x800")  # Größe des Fensters (Breite x Höhe)

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

# Suchleiste (Search Bar)
search_var = tk.StringVar()
search_var.trace_add("write", on_search_changed)  # Verknüpfe die Funktion mit der Änderung des Suchwortes
search_entry = ttk.Entry(window, textvariable=search_var, font=("Arial", 12))
search_entry.pack(pady=10, padx=20)
# Zeige die Icons
show_icons()

selected_champions_label = ttk.Label(window, text="", font=("Arial", 12))
selected_champions_label.pack()

selected_champions_label1 = ttk.Label(window, text="", font=("Arial", 12))
selected_champions_label1.pack()

result_label = ttk.Label(window, text="", font=("Arial", 12))
result_label.pack()

# Binden des Events für die Größenänderung des Canvas
canvas.bind("<Configure>", resize)

update_selected_champions_label_team_a()
update_selected_champions_label_team_b()
button = tk.Button(window, text="Empty Team A", command=empty_a)
button.pack()
button = tk.Button(window, text="Empty Team B", command=empty_b)
button.pack()
button = tk.Button(window, text="Calculate Winner", command=calculate_winner)
button.pack()
# Starte die Tkinter-Schleife
window.mainloop()
