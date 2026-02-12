"""
Centralized configuration for the Corrosion Rate Prediction application.
All paths are resolved relative to this file's location for CWD independence.
"""

import os
import logging

logger = logging.getLogger(__name__)

# ---- Path Resolution ----
# Resolve BASE_PATH relative to this config file so the app works regardless of CWD
_CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.normpath(os.path.join(_CONFIG_DIR, ".."))

# ---- Model Paths ----
MODEL_PATHS: dict[str, str] = {
    "pca": os.path.join(BASE_PATH, "models", "decomposers", "pca.pkl"),
    "model": os.path.join(BASE_PATH, "models", "classifiers", "rf_all_data.pkl"),
    "uns_encoder": os.path.join(BASE_PATH, "models", "encoders", "uns_encoder.pkl"),
    "env_encoder": os.path.join(
        BASE_PATH, "models", "encoders", "env_target_encoder.pkl"
    ),
    "temp_scaler": os.path.join(
        BASE_PATH, "models", "scalers", "temprature_scaler.pkl"
    ),
}

# ---- Feature Column Definitions ----
NOT_COMPOSE_COLUMNS: list[str] = [
    "Environment",
    "UNS",
    "Temperature (deg C)",
    "Concentration_clean",
]
CATEGORICAL_COLUMNS: list[str] = ["Environment"]

# ---- Asset Paths ----
PAGE_ICON: str = os.path.join(BASE_PATH, "assets", "images", "corrosive.png")
PIPE_ICON: str = os.path.join(BASE_PATH, "assets", "images", "pipe.png")
MATERIAL_SELECTION_IMAGE: str = os.path.join(
    BASE_PATH, "assets", "images", "material_selection.jpeg"
)
SIDEBAR_IMAGE: str = (
    "https://www.ddcoatings.co.uk/wp-content/uploads/2019/09/pipeline-corrosion.jpg"
)

# ---- LLM Configuration ----
GROQ_MODELS: list[str] = [
    "llama-3.3-70b-versatile",
    "llama3-70b-8192",
    "deepseek-r1-distill-llama-70b",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
    "qwen-qwq-32b",
]

OPENROUTER_MODELS: list[str] = [
    "deepseek/deepseek-r1",
    "google/gemini-2.5-flash-preview",
    "meta-llama/llama-4-maverick",
]

# ---- LLM Provider Selection ----
# Options: "groq", "openrouter"
DEFAULT_LLM_PROVIDER: str = "openrouter"
