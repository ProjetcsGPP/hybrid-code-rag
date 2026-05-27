# pipeline_v2/core/storage/postgres/postgres_repository.py

from psycopg2.extras import Json


class PostgresRepository:

    def __init__(self, connection):
        self.connection = connection

    def execute(self, sql, params=None):

        cursor = self.connection.cursor()

        try:

            if params:
                params = self._normalize_json(params)

            cursor.execute(sql, params)

            self.connection.commit()

        except Exception as e:
            print("POSTGRES ERROR:", e)
            self.connection.rollback()
            raise

        finally:
            cursor.close()

    def fetch_all(self, sql, params=None):

        cursor = self.connection.cursor()

        try:

            cursor.execute(sql, params)

            return cursor.fetchall()

        finally:
            cursor.close()

    def fetch_one(self, sql, params=None):

        cursor = self.connection.cursor()

        try:

            cursor.execute(sql, params)

            return cursor.fetchone()

        finally:
            cursor.close()

    def _normalize_json(self, params):

        if isinstance(params, dict):

            normalized = {}

            for k, v in params.items():

                if isinstance(v, dict):
                    normalized[k] = Json(v)
                else:
                    normalized[k] = v

            return normalized

        return params
