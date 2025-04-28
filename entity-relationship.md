# Deutsch / English

# Die Datenbankstruktur für dieses Projekt

Dieses Projekt verwendet eine PostgreSQL-Datenbank mit drei zentralen Tabellen: `conversation`, `sentiment_data` und `sentiment_convo`.  
Die Tabellen sind miteinander über Primär- und Fremdschlüsselbeziehungen verbunden.

---

## Tabellenübersicht

### 🗂 conversation

| Spalte           | Typ      | Beschreibung |
|:-----------------|:---------|:-------------|
| id_line           | text     | Primärschlüssel (PK), eindeutige ID der Zeile |
| id_convo          | text     | Fremdschlüssel zur Konversation (`sentiment_convo.id_convo`) |
| convo_iteration   | integer  | Iterationsnummer innerhalb der Konversation (Starter = -1) |
| speaker           | text     | Sprecher der Zeile (KI-Instanz) |
| text              | text     | Inhalt der Antwort |

---

### 🗂 sentiment_convo

| Spalte                  | Typ                | Beschreibung |
|:-------------------------|:-------------------|:-------------|
| id_convo                 | text                | Primärschlüssel (PK), ID der Konversation |
| convo_sentiment_score    | double precision    | Aggregierter Sentiment-Score der Konversation |
| convo_sentiment_category | text                | Aggregierte Sentiment-Kategorie (Positive / Neutral / Negative) |

---

### 🗂 sentiment_data

| Spalte            | Typ                | Beschreibung |
|:------------------|:-------------------|:-------------|
| id_line           | text                | Primärschlüssel (PK), Fremdschlüssel zu `conversation.id_line` |
| sentiment_score   | double precision    | Sentiment-Score für die einzelne Zeile |
| sentiment_category| text                | Klassifizierung des Satzes (Positive / Neutral / Negative) |

---

## Beziehungen (Relations)

- `conversation.id_convo` ➔ referenziert ➔ `sentiment_convo.id_convo`
- `conversation.id_line` ➔ referenziert ➔ `sentiment_data.id_line`

---

## Visualisierte Struktur

```text
+-----------------+           +----------------------+
| conversation    |           | sentiment_convo       |
|-----------------|           |----------------------|
| id_line (PK)    |           | id_convo (PK)         |
| id_convo (FK)   |<--------->|                      |
| convo_iteration |           | convo_sentiment_score|
| speaker         |           | convo_sentiment_category |
| text            |           |                      |
+-----------------+           +----------------------+

           |
           |
           v
+-----------------+
| sentiment_data  |
|-----------------|
| id_line (PK, FK)|
| sentiment_score |
| sentiment_category |
+-----------------+






# The Database Structure

This project uses a PostgreSQL database with three main tables: `conversation`, `sentiment_data`, and `sentiment_convo`.  
The tables are connected via primary and foreign key relationships.

---

## Table Overview

### 🗂 conversation

| Column            | Type      | Description |
|:------------------|:----------|:------------|
| id_line           | text      | Primary key (PK), unique ID for each line |
| id_convo          | text      | Foreign key referencing `sentiment_convo.id_convo` |
| convo_iteration   | integer   | Iteration number within the conversation (Starter = -1) |
| speaker           | text      | Speaker of the line (AI instance) |
| text              | text      | Text content of the response |

---

### 🗂 sentiment_convo

| Column                   | Type               | Description |
|:--------------------------|:-------------------|:------------|
| id_convo                  | text               | Primary key (PK), ID of the conversation |
| convo_sentiment_score     | double precision   | Aggregated sentiment score of the conversation |
| convo_sentiment_category  | text               | Aggregated sentiment classification (Positive / Neutral / Negative) |

---

### 🗂 sentiment_data

| Column            | Type                | Description |
|:------------------|:--------------------|:------------|
| id_line           | text                 | Primary key (PK), foreign key to `conversation.id_line` |
| sentiment_score   | double precision     | Sentiment score for the individual line |
| sentiment_category| text                 | Sentiment classification (Positive / Neutral / Negative) |

---

## Relationships

- `conversation.id_convo` ➔ references ➔ `sentiment_convo.id_convo`
- `conversation.id_line` ➔ references ➔ `sentiment_data.id_line`

---

## Visual Schema

```text
+-----------------+           +----------------------+
| conversation    |           | sentiment_convo       |
|-----------------|           |----------------------|
| id_line (PK)    |           | id_convo (PK)         |
| id_convo (FK)   |<--------->|                      |
| convo_iteration |           | convo_sentiment_score|
| speaker         |           | convo_sentiment_category |
| text            |           |                      |
+-----------------+           +----------------------+

           |
           |
           v
+-----------------+
| sentiment_data  |
|-----------------|
| id_line (PK, FK)|
| sentiment_score |
| sentiment_category |
+-----------------+




