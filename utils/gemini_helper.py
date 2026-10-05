"""
Turns a natural-language question into a validated, read-only MySQL query
using Google Gemini (google-genai SDK).

Safety:
- The model is instructed to generate only SELECT/WITH queries.
- Generated SQL is validated before being sent to the database.
- Write/DDL operations are rejected.
- Temporary Gemini 503 errors are retried automatically.
"""

import re
import time

from google import genai
from google.genai import types

from config import GOOGLE_API_KEY, GEMINI_MODEL


# -------------------------------------------------------------------
# Forbidden SQL keywords
# -------------------------------------------------------------------

FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE",
    "GRANT",
    "REVOKE",
    "EXEC",
    "EXECUTE",
    "CALL",
    "MERGE",
    "LOCK",
    "UNLOCK",
    "RENAME",
    "SET",
]


# -------------------------------------------------------------------
# Gemini prompt
# -------------------------------------------------------------------

SYSTEM_PROMPT_TEMPLATE = """
You are an expert MySQL query generator for an e-commerce analytics database.

Your ONLY task is to convert the user's natural-language question into ONE
COMPLETE, VALID, EXECUTABLE MySQL SELECT query.

DATABASE SCHEMA:
{schema}

STRICT RULES:

1. Return exactly ONE complete MySQL SELECT statement.

2. The SQL MUST be executable directly in MySQL.
   Never return a partial query.

3. Only use tables and columns that actually exist in the database schema
   provided above.

4. NEVER invent a table name or column name.

5. If you use a table alias, you MUST define that alias in the FROM or JOIN
   clause before using it.

   Correct example:
   SELECT p.product_name
   FROM products AS p

   Incorrect example:
   SELECT p.product_name

6. NEVER use an undefined table alias.

7. Pay close attention to the exact column names in the schema.
   For example, if the schema contains:

       products.product_name

   then use:

       p.product_name

   when the table is aliased as p.

   NEVER change it to:

       p.product

8. When information is required from multiple tables, use JOINs based on
   the relationships in the schema.

9. For product sales or revenue questions, use the appropriate relationship
   between products and order_items.

10. When the question asks for revenue, use the appropriate numeric revenue
    field from the schema. Do not invent a revenue column.

11. When the question asks for "top N", "best", "highest", "most", or similar:
    - calculate the relevant metric
    - GROUP BY the relevant entity
    - ORDER BY the metric DESC
    - use LIMIT N

12. Use aggregate functions such as:
    SUM()
    COUNT()
    AVG()
    MAX()
    MIN()

    whenever required by the question.

13. If an aggregate function is used together with non-aggregated columns,
    use an appropriate GROUP BY clause.

14. Give calculated columns clear aliases.

    Example:
    SUM(oi.subtotal) AS total_revenue

15. Dates are stored as DATE values.
    Use MySQL date functions such as YEAR(), MONTH(), DATE_FORMAT(), etc.
    when appropriate.

16. If the question requires data from more than one table, make sure every
    required JOIN condition is present.

17. Never generate:
    INSERT
    UPDATE
    DELETE
    DROP
    ALTER
    CREATE
    TRUNCATE
    REPLACE
    GRANT
    REVOKE
    EXEC
    EXECUTE
    CALL
    MERGE
    LOCK
    UNLOCK
    RENAME
    SET

18. Return ONLY the SQL query.

19. Do NOT return:
    - markdown
    - ```sql
    - explanations
    - comments
    - natural-language text
    - multiple queries
    - a trailing semicolon

20. Before returning the query, internally verify:
    - every table exists
    - every column exists
    - every alias is defined
    - all JOINs are valid
    - GROUP BY is correct
    - ORDER BY is correct
    - LIMIT is correct when required
    - the query is complete
    - the query can be executed directly in MySQL
"""


# -------------------------------------------------------------------
# Gemini SQL Generator
# -------------------------------------------------------------------

class GeminiSQLGenerator:

    def __init__(self, schema_description: str):

        if not GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY is not set. "
                "Add it to your .env file."
            )

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

        self.schema_description = schema_description

        self.model = GEMINI_MODEL

    # ----------------------------------------------------------------
    # Generate SQL
    # ----------------------------------------------------------------

    def generate_sql(self, question: str) -> str:

        prompt = self._build_prompt(question)

        response = None

        # Retry temporary Gemini 503 errors.
        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.1,
                        max_output_tokens=500,
                    ),
                )

                # Gemini request succeeded.
                break

            except Exception as e:

                error_message = str(e)

                # Retry temporary server overload.
                if "503" in error_message and attempt < 2:

                    wait_time = 2 ** attempt

                    time.sleep(wait_time)

                else:

                    raise

        # Safety check in case no response was received.
        if response is None:

            raise RuntimeError(
                "Gemini did not return a response."
            )

        # Extract generated text.
        sql = self._clean_sql(
            response.text or ""
        )

        # Validate generated SQL before database execution.
        self._validate_sql(sql)

        return sql

    # ----------------------------------------------------------------
    # Build Gemini prompt
    # ----------------------------------------------------------------

    def _build_prompt(self, question: str) -> str:

        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            schema=self.schema_description
        )

        return (
            f"{system_prompt}\n"
            f"USER QUESTION:\n"
            f"{question}\n\n"
            f"SQL:"
        )

    # ----------------------------------------------------------------
    # Clean Gemini output
    # ----------------------------------------------------------------

    @staticmethod
    def _clean_sql(raw: str) -> str:

        sql = raw.strip()

        # Remove opening markdown code fence.
        sql = re.sub(
            r"^```(?:sql)?",
            "",
            sql,
            flags=re.IGNORECASE
        ).strip()

        # Remove closing markdown code fence.
        sql = re.sub(
            r"```$",
            "",
            sql
        ).strip()

        # Remove trailing semicolon.
        sql = sql.rstrip(";").strip()

        return sql

    # ----------------------------------------------------------------
    # Validate generated SQL
    # ----------------------------------------------------------------

    @staticmethod
    def _validate_sql(sql: str) -> None:

        # Empty response.
        if not sql:

            raise ValueError(
                "Gemini returned an empty query."
            )

        # Only SELECT or WITH queries are allowed.
        if not re.match(
            r"^\s*(SELECT|WITH)\b",
            sql,
            flags=re.IGNORECASE
        ):

            raise ValueError(
                "Only SELECT queries are allowed. "
                "The generated query was rejected."
            )

        # Prevent multiple SQL statements.
        if ";" in sql:

            raise ValueError(
                "Multiple SQL statements are not allowed."
            )

        upper_sql = sql.upper()

        # Check forbidden keywords.
        for keyword in FORBIDDEN_KEYWORDS:

            if re.search(
                r"\b" + re.escape(keyword) + r"\b",
                upper_sql
            ):

                raise ValueError(
                    f"Generated query contains a forbidden keyword "
                    f"('{keyword}') and was rejected for safety."
                )

        # Basic protection against an obviously incomplete query.
        if sql.upper().startswith("SELECT"):

            if not re.search(
                r"\bFROM\b",
                sql,
                flags=re.IGNORECASE
            ):

                raise ValueError(
                    "Generated SELECT query does not contain a FROM clause."
                )