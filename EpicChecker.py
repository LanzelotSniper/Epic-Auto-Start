import datetime
import os
import json
import subprocess

# Pfad zur Konfigurationsdatei
config_file = "epic_games_config.json"

def save_config(epic_games_path, last_start):
    with open(config_file, 'w') as file:
        json.dump({"epic_games_path": epic_games_path, "last_start": last_start}, file)

def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            return config.get("epic_games_path"), config.get("last_start")
    return None, None

def get_valid_epic_games_path():
    while True:
        epic_games_path = input("Bitte den Pfad zum Epic Games Launcher eingeben: ").strip('"')
        print(f"Bereinigter Pfad: {epic_games_path}")  # Debug-Ausgabe
        if os.path.exists(epic_games_path):
            print("Pfad existiert.")  # Debug-Ausgabe
            return epic_games_path
        else:
            print("Der angegebene Pfad ist ungültig. Bitte versuchen Sie es erneut.")

def main():
    # Aktuelle Zeit und Wochentag
    now = datetime.datetime.now()
    current_weekday = now.weekday()  # 0 = Montag, 1 = Dienstag, ..., 3 = Donnerstag
    current_time = now.time()

    # Versuchen, den gespeicherten Pfad und die letzte Startzeit zu laden
    epic_games_path, last_start_str = load_config()
    
    # Wenn kein Pfad gespeichert ist oder der gespeicherte Pfad ungültig ist, den Benutzer nach dem Pfad fragen
    if not epic_games_path or not os.path.exists(epic_games_path):
        if epic_games_path:
            print("Der Pfad hat sich geändert. Bitte geben Sie den neuen Pfad ein:")
        epic_games_path = get_valid_epic_games_path()
    
    # Überprüfen, ob der Launcher gestartet werden soll
    should_start = False

    if last_start_str:
        last_start = datetime.datetime.fromisoformat(last_start_str)
        # Überprüfen, ob der letzte Start mehr als eine Woche her ist
        if (now - last_start).days > 7:
            should_start = True
    else:
        # Wenn last_start_str None ist (erster Programmstart), setze should_start auf True
        should_start = True
    
    # Überprüfen, ob heute Donnerstag ist und es nach 17 Uhr ist
    if current_weekday == 3 and current_time >= datetime.time(17, 0):
        should_start = True
    
    if should_start:
        # Versuchen, den Epic Games Launcher zu starten
        print(f"Versuche, den Epic Games Launcher zu starten: {epic_games_path}")  # Debug-Ausgabe
        try:
            subprocess.run([epic_games_path], check=True)
            print("Launcher erfolgreich gestartet.")  # Debug-Ausgabe
            # Speichern der aktuellen Startzeit nur bei erfolgreichem Start
            save_config(epic_games_path, now.isoformat())
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Starten des Epic Games Launchers: {e}")
            print("Der Pfad hat sich geändert. Bitte geben Sie den neuen Pfad ein:")
            epic_games_path = get_valid_epic_games_path()
            try:
                subprocess.run([epic_games_path], check=True)
                # Speichern der aktuellen Startzeit nur bei erfolgreichem Start
                save_config(epic_games_path, now.isoformat())
            except subprocess.CalledProcessError as e:
                print(f"Fehler beim Starten des Epic Games Launchers: {e}")
    else:
        print("Kein Start notwendig.")  # Ausgabe, wenn should_start False ist

if __name__ == "__main__":
    main()
