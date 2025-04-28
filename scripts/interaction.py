import requests
import time
import psycopg2
import pandas as pd
import uuid


PHI_URL = "http://localhost:11000/api/generate"

# Verbindung zu PostgreSQL herstellen
try:
    conn = psycopg2.connect(
        dbname="database",
        user="postgres",
        password="admin",
        host="localhost",
        port="5431"
    )
    cursor = conn.cursor()
    print("Verbindung zur Datenbank erfolgreich!")
except psycopg2.Error as e:
    print(f" Fehler bei der Datenbankverbindung: {e}")
    exit(1)

# Funktion zur Kommunikation mit Phi (API)
def chat_with_phi(url, prompt, retries=3):
    """Sendet eine Nachricht an Phi und gibt die Antwort zurück"""
    for attempt in range(retries):
        try:
            response = requests.post(url, json={
                "model": "phi",
                "prompt": prompt,
                "stream": False
            }, timeout=60)  #  Timeout auf 60s

            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                print(f"API-Fehler {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f" Netzwerkfehler: {e}")

        print(f"Neuer Versuch ({attempt+1}/{retries})...")
        time.sleep(20)  # Wartezeit vor erneutem Versuch

    print(" Alle Versuche fehlgeschlagen!")
    return None



with open("convo_starters.txt", mode="r", encoding="utf-8") as file:
    for starter_message in file:
        print(starter_message) # troubleshooting
        message = starter_message
        id_convo = str(uuid.uuid4())[:8] + "_convo"

        conversation_data = [{
            "id_line": str(uuid.uuid4())[:8] + "_x0",
            "id_convo": id_convo,
            "convo_iteration": -1,
            "speaker": "Convo starter",
            "text": message
        }]

        # 5 Durchläufe der Konversation
        for i in range(5):
            print(f"\nDurchlauf {i + 1}...")

            # Phi 1 antwortet
            phi_1_response = chat_with_phi(PHI_URL, message)
            if not phi_1_response:
                print("Phi 1 hat nicht geantwortet. Abbruch.")
                break
            conversation_data.append({
                "id_line": str(uuid.uuid4())[:8] + "_" + str(i),
                "id_convo": id_convo,
                "convo_iteration": i + 1,
                "speaker": "Phi instance one",
                "text": phi_1_response
            })

            time.sleep(20)  # Wartezeit um Timeout zu vermeiden

            # Phi 2 antwortet
            phi_2_response = chat_with_phi(PHI_URL, phi_1_response)
            if not phi_2_response:
                print("Phi 2 hat nicht geantwortet. Abbruch.")
                break
            conversation_data.append({
                "id_line": str(uuid.uuid4())[:8] + "_x" + str(i),
                "id_convo": id_convo,
                "convo_iteration": i + 1,
                "speaker": "Phi instance two",
                "text": phi_2_response
            })

            time.sleep(20)

            # Die Antwort von Phi_2 wird die neue Nachricht für Phi_1
            message = phi_2_response

        print("\n Konversation abgeschlossen.")

        # Daten in DataFrame speichern
        df = pd.DataFrame(conversation_data)
        print(df)

        # Datenbank-Tabelle erstellen (falls nicht vorhanden)
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation (
                    id_line TEXT PRIMARY KEY,
                    id_convo TEXT,
                    convo_iteration INT,
                    speaker TEXT,
                    text TEXT
                )
            """)
            conn.commit()

            # Daten in die Datenbank speichern
            for row in conversation_data:
                cursor.execute("""
                    INSERT INTO conversation (id_line, id_convo, convo_iteration, speaker, text)
                    VALUES (%s, %s, %s, %s, %s)
                """, (row["id_line"], row["id_convo"], row["convo_iteration"], row["speaker"], row["text"]))

            conn.commit()
            print("Daten erfolgreich in PostgreSQL gespeichert!")

        except psycopg2.Error as e:
            print(f"Fehler beim Speichern in die DB: {e}")

#Phi API-URL

# Konversation starten
#starter_message = "Tell me a story about success"

#Verbindung schließen
if cursor:
    cursor.close()
if conn:
    conn.close()
print("Verbindung zur DB geschlossen.")
