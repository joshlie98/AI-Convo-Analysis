ReadMe - Deutsch:

# Phi2 + PostgreSQL: KI-Konversationen und Sentiment-Analyse mit NLTK

## Projektüberblick

Dieses Projekt kombiniert:

- Phi2, ein leichtgewichtiges KI-Sprachmodell -> bereitgestellt über Ollama
- PostgreSQL zur strukturierten Speicherung von Konversationsdaten
- NLTK zur Sentiment-Analyse
- Docker für eine reproduzierbare Umgebung

Ziel ist es, KI-generierte Konversationen zu analysieren und daraus datenbasierte Erkenntnisse zu gewinnen.

---

## Funktionsweise

### 1. KI-generierte Konversationen

Da Phi2 kein eigenes Konversationsgedächtnis besitzt, wird jede Unterhaltung durch einen emotional geladenen Convo-Starter (positiv, neutral, negativ) initiiert. Diese Starter wurden mit ChatGPT generiert.

Ablauf:

- Phi2 erhält einen Starter-Prompt
- Die KI antwortet
- Ihre eigene Antwort wird als nächster Input verwendet
- So entsteht eine vollständige, turnbasierte Konversation

Die resultierende Unterhaltung wird in der PostgreSQL-Tabelle `conversations` gespeichert. Erfasst werden u. a.:

- `id_convo` - generiert mit UUID
- `id_line`- generiert mit UUID + Iterationsidentifikation
- `speaker` - die Output KI-Instanz
- `text` - Output der KI
- `convo_iteration` - Iteration der Unterhaltung, Konversationsstarter haben die Iteration -1

---

### 2. Sentiment-Analyse mit Python und NLTK

Ein separates Python-Skript übernimmt die emotionale Analyse:

- Zeilenweise Sentiment-Berechnung mit dem VADER-Modul aus NLTK
- Klassifikation in Positive, Neutral oder Negative
- Aggregation des Sentiments auf Konversationsebene
- Speicherung der Ergebnisse in zwei Tabellen:
  - `sentiment_data`: Einzelsätze
  - `sentiment_convo`: Durchschnittliches Konversations-Sentiment

---

### 3. Geplante Datenanalyse

Geplant ist ein ausführlicher Data-Storytelling-Teil mit:

- Vergleich unterschiedlicher Convo-Starter und deren Einfluss auf den Gesprächsverlauf
- Visualisierung des Stimmungsverlaufs über Konversations-Turns
- Clustering ähnlicher Gesprächsverläufe
- Identifikation besonders auffälliger oder emotionaler Konversationen

---

## Docker

Das Projekt ist vollständig über Docker containerisiert.

Architektur:

- PostgreSQL als Datenbank-Service
- Phi2-Modell als CLI-Anwendung


---

## Status

Die Konversationsgenerierung und Sentimentanalyse sind implementiert.  
Die explorative Datenanalyse und Visualisierung sind abgeschlossen - Übersetzung auf Englisch erfolgt noch


---



ReadMe - English:

# Phi2 + PostgreSQL: AI Conversations and Sentiment Analysis with NLTK

## Project Overview

This project combines:

- **Phi2**, a lightweight language model -> deployed via Ollama
- **PostgreSQL** for structured storage of conversation data
- **NLTK** for sentiment analysis
- **Docker** for a fully reproducible environment

The goal is to generate AI-driven conversations, analyze their emotional sentiment, and extract insights from the data.

---

## How It Works

### 1. AI-Generated Conversations

Since Phi2 has no built-in conversation memory, each dialogue is initiated using an **emotionally loaded conversation starter** (positive, neutral, or negative).  
These prompts were generated with ChatGPT.

Process:

- Phi2 receives an initial starter prompt
- It generates a response
- That response is used as the next input
- This loop creates a full, turn-based conversation

The resulting conversation is stored in the PostgreSQL table `conversations`, with the following structure:

- `id_convo`: unique conversation ID
- `id_line`: unique line ID
- `speaker`: the AI instance producing the output
- `text`: the generated response
- `convo_iteration`: the step in the conversation (starter prompts have iteration `-1`)

---

### 2. Sentiment Analysis with Python and NLTK

A separate Python script handles the sentiment analysis:

- Uses NLTK's **VADER** module to analyze each line of text
- Classifies each line as **Positive**, **Neutral**, or **Negative**
- Calculates average sentiment per conversation
- Results are saved in two tables:
  - `sentiment_data`: individual line sentiment
  - `sentiment_convo`: aggregated conversation sentiment

---

### 3. Planned Data Analysis

A full **data storytelling and exploration** phase is planned, including:

- Comparison of conversation starters and their emotional influence
- Sentiment evolution across conversation turns
- Clustering of similar conversational patterns
- Identification of particularly emotional or unexpected dialogues

---

## Docker

The entire environment runs via Docker.

Architecture:

- PostgreSQL as the database service
- Phi2 as a CLI-based AI generation tool

---

## Status

Conversation generation and sentiment analysis are fully implemented.  
Exploratory data analysis and visualization are finished - translation to english is in progress


