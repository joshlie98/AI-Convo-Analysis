import psycopg2
from kafka import KafkaConsumer
import json




# Funktion zum Einfügen der Daten in PostgreSQL
def _insert_data_to_postgres(data):
    conn = psycopg2.connect(
        dbname="database",
        user="postgres",
        password="admin",
        host="localhost",
        port="5431"
    )

    cur = conn.cursor()
    try: #ON CONFLICT (id) DO NOTHING
        cur.execute("""
            INSERT INTO rawdata_texts (id, text, filetype)
            VALUES (%s, %s, %s)
        """, (
            data.get('ID', 'UNKNOWN'),
            data.get('Text', ''),
            data.get('Filetype', 'UNKNOWN')
        ))
    except Exception as e:
        print(f"Fehler beim Einfügen in PostgreSQL: {e}")

    finally:
        conn.commit()
        cur.close()
        conn.close()


def consume_from_kafka(topic="text-data", bootstrap_servers="localhost:29092", group_id="text-consumer-group"):
    # Kafka Consumer
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset="earliest",  # Beginnt mit ältesten Nachrichten
        enable_auto_commit=True,  # Automatische Offset-Speicherung
        group_id=group_id,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))  # JSON-Deserialisierung
    )

    print(f"Konsumiere Nachrichten aus Topic '{topic}'...")

    for message in consumer:
        data = message.value  # JSON-Daten als Dictionary
        _insert_data_to_postgres(data)
        print(f"Erhalten: {data}")


# Kafka Consumer starten
consume_from_kafka()
