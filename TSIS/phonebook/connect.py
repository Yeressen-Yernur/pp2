import psycopg2
from config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def initialize_db():
    conn = get_connection()
    cur = conn.cursor()

    # schema
    with open("schema.sql", "r", encoding="utf-8") as f:
        sql = f.read().strip()
        if sql:
            cur.execute(sql)

    # procedures
    with open("procedures.sql", "r", encoding="utf-8") as f:
        sql = f.read().strip()
        if sql:
            cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()