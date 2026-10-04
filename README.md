# 🛒 E-Commerce Text-to-SQL Analytics

Ask questions about an e-commerce database in plain English and get back
real answers — pulled live from MySQL. Google Gemini converts each
question into SQL, the app validates and runs it, and the results are
shown as a table, an optional chart, and a downloadable CSV.

> "Which 10 customers have spent the most money overall?" →
> Gemini writes the JOIN + GROUP BY + ORDER BY + LIMIT for you.

## Features

- **Natural language → SQL** using Google Gemini, grounded in the live database schema (introspected via `SHOW TABLES` / `DESCRIBE`, not hard-coded).
- **Read-only by design** — every generated query is checked before it runs: only `SELECT` statements are allowed, write/DDL keywords (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, …) and multiple statements are rejected.
- **Streamlit UI** with sample questions, the generated SQL shown for transparency, a results table, an auto-suggested bar/line chart, and CSV export.
- **Relational schema** covering customers, products, orders, order items, and payments — enough structure for real sales/customer analysis (revenue by category, top customers, order status breakdowns, payment methods, etc).

## Tech stack

Python · Google Gemini (`google-genai`) · MySQL · Streamlit · pandas · Plotly

## Project structure

```
ecommerce-text-to-sql/
├── app.py                   # Streamlit UI
├── config.py                 # Loads settings from .env
├── requirements.txt
├── .env.example
├── database/
│   ├── schema.sql            # Table definitions
│   └── seed_data.sql         # Sample rows for demo/testing
└── utils/
    ├── db_helper.py           # MySQL connection + query execution
    ├── gemini_helper.py        # Prompting Gemini + SQL safety checks
    └── schema_context.py       # Static schema text + sample questions
```

## Database design

| Table         | Purpose                                              |
|---------------|-------------------------------------------------------|
| `customers`   | Customer profile and signup info                     |
| `products`    | Product catalog with category, price, stock          |
| `orders`      | One row per order, with status and total             |
| `order_items` | Line items linking orders to products                |
| `payments`    | Payment record for each order (method, status)        |

```
customers ──1:N── orders ──1:N── order_items ──N:1── products
                    │
                    └──1:N── payments
```

## Setup

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd ecommerce-text-to-sql
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create the database

Make sure MySQL is running locally, then:

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/seed_data.sql
```

This creates the `ecommerce_analytics` database with sample data (15 customers, 15 products, 25 orders, order items, and payments) so you can try the app immediately.

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```
GOOGLE_API_KEY=your_gemini_api_key_here     # https://aistudio.google.com/app/apikey
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=ecommerce_analytics
```

### 4. Run the app

```bash
streamlit run app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`).

## Example questions to try

- What are the top 5 best-selling products by revenue?
- Show total revenue by month
- Which 10 customers have spent the most money overall?
- How many orders were cancelled or returned?
- What is the average order value by city?
- List products that are low on stock, below 10 units
- Which payment method is used most often?
- What is the total revenue by product category?

## How it works

1. **Schema introspection** — on each query, `DatabaseHelper.get_schema_summary()` reads the live table/column structure from MySQL so the prompt sent to Gemini always matches the real database.
2. **Prompting Gemini** — `GeminiSQLGenerator` sends the question plus the schema and a strict instruction set (SELECT only, use the right joins/aggregates, no markdown fences) to the Gemini API via the `google-genai` SDK.
3. **Validation** — the returned text is cleaned (any stray code fences stripped) and checked: it must start with `SELECT`/`WITH`, contain no semicolon-separated statements, and contain none of a blocklist of write/DDL keywords. Anything that fails is rejected before it ever reaches the database.
4. **Execution & display** — the validated query runs through `mysql-connector-python` + `pandas.read_sql`, and Streamlit renders the table, an optional chart (auto-picking a text column and a numeric column), and a CSV download.

## Notes & limitations

- This is a portfolio/demo project. The SQL-safety checks (SELECT-only, keyword blocklist) are a reasonable guardrail for a single-user or internal tool, but for a production/multi-tenant deployment you'd also want a dedicated **read-only MySQL user**, query timeouts, and row limits enforced at the database level.
- Gemini can occasionally misread ambiguous questions — the generated SQL is always shown in the UI so you can sanity-check it before trusting the result.
- Swap `GEMINI_MODEL` in `.env` to try a different Gemini model.

## License

MIT — see [LICENSE](LICENSE).
