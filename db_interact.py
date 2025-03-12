import psycopg2

conn = psycopg2.connect(
    dbname="database",
    user="postgres",
    password="admin",
    host="localhost",
    port="5431"
)

cur = conn.cursor()

query = """
    CREATE TABLE rawdata_texts (
    id TEXT NOT NULL,
    text TEXT NOT NULL,
    filetype TEXT NOT NULL
     );
    """
query2 = 'drop table rawdata_texts;'
query3= """ 
drop table rawdata_texts;
 CREATE TABLE rawdata_texts (
    id TEXT NOT NULL,
    text TEXT NOT NULL,
    filetype TEXT NOT NULL
     );

"""
query4 = """
    CREATE TABLE sentiment_data (
    id TEXT NOT NULL,
    text TEXT NOT NULL,
    filetype TEXT NOT NULL,
    sentiment_score FLOAT,
    sentiment_category TEXT NOT NULL
     );
    """
cur.execute(query4)
conn.commit()
cur.close()
conn.close()