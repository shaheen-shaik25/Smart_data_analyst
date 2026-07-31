"""
nl_query.py
-----------
Turn a natural-language question into pandas code via the LLM, then
execute that code in a restricted sandbox and return the result.

If no AI provider is configured, falls back to a small set of simple
keyword-based lookups (max/min/count/mean of a column) so the "Ask a
question" tab still does something useful without an API key.
"""

import re
import pandas as pd
import numpy as np
from src import ai_engine

SYSTEM_PROMPT = """You are a Python data analyst assistant. You are given:
- The columns and dtypes of a pandas DataFrame called `df`
- A natural language question

Write ONLY Python code (pandas/numpy) that computes the answer and stores
it in a variable named `result`. Rules:
- Use only the variable `df` (already loaded), plus `pd` and `np`.
- Do not import anything, do not read/write files, do not use exec/eval/open.
- `result` can be a DataFrame, Series, number, or string.
- Return ONLY the code, no explanation, no markdown fences.
"""

SAFE_BUILTINS = {
    "len": len,
    "range": range,
    "sum": sum,
    "min": min,
    "max": max,
    "sorted": sorted,
    "abs": abs,
    "round": round,
    "list": list,
    "dict": dict,
    "set": set,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "enumerate": enumerate,
    "zip": zip,
}

FORBIDDEN_PATTERNS = [
    r"\bimport\b", r"\bopen\s*\(", r"\bexec\s*\(", r"\beval\s*\(",
    r"__", r"\bos\.", r"\bsys\.", r"\bsubprocess\b", r"\bshutil\b",
]


def _is_code_safe(code: str) -> bool:
    return not any(re.search(pattern, code) for pattern in FORBIDDEN_PATTERNS)


def ask_with_ai(df: pd.DataFrame, question: str):
    col_info = ", ".join(f"{c} ({df[c].dtype})" for c in df.columns)
    prompt = f"DataFrame columns: {col_info}\n\nQuestion: {question}\n\nCode:"
    code = ai_engine.ask_ai(prompt, system=SYSTEM_PROMPT, max_tokens=400, temperature=0.1)

    if not code or code.startswith("__ERROR__"):
        return None, code, "AI call failed."

    code = ai_engine.clean_code_block(code)

    if not _is_code_safe(code):
        return None, code, "Generated code was blocked for safety reasons."

    sandbox_globals = {"__builtins__": SAFE_BUILTINS, "pd": pd, "np": np, "df": df.copy()}
    local_vars = {}
    try:
        exec(code, sandbox_globals, local_vars)  # noqa: S102 (sandboxed)
        result = local_vars.get("result", sandbox_globals.get("result"))
        # Common LLM slip: referencing a method without calling it,
        # e.g. `result = series.abs` instead of `result = series.abs()`.
        if callable(result) and not isinstance(result, (pd.DataFrame, pd.Series)):
            try:
                result = result()
            except TypeError:
                pass  # leave as-is if it actually needs arguments
        return result, code, None
    except Exception as exc:  # noqa: BLE001
        return None, code, str(exc)


def ask_with_rules(df: pd.DataFrame, question: str):
    """Very small fallback for common questions when no AI key is set."""
    q = question.lower()
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    match = re.search(r"(highest|max|maximum|top)\s+([a-zA-Z0-9_ ]+)", q)
    if match and numeric_cols:
        col = _match_column(df, match.group(2), numeric_cols)
        if col:
            row = df.loc[df[col].idxmax()]
            return row, None, None

    match = re.search(r"(lowest|min|minimum)\s+([a-zA-Z0-9_ ]+)", q)
    if match and numeric_cols:
        col = _match_column(df, match.group(2), numeric_cols)
        if col:
            row = df.loc[df[col].idxmin()]
            return row, None, None

    match = re.search(r"(average|mean)\s+([a-zA-Z0-9_ ]+)", q)
    if match and numeric_cols:
        col = _match_column(df, match.group(2), numeric_cols)
        if col:
            return df[col].mean(), None, None

    if "how many rows" in q or "row count" in q or "number of rows" in q:
        return len(df), None, None

    return None, None, (
        "No AI key configured, and this question didn't match the simple "
        "built-in patterns (max/min/average of a column, row count). "
        "Add an API key in .env for full natural-language support."
    )


def _match_column(df, text, candidate_cols):
    text = text.strip()
    for col in candidate_cols:
        if col.lower() in text or text in col.lower():
            return col
    return candidate_cols[0] if candidate_cols else None


def answer_question(df: pd.DataFrame, question: str):
    """
    Returns (result, generated_code, error_message).
    generated_code is None when the rule-based fallback was used.
    """
    if ai_engine.is_ai_available():
        return ask_with_ai(df, question)
    return ask_with_rules(df, question)
