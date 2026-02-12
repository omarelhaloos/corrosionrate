"""
Corrosion rate prediction pipeline using scikit-learn models and SciBERT embeddings.
"""

import logging

import joblib
import numpy as np
import pandas as pd
import streamlit as st

from config.config import MODEL_PATHS, NOT_COMPOSE_COLUMNS
from utils.processors import clean_condition_text, get_cached_scibert_embedding
from utils.vars import targets

logger = logging.getLogger(__name__)

# Number of PCA components expected by the trained model
_N_PCA_COMPONENTS = 15


class CorrosionClassifier:
    """Loads pre-trained ML models and provides corrosion-rate predictions."""

    def __init__(self):
        self.models = self._load_models()

    @staticmethod
    @st.cache_resource
    def _load_models() -> dict:
        """Load all serialized models into memory (cached across Streamlit reruns)."""
        loaded = {}
        for name, path in MODEL_PATHS.items():
            try:
                loaded[name] = joblib.load(path)
                logger.info("Loaded model '%s' from %s", name, path)
            except FileNotFoundError:
                logger.error("Model file not found: %s", path)
                raise
            except Exception as e:
                logger.error("Failed to load model '%s': %s", name, e)
                raise
        return loaded

    def preprocess_input(
        self, env: str, temp: float, conc: float, uns_input: str, comment: str
    ) -> pd.DataFrame:
        """Transform raw user inputs into model-ready feature DataFrame."""
        # Build input DataFrame
        input_df = pd.DataFrame(
            [
                {
                    "Environment": env,
                    "Temperature (deg C)": temp,
                    "Concentration_clean": conc,
                    "UNS": uns_input,
                }
            ]
        )

        # Encode categorical variables
        input_df["Environment"] = self.models["env_encoder"].transform(
            input_df["Environment"]
        )
        input_df["UNS"] = self.models["uns_encoder"].transform(input_df["UNS"])

        # Scale temperature
        input_df["Temperature (deg C)"] = self.models["temp_scaler"].transform(
            input_df[["Temperature (deg C)"]]
        )

        # Process condition text using SciBERT
        cleaned_comment = clean_condition_text(comment)
        scibert_embedding = np.squeeze(get_cached_scibert_embedding(cleaned_comment))
        scibert_df = pd.DataFrame(
            [scibert_embedding],
            columns=[f"scibert_{i}" for i in range(len(scibert_embedding))],
        )

        # PCA transformation
        pca_emb = self.models["pca"].transform(scibert_df)
        pca_df = pd.DataFrame(
            pca_emb, columns=[f"PCA_{i+1}" for i in range(_N_PCA_COMPONENTS)]
        )

        # Assemble final feature vector in expected column order
        full_input = pd.concat([input_df.reset_index(drop=True), pca_df], axis=1)
        ordered_columns = NOT_COMPOSE_COLUMNS + [
            f"PCA_{i+1}" for i in range(_N_PCA_COMPONENTS)
        ]
        return full_input[ordered_columns]

    def predict(
        self, env: str, temp: float, conc: float, uns_input: str, comment: str
    ) -> tuple[str, pd.DataFrame]:
        """Run the full prediction pipeline and return (class_label, features_df)."""
        full_input = self.preprocess_input(env, temp, conc, uns_input, comment)
        prediction = self.models["model"].predict(full_input)
        predicted_class = targets.get(str(int(prediction[0])), "Unknown")
        logger.info("Prediction result: %s (raw=%s)", predicted_class, prediction[0])
        return predicted_class, full_input
