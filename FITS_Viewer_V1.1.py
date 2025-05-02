import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from tkinter import Tk, filedialog

# Maximieren des Fensters
def maximize_window():
    manager = plt.get_current_fig_manager()
    try:
        manager.window.state('zoomed')  # Windows
    except:
        try:
            manager.full_screen_toggle()  # Linux / MacOS
        except:
            pass  # Wenn nichts funktioniert, ignorieren

# Benutzeraktion global speichern
user_action = None

# Tasteneingaben abfangen
def on_key(event):
    global user_action
    if event.key == 'right':
        user_action = 'next'
    elif event.key == 'left':
        user_action = 'prev'
    elif event.key == 'd':
        user_action = 'delete'
    elif event.key == 'q':
        user_action = 'quit'

# Ordnerauswahl
root = Tk()
root.withdraw()  # Versteckt das Hauptfenster
FOLDER = filedialog.askdirectory(title="Wähle den Ordner mit den FITS-Dateien")
root.destroy()

fits_files = sorted(glob.glob(os.path.join(FOLDER, "*.fits")))

print(f"{len(fits_files)} FITS-Dateien gefunden.")

index = 0
fig, ax = plt.subplots()
maximize_window()

while 0 <= index < len(fits_files):
    file = fits_files[index]
    print(f"[{index + 1}/{len(fits_files)}] Öffne: {os.path.basename(file)}")

    with fits.open(file) as hdul:
        data = hdul[0].data

    # Nur anzeigen, NICHT speichern — Daten bleiben unverändert
    data = data[::4, ::4]  # Downsampling nur für Anzeige

    # Schnelle Skalierung
    median = np.median(data)
    std = np.std(data)
    vmin = median - std
    vmax = median + std

    ax.clear()
    ax.imshow(data, cmap='gray', origin='lower', vmin=vmin, vmax=vmax)

    # Hintergrund des Plots und des Rahmens auf schwarz setzen
    fig.set_facecolor('black')  # Hintergrund schwarz
    ax.set_facecolor('black')  # Hintergrund der Achse schwarz
    ax.set_title(f"{os.path.basename(file)}\n← = zurück | → = weiter | d = löschen | q = beenden", color='white')

    # Achsen ausblenden
    ax.axis('off')

    # Rahmenfarbe auf schwarz setzen
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')

    plt.connect('key_press_event', on_key)
    plt.draw()
    plt.pause(0.1)

    if user_action == 'next':
        index += 1
    elif user_action == 'prev':
        index -= 1
    elif user_action == 'delete':
        os.remove(file)
        print(f"❌ Datei gelöscht: {file}")
        fits_files.pop(index)
        if index >= len(fits_files):  # Ende erreicht
            break
    elif user_action == 'quit':
        print("🛑 Abbruch durch Benutzer.")
        break
    else:
        index += 1  # Fallback

print("✅ Durchsicht abgeschlossen.")
