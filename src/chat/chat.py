"""
LLM integration module — supports Groq and OpenRouter providers with
automatic fallback and round-robin key/model rotation.
"""

import logging
from itertools import cycle

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from config.config import GROQ_MODELS, OPENROUTER_MODELS, DEFAULT_LLM_PROVIDER

logger = logging.getLogger(__name__)

# ============================================================
# 🔐 API KEYS (INLINE – SAME FILE)
# ============================================================

GROQ_API_KEYS = [
    "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",
    
]

OPENROUTER_API_KEY = "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"

# ============================================================
# 🔁 Cycles (Keys + Models)
# ============================================================

_groq_key_cycle = cycle(GROQ_API_KEYS)
_groq_model_cycle = cycle(GROQ_MODELS)
_openrouter_model_cycle = cycle(OPENROUTER_MODELS)

# ============================================================
# 🧠 Providers
# ============================================================

def _get_groq_llm() -> ChatGroq:
    api_key = next(_groq_key_cycle)
    model = next(_groq_model_cycle)

    logger.info("Using Groq model: %s", model)

    return ChatGroq(
        model_name=model,
        api_key=api_key,
        temperature=0.3,
        max_tokens=1024,
    )


_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def _get_openrouter_llm() -> ChatOpenAI:
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is not set.")

    model = next(_openrouter_model_cycle)
    logger.info("Using OpenRouter model: %s", model)

    return ChatOpenAI(
        model=model,
        api_key=OPENROUTER_API_KEY,
        base_url=_OPENROUTER_BASE_URL,
        temperature=0.3,
        max_tokens=1024,
    )

# ============================================================
# 🔀 Unified LLM Access with Fallback
# ============================================================

_PROVIDERS = {
    "groq": _get_groq_llm,
    "openrouter": _get_openrouter_llm,
}


def invoke_llm(prompt: str, provider: str | None = None) -> str:
    provider = provider or DEFAULT_LLM_PROVIDER
    fallback = "groq" if provider == "openrouter" else "openrouter"

    for p in (provider, fallback):
        try:
            llm = _PROVIDERS[p]()
            response = llm.invoke(prompt)
            return response.content
        except Exception as e:
            logger.warning("Provider '%s' failed: %s", p, e)

    return "⚠️ All LLM providers failed. Check API keys or quota."

# ============================================================
# 🧪 Prompt Template
# ============================================================

def get_main_prompt(df) -> str:
    return f"""
You are a corrosion control expert assisting engineers in preventing material degradation in industrial environments.

Given the following dataframe:
{df}

Interpret the corrosion severity using the following scale:
- A (Resistant): < 0.05 mm/year
- B (Good): < 0.51 mm/year
- C (Questionable): 0.51 – 1.27 mm/year
- D (Poor): > 1.27 mm/year

Generate a concise technical recommendation with a clear bullet-point structure, suitable for field engineers.

Respond in exactly 5 bullet points.
"""
