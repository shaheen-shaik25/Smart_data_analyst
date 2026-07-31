"""
insights.py
-----------
Generate plain-English "business insights" from a dataset profile.
Uses AI when a key is configured, otherwise falls back to rule-based
heuristics so the app always produces something useful.
"""

import json
from src import ai_engine

SYSTEM_PROMPT = (
    "You are a senior data analyst. You are given a JSON profile of a "
    "dataset (shape, column types, missing values, summary stats, top "
    "categories, correlations). Write clear, specific business insights "
    "in concise bullet points. Mention concrete numbers from the profile. "
    "Avoid generic statements. Do not invent data that isn't in the profile. "
    "Return 5-8 bullet points, each starting with '- '."
)


def generate_ai_summary(profile: dict) -> str | None:
    prompt = f"Dataset profile:\n{json.dumps(profile, default=str, indent=2)}\n\nWrite the insights now."
    result = ai_engine.ask_ai(prompt, system=SYSTEM_PROMPT, max_tokens=700)
    if result and not result.startswith("__ERROR__"):
        return result.strip()
    return None


def generate_rule_based_summary(profile: dict) -> str:
    """Fallback insights that require no API key at all."""
    lines = []
    lines.append(f"- The dataset has **{profile['n_rows']} rows** and **{profile['n_cols']} columns**.")

    if profile.get("duplicate_rows"):
        lines.append(f"- Found **{profile['duplicate_rows']} duplicate rows** that may need cleaning.")

    if profile.get("missing_pct"):
        worst_col = max(profile["missing_pct"], key=profile["missing_pct"].get)
        lines.append(
            f"- Column **'{worst_col}'** has the most missing data at "
            f"**{profile['missing_pct'][worst_col]}%**. "
            f"{len(profile['missing_pct'])} column(s) have missing values overall."
        )
    else:
        lines.append("- No missing values were detected — the dataset is complete.")

    numeric_summary = profile.get("numeric_summary", {})
    for col, stats in list(numeric_summary.items())[:3]:
        try:
            lines.append(
                f"- **{col}**: average is {stats['mean']}, ranging from "
                f"{stats['min']} to {stats['max']}."
            )
        except KeyError:
            continue

    top_categories = profile.get("top_categories", {})
    for col, counts in list(top_categories.items())[:2]:
        if counts:
            top_val = max(counts, key=counts.get)
            lines.append(
                f"- In **{col}**, the most common value is **'{top_val}'** "
                f"({counts[top_val]} occurrences)."
            )

    correlations = profile.get("correlations", {})
    strongest = None
    strongest_val = 0
    for col_a, row in correlations.items():
        for col_b, val in row.items():
            if col_a != col_b and abs(val) > abs(strongest_val):
                strongest_val = val
                strongest = (col_a, col_b)
    if strongest and abs(strongest_val) >= 0.5:
        direction = "positive" if strongest_val > 0 else "negative"
        lines.append(
            f"- **{strongest[0]}** and **{strongest[1]}** show a strong {direction} "
            f"correlation ({strongest_val})."
        )

    return "\n".join(lines)


def generate_insights(profile: dict) -> tuple[str, bool]:
    """Returns (insight_text, used_ai)."""
    if ai_engine.is_ai_available():
        ai_text = generate_ai_summary(profile)
        if ai_text:
            return ai_text, True
    return generate_rule_based_summary(profile), False
