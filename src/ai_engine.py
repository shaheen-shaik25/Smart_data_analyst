"""
ai_engine.py
------------
Thin wrapper around OpenAI / Gemini so the rest of the app doesn't
care which provider is configured. If no API key is set, functions
return None and calling code falls back to rule-based logic.
"""

import os


def get_provider():
    return os.getenv("AI_PROVIDER", "openai").lower().strip()


def is_ai_available():
    provider = get_provider()
    if provider == "openai":
        return bool(os.getenv("OPENAI_API_KEY"))
    if provider == "gemini":
        return bool(os.getenv("GEMINI_API_KEY"))
    return False


def _call_openai(prompt, system, max_tokens, temperature):
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    client = OpenAI(api_key=api_key)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message.content


def _call_gemini(prompt, system, max_tokens, temperature):
    from google import genai
    from google.genai import types

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    client = genai.Client(api_key=api_key)
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

    config = types.GenerateContentConfig(
        system_instruction=system if system else None,
        max_output_tokens=max_tokens,
        temperature=temperature,
    )

    resp = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=config,
    )
    return resp.text


def ask_ai(prompt, system=None, max_tokens=900, temperature=0.3):
    """
    Send a prompt to whichever provider is configured.
    Returns the text response, or None if no key is set,
    or an "__ERROR__: ..." string if the call fails.
    """
    provider = get_provider()
    try:
        if provider == "openai":
            return _call_openai(prompt, system, max_tokens, temperature)
        if provider == "gemini":
            return _call_gemini(prompt, system, max_tokens, temperature)
        return None
    except Exception as exc:  # noqa: BLE001
        return f"__ERROR__: {exc}"


def clean_code_block(text):
    """Strip markdown code fences (```python ... ```) from a model response."""
    if not text:
        return text
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()
