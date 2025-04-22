import psycopg2
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


#nltk.download('vader_lexicon')


# Connect to PostgreSQL database and fetch data
def read_data_from_postgres():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="admin",
        host="localhost",
        port="5431"
    )
    cur = conn.cursor()
    insert_query = "SELECT * FROM data;"
    cur.execute(insert_query)

    # Fetch data
    data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()

    # Convert to DataFrame
    pd.set_option('display.max_columns', None)
    df = pd.DataFrame(data, columns=col_names)
    return df



# Sentiment analysis function
def get_vader_sentiment(text, sia):
    return sia.polarity_scores(text)['compound']

def interpret_sentiment(compound_score):
    if compound_score >= 0.05:
        return 'Positive'
    elif -0.05 < compound_score < 0.05:
        return 'Neutral'
    else:
        return 'Negative'

def get_convo_sentiment_summary(df):
    # Group by conversation ID and calculate the average compound score
    convo_scores = df.groupby('id_convo')['sentiment_score'].mean()

    # Convert to dict {id_convo: sentiment_scores}
    return convo_scores.to_dict()

def send_sentiment_back_to_postgres(df):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="admin",
        host="localhost",
        port="5431"
    )
    cur = conn.cursor()
    try:
        for index, row in df.iterrows():
            cur.execute("""
                INSERT INTO sentiment_data (id_line, id_convo, convo_iteration, text, sentiment_score, sentiment_category)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (text) DO UPDATE SET
                    text = EXCLUDED.text,
                    id_line = EXCLUDED.id_line,
                    id_convo = EXCLUDED.id_convo,
                    convo_iteration = EXCLUDED.convo_iteration,
                    sentiment_score = EXCLUDED.sentiment_score,
                    sentiment_category = EXCLUDED.sentiment_category
            """, (
                row['id_line'],
                row['id_convo'],
                row['convo_iteration'],
                row['text'],
                row['sentiment_score'],
                row['sentiment_category']
            ))
        # Insert conversation sentiment summary

        convo_sentiment_df = df[['id_convo', 'convo_sentiment_score', 'convo_sentiment_category']].drop_duplicates()
        for index, row in convo_sentiment_df.iterrows():
            cur.execute("""
                     INSERT INTO sentiment_convo (id_convo, convo_sentiment_score, convo_sentiment_category)
                     VALUES (%s, %s, %s)
                     ON CONFLICT (id_convo) DO UPDATE SET
                         convo_sentiment_score = EXCLUDED.convo_sentiment_score,
                         convo_sentiment_category = EXCLUDED.convo_sentiment_category
                 """, (
                row['id_convo'],
                row['convo_sentiment_score'],
                row['convo_sentiment_category']
            ))
        conn.commit()  # Commit the transaction
    except Exception as e:
        print(f"Error inserting into PostgreSQL: {e}")
    finally:
        cur.close()
        conn.close()

# Initialize SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Read data from PostgreSQL
data = read_data_from_postgres()

# Apply sentiment analysis to each line
data['sentiment_score'] = data['text'].apply(lambda comment: get_vader_sentiment(comment, sia))
data['sentiment_category'] = data['sentiment_score'].apply(interpret_sentiment)

# Get the summary as a dictionary
convo_scores = get_convo_sentiment_summary(data)

# Map scores back to each row based on id_convo
data['convo_sentiment_score'] = data['id_convo'].map(convo_scores)
data['convo_sentiment_category'] = data['convo_sentiment_score'].apply(interpret_sentiment)
print(data)
send_sentiment_back_to_postgres(data) #send back to postgres


#print(data)