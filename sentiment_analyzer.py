import psycopg2
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer # Nicht intelligent genug


#nltk.download('vader_lexicon')

filename = "test"
# Connect to PostgreSQL database and fetch data
def read_data_from_postgres():
    conn = psycopg2.connect(
        dbname="database",
        user="postgres",
        password="admin",
        host="localhost",
        port="5431"
    )
    cur = conn.cursor()
    insert_query = "SELECT * FROM rawdata_texts WHERE id = %s;"
    cur.execute(insert_query, (filename,))

    # Fetch data
    data = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()

    # Convert to DataFrame
    pd.set_option('display.max_columns', None)
    df = pd.DataFrame(data, columns=col_names)
    return df


# Word count function
def count_words(df):
    word_count = {}
    for comment in df['text']:
        for word in comment.split():  #Tokenize
            word_count[word] = word_count.get(word, 0) + 1
    return pd.DataFrame(list(word_count.items()), columns=['word', 'count']).sort_values(by='count', ascending=False)


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

def send_back_to_postgres(df):
    conn = psycopg2.connect(
        dbname="database",
        user="postgres",
        password="admin",
        host="localhost",
        port="5431"
    )
    cur = conn.cursor()
    try:
        for index, row in df.iterrows():
            cur.execute("""
                INSERT INTO sentiment_data (id, text, filetype, sentiment_score, sentiment_category)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (text) DO UPDATE SET
                    text = EXCLUDED.text,
                    filetype = EXCLUDED.filetype,
                    sentiment_score = EXCLUDED.sentiment_score,
                    sentiment_category = EXCLUDED.sentiment_category
            """, (
                row['id'],
                row['text'],
                row['filetype'],
                row['sentiment_score'],
                row['sentiment_category']
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
send_back_to_postgres(data) #send back to postgres

print(data)