"""
chart_generator.py
-------------------
Automatically pick sensible charts based on column types:
- Bar chart of top categories
- Histograms for numeric columns
- Correlation heatmap
- Time series line chart if a datetime column exists
"""

import pandas as pd
import plotly.express as px


def auto_charts(df: pd.DataFrame, profile: dict, max_charts: int = 6):
    """Return a list of (title, plotly_figure) tuples."""
    charts = []
    numeric_cols = profile["numeric_cols"]
    categorical_cols = profile["categorical_cols"]
    datetime_cols = profile["datetime_cols"]

    # 1. Bar charts: categorical vs a numeric aggregate (sum)
    for cat_col in categorical_cols[:2]:
        if df[cat_col].nunique() > 30:
            continue
        if numeric_cols:
            num_col = numeric_cols[0]
            grouped = (
                df.groupby(cat_col, dropna=True)[num_col]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )
            fig = px.bar(
                grouped,
                x=cat_col,
                y=num_col,
                title=f"Total {num_col} by {cat_col} (Top 10)",
                text_auto=True,
            )
        else:
            counts = df[cat_col].value_counts().head(10).reset_index()
            counts.columns = [cat_col, "count"]
            fig = px.bar(counts, x=cat_col, y="count", title=f"Top values in {cat_col}")
        charts.append((fig.layout.title.text, fig))

    # 2. Histograms for up to 2 numeric columns
    for num_col in numeric_cols[:2]:
        fig = px.histogram(df, x=num_col, nbins=30, title=f"Distribution of {num_col}")
        charts.append((fig.layout.title.text, fig))

    # 3. Correlation heatmap
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr(numeric_only=True)
        fig = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            title="Correlation Heatmap",
            aspect="auto",
        )
        charts.append((fig.layout.title.text, fig))

    # 4. Time series if a datetime column exists
    if datetime_cols and numeric_cols:
        date_col = datetime_cols[0]
        num_col = numeric_cols[0]
        try:
            ts_df = df[[date_col, num_col]].copy()
            ts_df[date_col] = pd.to_datetime(ts_df[date_col], errors="coerce")
            ts_df = ts_df.dropna(subset=[date_col]).sort_values(date_col)
            ts_df = ts_df.groupby(pd.Grouper(key=date_col, freq="W"))[num_col].sum().reset_index()
            fig = px.line(ts_df, x=date_col, y=num_col, title=f"{num_col} Over Time (weekly)")
            charts.append((fig.layout.title.text, fig))
        except Exception:
            pass

    # 5. Pie chart for a low-cardinality categorical column
    for cat_col in categorical_cols:
        if 1 < df[cat_col].nunique() <= 8:
            counts = df[cat_col].value_counts().reset_index()
            counts.columns = [cat_col, "count"]
            fig = px.pie(counts, names=cat_col, values="count", title=f"Share by {cat_col}")
            charts.append((fig.layout.title.text, fig))
            break

    return charts[:max_charts]
