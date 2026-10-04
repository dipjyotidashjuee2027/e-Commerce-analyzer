"""
E-Commerce Text-to-SQL Analytics
Streamlit UI that turns a plain-English question into a MySQL query
(via Google Gemini), runs it, and displays the results as a table,
chart, and downloadable CSV.
"""
import streamlit as st
import plotly.express as px

from config import MAX_ROWS_TO_CHART
from utils.db_helper import DatabaseHelper
from utils.gemini_helper import GeminiSQLGenerator
from utils.schema_context import SAMPLE_QUESTIONS

st.set_page_config(
    page_title="E-Commerce Text-to-SQL Analytics",
    page_icon="🛒",
    layout="wide",
)


@st.cache_resource
def get_db_helper() -> DatabaseHelper:
    return DatabaseHelper()


def init_session_state():
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("pending_question", "")


def render_sidebar(db: DatabaseHelper, connected: bool, message: str):
    with st.sidebar:
        st.header("⚙️ Connection")
        if connected:
            st.success("MySQL connected")
        else:
            st.error("MySQL not reachable")
            st.caption(message)

        st.divider()
        st.header("💡 Sample questions")
        for q in SAMPLE_QUESTIONS:
            if st.button(q, use_container_width=True, key=f"sample::{q}"):
                st.session_state.pending_question = q
                st.rerun()

        if st.session_state.history:
            st.divider()
            st.header("🕓 Recent queries")
            for item in reversed(st.session_state.history[-5:]):
                st.caption(item["question"])


def render_results(df, key_prefix: str):
    st.subheader(f"Results · {len(df)} row{'s' if len(df) != 1 else ''}")

    if df.empty:
        st.info("The query ran successfully but returned no rows.")
        return

    st.dataframe(df, use_container_width=True)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    label_cols = [c for c in df.columns if c not in numeric_cols]

    if numeric_cols and label_cols and len(df) <= MAX_ROWS_TO_CHART:
        st.subheader("Chart")
        c1, c2, c3 = st.columns(3)
        x_col = c1.selectbox("X axis", label_cols, key=f"{key_prefix}_x")
        y_col = c2.selectbox("Y axis", numeric_cols, key=f"{key_prefix}_y")
        chart_type = c3.selectbox("Chart type", ["Bar", "Line"], key=f"{key_prefix}_type")

        fig = px.bar(df, x=x_col, y=y_col) if chart_type == "Bar" else px.line(df, x=x_col, y=y_col)
        st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        "⬇️ Download results as CSV",
        df.to_csv(index=False).encode("utf-8"),
        "query_results.csv",
        "text/csv",
        key=f"{key_prefix}_download",
    )


def main():
    init_session_state()
    db = get_db_helper()
    connected, message = db.test_connection()

    st.title("🛒 E-Commerce Text-to-SQL Analytics")
    st.caption(
        "Ask a question in plain English. Gemini converts it into a MySQL "
        "query, runs it against your database, and shows the results below."
    )

    render_sidebar(db, connected, message)

    question = st.text_input(
        "Ask a question about your customers, orders, products, or payments",
        value=st.session_state.pending_question,
        placeholder="e.g. What are the top 5 best-selling products by revenue?",
        key="question_input",
    )
    st.session_state.pending_question = ""

    run = st.button("Run query", type="primary")

    if not run:
        return

    if not question.strip():
        st.warning("Please enter a question first.")
        return

    if not connected:
        st.error("Cannot reach the MySQL database. Check your .env settings and that MySQL is running.")
        return

    with st.spinner("Asking Gemini to write the SQL..."):
        try:
            schema_description = db.get_schema_summary()
            generator = GeminiSQLGenerator(schema_description)
            sql = generator.generate_sql(question)
        except Exception as e:
            st.error(f"Couldn't generate a query: {e}")
            return

    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    with st.spinner("Running query against MySQL..."):
        try:
            df = db.run_query(sql)
        except Exception as e:
            st.error(f"Couldn't run the query: {e}")
            return

    render_results(df, key_prefix=f"q{len(st.session_state.history)}")
    st.session_state.history.append({"question": question, "sql": sql})


if __name__ == "__main__":
    main()
