import psycopg2

conn = psycopg2.connect(
    dbname="database",
    user="postgres",
    password="admin",
    host="localhost",
    port="5431"
)

cur = conn.cursor()

query1 = """
    CREATE TABLE rawdata_conversations (
    id_convo TEXT NOT NULL,
    id_line TEXT NOT NULL,
    text TEXT NOT NULL,
    speaker TEXT NOT NULL,
    
    convo_iteration INT NOT NULL
    );
    """
query2 = 'drop table conversations;'
query3 = """
  CREATE TABLE sentiment_convo (
    id_convo TEXT NOT NULL Primary Key,
    convo_sentiment_score FLOAT NOT NULL, 
    convo_sentiment_category TEXT NOT NULL
    );
    """
query4 = """
    CREATE TABLE sentiment_data (
    id_line TEXT NOT NULL,
    sentiment_score FLOAT,
    sentiment_category TEXT NOT NULL
     );
    """
cur.execute(query3)
conn.commit()
cur.close()
conn.close()
