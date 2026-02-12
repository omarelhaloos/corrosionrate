"""
Text processing and SciBERT embedding utilities.
"""

import re
import logging
import numpy as np
import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel

logger = logging.getLogger(__name__)

# ---- SciBERT Model (lazy-loaded & cached) ----

_SCIBERT_MODEL_NAME = "allenai/scibert_scivocab_uncased"


@st.cache_resource
def _load_scibert():
    """Load SciBERT tokenizer and model once, cached across Streamlit reruns."""
    logger.info("Loading SciBERT model: %s", _SCIBERT_MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(_SCIBERT_MODEL_NAME)
    model = AutoModel.from_pretrained(_SCIBERT_MODEL_NAME)
    model.eval()  # Set to evaluation mode — disables dropout
    logger.info("SciBERT model loaded successfully.")
    return tokenizer, model


# ---- Text Cleaning ----


def clean_condition_text(text: str) -> str:
    """Normalize and clean condition description text."""
    text = text.lower().strip()
    text = re.sub(r"[\n\r]", " ", text)
    text = re.sub(r"[^a-z0-9%.\- ]+", "", text)
    text = re.sub(r"\s+", " ", text)  # collapse multiple spaces
    return text


# ---- SciBERT Embedding ----


def get_scibert_embedding(text: str) -> np.ndarray:
    """Generate a SciBERT embedding for the given text."""
    tokenizer, model = _load_scibert()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()


@st.cache_data
def get_cached_scibert_embedding(text: str) -> np.ndarray:
    """Cached wrapper for SciBERT embedding generation."""
    return get_scibert_embedding(text)


# ---- LLM Output Cleaning ----


def remove_think_tags(text: str) -> str:
    """Remove <think>...</think> tags from LLM responses (e.g. DeepSeek-R1)."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
