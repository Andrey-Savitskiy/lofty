from typing import Union
import psycopg2
from psycopg2.extras import DictCursor
from config import DB_NAME, DB_USER, DB_PASS, DB_HOST


def get_channel_id(cursor: DictCursor, channel_name: str) -> Union[None, list]:
    cursor.execute(f"SELECT id FROM channel WHERE name='{channel_name}';")
    return cursor.fetchone()


def set_connection_to_db():
    connect = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    connect.autocommit = True
    cursor = connect.cursor(cursor_factory=DictCursor)
    return connect, cursor


def create_db():
    connect, cursor = set_connection_to_db()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS channel (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE
    );
    CREATE TABLE IF NOT EXISTS video (
        video_id TEXT PRIMARY KEY,
        channel_id INT,
        video_href TEXT,
        FOREIGN KEY (channel_id) REFERENCES channel (id)
    );
    """)
    connect.close()


if __name__ == '__main__':
    create_db()
