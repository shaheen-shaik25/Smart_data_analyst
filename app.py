"""
AI Data Analyst
---------------
Upload a CSV/Excel file, get an AI-generated summary, ask natural
language questions about your data, view auto-generated charts, and
export everything as an HTML report.

Run with:  streamlit run app.py
"""

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from src import data_loader, insights, chart_generator, nl_query, report_exporter, ai_engine

load_dotenv()

st.set_page_config(page_title="AI Data Analyst", page_icon="📊", layout="wide")


# ---------- Sidebar: settings ----------
with st.sidebar:
    st.title("📊 AI Data Analyst")
    st.caption("Upload a dataset and let AI do the analysis.")

    st.subheader("AI Settings")
    provider = st.selectbox(
        "Provider",
        options=["openai", "gemini"],
        index=0 if os.getenv("AI_PROVIDER", "openai") == "openai" else 1,
    )
    os.environ["AI_PROVIDER"] = provider

    if provider == "openai":
        key_input = st.text_input(
            "OpenAI API Key",
            value=os.getenv("OPENAI_API_KEY", ""),
            type="password",
            help="Leave blank to use rule-based analysis instead of AI.",
        )
        if key_input:
            os.environ["OPENAI_API_KEY"] = key_input
    else:
        key_input = st.text_input(
            "Gemini API Key",
            value=os.getenv("GEMINI_API_KEY", ""),
            type="password",
            help="Leave blank to use rule-based analysis instead of AI.",
        )
        if key_input:
            os.environ["GEMINI_API_KEY"] = key_input

    if ai_engine.is_ai_available():
        st.success(f"AI enabled ({provider})")
    else:
        st.warning("No API key set — using rule-based fallback mode.")

    st.divider()
    st.caption("Built with Streamlit, Pandas, Plotly & OpenAI/Gemini.")


# ---------- Main: file upload ----------
st.title("AI Data Analyst")
st.write("Upload a CSV or Excel file to get instant AI-powered insights, charts, and answers to your questions.")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])

use_sample = st.button("Or try it with sample data")

if use_sample and not uploaded_file:
    sample_path = os.path.join(os.path.dirname(__file__), "sample_data", "sample_sales.csv")
    df = pd.read_csv(sample_path)
    st.session_state["df"] = df
    st.session_state["file_name"] = "sample_sales.csv"

if uploaded_file is not None:
    try:
        df = data_loader.load_file(uploaded_file)
        st.session_state["df"] = df
        st.session_state["file_name"] = uploaded_file.name
    except Exception as exc:
        st.error(f"Could not read the file: {exc}")

if "df" not in st.session_state:
    st.info("👆 Upload a file or click 'Or try it with sample data' to get started.")
    st.stop()

df = st.session_state["df"]
file_name = st.session_state["file_name"]

with st.spinner("Profiling dataset..."):
    profile = data_loader.build_profile(df)

tab_overview, tab_insights, tab_ask, tab_charts, tab_export = st.tabs(
    ["📋 Overview", "💡 AI Insights", "❓ Ask a Question", "📈 Charts", "📤 Export Report"]
)

# ---------- Overview tab ----------
with tab_overview:
    st.subheader(f"Dataset: {file_name}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", profile["n_rows"])
    col2.metric("Columns", profile["n_cols"])
    col3.metric("Duplicate Rows", profile["duplicate_rows"])
    col4.metric("Columns w/ Missing Data", len(profile.get("missing", {})))

    st.markdown("**Preview**")
    st.dataframe(df.head(20), use_container_width=True)

    st.markdown("**Column Types**")
    dtype_df = pd.DataFrame({"Column": df.columns, "Type": df.dtypes.astype(str)})
    st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    if profile["numeric_cols"]:
        st.markdown("**Numeric Summary**")
        st.dataframe(df[profile["numeric_cols"]].describe().round(2), use_container_width=True)

# ---------- Insights tab ----------
with tab_insights:
    st.subheader("Business Insights")
    if st.button("Generate Insights", type="primary"):
        with st.spinner("Analyzing dataset..."):
            text, used_ai = insights.generate_insights(profile)
            st.session_state["insights_text"] = text
            st.session_state["insights_used_ai"] = used_ai

    if "insights_text" in st.session_state:
        badge = "🤖 AI-generated" if st.session_state["insights_used_ai"] else "📐 Rule-based (no AI key set)"
        st.caption(badge)
        st.markdown(st.session_state["insights_text"])
    else:
        st.info("Click 'Generate Insights' to summarize this dataset.")

# ---------- Ask a Question tab ----------
with tab_ask:
    st.subheader("Ask a natural language question about your data")
    st.caption("e.g. \"Which product sold the most?\", \"What's the average revenue by region?\"")
    question = st.text_input("Your question")

    if st.button("Ask", type="primary") and question:
        with st.spinner("Thinking..."):
            result, code, error = nl_query.answer_question(df, question)

        if code:
            with st.expander("Generated code"):
                st.code(code, language="python")

        if error:
            st.error(error)
        elif result is not None:
            if isinstance(result, (pd.DataFrame, pd.Series)):
                st.dataframe(result, use_container_width=True)
            else:
                st.success(f"**Answer:** {result}")
        else:
            st.warning("No result was returned. Try rephrasing your question.")

# ---------- Charts tab ----------
with tab_charts:
    st.subheader("Automatic Charts")
    charts = chart_generator.auto_charts(df, profile)
    if not charts:
        st.info("Not enough numeric/categorical structure to auto-generate charts.")
    else:
        st.session_state["charts"] = charts
        for title, fig in charts:
            st.plotly_chart(fig, use_container_width=True)

# ---------- Export tab ----------
with tab_export:
    st.subheader("Export Report")
    st.write("Generates a single, self-contained HTML file with the overview, insights, and charts.")

    if st.button("Build Report", type="primary"):
        with st.spinner("Building report..."):
            insights_text = st.session_state.get("insights_text")
            used_ai = st.session_state.get("insights_used_ai", False)
            if not insights_text:
                insights_text, used_ai = insights.generate_insights(profile)

            charts = st.session_state.get("charts") or chart_generator.auto_charts(df, profile)

            html_report = report_exporter.build_html_report(
                file_name, profile, insights_text, charts, used_ai
            )
            st.session_state["html_report"] = html_report

    if "html_report" in st.session_state:
        st.download_button(
            "⬇️ Download HTML Report",
            data=st.session_state["html_report"],
            file_name=f"report_{os.path.splitext(file_name)[0]}.html",
            mime="text/html",
        )
        st.components.v1.html(st.session_state["html_report"], height=600, scrolling=True)
