# pipeline/structure/storage/postgres_connection.py

import psycopg2
from psycopg2.extras import RealDictCursor


class PostgresConnection:

    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
    ):

        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            cursor_factory=RealDictCursor,
        )

        self.conn.autocommit = True

    def cursor(self):
        return self.conn.cursor()
