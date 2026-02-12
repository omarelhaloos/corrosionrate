"""
LLM integration module — supports Groq and OpenRouter providers with
automatic fallback and round-robin key/model rotation.
"""

import os
import logging
from itertools import cycle

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from config.config import GROQ_MODELS, OPENROUTER_MODELS, DEFAULT_LLM_PROVIDER

logger = logging.getLogger(__name__)
GROQ_API_KEY_1="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"
OPENROUTER_API_KEY="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"
# ---- Load Environment Variables ----
load_dotenv()


# ---- Provider: Groq ----

def _get_groq_api_keys() -> list[str]:
    """Collect all configured Groq API keys."""
    keys = []
    for i in range(1, 10):
        key = os.getenv(f"GROQ_API_KEY_{i}")
        if key:
            keys.append(key)
    if not keys:
        logger.warning("No GROQ_API_KEY_* environment variables found.")
    return keys


_groq_keys = _get_groq_api_keys()
_groq_key_cycle = cycle(_groq_keys) if _groq_keys else None
_groq_model_cycle = cycle(GROQ_MODELS)


def _get_groq_llm() -> ChatGroq:
    """Create a ChatGroq instance using the next API key and model."""
    if not _groq_key_cycle:
        raise ValueError("No Groq API keys configured. Set GROQ_API_KEY_1 in .env")
    api_key = next(_groq_key_cycle)
    model = next(_groq_model_cycle)
    logger.info("Using Groq model: %s", model)
    return ChatGroq(model_name=model, api_key=api_key, temperature=0.3, max_tokens=1024)


# ---- Provider: OpenRouter ----

_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def _get_openrouter_api_key() -> str | None:
    """Get the OpenRouter API key from environment."""
    return os.getenv(OPENROUTER_API_KEY)


_openrouter_model_cycle = cycle(OPENROUTER_MODELS)


def _get_openrouter_llm() -> ChatOpenAI:
    """Create a ChatOpenAI instance pointed at the OpenRouter API."""
    api_key = _get_openrouter_api_key()
    if not api_key:
        raise ValueError("No OPENROUTER_API_KEY configured. Set OPENROUTER_API_KEY in .env")
    model = next(_openrouter_model_cycle)
    logger.info("Using OpenRouter model: %s", model)
    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=_OPENROUTER_BASE_URL,
        temperature=0.3,
        max_tokens=1024,
    )


# ---- Unified LLM Access ----

_PROVIDERS = {
    "groq": _get_groq_llm,
    "openrouter": _get_openrouter_llm,
}


def invoke_llm(prompt: str, provider: str | None = None) -> str:
    """
    Invoke the configured LLM provider. Falls back to the other provider on failure.

    Args:
        prompt: The prompt string to send.
        provider: Override the default provider ("groq" or "openrouter").

    Returns:
        The LLM response text, or an error message.
    """
    provider = provider or DEFAULT_LLM_PROVIDER
    fallback = "groq" if provider == "openrouter" else "openrouter"
    providers_to_try = [provider, fallback]

    for p in providers_to_try:
        factory = _PROVIDERS.get(p)
        if not factory:
            continue
        try:
            llm = factory()
            response = llm.invoke(prompt)
            return response.content
        except Exception as e:
            logger.warning("LLM provider '%s' failed: %s. Trying fallback...", p, e)
            continue

    error_msg = "⚠️ All LLM providers failed. Please check your API keys and try again."
    logger.error(error_msg)
    return error_msg


# ---- Prompt Templates ----


def get_main_prompt(df) -> str:
    """Build the corrosion prediction recommendation prompt."""
    return f"""
You are a corrosion control expert assisting engineers in preventing material degradation in industrial environments.

Given the following dataframe:
{df}

Interpret the corrosion severity using the following scale:
- A (Resistant): < 0.05 mm/year
- B (Good): < 0.51 mm/year
- C (Questionable): 0.51 – 1.27 mm/year
- D (Poor): > 1.27 mm/year

Generate a concise technical recommendation with a clear bullet-point structure, suitable for field engineers. Your output should include:

- The interpreted corrosion severity class and its implications.
- Likely causes based on the material and environment.
- Specific mitigation strategies (e.g., naming coating types, inhibitor types, or environmental controls).
- Suggested monitoring or tests (e.g., EIS, weight loss, visual inspection).
- Optional: Practical next steps such as documentation or sharing findings.

Ensure the tone is practical, professional, and clear. Respond in exactly 5 bullet points.
"""
