import psycopg2
from config import *

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS game_sessions (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER NOT NULL,
        level_reached INTEGER NOT NULL,
        played_at TIMESTAMP DEFAULT NOW()
    );
    """)

    conn.commit()
    conn.close()

def get_or_create_player(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    row = cur.fetchone()

    if row:
        player_id = row[0]
    else:
        cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
        player_id = cur.fetchone()[0]
        conn.commit()

    conn.close()
    return player_id

def save_game(player_id, score, level):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """, (player_id, score, level))

    conn.commit()
    conn.close()

def get_leaderboard():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        ORDER BY g.score DESC
        LIMIT 10
    """)

    data = cur.fetchall()
    conn.close()
    return data