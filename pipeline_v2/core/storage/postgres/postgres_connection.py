# pipeline_v2/core/storage/postgres/postgres_connection.py

import psycopg2


class PostgresConnection:

    def __init__(
        self,
        host,
        port,
        database,
        user,
        password,
    ):

        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
