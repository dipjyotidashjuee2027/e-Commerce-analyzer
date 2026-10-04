"""
Thin wrapper around mysql-connector-python.

Responsible for:
- opening/closing connections
- running read-only queries and returning a pandas DataFrame
- introspecting the live schema so the Gemini prompt always reflects
  the real database rather than a hand-written description that can
  drift out of date
"""
import mysql.connector
from mysql.connector import Error
import pandas as pd

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
from utils.schema_context import STATIC_SCHEMA_DESCRIPTION


class DatabaseHelper:
    def __init__(self):
        self.host = DB_HOST
        self.port = DB_PORT
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.database = DB_NAME

    def get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )

    def test_connection(self):
        """Returns (ok: bool, message: str)."""
        try:
            conn = self.get_connection()
            conn.close()
            return True, "Connected."
        except Error as e:
            return False, str(e)

    def run_query(self, sql: str) -> pd.DataFrame:
        """Executes a SELECT query and returns the results as a DataFrame.
        Caller is responsible for validating that `sql` is a safe,
        read-only statement (see utils.gemini_helper._validate_sql)."""
        conn = self.get_connection()
        try:
            return pd.read_sql(sql, conn)
        finally:
            if conn.is_connected():
                conn.close()

    def get_schema_summary(self) -> str:
        """Builds a text description of every table/column in the live
        database. Falls back to the static description in
        utils.schema_context if the DB can't be reached."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]

            lines = []
            for table in tables:
                cursor.execute(f"DESCRIBE `{table}`")
                columns = cursor.fetchall()
                col_desc = ", ".join(f"{col[0]} ({col[1]})" for col in columns)
                lines.append(f"Table `{table}`: {col_desc}")

            cursor.close()
            conn.close()
            return "\n".join(lines) if lines else STATIC_SCHEMA_DESCRIPTION
        except Error:
            return STATIC_SCHEMA_DESCRIPTION
