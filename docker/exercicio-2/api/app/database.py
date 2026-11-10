import os
import psycopg
from psycopg.rows import dict_row


def connect():
    return psycopg.connect(
        host=os.environ["DB_HOST"], port=os.environ["DB_PORT"],
        user=os.environ["DB_USER"], password=os.environ["DB_PASS"],
        dbname=os.environ["DB_NAME"], connect_timeout=3,
        options="-c statement_timeout=5000", row_factory=dict_row,
    )


def initialize():
    with connect() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tarefas (id SERIAL PRIMARY KEY, titulo VARCHAR(200) NOT NULL)")
