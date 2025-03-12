from kafka import KafkaProducer
import json
import time
import pandas as pd
from pathlib import Path


# Funktion zum Einlesen einer TXT-Datei in einen Pandas DataFrame
def read_txt_to_dataframe(file_path):
    file_name = Path(file_path).stem  # Datei-Name ohne Endung als ID
    file_type = Path(file_path).suffix  # Dateityp (Erweiterung, z. B. .txt)

    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()  # Entfernt unnötige Leerzeichen/Zeilenumbrüche
            if line:  # Leere Zeilen ignorieren
                data.append([file_name, line, file_type])

    df = pd.DataFrame(data, columns=["ID", "Text", "Filetype"])
    return df


# Funktion zum Senden von DataFrame-Daten an ein Kafka-Topic
def send_to_kafka(df, topic="text-data", bootstrap_servers="localhost:29092"):
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")  # JSON-Serialisierung
    )

    for _, row in df.iterrows():
        message = {
            "ID": row["ID"],
            "Text": row["Text"],
            "Filetype": row["Filetype"]
        }
        producer.send(topic, value=message)
        print(f"Gesendet: {message}")
        time.sleep(0.1)  # Verhindert Überlastung von Kafka

    producer.flush()  # Sicherstellen, dass alle Nachrichten gesendet wurden
    producer.close()


# Datei einlesen
file_path = "Textfiles/test.txt"
df = read_txt_to_dataframe(file_path)

# Daten an Kafka senden
send_to_kafka(df)
