"""
data_loader.py
--------------
Load CSV/Excel files and build a compact "profile" of the dataset
that both the rule-based logic and the AI prompts can use.
"""

import warnings

import pandas as pd


def load_file(uploaded_file):
    """Load a Streamlit UploadedFile into a pandas DataFrame."""
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a .csv or .xlsx file.")

    df = _clean_columns(df)
    return df


def _clean_columns(df):
    df.columns = [str(c).strip() for c in df.columns]
    return df


def build_profile(df: pd.DataFrame) -> dict:
    """Return a dictionary summarizing the dataset for insights/prompts."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()

    # try to detect date-like string columns
    for col in categorical_cols[:]:
        if col in datetime_cols:
            continue
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().mean() > 0.9:
                datetime_cols.append(col)
                categorical_cols.remove(col)
        except Exception:
            pass

    missing = df.isna().sum()
    missing_pct = (missing / max(len(df), 1) * 100).round(2)

    profile = {
        "n_rows": int(len(df)),
        "n_cols": int(df.shape[1]),
        "columns": df.columns.tolist(),
        "numeric_cols": numeric_cols,
        "categorical_cols": categorical_cols,
        "datetime_cols": datetime_cols,
        "missing": {c: int(missing[c]) for c in df.columns if missing[c] > 0},
        "missing_pct": {c: float(missing_pct[c]) for c in df.columns if missing_pct[c] > 0},
        "duplicate_rows": int(df.duplicated().sum()),
        "sample_rows": df.head(5).to_dict(orient="records"),
    }

    if numeric_cols:
        profile["numeric_summary"] = df[numeric_cols].describe().round(2).to_dict()

    top_categories = {}
    for col in categorical_cols[:8]:
        counts = df[col].value_counts(dropna=True).head(5)
        top_categories[col] = counts.to_dict()
    profile["top_categories"] = top_categories

    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr(numeric_only=True).round(2)
        profile["correlations"] = corr.to_dict()

    return profile
