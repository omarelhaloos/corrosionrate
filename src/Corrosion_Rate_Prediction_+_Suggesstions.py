import streamlit as st
import pandas as pd
import logging
from utils.predictor import CorrosionClassifier
from utils.processors import remove_think_tags
from utils.vars import environment, uns_nums
from config.config import SIDEBAR_IMAGE, PAGE_ICON
from config.theme import CUSTOM_CSS
from chat.chat import invoke_llm, get_main_prompt

# ── Logging ──
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)

# ── Page Config ──
st.set_page_config(
    page_title="Corrosion Rate Predictor",
    layout="wide",
    page_icon=PAGE_ICON,
    initial_sidebar_state="expanded",
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

clf = CorrosionClassifier()

# ═══════════════════ Sidebar ═══════════════════
with st.sidebar:
    st.image(SIDEBAR_IMAGE, use_container_width=True)
    st.markdown("## ⚗️ Corrosion Predictor")
    st.caption(
        "Predict corrosion rates based on material and environment conditions "
        "using machine learning and SciBERT embeddings."
    )
    st.markdown(
        '<div style="margin-top:0.8rem;">'
        '<span class="sidebar-badge">🧬 ML Model</span>'
        '<span class="sidebar-badge">📈 PCA</span>'
        '<span class="sidebar-badge">🔗 SciBERT</span>'
        '<span class="sidebar-badge">💡 LLM</span>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        "**How it works:**\n"
        "1. Enter material & environment data\n"
        "2. The ML model predicts corrosion rate\n"
        "3. An AI generates control recommendations"
    )

# ═══════════════════ Hero Header ═══════════════════
st.markdown('<div class="hero-title">Corrosion Rate Prediction</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">'
    "Enter material and environmental details below to get an AI-powered corrosion rate prediction "
    "with actionable recommendations."
    "</div>",
    unsafe_allow_html=True,
)

# ═══════════════════ Input Form ═══════════════════
with st.form("corrosion_form"):
    # ── Row 1: Main parameters ──
    st.markdown(
        '<div class="card-header">⚙️ Material & Environment Parameters</div>',
        unsafe_allow_html=True,
    )
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        env = st.selectbox(
            "🏭 Environment",
            options=environment,
            help="Surrounding medium (e.g., seawater, acidic, etc.)",
        )

    with col2:
        uns_input = st.selectbox(
            "🔩 Alloy UNS",
            options=uns_nums,
            help="Unified Numbering System (UNS) alloy code",
        )

    with col3:
        temp = st.number_input(
            "🌡️ Temperature (°C)",
            step=1,
            value=25,
            help="Environment temperature in Celsius",
        )

    with col4:
        conc = st.number_input(
            "💧 Concentration (%)",
            min_value=0,
            max_value=100,
            value=50,
            help="Medium concentration as a percentage",
        )

    # ── Row 2: Condition description ──
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-header">📋 Condition Description</div>',
        unsafe_allow_html=True,
    )
    comment = st.text_area(
        "Describe the condition in detail",
        height=100,
        placeholder="e.g., high chloride seawater environment with intermittent wetting, "
        "elevated H₂S levels, and moderate flow velocity...",
        help="The more detail you provide, the better the AI recommendations will be.",
        label_visibility="collapsed",
    )

    # ── Submit ──
    submitted = st.form_submit_button("⚡  Predict Corrosion Rate", use_container_width=True)

# ═══════════════════ Prediction Logic ═══════════════════
if submitted:
    if not comment.strip():
        st.warning("⚠️ Please describe the condition before predicting.")
    else:
        with st.spinner("🔄 Running prediction model..."):
            prediction, _ = clf.predict(env, temp, conc, uns_input, comment)
            raw_input = pd.DataFrame(
                [
                    {
                        "Environment": env,
                        "Temperature (°C)": temp,
                        "Concentration (%)": conc,
                        "Alloy UNS": uns_input,
                        "Condition Description": comment,
                        "Predicted Corrosion Rate": prediction,
                    }
                ]
            )

        with st.spinner("💭 Generating AI recommendations..."):
            main_page_prompt = get_main_prompt(raw_input)
            llm_output = remove_think_tags(invoke_llm(main_page_prompt))
            raw_input["AI Recommendations"] = llm_output

        st.session_state.prediction_data = raw_input
        st.session_state.llm_output = llm_output

# ═══════════════════ Results Display ═══════════════════
if "prediction_data" in st.session_state:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    pred_value = st.session_state.prediction_data["Predicted Corrosion Rate"][0]
    data = st.session_state.prediction_data

    # ── Result Badge ──
    st.markdown(
        f'<div class="result-badge">'
        f'<div class="label">Predicted Corrosion Rate</div>'
        f'<div class="value">{pred_value}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── Input summary chips ──
    chips = (
        f'<span class="chip"><span class="chip-label">Env:</span> {data["Environment"][0]}</span>'
        f'<span class="chip"><span class="chip-label">UNS:</span> {data["Alloy UNS"][0]}</span>'
        f'<span class="chip"><span class="chip-label">Temp:</span> {data["Temperature (°C)"][0]}°C</span>'
        f'<span class="chip"><span class="chip-label">Conc:</span> {data["Concentration (%)"][0]}%</span>'
    )
    st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)

    # ── Tabbed results ──
    tab_rec, tab_data, tab_export = st.tabs(
        ["💡 AI Recommendations", "📋 Input Data", "📦 Export"]
    )

    with tab_rec:
        st.markdown(
            f'<div class="rec-box">{st.session_state.llm_output}</div>',
            unsafe_allow_html=True,
        )

    with tab_data:
        display_df = st.session_state.prediction_data.drop(
            columns=["AI Recommendations"], errors="ignore"
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    with tab_export:
        exp_col1, exp_col2 = st.columns(2)

        csv_bytes = st.session_state.prediction_data.to_csv(index=False).encode("utf-8")
        with exp_col1:
            st.download_button(
                label="📊  Download as CSV",
                data=csv_bytes,
                file_name="corrosion_prediction.csv",
                mime="text/csv",
                use_container_width=True,
                key="download_csv",
            )

        txt_content = "Corrosion Prediction Report\n" + "=" * 40 + "\n\n"
        txt_content += "Input Parameters:\n"
        for col in st.session_state.prediction_data.columns:
            if col != "AI Recommendations":
                value = st.session_state.prediction_data[col].values[0]
                txt_content += f"  • {col}: {value}\n"
        txt_content += "\nAI Recommendations:\n" + "-" * 40 + "\n"
        txt_content += st.session_state.llm_output

        with exp_col2:
            st.download_button(
                label="📝  Download as TXT",
                data=txt_content.encode("utf-8"),
                file_name="corrosion_recommendations.txt",
                mime="text/plain",
                use_container_width=True,
                key="download_txt",
            )

# ═══════════════════ Footer ═══════════════════
st.markdown(
    '<div class="footer">'
    "Built with Streamlit · Machine Learning · SciBERT + PCA · LLM-Powered"
    "</div>",
    unsafe_allow_html=True,
)
