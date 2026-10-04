"""
Turns a natural-language question into a validated, read-only MySQL query
using Google Gemini (google-genai SDK).

Safety: the model is instructed to only ever produce a SELECT statement,
and the output is additionally checked in code before it is ever handed
to the database layer. Nothing generated here is allowed to write,
alter, or drop data.
"""
import re

from google import genai
from google.genai import types

from config import GOOGLE_API_KEY, GEMINI_MODEL

# Keywords that should never appear in a generated query. Word-boundary
# matching is used for alphabetic keywords so this doesn't false-positive
# on things like "OFFSET" or "RESET".
FORBIDDEN_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE",
    "REPLACE", "GRANT", "REVOKE", "EXEC", "EXECUTE", "CALL", "MERGE",
    "LOCK", "UNLOCK", "RENAME", "SET",
]

SYSTEM_PROMPT_TEMPLATE = """You are an expert MySQL query generator for an e-commerce analytics database.

Database schema:
{schema}

Rules you MUST follow:
1. Generate exactly one MySQL SELECT statement. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or any other write/DDL statement.
2. Only use tables and columns that appear in the schema above. Never invent a column or table.
3. Return ONLY the raw SQL query as plain text. No markdown code fences, no explanation, no trailing semicolon.
4. Use JOINs when the question needs data from more than one table, following the relationships described in the schema.
5. Use SUM, COUNT, AVG, MAX, or MIN with GROUP BY when the question asks for totals, counts, averages, or a breakdown.
6. When the question asks for "top N", "best", or "most", add ORDER BY on the relevant metric and a LIMIT clause.
7. Give computed columns a clear alias, e.g. SUM(subtotal) AS total_revenue.
8. Dates are stored as DATE columns; use MySQL date functions (YEAR(), MONTH(), DATE_FORMAT(), etc.) where relevant.
"""


class GeminiSQLGenerator:
    def __init__(self, schema_description: str):
        if not GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY is not set. Add it to your .env file "
                "(get a key at https://aistudio.google.com/app/apikey)."
            )
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.schema_description = schema_description
        self.model = GEMINI_MODEL

    def generate_sql(self, question: str) -> str:
        prompt = self._build_prompt(question)
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=400,
            ),
        )
        sql = self._clean_sql(response.text or "")
        self._validate_sql(sql)
        return sql

    def _build_prompt(self, question: str) -> str:
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(schema=self.schema_description)
        return f"{system_prompt}\nQuestion: {question}\nSQL:"

    @staticmethod
    def _clean_sql(raw: str) -> str:
        sql = raw.strip()
        # Strip markdown fences in case the model adds them anyway.
        sql = re.sub(r"^```(sql)?", "", sql, flags=re.IGNORECASE).strip()
        sql = re.sub(r"```$", "", sql).strip()
        return sql.rstrip(";").strip()

    @staticmethod
    def _validate_sql(sql: str) -> None:
        if not sql:
            raise ValueError("Gemini returned an empty query.")

        if not re.match(r"^\s*(SELECT|WITH)\b", sql, flags=re.IGNORECASE):
            raise ValueError(
                "Only SELECT queries are allowed. The generated query was rejected."
            )

        if ";" in sql:
            raise ValueError("Multiple statements are not allowed.")

        upper_sql = sql.upper()
        for keyword in FORBIDDEN_KEYWORDS:
            if re.search(r"\b" + re.escape(keyword) + r"\b", upper_sql):
                raise ValueError(
                    f"Generated query contains a forbidden keyword ('{keyword}') "
                    "and was rejected for safety."
                )
