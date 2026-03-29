"""
LLM Initialisation — supports Google Gemini and OpenAI
Auto-detects from environment variables.
"""
from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()

_llm = None  # module-level singleton


def get_llm():
    """Return an initialised LLM instance, or None if no API key is configured."""
    global _llm
    if _llm is not None:
        return _llm

    google_key = os.getenv("GOOGLE_API_KEY", "").strip()
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()

    if google_key and google_key != "your_google_api_key_here":
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            model = os.getenv("LLM_MODEL", "gemini-2.0-flash")
            temp = float(os.getenv("LLM_TEMPERATURE", "0.3"))
            _llm = ChatGoogleGenerativeAI(
                model=model,
                google_api_key=google_key,
                temperature=temp,
            )
            print(f"[FinSage] Using Google Gemini ({model})")
        except Exception as e:
            print(f"[FinSage] Gemini init failed: {e}")

    elif openai_key and openai_key != "your_openai_api_key_here":
        try:
            from langchain_openai import ChatOpenAI
            model = os.getenv("LLM_MODEL", "gpt-4o-mini")
            temp = float(os.getenv("LLM_TEMPERATURE", "0.3"))
            _llm = ChatOpenAI(model=model, temperature=temp)
            print(f"[FinSage] Using OpenAI ({model})")
        except Exception as e:
            print(f"[FinSage] OpenAI init failed: {e}")

    if _llm is None:
        print("[FinSage] No LLM configured — running in demo (rule-based) mode.")

    return _llm


def reset_llm():
    """Reset cached LLM (useful for testing)."""
    global _llm
    _llm = None
